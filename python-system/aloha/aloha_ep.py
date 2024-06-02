import math
import random
import numpy as np
import concurrent.futures

from aloha.user import UniqUser
from aloha import utils
from consts import RESPONSE_EMPTY, RESPONSE_OK, RESPONSE_CONFLICT, INFINITY, \
    RUS_TITLES


class MultichannelAlohaEP:
    def __init__(self, lambd, slot_len: float, slots, ch_num: int, 
                 verbose=False):
        
        self.lambd = lambd
        self.slot_len = slot_len

        self.slots = slots
        self.ch_num = ch_num

        self.verbose = verbose
        self.id_counter = 0


    def calc_throughput(self) -> float:
        term1 = self.slot_len * self.lambd * \
            math.e ** (-self.slot_len * self.lambd)

        term2 = 0.0 
        with concurrent.futures.ProcessPoolExecutor() as executor:
            running_tasks = []
            for l in range(1, self.ch_num+1):
                task = executor.submit(self._calc_multipliers_independently, l)
                running_tasks.append(task)
            
            for running_task in running_tasks:
                m1, m2 = running_task.result()
                term2 += m1*m2

        # for l in range(1, self.ch_num+1):
        #     multiplier1 = math.comb(self.ch_num-1, l-1) * \
        #         (self.slot_len * self.lambd) ** (self.ch_num-l) * \
        #         math.e ** (-self.slot_len * self.lambd * self.ch_num)
            
        #     multiplier2 = self._calc_multiplier2(l)
        #     term2 += multiplier1*multiplier2

        return (term1 + term2) / self.slot_len
    

    def _calc_multipliers_independently(self, l: int) -> tuple[float, float]:
        multiplier1 = math.comb(self.ch_num-1, l-1) * \
            (self.slot_len * self.lambd) ** (self.ch_num-l) * \
            math.e ** (-self.slot_len * self.lambd * self.ch_num)

        multiplier2 = self._calc_multiplier2(l)
        return multiplier1, multiplier2
    
    
    def _calc_multiplier2(self, l: int) -> float:
        multiplier2 = 0.0
        for users_in_channels in utils.generate_users_in_channels(INFINITY, l):
            if sum(users_in_channels) == 0:
                continue

            usr_sum = sum(users_in_channels)

            tmp = 0.0
            if usr_sum <= l:
                tmp = (usr_sum / l) * (1 - 1/l) ** (usr_sum - 1)
            else:
                tmp = (1 - 1/usr_sum) ** (usr_sum - 1)
            
            numerator = np.power(self.slot_len * self.lambd, usr_sum)
            denominator = utils.factorial_product(users_in_channels)
            tmp *= float(numerator / denominator)
            
            multiplier2 += tmp
        
        return multiplier2


    def run_simulation(self, g_param: float) -> tuple[float, float, float]:
        # Init runtime data
        timestamps, poisson_dist = utils.generate_stream(self.lambd, 
                                              self.slots, 
                                              self.slot_len,
                                              self.verbose)
        active_users = {}
        sent_data_packets = []

        # Run simulation
        for cur_slot in range(self.slots):
            if self.verbose: 
                if RUS_TITLES: print(f"\n>>> СЛОТ #{cur_slot}:")
                else: print(f"\n>>> SLOT #{cur_slot}:")

            bs_response = self._run_frame(
                poisson_dist, 
                active_users, 
                sent_data_packets,
                cur_slot,
                g_param)
            if self.verbose: utils.print_bs_response(bs_response)

        # Calculate system params
        # Data packet == unique user in case of infinite number of users
        total_time = timestamps[-1]
        lambda_in = (len(sent_data_packets) + len(active_users)) / total_time
        lambda_out = len(sent_data_packets) / total_time
        avg_delay = utils.calc_avg_delay(sent_data_packets)

        return lambda_in, lambda_out, avg_delay


    def _run_frame(self, poisson_dist: list[int], 
                   active_users: dict[int, UniqUser], 
                   sent_data_packets: list[UniqUser], 
                   cur_slot: int,
                   g_param: float) -> list[int]:
        
        # Update active users list
        for _ in range(poisson_dist[cur_slot]):
            self.id_counter += 1
            active_users[self.id_counter] = UniqUser(self.id_counter, cur_slot,
                                                    self.slot_len)

        if len(active_users) == 0: 
            if self.verbose:
                if RUS_TITLES: print("В текущем слоте нет заявок")
                else: print("No active users in the current slot")
            return [RESPONSE_EMPTY for _ in range(self.ch_num)]
        
        # Exploration phase
        # EP: active users choosing channels
        ch_situation = {num: set() for num in range(self.ch_num)}
        P_ep = min(1, self.ch_num  * g_param / len(active_users))
        for user in active_users.values():
            if np.random.rand() < P_ep:
                channel = random.randrange(len(ch_situation))
                ch_situation[channel].add(user)

        if self._is_empty(ch_situation):
            if self.verbose:
                if RUS_TITLES: print("Пользователи решили не передавать \
сообщения в текущем слоте")
                else: print("All active users decided not to transmit message \
in the current slot")
            return [RESPONSE_EMPTY for _ in range(self.ch_num)]

        if self.verbose:
            if RUS_TITLES: print("Абоненты выбрали следующие каналы:")
            else: print("Users make next choice:")
            utils.print_channels_situation(ch_situation)
        
        # EP: split active users who decide to transmit a preamble into 2 
        # groups
        group_success = {}
        group_conflict = {}

        for channel, users in ch_situation.items():
            if len(users) == 1:
                contention_free_user = users.pop()
                group_success[channel] = {contention_free_user}
            else:
                group_conflict[channel] = users.copy()

        if not self._is_empty(group_conflict):
            # EP: users from a confict group reselect channels from this group
            users_in_contention = set()
            for users in group_conflict.values():
                users_in_contention.update(users)
                users.clear()

            for user in users_in_contention:
                new_channel = random.choice(list(group_conflict.keys()))
                group_conflict[new_channel].add(user)

            if self.verbose:
                if RUS_TITLES: print("Конфликтующие абоненты заново выбрали \
каналы")
                else: print("Users in contention reselect channels:")
                utils.print_channels_situation(group_conflict)

        # Data transmission phase
        bs_response = [0 for _ in range(self.ch_num)]

        for channel, user in group_success.items():
            contention_free_user = user.pop()

            user_data_packet = active_users.pop(contention_free_user.id_)
            user_data_packet.processed(cur_slot)
            sent_data_packets.append(user_data_packet)
            bs_response[channel] = RESPONSE_OK

        for channel, users in group_conflict.items():
            if len(users) == 0:
                bs_response[channel] = RESPONSE_EMPTY
            else:
                active_users_decisions = {}
                P_dtp = min(1, (self.ch_num - len(group_success)) / 
                            self._users_in(group_conflict))
                for user in users:
                    active_users_decisions[user] = np.random.rand() < P_dtp

                # No one decided to transmit packet
                if all(dec == False for dec in 
                       list(active_users_decisions.values())):
                    bs_response[channel] = RESPONSE_EMPTY
                # Someone decided to transmit packet
                else:
                    if list(active_users_decisions.values()).count(True) == 1:
                        bs_response[channel] = RESPONSE_OK
                        for user, decision in active_users_decisions.items():
                            if decision == True:
                                
                                user_data_packet = active_users.pop(user.id_)
                                user_data_packet.processed(cur_slot)
                                sent_data_packets.append(user_data_packet)
                                break
                    else:
                        bs_response[channel] = RESPONSE_CONFLICT
                        # No one leaves from active users list
        
        return bs_response
        
    
    def _is_empty(self, group: dict[int, set[UniqUser]]) -> bool:
        for users in group.values():
            if len(users) != 0:
                return False
        return True
    

    def _users_in(self, group: dict[int, set[UniqUser]]) -> int:
        amount = 0
        for users in group.values():
            amount += len(users)
        return amount

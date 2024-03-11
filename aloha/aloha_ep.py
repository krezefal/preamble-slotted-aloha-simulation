import numpy as np
import random

from aloha.user import UniqUser
from aloha import utils
from consts import RESPONSE_EMPTY, RESPONSE_OK, RESPONSE_CONFLICT


class MultichannelAlohaEP:
    def __init__(self, lambd: float, slots, slot_len: float, ch_count: int, 
                 ep_len: float, verbose=False):
        self.lambd = lambd
        self.slots = slots
        self.slot_len = slot_len
        self.ch_count = ch_count
        self.ep_len = ep_len
        self.verbose = verbose

        self.id_counter = 0


    def run_theory(self):
        # l = self.lambd
        # M = self.channels
        # # K = self.users_count
        # # K = (l/M) / (1 - l/M) # Erlang

        # # max_throughput = K * math.e ** (-K/M) # 1 ((10) in article)
        # max_throughput = M * math.e ** (-1) # 2 ((10) in article)
        # input_arrival_rate = l * math.e ** (- l/M)
        # return max_throughput, input_arrival_rate
        return 0.0, 0.0, 0.0


    def run_simulation(self) -> tuple[float, float, float]:
        # Init runtime data
        poisson_dist = utils.generate_stream(self.lambd, 
                                              self.slots, 
                                              self.slot_len,
                                              self.verbose)
        active_users = {}
        sent_data_packets = []

        # Run simulation
        for cur_slot in range(self.slots):
            if self.verbose: print(f"\n>>> SLOT #{cur_slot+1}:")
            bs_response = self._run_frame(
                poisson_dist, 
                active_users, 
                sent_data_packets,
                cur_slot)
            if self.verbose: utils.print_bs_response(bs_response)

        # Calculate system params
        # Data packet == unique user in case of infinite number of users
        lambda_in = (len(sent_data_packets) + len(active_users)) / self.slots
        lambda_out = len(sent_data_packets) / self.slots
        avg_delay = utils.calc_avg_delay(sent_data_packets)

        return lambda_in, lambda_out, avg_delay


    def _run_frame(self, poisson_dist: list[int], 
                   active_users: dict[int, UniqUser], 
                   sent_data_packets: list[UniqUser], 
                   cur_slot: int) -> list[int]:
        
        # Update active users list
        for _ in range(poisson_dist[cur_slot]):
            self.id_counter += 1
            active_users[self.id_counter] = UniqUser(self.id_counter, cur_slot,
                                                    self.slot_len)

        if len(active_users) == 0: 
            if self.verbose:
                print("No active users in the current slot")
            return [RESPONSE_EMPTY for _ in range(self.ch_count)]
        
        # Exploration phase
        # EP: active users choosing channels
        ch_situation = {num: set() for num in range(self.ch_count)}
        P_ep = min(1, self.ch_count / len(active_users))
        for user in active_users.values():
            if np.random.rand() < P_ep:
                channel = random.randrange(len(ch_situation))
                ch_situation[channel].add(user)

        if self.verbose:
            print("Users make next choice:")
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
                print("Users in contention reselect channels:")
                utils.print_channels_situation(group_conflict)

        # Data transmission phase
        bs_response = [0 for _ in range(self.ch_count)]

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
                P_dtp = min(1, (self.ch_count - len(group_success)) / 
                            len(group_conflict))
                for user in users:
                    active_users_decisions[user] = np.random.rand() < P_dtp

                # No one decided to transmit packet
                if all(dec is False for dec in 
                       list(active_users_decisions.values())):
                    bs_response[channel] = RESPONSE_EMPTY
                # Someone decided to transmit packet
                else:
                    if list(active_users_decisions.values()).count(True) == 1:
                        bs_response[channel] = RESPONSE_OK
                        for user, decision in active_users_decisions.items():
                            if decision is True:
                                
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

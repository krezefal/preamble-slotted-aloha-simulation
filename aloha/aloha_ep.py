from aloha.user_ep import User
from aloha import utils
from aloha.utils import Group
from consts import RESPONSE_EMPTY, RESPONSE_OK, RESPONSE_CONFLICT


class MultichannelAlohaEP:
    def __init__(self, lambd: float, slots, users_count, ch_count: int, 
                 ep_len: float, verbose=False):
        self.lambd = lambd
        self.slots = slots
        self.users_count = users_count
        self.ch_count = ch_count
        self.ep_len = ep_len
        self.verbose = verbose


    def run_theory(self):
        # l = self.lambd
        # M = self.channels
        # # K = self.users_count
        # # K = (l/M) / (1 - l/M) # Erlang

        # # max_throughput = K * math.e ** (-K/M) # 1 ((10) in article)
        # max_throughput = M * math.e ** (-1) # 2 ((10) in article)
        # input_arrival_rate = l * math.e ** (- l/M)
        # return max_throughput, input_arrival_rate
        return 0.0, 0.0


    def run_simulation(self) -> tuple[float, float, float]:
        users = [User(id_, self.lambd/self.users_count, self.slots) 
                    for id_ in range(self.users_count)]

        for cur_slot in range(self.slots):
            if self.verbose: print(f"\n>>> SLOT #{cur_slot+1}:")
            bs_response = self._run_frame(users, cur_slot)
            if self.verbose: utils.print_bs_response(bs_response)

        processed_requests = 0
        requests_overall = 0

        for user in users:
            processed_requests += len(user.sent_data_packets)
            requests_overall += len(user.data_packets_to_send) + \
                len(user.sent_data_packets)

        lambda_in = requests_overall / self.slots
        lambda_out = processed_requests / self.slots
        avg_delay = utils.calc_avg_delay(users)

        return lambda_in, lambda_out, avg_delay


    def _run_frame(self, users: list, cur_slot: int) -> list[int]:
        self._generate_requests(users, cur_slot)
        active_users = self._find_active_users(users)
        if len(active_users) == 0: 
            if self.verbose:
                print("No active users in the current slot")
            return [0 for _ in range(self.ch_count)]
        
        ch_situation = self._exploration_phase(active_users)
        if self.verbose:
            print("Users make next choice:")
            utils.print_channels_situation(ch_situation)
        group_success, group_conflict = self._split_to_groups(ch_situation)

        if not self._is_empty(group_conflict):
            self._reselect(group_conflict)
            if self.verbose:
                print("Users in contention reselect channels:")
                utils.print_channels_situation(group_conflict)
        bs_response = \
            self._data_transmission_phase(group_success, group_conflict, cur_slot)

        return bs_response


    def _generate_requests(self, users: list, cur_slot: int):
        for user in users:
            user.update_requests(cur_slot)

    
    def _find_active_users(self, users: list) -> list:
        active_users = []
        for user in users:
            # if user has data packet to send
            if user.is_active():
                active_users.append(user)
        return active_users
    

    def _exploration_phase(self, active_users: list) -> dict[int, set["User"]]:
        ch_situation = {num: set() for num in range(self.ch_count)}
        P_ep = min(1, self.ch_count / len(active_users))
        for user in active_users:
            if user.decide_transmit(P_ep):
                user.choose_channel(ch_situation)
        return ch_situation
    

    def _split_to_groups(self, ch_situation: dict[int, set["User"]]) \
            -> tuple[Group, Group]:
        group_success = {}
        group_conflict = {}

        # Assign a user to group G_s or G_c
        for channel, users in ch_situation.items():
            if len(users) == 1:
                contention_free_user = users.pop()
                group_success[channel] = {contention_free_user}
            else:
                group_conflict[channel] = users.copy()
        return group_success, group_conflict
    

    def _is_empty(self, group: Group) -> bool:
        for users in group.values():
            if len(users) != 0:
                return False
        return True


    def _reselect(self, group: Group):
        users_in_contention = set()
        for users in group.values():
            users_in_contention.update(users)
            users.clear()

        for user in users_in_contention:
            new_channel = user.reselect_channel(list(group.keys()))
            group[new_channel].add(user)


    def _data_transmission_phase(self, group_success, group_conflict: Group, \
                                 cur_slot: int) -> list[int]:
        bs_response = [0 for _ in range(self.ch_count)]

        for channel, user in group_success.items():
            contention_free_user = user.pop()
            contention_free_user.get_response_from_BS(RESPONSE_OK, cur_slot)
            bs_response[channel] = RESPONSE_OK

        for channel, users in group_conflict.items():
            if len(users) == 0:
                bs_response[channel] = RESPONSE_EMPTY
            else:
                users_decisions = {}
                P_dtp = min(1, (self.ch_count - len(group_success)) / len(group_conflict))
                for user in users:
                    users_decisions[user] = user.decide_transmit(P_dtp)

                # No one decided to transmit packet
                if all(dec is False for dec in list(users_decisions.values())):
                    bs_response[channel] = RESPONSE_EMPTY
                # Someone decided to transmit packet
                else:
                    if list(users_decisions.values()).count(True) == 1:
                        bs_response[channel] = RESPONSE_OK
                        for user, decision in users_decisions.items():
                            if decision is True:
                                user.get_response_from_BS(RESPONSE_OK, cur_slot)
                                break
                    else:
                        bs_response[channel] = RESPONSE_CONFLICT
                        for user, decision in users_decisions.items():
                            if decision is True:
                                user.get_response_from_BS(RESPONSE_CONFLICT, cur_slot)
        
        return bs_response

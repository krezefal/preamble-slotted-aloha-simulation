import math

from aloha.old.user_conv import User
from aloha import utils

from aloha.utils import BS_feedback, Group, BS_response
from consts import RESPONSE_EMPTY, RESPONSE_OK, RESPONSE_CONFLICT


class AlohaEP:
    def __init__(self, lambda_, slots, users_count: int, *, channels=1, \
                 p_dtp=None, verbose=False):
        self.lambda_ = lambda_
        self.slots = slots
        self.users_count = users_count

        self.channels = channels
        self.p_dtp = p_dtp

        self.verbose = verbose


    def run_theory(self):
        l = self.lambda_
        M = self.channels
        # K = self.users_count
        K = (l/M) / (1 - l/M) # Erlang
        max_S_K = K * math.e * (- K/M)

        max_throughput = M * math.e ** (-1) + (1 - math.e ** (-1)) * max_S_K
        input_arrival_rate = l * math.e ** (- l/M)
        return max_throughput, input_arrival_rate


    def run_simulation(self) -> tuple[float, float, float, float]:
        users = [User(id_, self.lambda_, self.slots, self.channels) \
                 for id_ in range(self.users_count)]

        for cur_slot in range(self.slots):
            if self.verbose:
                print(f"Slot #{cur_slot}:")

            bs_response = self._run_frame(users, cur_slot)

            if self.verbose:
                utils.print_bs_response(bs_response)

        processed_requests = 0
        requests_overall = 0

        for user in users:
            processed_requests += len(user.sent_data_packets)
            requests_overall += len(user.data_packets_to_send) + \
                len(user.sent_data_packets)

        lambda_in = requests_overall / self.slots
        lambda_out = processed_requests / self.slots # throughput?
        avg_delay = utils.calc_avg_delay(users)
        avg_active_users = utils.calc_avg_active_users(users, self.slots)

        return lambda_in, lambda_out, avg_delay, avg_active_users


    def _run_frame(self, users: list, cur_slot: int) -> BS_response:
        self._generate_requests(users, cur_slot)
        feedback = self._exploration_phase(users)

        if self.verbose:
            print("Users make next choice:")
            utils.print_channels_situation(feedback)

        # If p_dtp calculation is performed, the simulation will end with
        # better results than with random p_dtp
        if self.p_dtp is None:
            self.p_dtp = self._calc_p_dtp(feedback)
        group1, group2 = self._calc_groups(feedback)

        if self._is_not_empty(group2):

            if self.verbose:
                print("Users in contention will choose channels again \
                        (excluding those where only 1 active user)")

            self._rearrange_group2(group2)

            if self.verbose:
                print(f"Their new choices:\n{feedback}")
                utils.print_channels_situation(group2)

        base_station_response = \
            self._data_transmission_phase(group1, group2, cur_slot)
        return base_station_response


    def _generate_requests(self, users: list, cur_slot: int):
        for user in users:
            user.update_requests(cur_slot)


    def _exploration_phase(self, users: list) -> BS_feedback:
        channels_situation = {num: set() for num in range(self.channels)}
        for user in users:
            if user.is_active():
                user.send_self(channels_situation) # send preamble
        return channels_situation


    def _calc_p_dtp(self, feedback: BS_feedback) -> float:
        S, K = 0, 0
        for users in feedback.values():
            if len(users) == 1:
                S += 1
            K += len(users)

        W = K - S
        L = self.channels - S
        
        if W == 0:
            return 1
        else:
            return min(1, L/W)


    def _calc_groups(self, feedback: BS_feedback) -> tuple[Group, Group]:
        group1 = {}
        group2 = {}

        # Distribution of users by groups (I or II)
        for channel, users in feedback.items():
            if len(users) == 1:
                contention_free_user = users.pop()
                contention_free_user.p = 1
                group1[channel] = {contention_free_user}
            else:
                for user_in_contention in users:
                    user_in_contention.p = self.p_dtp
                group2[channel] = users.copy()
                users.clear()
        return group1, group2


    def _is_not_empty(self, group: Group) -> bool:
        for users in group.values():
            if len(users) != 0:
                return False
        return True


    def _rearrange_group2(self, group2: Group):
        users_in_contention = set()
        for users in group2.values():
            users_in_contention.update(users)
            users.clear()

        for user in users_in_contention:
            user.change_channel(list(group2.keys()))
            group2[user.channel].add(user)


    def _data_transmission_phase(self, group1, group2: Group, \
                                 cur_slot) -> BS_response:
        base_station_response = [num for num in range(self.channels)]

        for channel, user in group1.items():
            contention_free_user = user.pop()
            contention_free_user.decide_transmit_packet()

            base_station_response[channel] = RESPONSE_OK
            contention_free_user.get_response_from_BS(RESPONSE_OK, cur_slot)

        for channel, users in group2.items():
            if len(users) == 0:
                base_station_response[channel] = RESPONSE_EMPTY

            elif len(users) == 1:
                contention_free_user = users.pop()
                contention_free_user.decide_transmit_packet()

                base_station_response[channel] = RESPONSE_OK
                contention_free_user.get_response_from_BS(RESPONSE_OK, cur_slot)

            else:
                users_decisions = {}
                for user in users:
                    users_decisions[user] = user.decide_transmit_packet()

                # No one decided to transmit packet
                if all(
                    decision is False for decision in list(users_decisions.values())
                ):
                    base_station_response[channel] = RESPONSE_EMPTY
                # Everyone decided to transmit packet
                elif all(
                    decision is True for decision in list(users_decisions.values())
                ):
                    base_station_response[channel] = RESPONSE_CONFLICT
                    for user in users:
                        user.get_response_from_BS(RESPONSE_CONFLICT, cur_slot)
                # Someone decided to transmit packet, but someone did not
                else:
                    if list(users_decisions.values()).count(True) == 1:
                        contention_free_user = None
                        for user, decision in users_decisions.items():
                            if decision is True:
                                contention_free_user = user
                                break

                        base_station_response[channel] = RESPONSE_OK
                        contention_free_user.get_response_from_BS(RESPONSE_OK, cur_slot)
                    else:
                        for user, decision in users_decisions.items():
                            if decision is True:
                                user.get_response_from_BS(RESPONSE_CONFLICT, cur_slot)
                        base_station_response[channel] = RESPONSE_CONFLICT

        return base_station_response

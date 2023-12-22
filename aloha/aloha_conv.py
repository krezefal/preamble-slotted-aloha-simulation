from aloha.user_conv import User
from aloha import utils
from consts import RESPONSE_EMPTY, RESPONSE_OK, RESPONSE_CONFLICT


class AlohaConv:
    def __init__(self, lambd: float, slots, users_count: int, verbose=False):
        self.lambd = lambd
        self.slots = slots
        self.users_count = users_count
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


    def _run_frame(self, users: list, cur_slot: int) -> int:
        self._generate_requests(users, cur_slot)
        active_users = self._find_active_users(users)
        bs_response = self._data_transmission_phase(active_users, cur_slot)
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


    def _data_transmission_phase(self, active_users: list, cur_slot: int) -> int:
        if len(active_users) == 0:
            base_station_response = RESPONSE_EMPTY
        else:
            active_users_decisions = {}
            P_dtp = 1 / len(active_users)
            for user in active_users:
                active_users_decisions[user] = user.decide_transmit_packet(P_dtp)

            # No one decided to transmit packet
            if all(dec is False for dec in list(active_users_decisions.values())):
                base_station_response = RESPONSE_EMPTY
            # Someone decided to transmit packet
            else:
                if list(active_users_decisions.values()).count(True) == 1:
                    base_station_response = RESPONSE_OK
                    for user, decision in active_users_decisions.items():
                        if decision is True:
                            user.get_response_from_BS(RESPONSE_OK, cur_slot)
                            break
                else:
                    base_station_response = RESPONSE_CONFLICT
                    for user, decision in active_users_decisions.items():
                        if decision is True:
                            user.get_response_from_BS(RESPONSE_CONFLICT, cur_slot)
        
        return base_station_response

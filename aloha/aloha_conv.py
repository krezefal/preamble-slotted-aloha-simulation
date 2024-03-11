import numpy as np

from aloha.user import UniqUser
from aloha import utils
from consts import RESPONSE_EMPTY, RESPONSE_OK, RESPONSE_CONFLICT


class AlohaConv:
    def __init__(self, lambd: float, slots: int, slot_len: float, 
                 verbose=False):
        
        self.lambd = lambd
        self.slots = slots
        self.slot_len = slot_len
        self.verbose = verbose

        self.id_counter = 0


    def run_theory(self) -> tuple[float, float, float]:
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
        # Average delay is calculated in seconds (not in 'slots')
        avg_delay = utils.calc_avg_delay(sent_data_packets)
        
        return lambda_in, lambda_out, avg_delay


    def _run_frame(self, poisson_dist: list[int], 
                   active_users: dict[int, UniqUser], 
                   sent_data_packets: list[UniqUser], cur_slot: int) -> int:
        
        # Update active users list
        for _ in range(poisson_dist[cur_slot]):
            self.id_counter += 1
            active_users[self.id_counter] = UniqUser(self.id_counter, cur_slot,
                                                    self.slot_len)

        # Data transmission phase
        if len(active_users) == 0:
            base_station_response = RESPONSE_EMPTY
        else:
            active_users_decisions = {}
            P_dtp = 1 / len(active_users)
            for user in active_users.values():
                active_users_decisions[user] = np.random.rand() < P_dtp

            # No one decided to transmit packet
            if all(dec is False for dec in 
                   list(active_users_decisions.values())):
                base_station_response = RESPONSE_EMPTY
            # Someone decided to transmit packet
            else:
                if list(active_users_decisions.values()).count(True) == 1:
                    base_station_response = RESPONSE_OK
                    for user, decision in active_users_decisions.items():
                        if decision is True:

                            user_data_packet = active_users.pop(user.id_)
                            user_data_packet.processed(cur_slot)
                            sent_data_packets.append(user_data_packet)
                            break
                else:
                    base_station_response = RESPONSE_CONFLICT
                    # No one leaves from active users list
        
        return base_station_response

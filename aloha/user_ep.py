import random
import numpy as np
from numpy.random import poisson

from aloha.data_packet import DataPacket
from consts import RESPONSE_OK, RESPONSE_CONFLICT


class User:
    def __init__(self, id_: int, lambd: float, slots: int):
        self.id_ = id_
        self.poisson_dist = poisson(lambd, slots)
        self.data_packets_to_send = []
        self.sent_data_packets = []


    def update_requests(self, slot: int):
        for _ in range(self.poisson_dist[slot]):
            self.data_packets_to_send.append(DataPacket(slot))


    def is_active(self) -> bool:
        # If there is data packet to send
        if self.data_packets_to_send:
            return True
        else:
            return False


    def decide_transmit(self, P: float) -> bool:
        decision = np.random.rand() < P
        return decision
    

    def choose_channel(self, ch_dict: dict[int, set["User"]]):
        channel = random.randrange(len(ch_dict))
        # Adding self to be able to make some calculations later
        ch_dict[channel].add(self)


    def reselect_channel(self, available_channels: list[int]):
        return random.choice(available_channels)


    def get_response_from_BS(self, channel_response, exit_slot: int):
        if channel_response == RESPONSE_OK:
            cur_data_packet = self.data_packets_to_send.pop(0)
            cur_data_packet.processed(exit_slot)
            self.sent_data_packets.append(cur_data_packet)
        if channel_response == RESPONSE_CONFLICT:
            # Nothing to do
            return


    def get_avg_delay(self):
        if len(self.sent_data_packets) == 0:
            return 0

        overall_delay = 0
        for sent_data_packet in self.sent_data_packets:
            overall_delay += sent_data_packet.get_processing_time()
        return overall_delay / len(self.sent_data_packets)

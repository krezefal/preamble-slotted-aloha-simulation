import random
from numpy.random import poisson

from aloha.user import DataPacket
from aloha.utils import BS_feedback, ChannelList
from consts import RESPONSE_OK


class User:
    def __init__(self, id_, lambda_, slots, channels: int, p: float):
        self.id_ = id_
        self.poisson_dist = poisson(lambda_, slots)
        self.channels = channels

        self.activity_counter = 0
        self.sending_flag = None
        self.channel = None
        self.p = p

        self.data_packets_to_send = []
        self.sent_data_packets = []


    def update_requests(self, slot: int):
        for _ in range(self.poisson_dist[slot]):
            self.data_packets_to_send.append(DataPacket(slot))


    def is_active(self) -> bool:
        # If there is data packet to send
        if self.data_packets_to_send:
            self.activity_counter += 1
            self.sending_flag = True
            return True
        else:
            return False


    def send_message(self, channels_situation: BS_feedback):
        self.channel = random.randrange(self.channels)
        # Adding self to be able to make some calculations later
        channels_situation[self.channel].add(self)


    def change_channel(self, available_channels: ChannelList):
        self.channel = random.choice(available_channels)


    def decide_transmit_packet(self) -> bool:
        decision = random.uniform(0, 1) < self.p
        # User decided to transmit packet in next slot in which a new
        # choice of channels will be appeared
        if decision is False:
            self.sending_flag = None
            self.channel = None
            self.p = 0.0
        return decision


    def get_response_from_BS(self, channel_response, exit_slot: int):
        if channel_response == RESPONSE_OK:
            cur_data_packet = self.data_packets_to_send.pop(0)
            cur_data_packet.processed(exit_slot)
            self.sent_data_packets.append(cur_data_packet)
            self.sending_flag = None
            self.channel = None
            self.p = 0.0
        else:  # RESPONSE_CONFLICT
            self.sending_flag = None
            self.channel = None
            self.p = 0.0
        # There is no option with RESPONSE_EMPTY, because in this case
        # user just skip packet transmission and does not participate
        # in any channel => user does not wait for a BS response


    def get_avg_delay(self):
        if len(self.sent_data_packets) == 0:
            return 0

        overall_delay = 0
        for sent_data_packet in self.sent_data_packets:
            overall_delay += sent_data_packet.get_processing_time()
        return overall_delay / len(self.sent_data_packets)

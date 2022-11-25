from random import randrange, uniform
from numpy.random import poisson

from data_packet import DataPacket
from utils import *
from vars import *


class User:
    def __init__(self, id_: int):
        self.id_ = id_

        self.poisson_dist = poisson(LAMBDA, SLOTS)

        self.sending_flag = None
        self.channel = None
        self.p = None

        self.data_packets_to_send = []
        self.sent_data_packets = []

    def update_requests(self, slot: int):
        for _ in range(self.poisson_dist[slot]):
            self.data_packets_to_send.append(DataPacket(slot))

    def is_active(self) -> bool:
        # There is data packet to send
        if self.data_packets_to_send:
            self.sending_flag = True
        return self.sending_flag

    def send_preamble(self, channels_situation: BS_feedback):
        self.channel = randrange(CHANNELS)
        channels_situation[self.channel].add(self)

    def change_channel(self, available_channels: ChannelSet):
        self.channel = random.choice(tuple(available_channels))

    def decide_transmit_packet(self) -> bool:
        decision = uniform(0, 1) <= self.p
        # User decided to transmit packet in next slot in which a new 
        # choice of channels will be appeared
        if decision is False:
            self.sending_flag = None
            self.channel = None
            self.p = None
        return decision

    def get_response_from_BS(self, channel_response, exit_slot: int):
        if channel_response == RESPONSE_OK:
            cur_data_packet = self.data_packets_to_send.pop(0)
            cur_data_packet.processed(exit_slot)
            self.sent_data_packets.append(cur_data_packet)
            self.sending_flag = None
            self.channel = None
            self.p = None
        else:  # RESPONSE_CONFLICT
            self.sending_flag = None
            self.channel = None
            self.p = None
        # There is no option with RESPONSE_EMPTY, because in this case 
        # user just skip packet transmission and does not participate 
        # in any channel => user does not wait for a BS response

    def sum(self):
        overall_delay = 0

        for processed_request in self.sent_data_packets:
            overall_delay += processed_request.get_processing_time()

        return overall_delay / len(self.sent_data_packets)

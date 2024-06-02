import math
import numpy as np
from prettytable import PrettyTable
from colorama import Fore, Style

from aloha.user import UniqUser
from consts import RESPONSE_EMPTY, RESPONSE_OK, RUS_TITLES


def generate_stream(lambd: float, slots: int, slot_len: float, 
                    verbose: bool) -> tuple[list[int], list[int]]:
    poisson_dist = [0] * slots
    cur_timestamp = 0.0
    timestamps = []

    while True:
        dt = ((-1 / lambd) * (np.log(np.random.rand())))
        cur_timestamp += dt
        if cur_timestamp > (slots - 1) * slot_len:
            break

        timestamps.append(cur_timestamp)

    for t in timestamps:
        slot_num = np.ceil(t / slot_len)
        poisson_dist[int(slot_num)] += 1

    if verbose:
        if RUS_TITLES:
            print(f"ВРЕМЕННЫЕ МЕТКИ:\n{timestamps}\n")
            print(f"АКТИВНОСТЬ АБОНЕНТОВ ПО СЛОТАМ (длина слота = \
{slot_len}):\n{poisson_dist}")
        else:
            print(f"REQUESTS TIMESTAMPS:\n{timestamps}\n")
            print(f"ACTIVE USERS IN SLOTS (slot length = {slot_len}):\n\
{poisson_dist}")

    return timestamps, poisson_dist


def calc_avg_delay(sent_data_packets: list[UniqUser]) -> float:
    if len(sent_data_packets) == 0:
        return 0.0
    else:
        overall_delay = 0
        for sent_data_packet in sent_data_packets:
            overall_delay += sent_data_packet.get_processing_time()
        return overall_delay / len(sent_data_packets)
    

def calc_avg_delay_tuples(sent_data_packets: list[tuple[int, int]], 
                          slot_len: float) -> float:
    if len(sent_data_packets) == 0:
        return 0.0
    else:
        overall_delay = 0
        for sent_data_packet in sent_data_packets:
            overall_delay += \
                (sent_data_packet[1] - sent_data_packet[0] + 1) * slot_len
        return overall_delay / len(sent_data_packets)


def print_channels_situation(ch_dict: dict[int, set[UniqUser]]):
    chan_no = "Channel #"
    usr_id_header =  "Users ID"

    if RUS_TITLES:
        chan_no = "Канал №"
        usr_id_header = "Номер абонента"

    table = PrettyTable()
    table.field_names = [chan_no, usr_id_header]

    for chan, users in ch_dict.items():
        table.add_row([chan] + [[user.id_ for user in users]])
    print(table)


def print_channels_situation_users_id(ch_dict: dict[int, set[int]]):
    chan_no = "Channel #"
    usr_id_header =  "Users ID"

    if RUS_TITLES:
        chan_no = "Канал №"
        usr_id_header = "Номер абонента"

    table = PrettyTable()
    table.field_names = [chan_no, usr_id_header]

    for chan, users_id in ch_dict.items():
        table.add_row([chan] + [[user_id for user_id in users_id]])
    print(table)


def print_bs_response(bs_response: int | list[int]):
    empty, ok, conflict = "EMP", "OK", "CON"
    bs_resp_str = "Base station response"
    chan_no = "Channel #"
    resp_header = "Response"

    if RUS_TITLES:
        empty = "П"
        ok = "У"
        conflict = "К"
        bs_resp_str = "Ответ от БС"
        chan_no = "Канал №"
        resp_header = "Ответ"

    if isinstance(bs_response, int):
        if bs_response == RESPONSE_EMPTY:
            print(f"{bs_resp_str}: {Fore.LIGHTBLACK_EX}{empty}{Style.RESET_ALL}")
        elif bs_response == RESPONSE_OK:
            print(f"{bs_resp_str}: {Fore.GREEN}{ok}{Style.RESET_ALL}")
        else:
            print(f"{bs_resp_str}: {Fore.RED}{conflict}{Style.RESET_ALL}")
    else:
        print(f"{bs_resp_str}:")
        table = PrettyTable()
        table.field_names = [chan_no, resp_header]
        for chan, event in enumerate(bs_response):
            if event == RESPONSE_EMPTY:
                table.add_row([chan] + [Fore.LIGHTBLACK_EX + empty + Style.RESET_ALL])
            elif event == RESPONSE_OK:
                table.add_row([chan] + [Fore.GREEN + ok + Style.RESET_ALL])
            else:
                table.add_row([chan] + [Fore.RED + conflict + Style.RESET_ALL])
        print(table)


def factorial_product(arr: list[int]) -> int:
    result = 1
    for el in arr:
        result *= math.factorial(el)
    return result


def generate_users_in_channels(upper_lim, l: int):
    def gen_combs_recursion(curr_combination, depth):
        if depth == l:
            yield curr_combination.copy()
            return
        
        for num in range(upper_lim):
            if num == 1:
                continue
            curr_combination.append(num)
            yield from gen_combs_recursion(curr_combination, depth + 1)
            curr_combination.pop()
    
    initial_combination = []
    yield from gen_combs_recursion(initial_combination, 0)

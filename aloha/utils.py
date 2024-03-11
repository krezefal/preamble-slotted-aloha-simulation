import numpy as np
from prettytable import PrettyTable
from colorama import Fore, Style

from aloha.user import UniqUser
from consts import RESPONSE_EMPTY, RESPONSE_OK


def generate_stream(lambd: float, slots: int, slot_len: float, 
                    verbose: bool) -> list[int]:
    poisson_dist = [0] * slots
    cur_timestamp = 0.0
    timestamps = []

    while True:
        dt = ((-1 / (lambd)) * (np.log(np.random.rand())))
        cur_timestamp += dt
        if cur_timestamp > (slots - 1) * slot_len:
            break

        timestamps.append(cur_timestamp)

    for t in timestamps:
        slot_num = np.ceil(t / slot_len) 
        poisson_dist[int(slot_num)] += 1

    if verbose: 
        print(f"REQUESTS TIMESTAMPS:\n{timestamps}\n")
        print(f"ACTIVE USERS IN SLOTS (slot length = {slot_len}):\n\
{poisson_dist}")

    return poisson_dist


def calc_avg_delay(sent_data_packets: list[UniqUser]) -> float:
    if len(sent_data_packets) == 0:
        return 0.0
    else:
        overall_delay = 0
        for sent_data_packet in sent_data_packets:
            overall_delay += sent_data_packet.get_processing_time()
        return overall_delay / len(sent_data_packets)


def print_channels_situation(ch_dict: dict[int, set[UniqUser]]):
    table = PrettyTable()
    table.field_names = ["Channel #", "Users ID"]
    for chan, users in ch_dict.items():
        table.add_row([chan] + [[user.id_ for user in users]])
    print(table)


def print_bs_response(bs_response: int | list[int]):
    if isinstance(bs_response, int):
        if bs_response == RESPONSE_EMPTY:
            print(f"Base station response: {Fore.LIGHTBLACK_EX}EMP{Style.RESET_ALL}")
        elif bs_response == RESPONSE_OK:
            print(f"Base station response: {Fore.GREEN}OK{Style.RESET_ALL}")
        else:
            print(f"Base station response: {Fore.RED}CON{Style.RESET_ALL}")
    else:
        print("Base station response:")
        table = PrettyTable()
        table.field_names = ["Channel #", "Response"]
        for chan, event in enumerate(bs_response):
            if event == RESPONSE_EMPTY:
                table.add_row([chan] + [Fore.LIGHTBLACK_EX + 'EMP'+ Style.RESET_ALL])
            elif event == RESPONSE_OK:
                table.add_row([chan] + [Fore.GREEN + 'OK' + Style.RESET_ALL])
            else:
                table.add_row([chan] + [Fore.RED + 'CON' + Style.RESET_ALL])
        print(table)

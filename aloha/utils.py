from prettytable import PrettyTable
from colorama import Fore, Style

from consts import RESPONSE_EMPTY, RESPONSE_OK


Group = dict[int, set["User"]]


def calc_avg_delay(users):
    overall_delay = 0
    for user in users:
        overall_delay += user.get_avg_delay()
    return overall_delay / len(users)


def print_channels_situation(ch_dict: dict[int, set["User"]]):
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

import matplotlib.pyplot as plt
from colorama import Fore, Style

from user import User
from utils import *
from vars import *


def generate_requests(users: list, cur_slot: int):
    for user in users:
        user.update_requests(cur_slot)


def exploration_phase(users: list) -> BS_feedback:
    channels_situation = {num: set() for num in range(CHANNELS)}
    for user in users:
        if user.is_active():
            user.send_preamble(channels_situation)

    return channels_situation


def calc_user_groups(feedback: BS_feedback) -> tuple[Group, Group]:
    group1 = {}
    group2 = {}

    # Probability assignment according to the Group (I or II)
    for channel, users in feedback.items():
        if len(users) == 1:
            contention_free_user = users.pop()
            contention_free_user.p = 1
            group1[channel] = {contention_free_user}
        else:
            for user_in_contention in users:
                user_in_contention.p = P_dtp
            group2[channel] = users

    return group1, group2


def users_in_contention_change_channel(group2: Group) -> Group:
    available_channels = set(group2.keys())
    users_in_contention = set()
    for users in group2.values():
        users_in_contention.update(users)

    new_group2 = {}
    for user in users_in_contention:
        user.change_channel(available_channels)
        if user.channel not in new_group2:
            new_group2[user.channel] = {user}
        else:
            new_group2[user.channel].add(user)

    return new_group2


def data_transmission_phase(group1, group2: Group, cur_slot) -> BS_response:
    base_station_response = [num for num in range(CHANNELS)]

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
            if all(decision is False for decision in list(users_decisions.values())):
                base_station_response[channel] = RESPONSE_EMPTY
            # Everyone decided to transmit packet
            elif all(decision is True for decision in list(users_decisions.values())):
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
                            base_station_response[channel] = RESPONSE_CONFLICT
                            user.get_response_from_BS(RESPONSE_CONFLICT, cur_slot)

    return base_station_response


def simulation():
    users = [User(id_) for id_ in range(USERS_COUNT)]

    for cur_slot in range(SLOTS):

        print(f'{Fore.YELLOW}Slot #{cur_slot}:{Style.RESET_ALL}')
        generate_requests(users, cur_slot)
        feedback = exploration_phase(users)
        print(f'Users make next choice: ...')
        group1, group2 = calc_user_groups(feedback)
        print(f'So: ...')
        new_group2 = users_in_contention_change_channel(group2)
        print(f'New choices for users in group2: ...')
        base_stations_response = data_transmission_phase(group1, new_group2, cur_slot)

    requests_overall = 0
    lambda_out = 0

    for user in users:
        lambda_out += len(user.sent_data_packets)
        requests_overall += (len(user.data_packets_to_send) + len(user.sent_data_packets))

    print(f'\033[92mLamb_in: {requests_overall / SLOTS}')
    print(f'Lamb_out: {lambda_out / SLOTS}\n')

    print(f'Average delay: {calculate_average_delay(users)}\033[0m')

    plt.figure(1)
    plt.axhline(y=LAMBDA, color='grey', linestyle='--')
    plt.grid(True)
    plt.xlabel('Timeline')
    plt.ylabel('Lambda')

    plt.legend(['Lambda_1', 'Lambda_2'])
    plt.show()


if __name__ == '__main__':
    simulation()

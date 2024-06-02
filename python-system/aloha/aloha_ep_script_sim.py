import random
import numpy as np

from aloha.utils import *
from consts import ONE_PREAMBLE_MODE, RUS_TITLES, \
    RESPONSE_EMPTY, RESPONSE_OK, RESPONSE_CONFLICT, SIM_P_EP_EQ_ONE


ID_INDEX = 0
ENTRY_SLOT_INDEX = 1


def run_simulation(lambd, slot_len, g_param: float, 
                   slots, ch_num: int, 
                   verbose=False, lossless=False) \
                   -> tuple[float, float, float]:
    
    # Init runtime data
    id_counter = 0
    active_users = {}
    group_success = {}
    group_conflict = {}
    sent_data_packets = []
    ch_situation = {num: set() for num in range(ch_num)}
    timestamps, poisson_dist = generate_stream(lambd, slots, slot_len, verbose)

    # Run simulation
    for cur_slot in range(slots):
        if verbose: 
            if RUS_TITLES: print(f"\n>>> СЛОТ #{cur_slot}:")
            else: print(f"\n>>> SLOT #{cur_slot}:")

        id_counter, bs_response = run_frame(g_param, slot_len,
                                            ch_num, cur_slot, id_counter, 
                                            poisson_dist, 
                                            active_users, 
                                            ch_situation,
                                            group_success,
                                            group_conflict,
                                            sent_data_packets,
                                            verbose)
        
        group_success.clear()
        group_conflict.clear()
        ch_situation = {num: set() for num in range(ch_num)}
        if not lossless: active_users.clear()

        if verbose: print_bs_response(bs_response)

    # Calculate system params
    # Data packet == unique user in case of infinite number of users
    total_time = timestamps[-1]
    lambda_in = (len(sent_data_packets) + len(active_users)) / total_time
    lambda_out = len(sent_data_packets) / total_time
    avg_delay = calc_avg_delay_tuples(sent_data_packets, slot_len)

    return lambda_in, lambda_out, avg_delay


def run_frame(g_param, slot_len: float,
              ch_num, cur_slot, id_counter: int,
              poisson_dist: list[int],
              active_users: dict[int, tuple[int, int]],
              ch_situation: dict[int, set[int]],
              group_success: dict[int, set[int]],
              group_conflict: dict[int, set[int]],
              sent_data_packets: list[tuple[int, int]],
              verbose: bool) -> tuple[int, list[int]]:
    
    # Update active users list
    for _ in range(poisson_dist[cur_slot]):
        id_counter += 1
        active_users[id_counter] = (id_counter, cur_slot)

    if len(active_users) == 0: 
        if verbose:
            if RUS_TITLES: print("В текущем слоте нет заявок")
            else: print("No active users in the current slot")
        return id_counter, [RESPONSE_EMPTY for _ in range(ch_num)]
        
    # If there is only 1 unique preamble and >1 users arrive, the conflict 
    # appears (because of preamble collision)
    if ONE_PREAMBLE_MODE:
        if len(active_users) > 1:
            return id_counter, [RESPONSE_CONFLICT for _ in range(ch_num)]

    # Exploration phase
    # EP: active users choosing channels
    if SIM_P_EP_EQ_ONE: P_ep = 1
    else: P_ep = min(1, (ch_num  * g_param * slot_len) / len(active_users))

    for user in active_users.values():
        if np.random.rand() < P_ep:
            channel = random.randrange(len(ch_situation))
            ch_situation[channel].add(user[ID_INDEX])

    if is_empty(ch_situation):
        if verbose:
            if RUS_TITLES: print("Пользователи решили не передавать \
сообщения в текущем слоте")
            else: print("All active users decided not to transmit message \
in the current slot")
        return id_counter, [RESPONSE_EMPTY for _ in range(ch_num)]

    if verbose:
        if RUS_TITLES: print("Абоненты выбрали следующие каналы:")
        else: print("Users make next choice:")
        print_channels_situation_users_id(ch_situation)
    
    # EP: split active users who decide to transmit a preamble into 2 groups
    for channel, users_id in ch_situation.items():
        if len(users_id) == 1:
            contention_free_user_id = users_id.pop()
            group_success[channel] = {contention_free_user_id}
        else:
            group_conflict[channel] = users_id.copy()

    if not is_empty(group_conflict) and ch_num > 1:
        # EP: users from a confict group reselect channels from this group
        users_id_in_contention = set()
        for users_id in group_conflict.values():
            users_id_in_contention.update(users_id)
            users_id.clear()

        for user_id in users_id_in_contention:
            new_channel = random.choice(list(group_conflict.keys()))
            group_conflict[new_channel].add(user_id)

        if verbose:
            if RUS_TITLES: print("Конфликтующие абоненты заново выбрали \
каналы")
            else: print("Users in contention reselect channels:")
            print_channels_situation_users_id(group_conflict)

    # Data transmission phase
    bs_response = [RESPONSE_EMPTY for _ in range(ch_num)]

    for channel, user_id in group_success.items():
        contention_free_user_id = user_id.pop()

        contention_free_user = active_users.pop(contention_free_user_id)
        user_data_packet = (contention_free_user[ENTRY_SLOT_INDEX], cur_slot)
        sent_data_packets.append(user_data_packet)
        bs_response[channel] = RESPONSE_OK

    P_dtp = 0.0
    if not is_empty(group_conflict):
        P_dtp = \
            min(1, (ch_num - len(group_success)) / users_in(group_conflict))
    else: 
        return id_counter, bs_response
        
    for channel, users_id in group_conflict.items():
        if len(users_id) != 0:
            active_users_decisions = {}
            for user_id in users_id:
                active_users_decisions[user_id] = np.random.rand() < P_dtp

            num_of_users_decided_to_transmit = \
                  calc_users_decided_to_transmit(active_users_decisions)

            # No one decided to transmit packet
            if num_of_users_decided_to_transmit == 0:
                bs_response[channel] = RESPONSE_EMPTY
            # Someone decided to transmit packet
            else:
                if num_of_users_decided_to_transmit == 1:
                    bs_response[channel] = RESPONSE_OK
                    for user_id, decision in active_users_decisions.items():
                        if decision == True:
                            
                            user = active_users.pop(user_id)
                            user_data_packet = (user[ENTRY_SLOT_INDEX], \
                                                cur_slot)
                            sent_data_packets.append(user_data_packet)
                            break
                else:
                    bs_response[channel] = RESPONSE_CONFLICT
                    # No one leaves from active users list unless it is not 
                    # lossy system. If so, active_users dict is cleared on exit
                    # from the run_frame()
    
    return id_counter, bs_response
    

def is_empty(group: dict[int, set[int]]) -> bool:
    for users_id in group.values():
        if len(users_id) != 0:
            return False
    return True


def users_in(group: dict[int, set[int]]) -> int:
    amount = 0
    for users_id in group.values():
        amount += len(users_id)
    return amount


def calc_users_decided_to_transmit(users_decisions: dict[int, bool]) -> int:
    amount = 0
    for decision in users_decisions.values():
        if decision == True:
            amount += 1
    return amount

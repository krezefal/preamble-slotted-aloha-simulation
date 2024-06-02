from colorama import Fore, Style

from aloha.aloha_ep_script_theory import calc_throughput
from aloha.aloha_ep_script_sim import run_simulation
from pkg import utils
from consts import *


def run_theory_per_slot_len(idx: int, slot_len: float) -> list[float]:
    slot_len = round(slot_len, ROUNDING)
    ep_len = round(slot_len - DTP_LEN, ROUNDING)

    if RUS_TITLES:
        print(f"Итерация #{idx+1}: длина слота = {slot_len} (ФИ={ep_len}, \
ФП={DTP_LEN})")
    else:
        print(f"Iteration #{idx+1}: slot len = {slot_len} (EP={ep_len}, \
DTP={DTP_LEN})")
        
    lambda_out_th_arr = []

    lambd_print_interval = len(LAMBDAS) // 10
    lambd_print_idx = 0

    for lambd in LAMBDAS:
        if HEARTBEAT_LOGS and LAMBDAS[lambd_print_idx] == lambd:
            lambd = round(lambd, ROUNDING)
            print(f"{Fore.LIGHTBLACK_EX}[Theor] slot len = {slot_len}; \
λ = {lambd}{Style.RESET_ALL}")
            if lambd_print_idx + lambd_print_interval < len(LAMBDAS):
                lambd_print_idx += lambd_print_interval

        lambda_out_th_arr.append(calc_throughput(lambd, slot_len, CH_NUM))

    return lambda_out_th_arr


def run_simulation_per_slot_len(idx: int, slot_len: float) -> \
    tuple[list[float],list[float],list[float],list[float],float,float]:

    slot_len = round(slot_len, ROUNDING)
    ep_len = round(slot_len - DTP_LEN, ROUNDING)

    if RUS_TITLES:
        print(f"Итерация #{idx+1}: длина слота = {slot_len} (ФИ={ep_len}, \
ФП={DTP_LEN})")
    else:
        print(f"Iteration #{idx+1}: slot len = {slot_len} (EP={ep_len}, \
DTP={DTP_LEN})")
        
    g_param = 1.0
    thr_limit_g_1 = 0.0
    lambda_out_g_1_arr = []
    avg_delay_g_1_arr = []

    lambd_print_interval = len(LAMBDAS) // 10
    lambd_print_idx = 0

    for lambd in LAMBDAS:
        if HEARTBEAT_LOGS and LAMBDAS[lambd_print_idx] == lambd:
            lambd = round(lambd, ROUNDING)
            print(f"{Fore.LIGHTBLACK_EX}[Sim] G = 1; slot len = {slot_len}; \
λ = {lambd}{Style.RESET_ALL}")
            if lambd_print_idx + lambd_print_interval < len(LAMBDAS):
                lambd_print_idx += lambd_print_interval
        
        _, lambda_out_sim, avg_delay_sim = run_simulation(lambd, slot_len, 
                                                          g_param, SLOTS, 
                                                          CH_NUM, VERBOSE,
                                                          LOSSLESS_SIM)

        lambda_out_g_1_arr.append(lambda_out_sim)
        avg_delay_g_1_arr.append(avg_delay_sim)

    if LOSSLESS_SIM and not DISABLE_CEILING_CALC:
        thr_limit_g_1 = utils.get_ceiling_avg(lambda_out_g_1_arr)

#     print(f"Slot len = {slot_len}, λ_in = {g_param}, λ_out = \
# {utils.calc_lambda_out_theoretically(slot_len, g_param)}")

    thr_limit_g_opt = 0.0
    lambda_out_g_opt_arr = []
    avg_delay_g_opt_arr = []

    if not DISABLE_G_OPT_SIM:

        g_param = G_OPT_ARR[idx]
        lambd_print_idx = 0

        for lambd in LAMBDAS:
            if HEARTBEAT_LOGS and LAMBDAS[lambd_print_idx] == lambd:
                lambd = round(lambd, ROUNDING)
                print(f"{Fore.LIGHTBLACK_EX}[Sim] G = {g_param}; \
slot len = {slot_len}; λ = {lambd}{Style.RESET_ALL}")
                if lambd_print_idx + lambd_print_interval < len(LAMBDAS):
                    lambd_print_idx += lambd_print_interval
            
            _, lambda_out_sim, avg_delay_sim = run_simulation(lambd, slot_len, 
                                                              g_param, SLOTS, 
                                                              CH_NUM, VERBOSE,
                                                              LOSSLESS_SIM)
            
            lambda_out_g_opt_arr.append(lambda_out_sim)
            avg_delay_g_opt_arr.append(avg_delay_sim)
        
        if LOSSLESS_SIM and not DISABLE_CEILING_CALC:
            thr_limit_g_opt = utils.get_ceiling_avg(lambda_out_g_opt_arr)

#         print(f"Slot len = {slot_len}, λ_in = {g_param}, λ_out = \
# {utils.calc_lambda_out_theoretically(slot_len, g_param)}")

    return \
        lambda_out_g_1_arr, lambda_out_g_opt_arr, \
        avg_delay_g_1_arr, avg_delay_g_opt_arr, \
        thr_limit_g_1, thr_limit_g_opt

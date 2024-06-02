import time
import numpy as np
import concurrent.futures
import matplotlib.pyplot as plt
from colorama import Fore, Style

from pkg import plotting, calculating
from consts import *


def run_theory() -> tuple[list[list[float]], list[float], list[float], str]:
    if RUS_TITLES: print(">> Аналитический расчет (система с потерями)")
    else: print(">> Theory (lossy system)")

    lambda_out_th_diff_slot_len = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        running_tasks = []
        for idx, slot_len in enumerate(SLOTS_LEN):
            task = executor.submit(calculating.run_theory_per_slot_len, 
                                   idx, slot_len)
            running_tasks.append(task)

        for running_task in running_tasks:
            lambda_out_th_arr = running_task.result()
            lambda_out_th_diff_slot_len.append(lambda_out_th_arr)

    max_throughput_diff_slot_len = [max(cur_lambda_out_th_arr) for 
        cur_lambda_out_th_arr in lambda_out_th_diff_slot_len]
    argmax_lambd_in_diff_slot_len = []

    print()
    for i, slot_len in enumerate(SLOTS_LEN):
        max_thr = round(max_throughput_diff_slot_len[i], ROUNDING)
        lambd_in = np.round(LAMBDAS[lambda_out_th_diff_slot_len[i].\
                    index(max_throughput_diff_slot_len[i])], ROUNDING)
        argmax_lambd_in_diff_slot_len.append(lambd_in)

        if RUS_TITLES:
            print(f"Макс. T(λ) на итерации #{i+1} = {max_thr} (λ={lambd_in})")
        else:
            print(f"Max T(λ) over iteration #{i+1} = {max_thr} (λ={lambd_in})")

    label = "Длина слота = "
    if not RUS_TITLES: label = "Slot len = "

    return lambda_out_th_diff_slot_len, max_throughput_diff_slot_len, \
        argmax_lambd_in_diff_slot_len, label


def run_simulation() -> tuple[list[list[float]], list[list[float]], \
                              list[list[float]], list[list[float]], \
                                list[float], list[float], list[str]]:

    if len(SLOTS_LEN) > len(G_OPT_ARR):
        if RUS_TITLES:
            print("[!] Для каждого значения длины слота необходимо указать \
свой параметр G_opt")
        else:
            print("[!] It is necessary to specify G_opt parameter per each \
slot len")
        return

    if RUS_TITLES and LOSSLESS_SIM: 
        print(">> Моделирование (система без потерь)")
    if RUS_TITLES and not LOSSLESS_SIM:
        print(">> Моделирование (система с потерями)")
    if not RUS_TITLES and LOSSLESS_SIM:
        print(">> Simulation (lossless system)")
    if not RUS_TITLES and not LOSSLESS_SIM:
        print(">> Simulation (lossy system)")

    lambda_out_g_1_diff_slot_len_sim = []
    lambda_out_g_opt_diff_slot_len_sim = []

    avg_delay_g_1_diff_slot_len_sim = []
    avg_delay_g_opt_diff_slot_len_sim = []

    thr_limit_g_1_diff_slot_len = []
    thr_limit_g_opt_diff_slot_len = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        running_tasks = []
        for idx, slot_len in enumerate(SLOTS_LEN):
            task = executor.submit(calculating.run_simulation_per_slot_len, 
                                   idx, slot_len)
            running_tasks.append(task)

        for running_task in running_tasks:
            lambda_out_g_1_arr, lambda_out_g_opt_arr, \
            avg_delay_g_1_arr, avg_delay_g_opt_arr, \
            thr_limit_g_1, thr_limit_g_opt = \
                running_task.result()

            lambda_out_g_1_diff_slot_len_sim.append(lambda_out_g_1_arr)
            lambda_out_g_opt_diff_slot_len_sim.append(lambda_out_g_opt_arr)

            avg_delay_g_1_diff_slot_len_sim.append(avg_delay_g_1_arr)
            avg_delay_g_opt_diff_slot_len_sim.append(avg_delay_g_opt_arr)

            thr_limit_g_1_diff_slot_len.append(thr_limit_g_1)
            thr_limit_g_opt_diff_slot_len.append(thr_limit_g_opt)

    if LOSSLESS_SIM and not DISABLE_G_OPT_SIM and not DISABLE_CEILING_CALC:
        for i, slot_len in enumerate(SLOTS_LEN):
            thr_limit_g_1 = round(thr_limit_g_1_diff_slot_len[i], ROUNDING)
            thr_limit_g_opt = round(thr_limit_g_opt_diff_slot_len[i], ROUNDING)
            thr_diff = round(thr_limit_g_opt - thr_limit_g_1, ROUNDING)
            thr_diff_percent = round(thr_diff * 100 / thr_limit_g_1, ROUNDING)

            if RUS_TITLES:
                print(f"\nИтерация #{i+1}:")
                print(f"  При G=1 T(λ)={thr_limit_g_1}")
                print(f"  При G_opt={G_OPT_ARR[i]} T(λ)={thr_limit_g_opt}")
                print(f"  Прирост при оптимальном параметре G составил \
{thr_diff} ({thr_diff_percent} %)")
            else:
                print(f"\nIteration #{i+1}:")
                print(f"  At G=1 T(λ)={thr_limit_g_1}")
                print(f"  At G_opt={G_OPT_ARR[i]} T(λ)={thr_limit_g_opt}")
                print(f"  The increase with G_opt = {thr_diff} \
({thr_diff_percent} %)")
    elif LOSSLESS_SIM and not DISABLE_CEILING_CALC:
        for i, slot_len in enumerate(SLOTS_LEN):
            thr_limit_g_1 = round(thr_limit_g_1_diff_slot_len[i], ROUNDING)

            if RUS_TITLES:
                print(f"\nИтерация #{i+1}:")
                print(f"  При G=1 T(λ)={thr_limit_g_1}")
            else:
                print(f"\nIteration #{i+1}:")
                print(f"  At G=1 T(λ)={thr_limit_g_1}")


    labels = [''] * 3

    if RUS_TITLES: labels[SLOT_LEN_IDX] = "Длина слота = "
    else: labels[SLOT_LEN_IDX] = "Slot len = "

    labels[G_1_IDX]= "G = 1"
    labels[G_OPT_IDX] = "G_opt = "

    #ma_len = int(len(LAMBDAS) * LAMBD_STEP * MOVING_AVG_FACTOR)
    #x_lim_right = LAMBDAS[-1] - LAMBDAS[-1] * PLOT_HIDE_PERCENT

    return lambda_out_g_1_diff_slot_len_sim, avg_delay_g_1_diff_slot_len_sim, \
        lambda_out_g_opt_diff_slot_len_sim, avg_delay_g_opt_diff_slot_len_sim,\
        thr_limit_g_1_diff_slot_len, thr_limit_g_opt_diff_slot_len, labels


def main():

    if RUS_TITLES: print(f"КОЛ-ВО КАНАЛОВ = {CH_NUM}:")
    else:  print(f"CHANNELS NUM = {CH_NUM}:")

    if not SINGLE_PLOT_FOR_THEORY_AND_SIM:
        if DISABLE_THEORY and DISABLE_SIM:
            if RUS_TITLES: print("Теория и моделирование отключены")
            else: print("Theory and simulation are disabled")

        if not DISABLE_THEORY: 
            start_time = time.time()
            lambda_out_th_diff_slot_len, max_throughput_diff_slot_len, \
                argmax_lambd_in_diff_slot_len, label = run_theory()
            
            plotting.plot_throughput_theory(lambda_out_th_diff_slot_len, 
                                            max_throughput_diff_slot_len,
                                            argmax_lambd_in_diff_slot_len,
                                            label)
            
            end_time = time.time()
            print(f"\n{Fore.LIGHTBLACK_EX}Theoretical calculations took \
{end_time - start_time} sec{Style.RESET_ALL}\n")

        if not DISABLE_SIM: 
            start_time = time.time()
            lambda_out_g_1_diff_slot_len_sim, \
                avg_delay_g_1_diff_slot_len_sim, \
                lambda_out_g_opt_diff_slot_len_sim, \
                avg_delay_g_opt_diff_slot_len_sim, \
                thr_limit_g_1_diff_slot_len, \
                thr_limit_g_opt_diff_slot_len, labels = run_simulation()

            plotting.plot_throughput_sim(lambda_out_g_1_diff_slot_len_sim,
                                         lambda_out_g_opt_diff_slot_len_sim,
                                         thr_limit_g_1_diff_slot_len,
                                         thr_limit_g_opt_diff_slot_len,
                                         labels)

            plotting.plot_delay_sim(avg_delay_g_1_diff_slot_len_sim,
                                    avg_delay_g_opt_diff_slot_len_sim,
                                    thr_limit_g_1_diff_slot_len,
                                    thr_limit_g_opt_diff_slot_len,
                                    labels)
            
            end_time = time.time()
            print(f"\n{Fore.LIGHTBLACK_EX}Simulation took \
{end_time - start_time} sec{Style.RESET_ALL}")
            
    else:
        start_time = time.time()

        lambda_out_diff_slot_len_sim, _, _, _, \
            thr_limit_diff_slot_len, _, _ = run_simulation()
        print()
        lambda_out_th_diff_slot_len, max_throughput_diff_slot_len, \
                argmax_lambd_in_diff_slot_len, label = run_theory()
        
        plotting.plot_throughput(lambda_out_diff_slot_len_sim,
                                 lambda_out_th_diff_slot_len,
                                 thr_limit_diff_slot_len,
                                 max_throughput_diff_slot_len,
                                 argmax_lambd_in_diff_slot_len,
                                 label)

        end_time = time.time()
        print(f"\n{Fore.LIGHTBLACK_EX}Theoretical calculations & simulation \
took {end_time - start_time} sec{Style.RESET_ALL}")

    plt.show()


if __name__ == '__main__':
    main()

import numpy as np
import matplotlib.pyplot as plt

from aloha.aloha_ep import MultichannelAlohaEP
from plotting import *
from consts import *


def simulate_system_per_slot_len(ch_num: int):
    lambda_out_diff_slot_len_theory = []
    lambda_out_diff_slot_len_sim = []
    avg_delay_diff_slot_len_sim = []

    if RUS_TITLES:
        print(f"КОЛ-ВО КАНАЛОВ = {ch_num}:")
    else:
        print(f"CHANNELS NUM = {ch_num}:")

    for i, slot_len in enumerate(SLOTS_LEN):

        slot_len = round(slot_len, ROUNDING)
        ep_len = round(slot_len - DTP_LEN, ROUNDING)

        if RUS_TITLES:
            print(f"Итерация #{i+1}: длина слота = {slot_len} \
(ФИ={ep_len}, ФП={DTP_LEN})")
        else:
            print(f"Iteration #{i+1}: slot len = {slot_len} \
(EP={ep_len}, DTP={DTP_LEN})")

        lambda_out_th_arr = []
        lambda_out_arr = []
        avg_delay_arr = []

        for lambd in LAMBDAS:
            #if VERBOSE:
            #    print(f"======( λ = {round(lambd, ROUNDING)} )======")
            
            mch_aloha_ep = MultichannelAlohaEP(lambd, SLOTS, slot_len, ch_num, 
                                               VERBOSE, DISABLE_THEORY, 
                                               DISABLE_SIM)

            # lambda_out_th == T(λ)
            lambda_out_th = mch_aloha_ep.calc_throughput()
            lambda_out_th_arr.append(lambda_out_th)

            _, lambda_out_sim, avg_delay_sim = mch_aloha_ep.run_simulation()
            lambda_out_arr.append(lambda_out_sim)
            avg_delay_arr.append(avg_delay_sim)

        lambda_out_diff_slot_len_theory.append(lambda_out_th_arr)
        lambda_out_diff_slot_len_sim.append(lambda_out_arr)
        avg_delay_diff_slot_len_sim.append(avg_delay_arr)

    max_throughput_diff_slot_len = [max(cur_lambda_out_th_arr) for 
        cur_lambda_out_th_arr in lambda_out_diff_slot_len_theory]
    
    if not DISABLE_THEORY:
        print()
        for i, slot_len in enumerate(SLOTS_LEN):
            t_lambd = round(max_throughput_diff_slot_len[i], ROUNDING)
            lambd_in = np.round(
                LAMBDAS[lambda_out_diff_slot_len_theory[i].\
                        index(max_throughput_diff_slot_len[i])], ROUNDING)
            
            if RUS_TITLES:
                print(f"Макс. T(λ) на итерации #{i+1} = {t_lambd} (λ={lambd_in})")
            else:
                print(f"Max T(λ) over iteration #{i+1} = {t_lambd} (λ={lambd_in})")

    label = "Длина слота = "
    if not RUS_TITLES: label = "Slot len = "
    
    # T(λ) theory
    plot_throughput_theory(ch_num, lambda_out_diff_slot_len_theory, label)
    
    #ma_len = int(len(LAMBDAS) * LAMBD_STEP * MOVING_AVG_FACTOR)
    #x_lim_right = LAMBDAS[-1] - LAMBDAS[-1] * PLOT_HIDE_PERCENT

    # T(λ) sim
    plot_throughput_sim(ch_num, lambda_out_diff_slot_len_sim, label)
    
    # Delay sim
    plot_delay_sim(ch_num, avg_delay_diff_slot_len_sim, label)


def main():
    for ch_num in CH_NUM:
        simulate_system_per_slot_len(ch_num)
        print()

    plt.show()


if __name__ == '__main__':
    main()

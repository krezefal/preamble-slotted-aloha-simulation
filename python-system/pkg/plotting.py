import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from pkg import utils
from consts import *


Y_LIM_DELAY = 30
PLOT_DARK_FACTOR = 0.7


def plot_throughput_theory(lambda_out_th_diff_slot_len: list[list[float]],
                           max_throughput_diff_slot_len: list[float],
                           argmax_lambd_in_diff_slot_len: list[float],
                           label: str):

    plt.figure(figsize=(12, 8))
    for i, slot_len in enumerate(SLOTS_LEN):
        slot_len = round(slot_len, ROUNDING)
        slot_len_label = label + str(slot_len)

        if i < len(COLORS): color = COLORS[i]
        else: color = utils.generate_random_color_rgb()

        # lambd_in_per_time = [lambd * slot_len for lambd in LAMBDAS]

        plt.plot(LAMBDAS, lambda_out_th_diff_slot_len[i], 
                 label = slot_len_label, color=color, linestyle='-')
        # plt.hlines(y=max_throughput_diff_slot_len[i], 
        #            xmin=0, xmax=argmax_lambd_in_diff_slot_len[i], 
        #            colors=color, linewidth=0.8, linestyle='--')
        # plt.vlines(x=argmax_lambd_in_diff_slot_len[i], 
        #            ymin=0, ymax=max_throughput_diff_slot_len[i],
        #            color=color, linewidth=0.8, linestyle='--')


    if RUS_TITLES:
        plt.title(f'Зависимость пропускной способности от интенсивности вх. \
потока\n(аналитический расчет системы с потерями, кол-во каналов {CH_NUM})')
        plt.xlabel('Интенсивность вх. потока')
        plt.ylabel('T(λ)')  
    else:
        plt.title(f'Throughput on the input arrival rate\n(theoretically \
calculations of lossy system, channels num {CH_NUM})')
        plt.xlabel('Input arrival rate')
        plt.ylabel('T(λ)')

    plt.legend()

    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.xlim(0, MAX_LAMBD)

    # Set the chart layout / Задать разлиновку графика
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))

    plt.savefig(f"{SAVE_PATH}/{CH_NUM}ch_lambd_step_{LAMBD_STEP}\
_throughput_theory.png")


def plot_throughput_sim(lambda_out_g_1_diff_slot_len_sim: list[list[float]],
                        lambda_out_g_opt_diff_slot_len_sim: list[list[float]],
                        thr_limit_g_1_diff_slot_len: list[float],
                        thr_limit_g_opt_diff_slot_len: list[float],
                        labels: list[str]):

    plt.figure(figsize=(12, 8))
    for i, slot_len in enumerate(SLOTS_LEN):

        slot_len = round(slot_len, ROUNDING)
        slot_len_label = labels[SLOT_LEN_IDX] + str(slot_len)

        if i < len(COLORS): 
            color1 = COLORS[i]
            color2 = utils.darken_color_hex(color1, PLOT_DARK_FACTOR)
        else: 
            color1 = utils.generate_random_color_rgb()
            color2 = utils.darken_color_rgb(color1, PLOT_DARK_FACTOR)

        plt.plot(LAMBDAS, lambda_out_g_1_diff_slot_len_sim[i],
                 label = slot_len_label + "; " + labels[G_1_IDX],
                 color=color1)

        if LOSSLESS_SIM and not DISABLE_CEILING_CALC:
            plt.axhline(y=thr_limit_g_1_diff_slot_len[i], 
                        color=color1, linewidth=0.8, linestyle='--')

        if not DISABLE_G_OPT_SIM:
            plt.plot(LAMBDAS, lambda_out_g_opt_diff_slot_len_sim[i],
                    label = slot_len_label + "; " + labels[G_OPT_IDX] + 
                    str(G_OPT_ARR[i]), color=color2)

            if LOSSLESS_SIM and not DISABLE_CEILING_CALC:
                plt.axhline(y=thr_limit_g_opt_diff_slot_len[i], 
                            color=color2, linewidth=0.8, linestyle='--')

    if RUS_TITLES:
        if LOSSLESS_SIM:
            lossless_label = 'системы без потерь'
        else:
            lossless_label = 'системы с потерями'

        plt.title(f'Зависимость пропускной способности от интенсивности вх. \
потока\n(моделирование {lossless_label}, кол-во каналов {CH_NUM})')
        plt.xlabel('Интенсивность вх. потока')
        plt.ylabel('T(λ)')

    else:
        if LOSSLESS_SIM:
            lossless_label = 'lossless system'
        else:
            lossless_label = 'lossy system'

        plt.title(f'Throughput on the input arrival rate\n(simulation of \
{lossless_label}, channels num {CH_NUM})')
        plt.xlabel('Input arrival rate')
        plt.ylabel('T(λ)')

    plt.legend()

    plt.ylim(bottom=0)
    plt.xlim(left=0)

    # Set the chart layout / Задать разлиновку графика
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))

    plt.savefig(f"{SAVE_PATH}/{CH_NUM}ch_lambd_step_{LAMBD_STEP}\
_slots_{SLOTS}_throughput_sim.png")


def plot_delay_sim(avg_delay_g_1_diff_slot_len_sim: list[list[float]],
                   avg_delay_g_opt_diff_slot_len_sim: list[list[float]],
                   thr_limit_g_1_diff_slot_len: list[float],
                   thr_limit_g_opt_diff_slot_len: list[float],
                   labels: list[str]):

    plt.figure(figsize=(12, 8))
    for i, slot_len in enumerate(SLOTS_LEN):

        slot_len = round(slot_len, ROUNDING)
        slot_len_label = labels[SLOT_LEN_IDX] + str(slot_len)

        if i < len(COLORS): 
            color1 = COLORS[i]
            color2 = utils.darken_color_hex(color1, PLOT_DARK_FACTOR)
        else: 
            color1 = utils.generate_random_color_rgb()
            color2 = utils.darken_color_rgb(color1, PLOT_DARK_FACTOR)

        plt.plot(LAMBDAS, avg_delay_g_1_diff_slot_len_sim[i],
                 label = slot_len_label + "; " + labels[G_1_IDX],
                 color=color1)

        if LOSSLESS_SIM and not DISABLE_CEILING_CALC:
            plt.axvline(x=thr_limit_g_1_diff_slot_len[i], 
                        color=color1, linewidth=0.8, linestyle='--')

        if not DISABLE_G_OPT_SIM:
            plt.plot(LAMBDAS, avg_delay_g_opt_diff_slot_len_sim[i],
                    label = slot_len_label + "; " + labels[G_OPT_IDX] + 
                    str(G_OPT_ARR[i]), color=color2)

            if LOSSLESS_SIM and not DISABLE_CEILING_CALC:
                plt.axvline(x=thr_limit_g_opt_diff_slot_len[i], 
                            color=color2, linewidth=0.8, linestyle='--')

    if RUS_TITLES:
        if LOSSLESS_SIM:
            lossless_label = 'системы без потерь'
        else:
            lossless_label = 'системы с потерями'

        plt.title(f'Зависимость задержки от интенсивности вх. потока\
\n(моделирование {lossless_label}, кол-во каналов {CH_NUM})')
        plt.xlabel('Интенсивность вх. потока')
        plt.ylabel('Задержка')

    else:
        if LOSSLESS_SIM:
            lossless_label = 'lossless system'
        else:
            lossless_label = 'lossy system'

        plt.title(f'Delay on the input arrival rate\n(simulation of \
{lossless_label}, channels num {CH_NUM})')
        plt.xlabel('Input arrival rate')
        plt.ylabel('Delay')

    plt.legend()

    plt.ylim(0, Y_LIM_DELAY)
    plt.xlim(left=0)
    plt.xlim(0, MAX_LAMBD * 0.8)

    # Set the chart layout / Задать разлиновку графика
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
    #plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))

    plt.savefig(f"{SAVE_PATH}/{CH_NUM}ch_lambd_step_{LAMBD_STEP}\
_slots_{SLOTS}_delay_sim.png")


def plot_throughput(lambda_out_diff_slot_len_sim: list[list[float]], 
                    lambda_out_th_diff_slot_len: list[list[float]],
                    thr_limit_diff_slot_len: list[float],
                    max_throughput_diff_slot_len: list[float],
                    argmax_lambd_in_diff_slot_len:  list[float],
                    label: str):

    plt.figure(figsize=(12, 8))
    for i, slot_len in enumerate(SLOTS_LEN):
        slot_len = round(slot_len, ROUNDING)
        slot_len_label = label + str(slot_len)

        if i < len(COLORS): 
            color1 = COLORS[i]
            color2 = utils.darken_color_hex(color1, PLOT_DARK_FACTOR)
        else: 
            color1 = utils.generate_random_color_rgb()
            color2 = utils.darken_color_rgb(color1, PLOT_DARK_FACTOR)

        plt.plot(LAMBDAS, lambda_out_th_diff_slot_len[i], 
                 label = slot_len_label + ", расчет", color=color1)
        plt.plot(LAMBDAS, lambda_out_diff_slot_len_sim[i], 
                 label = slot_len_label + ", моделирование", color=color2)

        plt.hlines(y=max_throughput_diff_slot_len[i], 
                   xmin=0, xmax=argmax_lambd_in_diff_slot_len[i], 
                   colors=color1, linewidth=0.8, linestyles='--')
        plt.vlines(x=argmax_lambd_in_diff_slot_len[i], 
                   ymin=0, ymax=max_throughput_diff_slot_len[i],
                   color=color1, linewidth=0.8, linestyle='--')
        if LOSSLESS_SIM and not DISABLE_CEILING_CALC:
            plt.axhline(y=thr_limit_diff_slot_len[i], 
                        color=color2, linewidth=0.8, linestyle='--')

    if RUS_TITLES:
        plt.title(f'Зависимость пропускной способности от интенсивности вх. \
потока\n(аналитический расчет + моделирование, кол-во каналов {CH_NUM})')
        plt.xlabel('Интенсивность вх. потока')
        plt.ylabel('T(λ)')  
    else:
        plt.title(f'Throughput on the input arrival rate\n(theoretically \
calculations + simulation, channels num {CH_NUM})')
        plt.xlabel('Input arrival rate')
        plt.ylabel('T(λ)')

    plt.legend()

    plt.ylim(bottom=0)
    plt.xlim(left=0)

    # Set the chart layout / Задать разлиновку графика
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))

    plt.savefig(f"{SAVE_PATH}/{CH_NUM}ch_lambd_step_{LAMBD_STEP}_slots_{SLOTS}\
_throughput_theory_and_sim.png")

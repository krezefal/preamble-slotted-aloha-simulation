import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

#from aloha.utils import moving_average
from consts import *


def plot_throughput_theory(ch_num: int,
                           lambda_out_th_diff_slot_len: list[float],
                           label: str):
    if DISABLE_THEORY:
        return
    
    plt.figure(figsize=(12, 8))
    for i, slot_len in enumerate(SLOTS_LEN):
        slot_len = round(slot_len, ROUNDING)
        plt.plot(LAMBDAS, lambda_out_th_diff_slot_len[i], 
                 label = label + str(slot_len))
        
    if RUS_TITLES:
        plt.title(f'Зависимость пропускной способности от интенсивности вх. \
потока\n(аналитический расчет, кол-во каналов {ch_num})')
        plt.xlabel('Интенсивность вх. потока')
        plt.ylabel('T(λ)')  
    else:
        plt.title(f'Throughput on the input arrival rate\n(theoretically, \
channels num {ch_num})')
        plt.xlabel('Input arrival rate')
        plt.ylabel('T(λ)')

    plt.legend()
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))
    plt.savefig(f"{SAVE_PATH}/{ch_num}ch_lambd_step_{LAMBD_STEP}\
_throughput_theory.png")
    

def plot_throughput_sim(ch_num: int,
                        lambda_out_diff_slot_len_sim: list[float],
                        label: str):
    if DISABLE_SIM:
        return
    
    plt.figure(figsize=(12, 8))
    for i, slot_len in enumerate(SLOTS_LEN):
        slot_len = round(slot_len, ROUNDING)
        plt.plot(LAMBDAS, lambda_out_diff_slot_len_sim[i],
                 label = label + str(slot_len))
    
    if RUS_TITLES:
        plt.title(f'Зависимость пропускной способности от интенсивности вх. \
потока\n(моделирование, кол-во каналов {ch_num})')
        plt.xlabel('Интенсивность вх. потока')
        plt.ylabel('T(λ)')
    else:
        plt.title(f'Throughput on the input arrival rate\n(simulation, \
channels num {ch_num})')
        plt.xlabel('Input arrival rate')
        plt.ylabel('T(λ)')

    plt.legend()
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))
    plt.savefig(f"{SAVE_PATH}/{ch_num}ch_lambd_step_{LAMBD_STEP}\
_slots_{SLOTS}_throughput_sim.png")


def plot_delay_sim(ch_num: int, 
                   avg_delay_diff_slot_len_sim: list[float],
                   label: str):
    if DISABLE_SIM:
        return
    
    plt.figure(figsize=(12, 8))
    for i, slot_len in enumerate(SLOTS_LEN):
        slot_len = round(slot_len, ROUNDING)
        plt.plot(LAMBDAS, avg_delay_diff_slot_len_sim[i], 
                 label = label + str(slot_len))

    if RUS_TITLES:
        plt.title(f'Зависимость задержки от интенсивности вх. потока\
\n(моделирование, кол-во каналов {ch_num})')
        plt.xlabel('Интенсивность вх. потока')
        plt.ylabel('Задержка')
    else:
        plt.title(f'Delay on the input arrival rate\n(simulation, \
channels num {ch_num})')
        plt.xlabel('Input arrival rate')
        plt.ylabel('Delay')

    plt.ylim(0, 20)
    plt.legend()
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
    #plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))
    plt.savefig(f"{SAVE_PATH}/{ch_num}ch_lambd_step_{LAMBD_STEP}\
_slots_{SLOTS}_delay_sim.png")

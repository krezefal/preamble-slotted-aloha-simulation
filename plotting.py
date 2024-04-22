from datetime import datetime
import matplotlib.pyplot as plt

#from aloha.utils import moving_average
from consts import *


def plot_throughput_theory(ch_num: int,
                           lambda_out_th_diff_slot_len: list[float],
                           label: str):
    if DISABLE_THEORY:
        return
    
    for i, slot_len in enumerate(SLOTS_LEN):
        plt.plot(LAMBDAS, lambda_out_th_diff_slot_len[i], 
                 label = label % slot_len)
        
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
    plt.savefig(f"{SAVE_PATH}/{datetime.now().strftime(TIMESTAMP)}-{ch_num}\
ch_throughput_theory.png")
    plt.figure()
    

def plot_throughput_sim(ch_num: int,
                        lambda_out_diff_slot_len_sim: list[float],
                        label: str):
    if DISABLE_SIM:
        return
    
    for i, slot_len in enumerate(SLOTS_LEN):
        plt.plot(LAMBDAS, 
                 lambda_out_diff_slot_len_sim[i], 
                 label = label % slot_len)
    
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
    plt.savefig(f"{SAVE_PATH}/{datetime.now().strftime(TIMESTAMP)}-{ch_num}\
ch_throughput_sim.png")
    plt.figure()


def plot_delay_sim(ch_num: int, 
                   avg_delay_diff_slot_len_sim: list[float],
                   label: str):
    if DISABLE_SIM:
        return
    
    for i, slot_len in enumerate(SLOTS_LEN):
        plt.plot(LAMBDAS, avg_delay_diff_slot_len_sim[i], 
                 label = label % slot_len)

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
    plt.savefig(f"{SAVE_PATH}/{datetime.now().strftime(TIMESTAMP)}-{ch_num}\
ch_delay_sim.png")
    plt.figure()

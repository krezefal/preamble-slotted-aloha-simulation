import math
import random
import numpy as np

from consts import *


DECIMATION_DENSITY = 10
ERR_AREA_ACCURACY = 3


def get_ceiling_avg(data: list[float]) -> float:
    sample_arr = []
    if len(LAMBDAS) >= 100:
        # Take every Nth element
        sample_arr = data[::DECIMATION_DENSITY]
        error_area = LAMBD_STEP * DECIMATION_DENSITY / ERR_AREA_ACCURACY
        idx_scaling = DECIMATION_DENSITY
    else:
        sample_arr = data
        error_area = LAMBD_STEP / ERR_AREA_ACCURACY
        idx_scaling = 1

    diff_arr = [diff_val if abs(diff_val) >= error_area else 0 
                for diff_val in np.diff(sample_arr)]
    
    try:
        ceiling_idx = diff_arr.index(0)
        ceiling_idx_in_data = (ceiling_idx + 1) * idx_scaling
        ceiling_avg_val = sum(data[ceiling_idx_in_data:]) / \
            len(data[ceiling_idx_in_data:])

        return ceiling_avg_val

    except ValueError:
        if RUS_TITLES:
            print("[!] Не удалось определелить начало \"потолка\" графика, \
будет использован более грубый метод")
        else:
            print("[!] Unable to determine beginning of the graph ceiling, \
a less accurate method will be used instead")
            
        return max(data)


def moving_average(data, window_size):
    moving_averages = []
    for i in range(len(data) - window_size + 1):
        window = data[i:i+window_size]
        window_average = sum(window) / window_size
        moving_averages.append(window_average)

    moving_averages += data[len(data) - window_size + 1:]

    return moving_averages


def generate_random_color_rgb() -> tuple[float, float, float]:
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)


def darken_color_rgb(color: tuple[float, float, float], 
                     dark_factor: float) -> tuple[float, float, float]:
    r, g, b = color
    return (r * dark_factor, g * dark_factor, b * dark_factor)


def darken_color_hex(hex_color: str, dark_factor: float) -> str:
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    darkened_rgb = [max(0, int(c * dark_factor)) for c in rgb]
    return '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)


def calc_lambda_out_theoretically(slot_len, lambd: float) -> float:
    lambd_out = 0.0
    for i in range(1, INFINITY):
        multiplier1 = (slot_len * lambd) ** i * \
            math.e ** (-slot_len * lambd) / math.factorial(i)
        multiplier2 = (1 - 1/i) ** (i - 1)
        lambd_out += multiplier1*multiplier2
    return lambd_out / slot_len


def calc_pr_success_from_g_1_ch(g: float) -> float:
    pr_s = 0.0
    for i in range(1, INFINITY):
        multiplier1 = g ** i * math.e ** (-g) / math.factorial(i)
        multiplier2 = (1 - 1/i) ** (i - 1)
        pr_s += multiplier1*multiplier2
    return pr_s


def calc_lambda_out_theoretically_debug(slot_len, lambd: float) \
    -> tuple[float, list[float], list[float]]:

    lambd_out = 0.0
    pr_users = [0.0] * INFINITY
    pr_success = [0.0] * INFINITY

    for i in range(0, INFINITY):
        pr_users[i] = (slot_len * lambd) ** i * \
            math.e ** (-slot_len * lambd) / math.factorial(i)
        if i != 0:
            pr_success[i] = (1 - 1/i) ** (i - 1)
        else:
            pr_success[i] = 0
        lambd_out += pr_users[i]*pr_success[i]
    return lambd_out / slot_len, pr_users, pr_success

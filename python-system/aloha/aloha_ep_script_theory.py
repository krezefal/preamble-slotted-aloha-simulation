import math
import concurrent.futures

from aloha.utils import generate_users_in_channels, factorial_product
from consts import INFINITY


def calc_throughput(lambd, slot_len: float, ch_num: int) -> float:
    
    term1 = slot_len * lambd * \
        math.e ** (-slot_len * lambd)

    term2 = 0.0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        running_tasks = []
        for l in range(1, ch_num+1):
            task = executor.submit(calc_multipliers_independently, l, ch_num, 
                                   lambd, slot_len)
            running_tasks.append(task)
        
        for running_task in running_tasks:
            m1, m2 = running_task.result()
            term2 += m1*m2

    return (term1 + term2) / slot_len


def calc_multipliers_independently(l, ch_num: int, lambd, slot_len: float) \
    -> tuple[float, float]:

    multiplier1 = math.comb(ch_num-1, l-1) * \
        (slot_len * lambd) ** (ch_num-l) * \
        math.e ** (-slot_len * lambd * ch_num)

    multiplier2 = calc_multiplier2(l, lambd, slot_len)
    return multiplier1, multiplier2
    
    
def calc_multiplier2(l: int, lambd, slot_len: float) -> float:
    multiplier2 = 0.0
    for users_in_channels in generate_users_in_channels(INFINITY, l):
        if sum(users_in_channels) == 0:
            continue

        usr_sum = sum(users_in_channels)

        tmp = 0.0
        if usr_sum <= l:
            tmp = (usr_sum / l) * (1 - 1/l) ** (usr_sum - 1)
        else:
            tmp = (1 - 1/usr_sum) ** (usr_sum - 1)

        numerator = (slot_len * lambd) ** usr_sum
        denominator = factorial_product(users_in_channels)
        tmp *= float(numerator / denominator)
        
        multiplier2 += tmp
    
    return multiplier2

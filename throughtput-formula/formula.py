import math
import time
import concurrent.futures

INFINITY = 10


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

    # DEPRECATED APPROACH - may crash on high ch_num
    # base = [[]]
    # for l in range(1, ch_num+1):
    #     multiplier1 = math.comb(ch_num-1, l-1) * \
    #         (slot_len * lambd) ** (ch_num-l) * \
    #         math.e ** (-slot_len * lambd * ch_num)
        
    #     multiplier2, base = \
    #         calc_multiplier2_with_base(l, lambd, slot_len, base)
    #     term2 += multiplier1*multiplier2

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


def generate_users_in_channels(upper_lim, l: int):
    def gen_combs_recursion(curr_combination, depth):
        if depth == l:
            yield curr_combination.copy()
            return
        
        for num in range(upper_lim):
            if num == 1:
                continue
            curr_combination.append(num)
            yield from gen_combs_recursion(curr_combination, depth + 1)
            curr_combination.pop()
    
    initial_combination = []
    yield from gen_combs_recursion(initial_combination, 0)


# def generate_users_in_channels_from_base(upper_lim, l: int, 
#                                          base: list[list[int]]) \
#                                             -> list[list[int]]:
    
#     if l == 1:
#         return [[num] for num in range(upper_lim) if num != 1]

#     users_comb_arr = [cur_comb + [num] for cur_comb in base 
#                       for num in range(upper_lim) if num != 1]

#     return users_comb_arr


def factorial_product(arr: list[int]) -> int:
    result = 1
    for el in arr:
        result *= math.factorial(el)
    return result


def main():
    # print(calc_throughput(lambd=1.775, slot_len=1, ch_num=1)) # 0.5482
    # print(calc_throughput(lambd=0.836, slot_len=1.6, ch_num=4)) # 0.3739
    # print(calc_throughput(lambd=0.62, slot_len=2, ch_num=6)) # 0.3016

    start_time = time.time()
    print(calc_throughput(lambd=1, slot_len=1, ch_num=7))
    end_time = time.time()
    print(f"{end_time - start_time} sec")


if __name__ == '__main__':
    main()
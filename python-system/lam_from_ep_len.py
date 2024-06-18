import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


MIN_EP_LEN = 0.0
MAX_EP_LEN = 4.0
EP_LEN_STEP = 0.1
# SLOTS_LEN is EP_LEN with DTP_LEN.
SLOTS_LEN = \
    np.arange(MIN_EP_LEN, MAX_EP_LEN+EP_LEN_STEP, EP_LEN_STEP)


EP_LEN_STEP_2 = 0.2
# SLOTS_LEN is EP_LEN with DTP_LEN.
SLOTS_LEN_2 = \
    np.arange(MIN_EP_LEN, MAX_EP_LEN+EP_LEN_STEP_2, EP_LEN_STEP_2)

#############################

LAMBDA_OUT_LOSSY_1_CH = [0.5482, 0.4984, 0.4568, 0.4217, 0.3916, 0.3655, 0.3426, \
                         0.3225, 0.3046, 0.2885, 0.2741, 0.261, 0.2492, 0.2383,\
                         0.2284, 0.2193, 0.2108, 0.203, 0.1958, 0.189, 0.1827, \
                         0.1768, 0.1713, 0.1661,  0.1612, 0.1566, 0.1523, 0.1482, \
                         0.1443,0.1406 , 0.137, 0.1337, 0.1305, 0.1275, 0.1246, \
                         0.1218, 0.1192, 0.1166, 0.1142, 0.1119, 0.1096]

LAMBDA_CR_LOSSLESS_1_CH = [0.5491, 0.4953, 0.4595, 0.4225, 0.3919, 0.3671, 0.3419, \
                           0.3234, 0.304, 0.2869, 0.2743, 0.2598, 0.2518, 0.238, \
                           0.2293, 0.2183, 0.2103, 0.2034, 0.195, 0.1886, 0.1834, \
                           0.1763, 0.1708, 0.1656, 0.1611, 0.1559, 0.1533, 0.1482, \
                           0.144, 0.1411, 0.1374, 0.1331, 0.1302, 0.1263, 0.1243, \
                           0.1218, 0.12, 0.1165, 0.1139, 0.1121, 0.1098]

#############################

LAMBDA_OUT_LOSSY_2_CH = [0.578, 0.5254, 0.4816, 0.4446, 0.4128, 0.3853, 0.3612, \
                         0.34, 0.3211, 0.3042, 0.289, 0.2752, 0.2627, 0.2513,\
                         0.2408, 0.2312, 0.2223, 0.2141, 0.2064, 0.1993, 0.1927, \
                         0.1864, 0.1806, 0.1751,  0.17, 0.1651, 0.1605, 0.1562, \
                         0.1521, 0.1482 , 0.1445, 0.141, 0.1376, 0.1344, 0.1314, \
                         0.1284, 0.1256, 0.123, 0.1204, 0.1179, 0.1156]

LAMBDA_CR_LOSSLESS_2_CH = [0.5759, 0.52695, 0.4841, 0.4451, 0.41505, 0.38385, \
                           0.36325, 0.3388, 0.32065, 0.30505, 0.28915, \
                           0.2753, 0.2639, 0.2514, 0.24085, 0.23125, 0.22255, \
                           0.21385, 0.20665, 0.19925, 0.1933, 0.1867, 0.1808, \
                           0.17525, 0.16955, 0.1657, 0.1608, 0.15625, 0.1519, \
                           0.1476, 0.14415, 0.14095, 0.1375, 0.1346, 0.13115, \
                           0.12805, 0.12555, 0.12285, 0.12025, 0.1185, 0.11555]

#############################

LAMBDA_OUT_LOSSY_4_CH = [0.5983, 0.4985, 0.4274, 0.3739, 0.3324, 0.2991, 0.2719,\
                         0.2493, 0.23, 0.2135, 0.1994, 0.1868,  0.1759,  0.166, \
                         0.1574, 0.1494, 0.1422, 0.136, 0.13, 0.1243, 0.1194]

LAMBDA_CR_LOSSLESS_4_CH = [0.600, 5.025, 0.431, 0.377, 0.3325, 0.2975, 0.272, \
                           0.2493, 0.23, 0.2135, 0.1994, 0.1868,  0.1759,  0.167, \
                           0.1574, 0.1494, 0.1422, 0.136, 0.13, 0.1243, 0.1194]

#############################

LAMBDA_OUT_LOSSY_8_CH = [0.6042, 0.5035, 0.4315, 0.3776, 0.3355, 0.3021, 0.2746, \
                         0.2517, 0.2323, 0.2014, 0.2156, 0.1885, 0.1777, 0.1676, 
                         0.1588, 0.151, 0.1437, 0.1369, 0.1312, 0.1259, 0.1207]

LAMBDA_CR_LOSSLESS_8_CH = [0.6042, 0.5035, 0.435, 0.378, 0.338, 0.303, 0.274, \
                           0.252, 0.2322, 0.213, 0.202, 0.1887, 0.1777, 0.1676,\
                           0.1588, 0.151, 0.1437, 0.1369, 0.1312, 0.1259, 0.1207]

G_OPT_1_CH = 1.77
G_OPT_2_CH = 1.54
G_OPT_4_CH = 1.34
G_OPT_8_CH = 1.20

T_lam_max_1_CH = 0.5482

SAVE_PATH = "../graphs/py"

def darken_color_hex(hex_color: str, dark_factor: float) -> str:
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    darkened_rgb = [max(0, int(c * dark_factor)) for c in rgb]
    return '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)


def main():

    color_1_ch = '#ff3d33'
    color_2_ch = darken_color_hex(color_1_ch, 0.7)
    color_4_ch = darken_color_hex(color_2_ch, 0.7)
    color_8_ch = darken_color_hex(color_4_ch, 0.2)

    color_1_ch_ = '#2baebf'
    color_2_ch_ = darken_color_hex(color_1_ch_, 0.7)
    color_4_ch_ = darken_color_hex(color_2_ch_, 0.7)
    color_8_ch_ = darken_color_hex(color_4_ch_, 0.2)

    plt.figure(figsize=(8, 8))
    plt.plot(SLOTS_LEN, LAMBDA_OUT_LOSSY_1_CH, color=color_1_ch, linestyle='-', \
             label='теоретический расчет макс. T(λ) \nв режиме с потерями для 1 канала')
    for i, slot_len in enumerate(SLOTS_LEN):
        if i == len(SLOTS_LEN)  -1:
            plt.plot(slot_len, LAMBDA_CR_LOSSLESS_1_CH[i], 'o', color=color_1_ch_, \
                     label='моделирование макс. T(λ) \nв режиме без потерь при $G_{опт}$ для 1 канала')
            break
        plt.plot(slot_len, LAMBDA_CR_LOSSLESS_1_CH[i], 'o', color=color_1_ch_,)

    plt.plot(SLOTS_LEN, LAMBDA_OUT_LOSSY_2_CH, color=color_2_ch, linestyle='-', \
             label='теоретический расчет макс. T(λ) \nв режиме с потерями для 2 каналов')
    for i, slot_len in enumerate(SLOTS_LEN):
        if i == len(SLOTS_LEN)  -1:
            plt.plot(slot_len, LAMBDA_CR_LOSSLESS_2_CH[i], 'o', color=color_2_ch_, \
                     label='моделирование макс. T(λ) \nв режиме без потерь при $G_{опт}$ для 2 каналов')
            break
        plt.plot(slot_len, LAMBDA_CR_LOSSLESS_2_CH[i], 'o', color=color_2_ch_,)

    plt.plot(SLOTS_LEN_2, LAMBDA_OUT_LOSSY_4_CH, color=color_4_ch, linestyle='-', \
             label='теоретический расчет макс. T(λ) \nв режиме с потерями для 4 каналов')
    for i, slot_len in enumerate(SLOTS_LEN_2):
        if i == len(SLOTS_LEN_2)  -1:
            plt.plot(slot_len, LAMBDA_CR_LOSSLESS_4_CH[i], 'o', color=color_4_ch_, \
                     label='моделирование макс. T(λ) \nв режиме без потерь при $G_{опт}$ для 4 каналов')
            break
        plt.plot(slot_len, LAMBDA_CR_LOSSLESS_4_CH[i], 'o', color=color_4_ch_,)

    # plt.plot(SLOTS_LEN_2, LAMBDA_OUT_LOSSY_8_CH, color=color_4_ch, linestyle='-', \
    #          label='теоретический расчет макс. T(λ) \nсистемы с потерями для 8 каналов')
    # for i, slot_len in enumerate(SLOTS_LEN_2):
    #     if i == len(SLOTS_LEN_2)  -1:
    #         plt.plot(slot_len, LAMBDA_CR_LOSSLESS_8_CH[i], 'o', color=color_8_ch_, \
    #                  label='моделирование макс. T(λ) \nсистемы без потерь при $G_{опт}$ для 8 каналов')
    #         break
    #     plt.plot(slot_len, LAMBDA_CR_LOSSLESS_8_CH[i], 'o', color=color_8_ch_,)

    # plt.hlines(y=G_OPT_1_CH, xmin=0, xmax=4, 
    #            colors='#ff3d33', linewidth=1.5, linestyle='-', label = 'кол-во каналов 1')
    # plt.hlines(y=G_OPT_2_CH, xmin=0, xmax=4, 
    #         colors=color_2_ch, linewidth=1.5, linestyle='-', label = 'кол-во каналов 2')
    # plt.hlines(y=G_OPT_4_CH, xmin=0, xmax=4, 
    #         colors=color_4_ch, linewidth=1.5, linestyle='-', label = 'кол-во каналов 4')
    # plt.hlines(y=G_OPT_8_CH, xmin=0, xmax=4, 
    #         colors=color_8_ch, linewidth=1.5, linestyle='-', label = 'кол-во каналов 8')
        
    plt.title('Зависимость максимальной интенсивности \nвыходного потока от длительности ФИ', fontsize=20)
    plt.ylabel('T(λ)', fontsize=20)

    # plt.title('Зависимость оптимального параметра G\n от длительности ФИ', fontsize=20)
    # plt.ylabel('G опт', fontsize=20)

    plt.xlabel('Длительность ФИ', fontsize=20)

    plt.ylim(0, 0.65)
    plt.xlim(left=0)
    plt.legend(fontsize=12,loc='upper right')

    # Set the chart layout / Задать разлиновку графика
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.4))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.1))

    plt.savefig(f"{SAVE_PATH}/lam_from_ep_len_theory.png")
    plt.show()


if __name__ == '__main__':
    main()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from pkg import utils


G_STEP = 0.01
MAX_G = 4
Gs = np.arange(0.01, MAX_G+G_STEP, G_STEP)
SAVE_PATH = "../graphs/py"


def main():

    pr_success_arr = []

    for g in Gs:
        pr_success = utils.calc_pr_success_from_g_1_ch(g)
        pr_success_arr.append(pr_success)

    # print(pr_success_arr)
    max_success = max(pr_success_arr)
    argmax_success = Gs[pr_success_arr.index(max_success)]

    print(f'max Pr(Y) = {max_success} on G = {argmax_success}')

    plt.figure(figsize=(12, 8))
    plt.plot(Gs, pr_success_arr, color='black', linestyle='-')
    plt.hlines(y=max_success, xmin=0, xmax=argmax_success, 
               colors='black', linewidth=0.8, linestyle='--')
    plt.vlines(x=argmax_success, ymin=0, ymax=max_success,
               color='black', linewidth=0.8, linestyle='--')
    plt.plot(argmax_success, max_success, 'o', color='black',)
        
    #plt.title('Зависимость вероятности успеха от параметра G для 1 канала')
    plt.xlabel('G', fontsize=20)
    plt.ylabel('Pr{У|G}', fontsize=20)

    plt.ylim(bottom=0)
    plt.xlim(left=0)

    # Set the chart layout / Задать разлиновку графика
    plt.grid(True, linewidth=0.25, which='both')
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.2))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))

    plt.savefig(f"{SAVE_PATH}/pr_success_from_g_1_ch.png")
    plt.show()


if __name__ == '__main__':
    main()

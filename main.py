import matplotlib.pyplot as plt
import numpy as np

#from aloha.aloha_conv import AlohaConv
from aloha.aloha_ep import MultichannelAlohaEP
from consts import SLOTS, SLOT_LEN, CHANNELS_COUNT, VERBOSE


def main():
    plt.close('all')

    lambdas = np.arange(0.1, 4, 0.005)

    lambda_in_arr = []
    lambda_out_arr = []
    avg_delay_arr = []

    for lambd in lambdas:
        if VERBOSE: print(f"\n====( λ = {lambd} )======")
        mch_aloha_ep = MultichannelAlohaEP(lambd, SLOTS, SLOT_LEN, 
                                           CHANNELS_COUNT, VERBOSE)

        _, _, _ = mch_aloha_ep.run_theory()
        lambda_in, lambda_out, avg_delay = mch_aloha_ep.run_simulation()

        # aloha_conv = AlohaConv(lambd, SLOTS, SLOT_LEN, VERBOSE)

        # _, _, _ = aloha_conv.run_theory()
        # lambda_in, lambda_out, avg_delay = aloha_conv.run_simulation()

        lambda_in_arr.append(lambda_in)
        lambda_out_arr.append(lambda_out)
        avg_delay_arr.append(avg_delay)

    print(f"\n{lambda_in_arr}")
    print(f"\n{lambdas}")
    print(f"\n{lambda_out_arr}")

    plt.plot(lambdas, lambda_out_arr)
    plt.title('Зависимость пропускной способности от интенсивности вх. потока')
    plt.xlabel('Input arrival rate')
    plt.ylabel('T(λ)')

    plt.figure()

    plt.plot(lambdas, avg_delay_arr)
    plt.title('Зависимость задержки от интенсивности вх. потока')
    plt.xlabel('Input arrival rate')
    plt.ylabel('Delay')
    #plt.ylim(0, 18)

    plt.show()

    ########### Single lambda ##############

    # lambd = 0.9

    # aloha_conv = AlohaConv(lambd, SLOTS, SLOT_LEN, VERBOSE)
    # _, _, _ = aloha_conv.run_theory()
    # lambda_in, lambda_out, avg_delay = aloha_conv.run_simulation()

    # print()
    # print(f"{lambda_in}")
    # print(f"{lambda_out}")
    # print(f"{avg_delay}")

if __name__ == '__main__':
    main()

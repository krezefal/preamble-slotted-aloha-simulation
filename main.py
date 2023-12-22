import matplotlib.pyplot as plt
import numpy as np

from aloha.aloha_conv import AlohaConv
from aloha.aloha_ep import MultichannelAlohaEP
from consts import SLOTS, USERS_COUNT, CHANNELS_COUNT, EP_LEN, VERBOSE


def main():
    lambdas = np.arange(0.1, 2.1, 0.01)

    lambda_in_arr = []
    lambda_out_arr = []
    avg_delay_arr = []

    # for lambd in lambdas:
    #     if VERBOSE: print(f"\n====( λ = {lambd} )======")
    #     aloha_conv = AlohaConv(lambd, SLOTS, USERS_COUNT, VERBOSE)

    #     _, _ = aloha_conv.run_theory()
    #     lambda_in, lambda_out, avg_delay = aloha_conv.run_simulation()

    #     lambda_in_arr.append(lambda_in)
    #     lambda_out_arr.append(lambda_out)
    #     avg_delay_arr.append(avg_delay)

    # print(f"\n{lambda_in_arr}")
    # print(f"\n{lambdas}")
    # print(f"\n{lambda_out_arr}")

    # plt.plot(lambdas, lambda_out_arr)
    # plt.title('Зависимость пропускной способности от интенсивности вх. потока')
    # plt.xlabel('Input arrival rate')
    # plt.ylabel('T(λ)')

    # plt.figure()

    # plt.plot(lambdas, avg_delay_arr)
    # plt.title('Зависимость задержки от интенсивности вх. потока')
    # plt.xlabel('Input arrival rate')
    # plt.ylabel('Delay')

    # plt.show()

    for lambd in lambdas:
        if VERBOSE: print(f"\n====( λ = {lambd} )======")
        mch_aloha_ep = MultichannelAlohaEP(lambd, SLOTS, USERS_COUNT, 
                                         CHANNELS_COUNT, EP_LEN, VERBOSE)

        _, _ = mch_aloha_ep.run_theory()
        lambda_in, lambda_out, avg_delay = mch_aloha_ep.run_simulation()

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

    plt.show()

if __name__ == '__main__':
    main()

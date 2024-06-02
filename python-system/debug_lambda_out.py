import time

from aloha.aloha_ep_script_sim_debug import run_simulation
from pkg.utils import calc_lambda_out_theoretically_debug

lambd = 1
g_param = 1
slot_len = 1.5
SLOTS = 30000
CH_NUM = 1
VERBOSE = False
LOSSLESS_SIM = True
NUM_OF_USERS_FOR_LAMBDA_OUT = 10

print(f"λ_in = {lambd}; G = {g_param}; 10 users; slot_len = {slot_len}; \
slots = {SLOTS}")
print("----------------- Simulation (P_ep = G/M; lossless) -----------------")

start_time = time.time()
lambda_in_sim, lambda_out_sim, avg_delay_sim, pr_users, pr_success = \
    run_simulation(lambd, slot_len, g_param, SLOTS, CH_NUM, VERBOSE, \
                   LOSSLESS_SIM)
end_time = time.time()

print("Pr users:")
for i in range(NUM_OF_USERS_FOR_LAMBDA_OUT):
    print(f"i = {i}: Pr = {pr_users[i]}")

print()

print("Pr success:")
for i in range(NUM_OF_USERS_FOR_LAMBDA_OUT):
    print(f"i = {i}: Pr = {pr_success[i]}")

print()

lambda_out = 0.0
for i in range(NUM_OF_USERS_FOR_LAMBDA_OUT):
    lambda_out += pr_users[i]*pr_success[i]
lambda_out /= slot_len

print(f"Lambda in sim = {lambda_in_sim}")
print(f"Lambda out cumulative = {lambda_out}")
print(f"Lambda out sim = {lambda_out_sim}")
print(f"\nSimulation took {end_time - start_time} sec")

print()
print(f"--------------------- Theory (λ=G={g_param}) ---------------------")

lambda_out, pr_users, pr_success = \
    calc_lambda_out_theoretically_debug(slot_len, g_param)

print("Pr users:")
for i in range(NUM_OF_USERS_FOR_LAMBDA_OUT):
    print(f"i = {i}: Pr = {pr_users[i]}")

print()

print("Pr success:")
for i in range(NUM_OF_USERS_FOR_LAMBDA_OUT):
    print(f"i = {i}: Pr = {pr_success[i]}")

print()

print(f"Lambda out = {lambda_out}")

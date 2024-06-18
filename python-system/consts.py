import numpy as np


# SIM CONSTANTS
SLOTS = 70000
CH_NUM = 1

DTP_LEN = 1.0
MIN_EP_LEN = 0.0
MAX_EP_LEN = 1
EP_LEN_STEP = 0.5
# SLOTS_LEN is EP_LEN with DTP_LEN.
SLOTS_LEN = \
    np.arange(DTP_LEN+MIN_EP_LEN, MAX_EP_LEN+DTP_LEN+EP_LEN_STEP, EP_LEN_STEP)

# 1 channel
# G_OPT_ARR = [1.771, 1.181, 0.885]
# 2 channels
# G_OPT_ARR = [1.543, 1.029, 0.771]
# 3 channels
# G_OPT_ARR = [1.416, 0.944, 0.708]

G_OPT_ARR = [1.771] * 3

# COLORS are used for graphs per each slot len in a plot. If number of slots is
# higher than colors, the random one will be used.
COLORS = ['#ff3d33', '#2baebf', '#dd8335']

MAX_LAMBD = 1
LAMBD_STEP = 0.01
LAMBDAS = np.arange(LAMBD_STEP, MAX_LAMBD+LAMBD_STEP, LAMBD_STEP)


# MATH CONSTANTS
INFINITY = 10


# PROG CONSTANTS

# If SINGLE_PLOT_FOR_THEORY_AND_SIM = True, DISABLE_THEORY and DISABLE_SIM 
# constants aren't taken into account (always False). Average delay plot is \
# ignorred in this case. Plot of throughputs for G_opt are ignorred too.
SINGLE_PLOT_FOR_THEORY_AND_SIM = False

DISABLE_THEORY = True
DISABLE_SIM = False

LOSSLESS_SIM = True
DISABLE_G_OPT_SIM = False
# Calculation of the graph ceiling doesn't work when LOSSLESS_SIM = False.
DISABLE_CEILING_CALC = False
# X axis: λ, Y axis: λ(e^(-λ)). LOSSLESS_SIM should = False.
ONE_PREAMBLE_MODE = False
SIM_P_EP_EQ_ONE = False

RUS_TITLES = True
VERBOSE = False
HEARTBEAT_LOGS = True

ROUNDING = 4
SAVE_PATH = "../graphs/py"


# DON'T TOUCH
SLOT_LEN_IDX = 0
G_1_IDX = 1
G_OPT_IDX = 2

RESPONSE_EMPTY = 0
RESPONSE_OK = 1
RESPONSE_CONFLICT = 2

# PLOT_HIDE_PERCENT = 0.0
# MOVING_AVG_FACTOR = 10

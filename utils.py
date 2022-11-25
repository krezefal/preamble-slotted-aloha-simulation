import random


BS_feedback = dict[int, set['User']]
Group = dict[int, set['User']]
ChannelSet = set[int]
BS_response = list[int]


def rand_gen(probability):
    gen = random.random()
    
    return gen <= probability


def calculate_average_delay(users):
    overall_delay = 0
    
    for subscriber in users:
        overall_delay += subscriber.sum()
        
    return overall_delay / len(users)
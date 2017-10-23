import random

chars = ['A', 'B', 'C', 'D', 'E']

def rand_chars(char_count):
    return [random.choice(chars) for _ in range(char_count)]


def freq(char_list):
    reps = [0 for _ in range(5)]
    for char in char_list:
        reps[chars.index(char)] += 1
    print(chars[reps.index(max(reps))])
    return reps

print(freq(rand_chars(20)))

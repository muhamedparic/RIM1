import random

def bubble_sort(array):
    for i in range(len(array) - 1):
        for j in range(len(array) - 1, i, -1):
            if array[j - 1] < array[j]:
                array[j - 1], array[j] = array[j], array[j - 1]


def test():
    n = 100
    size_interval = (1, 100)
    for i in range(n):
        array = [random.randint(1, 1000) for _ in range(random.randint(size_interval[0], size_interval[1]))]
        control = array[:]
        bubble_sort(array)
        control.sort(reverse=True)
        print(array == control)


test()

import random

def Pronadji(haystack, needle):
    # Pretpostavka je da je haystack sortiran niz
    lower = 0
    upper = len(haystack) - 1
    while lower < upper:
        if haystack[lower] == needle:
            return lower
        if haystack[upper] == needle:
            return upper
        if haystack[lower] > needle or haystack[upper] < needle:
            raise Exception('Element se ne nalazi u nizu')
        mid = (upper + lower) // 2
        if haystack[mid] >= needle:
            upper = mid
        else:
            lower = mid
    if haystack[lower] == needle:
        return lower
    else:
        raise Exception('Element se ne nalazi u nizu')


def test():
    test_list = sorted(list(set([random.randint(1, 100) for _ in range(200)])))
    print(test_list)
    for item in test_list:
        print(Pronadji(test_list, item) == test_list.index(item))


test()

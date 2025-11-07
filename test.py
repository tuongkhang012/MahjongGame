arr = [1, 2, 3, 4]


def func(arr: list[int]):
    num = arr.pop()
    return num


pop_num = func(arr)
print(pop_num, arr)

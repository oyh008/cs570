import timeit
from generator import *
import time
import psutil

alpha = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
         'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
         'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
         'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}

delta = 30


def optimized_solver(X: str, Y: str):
    m = len(X)
    n = len(Y)

    # base case
    if m == 0 and n == 0:
        return "", ""

    if n <= 1 or m <= 1:
        if m == 0:
            return "_" * n, Y
        elif n == 0:
            return X, "_" * m
        else:
            shorter = X if m == 1 else Y
            longer = X if m != 1 else Y

            idx = max(m, n) - 1
            cur_min = 2 * delta
            result = -1

            for idx in range(max(m, n) - 1, -1, -1):
                if alpha[longer[idx]][shorter[0]] < cur_min:
                    result = idx
                    cur_min = alpha[longer[idx]][shorter[0]]
                    if cur_min == 0:
                        break

            if result < 0:
                return "_" * n + X, Y + "_" * m
            else:
                shorter_res = ["_"] * max(m, n)
                shorter_res[result] = shorter[0]

                return (longer, ''.join(shorter_res)) if m > n else (''.join(shorter_res), longer)

                # memory efficient
    # compress 2d dp table into 1d
    dp_left = [i * delta for i in range(n + 1)]
    dp_right = [i * delta for i in range(n + 1)]

    # left half of X
    for i in range(1, m // 2 + 1):
        prev = dp_left[0]
        dp_left[0] = i * delta
        for j in range(1, n + 1):
            cur = dp_left[j]

            match_i_j = prev + alpha[X[i - 1]][Y[j - 1]]
            ignore_i = dp_left[j] + delta
            ignore_j = dp_left[j - 1] + delta
            dp_left[j] = min(match_i_j, ignore_i, ignore_j)

            prev = cur

    # right half of X
    for i in range(m, m // 2, -1):
        prev = dp_right[0]
        dp_right[0] = (m + 1 - i) * delta
        for j in range(n, 0, -1):
            cur = dp_right[n + 1 - j]

            match_i_j = prev + alpha[X[i - 1]][Y[j - 1]]
            ignore_i = dp_right[n + 1 - j] + delta
            ignore_j = dp_right[n + 1 - j - 1] + delta
            dp_right[n + 1 - j] = min(match_i_j, ignore_i, ignore_j)

            prev = cur

    # check the optimized split point
    left = right = -1
    min_cost = float('inf')

    for i in range(0, n + 1):
        if dp_left[i] + dp_right[n - i] <= min_cost:
            left = i
            right = n - i
            min_cost = dp_left[i] + dp_right[n - i]

    # divide
    left_x, left_y = optimized_solver(X[:m // 2], Y[: left])
    right_x, right_y = optimized_solver(X[m // 2:], Y[left:])

    # conquer
    return left_x + right_x, left_y + right_y

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

if __name__ == '__main__':
    X, Y = generator()
    start_time = time.time()
    A, B = optimized_solver(X, Y)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    memory_consumed = process_memory()
    data = open("output.txt", 'w+')
    print((A, B), file=data)
    print(f"\nruntime of naive solution is      :{time_taken}", file=data)
    print(f"\nMemory usage of naive solution is     :{memory_consumed / 10 ** 6} MB", file=data)
    data.close()

    with open('cpu_time.txt', 'a') as f:
        f.write(str(time_taken) + "\n")
        f.write(str(max(len(X), len(Y))) + "\n")

    with open('memory_usage.txt', 'a') as f:
        f.write(str(memory_consumed / 10 ** 6) + "\n")
        f.write(str(max(len(X), len(Y))) + "\n")














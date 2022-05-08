import os
from generator import *
import time
import psutil
import sys

alpha = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
         'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
         'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
         'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}

delta = 30


def naive_solver(X: str, Y: str):
    m = len(X)
    n = len(Y)

    dp = [[float("inf") for _ in range(n + 1)] for _ in range(m + 1)]

    # Initialization
    for i in range(1, n + 1):
        dp[0][i] = i * delta

    for i in range(1, m + 1):
        dp[i][0] = i * delta

    dp[0][0] = 0

    # 2d dp table construction
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_i_j = dp[i - 1][j - 1] + alpha[X[i - 1]][Y[j - 1]]
            ignore_i = dp[i - 1][j] + delta
            ignore_j = dp[i][j - 1] + delta
            dp[i][j] = min(match_i_j, ignore_i, ignore_j)

    X_result = ''
    Y_result = ''
    i = m
    j = n

    while i != 0 or j != 0:

        if i == 0:
            X_result += '_'
            Y_result += Y[j - 1]
            j -= 1
            continue
        elif j == 0:
            Y_result += '_'
            X_result += X[i - 1]
            i -= 1
            continue

        # this is the standard backtrack process
        match_i_j = dp[i - 1][j - 1] + alpha[X[i - 1]][Y[j - 1]]
        ignore_i = dp[i - 1][j] + delta
        ignore_j = dp[i][j - 1] + delta

        if dp[i][j] == match_i_j:
            X_result += X[i - 1]
            Y_result += Y[j - 1]
            i -= 1
            j -= 1
        elif dp[i][j] == ignore_i:
            X_result += X[i - 1]
            Y_result += '_'
            i -= 1
        elif dp[i][j] == ignore_j:
            X_result += '_'
            Y_result += Y[j - 1]
            j -= 1

    X_result = X_result[::-1]
    Y_result = Y_result[::-1]

    return X_result, Y_result

def optimized_solver(X: str, Y: str):
    m = len(X)
    n = len(Y)

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

    dp_left = [i * delta for i in range(n + 1)]
    dp_right = [i * delta for i in range(n + 1)]

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
    for ind in range(1,16):
        X, Y = generator(os.path.join('dat','in'+str(ind)+'.txt'))

        #naive solver
        start_time_naive = time.time()
        A1, B1 = naive_solver(X, Y)
        end_time_naive = time.time()
        time_taken_naive = (end_time_naive - start_time_naive) * 1000
        memory_consumed_naive = process_memory()

        #opt solver
        start_time_opt = time.time()
        A2, B2 = optimized_solver(X, Y)
        end_time_opt = time.time()
        time_taken_opt = (end_time_opt - start_time_opt) * 1000
        memory_consumed_opt = process_memory()

        with open('cpu_time.txt', 'a') as f:
            f.write(str(time_taken_naive) + "\n")
            f.write(str(time_taken_opt) + "\n")
            f.write(str(max(len(X), len(Y))) + "\n")

        with open('memory_usage.txt', 'a') as f:
            f.write(str(memory_consumed_naive / 1000) + "\n")
            f.write(str(memory_consumed_opt / 1000) + "\n")
            f.write(str(max(len(X), len(Y))) + "\n")

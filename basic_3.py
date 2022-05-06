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

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed



if __name__ == '__main__':
        X, Y = generator(sys.argv[1])
        start_time = time.time()
        A, B = naive_solver(X, Y)
        end_time = time.time()
        time_taken = (end_time - start_time)*1000
        memory_consumed = process_memory()
        data = open(sys.argv[2], 'w+')
        print((A, B), file=data)
        print(f"\nruntime of naive solution is      :{time_taken}", file=data)
        print(f"\nMemory usage of naive solution is     :{memory_consumed / 1000} KB", file=data)
        data.close()

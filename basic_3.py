import sys
from resource import *
import time
import psutil

alpha = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
         'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
         'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
         'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}

gap_penalty = 30


def basic(x, y):
    m = len(x)
    n = len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i * gap_penalty
    for j in range(n + 1):
        dp[0][j] = j * gap_penalty
    # Construct the solution
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            mismatch = dp[i - 1][j - 1] + alpha[x[i - 1]][y[j - 1]]
            x_gap = dp[i - 1][j] + gap_penalty
            y_gap = dp[i][j - 1] + gap_penalty
            dp[i][j] = min(mismatch, x_gap, y_gap)
    # Backtrack dp to find the solution
    x_gen = ""
    y_gen = ""
    i = m
    j = n
    while i > 0 and j > 0:
        mismatch = dp[i - 1][j - 1] + alpha[x[i - 1]][y[j - 1]]
        x_gap = dp[i - 1][j] + gap_penalty
        y_gap = dp[i][j - 1] + gap_penalty
        if dp[i][j] == mismatch:
            x_gen += x[i - 1]
            y_gen += y[j - 1]
            i -= 1
            j -= 1
        elif dp[i][j] == x_gap:
            x_gen += x[i - 1]
            y_gen += "_"
            i -= 1
        elif dp[i][j] == y_gap:
            x_gen += "_"
            y_gen += y[j - 1]
            j -= 1
    # concat if one string runs out
    while i > 0:
        x_gen += x[i - 1]
        y_gen += "_"
        i -= 1
    while j > 0:
        x_gen += "_"
        y_gen += y[j - 1]
        j -= 1
    # return results
    return dp[-1][-1], x_gen[::-1], y_gen[::-1]


def generate_str(path):
    with open(path) as file:
        # create string 1
        basestr1 = file.readline().strip("\n")
        str1 = basestr1
        index = file.readline().strip("\n")
        i = 0
        while index.isnumeric():
            i += 1
            index = int(index)
            str1 = str1[:index + 1] + str1 + str1[index + 1:]
            index = file.readline().strip("\n")
        # create string 2
        basestr2 = index
        str2 = basestr2
        index = file.readline().strip("\n")
        j = 0
        while index.isnumeric():
            j += 1
            index = int(index)
            str2 = str2[:index + 1] + str2 + str2[index + 1:]
            index = file.readline().strip("\n")
        # validate the length of the strings
        assert len(str1) == (2 ** i) * len(basestr1)
        assert len(str2) == (2 ** j) * len(basestr2)
        return str1, str2


def write_output(cost, align1, align2, time, memory):
    # write to output
    output = sys.argv[2]
    with open(output, "w") as file:
        file.write(str(cost) + "\n")
        file.write(align1 + "\n")
        file.write(align2 + "\n")
        file.write(str(time) + "\n")
        file.write(str(memory) + "\n")
        file.close()


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


if __name__ == '__main__':
    input = sys.argv[1]
    start_time = time.time()
    str1, str2 = generate_str(input)
    cost, align1, align2 = basic(str1, str2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    memory_consumed = process_memory()
    write_output(cost, align1, align2, time_taken, memory_consumed)

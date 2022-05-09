import sys
from resource import *
import time
import psutil
from basic_3 import basic


alpha = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
         'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
         'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
         'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}

gap_penalty = 30


def prefix(x, y):
    m = len(x)
    n = len(y)
    a = [0 for _ in range(n + 1)]
    for j in range(n + 1):
        a[j] = j * gap_penalty
    for i in range(1, m + 1):
        prev = a[0]
        a[0] = i * gap_penalty
        for j in range(1, n + 1):
            temp = a[j]
            mismatch = prev + alpha[x[i - 1]][y[j - 1]]
            x_gap = a[j] + gap_penalty
            y_gap = a[j - 1] + gap_penalty
            a[j] = min(mismatch, x_gap, y_gap)
            prev = temp
    return a


def suffix(x, y):
    return prefix(x[::-1], y[::-1])[::-1]


def efficient(x, y, x_start, x_end, y_start, y_end):
    if x_end - x_start <= 2 or y_end - y_start <= 2:
        cost, align_x, align_y = basic(x[x_start:x_end], y[y_start:y_end])
        return cost, align_x, align_y
    else:
        i = (x_start + x_end) // 2
        prefix_cost = prefix(x[x_start:i], y[y_start:y_end])
        suffix_cost = suffix(x[i:x_end], y[y_start:y_end])
        pos = 0
        min_cost = prefix_cost[0] + suffix_cost[0]
        for j in range(len(prefix_cost)):
            cost = prefix_cost[j] + suffix_cost[j]
            if cost < min_cost:
                min_cost = cost
                pos = j
        pos += y_start
        pre_cost, pre_align_x, pre_align_y = efficient(x, y, x_start, i, y_start, pos)
        suf_cost, suf_align_x, suf_align_y = efficient(x, y, i, x_end, pos, y_end)
        cost = pre_cost + suf_cost
        align_x = pre_align_x + suf_align_x
        align_y = pre_align_y + suf_align_y
        return cost, align_x, align_y


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
        # return
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
    cost, align1, align2 = efficient(str1, str2, 0, len(str1), 0, len(str2))
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    memory_consumed = process_memory()
    write_output(cost, align1, align2, time_taken, memory_consumed)

from common import dc, alpha, gap_penalty
from basic_3 import basic


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


if __name__ == '__main__':
    dc(efficient)

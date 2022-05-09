from common import dp, alpha, gap_penalty


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


if __name__ == '__main__':
    dp(basic)

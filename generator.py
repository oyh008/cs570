import sys


def generator(input):
    with open(input) as f:
        data = f.readlines()
        for i in range(len(data)):
            data[i] = data[i].strip('\n')
            if i > 0 and '0' <= data[i][0] <= '9':
                continue
            elif i > 0:
                k = i - 1
                j = len(data) - i - 1
        base1, base2 = data[0], data[k + 1]
        index1, index2 = list(map(int, data[1:k + 1])), list(map(int, data[k + 2:]))
        # print(data)
        # print(base1, base2, index1, index2)

    for i in range(k):
        base1 = base1[:index1[i] + 1] + base1 + base1[index1[i] + 1:]
    # print(base1)

    for i in range(j):
        base2 = base2[:index2[i] + 1] + base2 + base2[index2[i] + 1:]
    # print(base2)
    return base1, base2


if __name__ == '__main__':
    X, Y = generator(sys.argv[1])
    print(X, Y)

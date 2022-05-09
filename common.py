import sys

alpha = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
         'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
         'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
         'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}

gap_penalty = 30


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


def write_output(cost, align1, align2):
    # write to output
    output = sys.argv[2]
    # print(cost)
    # print(align1)
    # print(align2)
    with open(output, "w") as file:
        file.write(str(cost) + "\n")
        file.write(align1 + "\n")
        file.write(align2 + "\n")
        # write time
        # write memory
        file.close()


# def calculate_cost(x, y):
#     cost = 0
#     for i in range(len(x)):
#         if x[i] == "_" or y[i] == "_":
#             cost += 30
#         else:
#             cost += alpha[x[i]][y[i]]
#         print(cost)


# basic solution that uses dynamic programming
def dp(algorithm):
    input = sys.argv[1]
    # time and memory function start here
    str1, str2 = generate_str(input)
    cost, align1, align2 = algorithm(str1, str2)
    # calculate_cost(align1, align2)
    write_output(cost, align1, align2)


# efficient solution that uses divide and conquer on top of dynamic programming
def dc(algorithm):
    input = sys.argv[1]
    # time and memory function start here
    str1, str2 = generate_str(input)
    cost, align1, align2 = algorithm(str1, str2, 0, len(str1), 0, len(str2))
    # calculate_cost(align1, align2)
    write_output(cost, align1, align2)
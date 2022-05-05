import matplotlib.pyplot as plt
import seaborn as sns
import math

with open("cpu_time.txt") as f:
    data = f.readlines()
    for i in range(len(data)):
        data[i] = data[i].strip('\n')

    print(data)

with open("memory_usage.txt") as f:
    data_m = f.readlines()
    for i in range(len(data_m)):
        data_m[i] = data_m[i].strip('\n')

    print(data_m)

size_x = []
naive_y = []
optimized_y = []

for i in range(len(data)):
    if i % 3 == 0:
        naive_y.append(float(data[i]))
    elif i % 3 == 1:
        optimized_y.append(float(data[i]))
    elif i % 3 == 2:
        size_x.append(math.log(int(data[i]), 2))

size_m_x = []
naive_m_y = []
optimized_m_y = []

for i in range(len(data)):
    if i % 3 == 0:
        naive_m_y.append(float(data_m[i]))
    elif i % 3 == 1:
        optimized_m_y.append(float(data_m[i]))
    elif i % 3 == 2:
        size_m_x.append(math.log(int(data_m[i]), 2))

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True)
fig.set_size_inches(18, 10, forward=True)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")

ax1.set_title("CPU time vs problem size for the two solutions")
ax1.plot(size_x, naive_y, linestyle="-", marker="s", label="naive solution")
ax1.plot(size_x, optimized_y, linestyle="--", marker="^", label="optimized solution")
ax1.set_xlabel("Problem size(2^X bits)")
ax1.set_ylabel("CPU time(Y s)")
ax1.legend(loc="upper left")

ax2.set_title("Memory usage vs problem size for the two solutions")
ax2.plot(size_m_x, naive_m_y, linestyle="-", marker="s", label="naive solution")
ax2.plot(size_m_x, optimized_m_y, linestyle="--", marker="^", label="optimized solution")
ax2.set_xlabel("Problem size(2^X bits)")
ax2.set_ylabel("Memory usage(Y MB)")
ax2.legend(loc="upper left")

plt.show()

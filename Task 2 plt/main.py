import matplotlib.pyplot as plt
import numpy as np

# 1
x = np.linspace(-10, 10, 1000)
y = x ** 2 * np.sin(x)
plt.plot(x, y)
plt.show()

# 2
mean = 5
sigma = 2
x = np.random.normal(mean, sigma, 1000)
plt.hist(x, bins=30, color="skyblue", edgecolor="black", density=True)
plt.show()

#3
hobbies = [
    "Програмування",
    "Cs2",
    "Волейбол",
    "Музика",
    "Робототехніка",
]
shares = [30, 25, 70, 15, 20]
colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]

plt.figure(figsize=(6, 6))
plt.pie(
    shares,
    labels=hobbies,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    explode=[0.05] * len(shares),
)
plt.show()

#4
apples = np.random.normal(loc=180, scale=20, size=100)
bananas = np.random.normal(loc=120, scale=15, size=100)
oranges = np.random.normal(loc=200, scale=25, size=100)
pears = np.random.normal(loc=160, scale=18, size=100)

fruits_data = [apples, bananas, oranges, pears]
fruit_labels = ["Яблука", "Банани", "Апельсини", "Груші"]

plt.figure(figsize=(6, 6))
plt.boxplot(fruits_data, tick_labels=fruit_labels)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

#5
x = np.random.uniform(0,1,100)
y = np.random.uniform(0,1,100)
plt.scatter(x,y, color="green", alpha = 0.6)
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()

#6
x = np.linspace(-10, 10, 1000)

f = np.sin(x)
g = np.cos(x)
h = np.sin(x) + np.cos(x)

plt.plot(x, f, label=r"sin(x)", color="blue", linewidth=2)
plt.plot(x, g, label=r"cos(x)", color="orange", linewidth=2)
plt.plot(x, h,label=r"sin(x)+cos(x)", color="green",linewidth=2,linestyle="--")
plt.title("Plots", fontsize=14, fontweight="bold")
plt.xlabel("x", fontsize=12)
plt.ylabel("y", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(loc="upper right", fontsize=10)
plt.show()

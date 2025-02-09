from time import time
import matplotlib.pyplot as plt
from generate import generate_random_points
from convex_hull import compute_hull
from plotting import plot_points, draw_hull, title, show_plot  # type: ignore
import numpy as np


def run_report(n: int, distribution: str, seed: int | None):
    points = generate_random_points(distribution, n, seed)
    plot_points(points)

    start = time()
    hull_points = compute_hull(points)
    end = time()

    draw_hull(hull_points)
    title(f"{n} {distribution} points: {round(end - start, 4)} seconds")
    show_plot(block=True)

    return end - start


#  # sys.argv = ["main.py", "-n", "1000", "--seed", "312", "-d"]
# time_elapsed = run_report(1000, "normal", 312)
# print(time_elapsed)

meanTimes = []
numberOfTimes = [
    10,
    100,
    1000,
    10000,
    100000,
    500000,
    1000000,
]  # add , 500000, 1000000 later

for n in numberOfTimes:
    meanTime: float = 0
    for i in range(5):
        reportTime = run_report(n, "uniform", 312)
        meanTime += reportTime
        print(f"Time for {n} number of points: {reportTime} ")
    meanTime /= 5
    meanTimes.append(meanTime)

print(meanTimes)
print(numberOfTimes)

nlogn_values = [n * np.log(n) for n in numberOfTimes]

# plot mean time (dependant) required and number of points (independant)
plt.clf()
plt.xscale("log")
plt.yscale("log")

plt.title("Number of Points vs Mean Time")
plt.xlabel("Size of n")
plt.ylabel("Time in seconds")
plt.plot(numberOfTimes, meanTimes, label="Mean Time", marker="o")

plt.plot(numberOfTimes, nlogn_values, label="n log(n) Complexity", linestyle="--")
plt.legend()

plt.show()

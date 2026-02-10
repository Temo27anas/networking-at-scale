import matplotlib.pyplot as plt

intervals = [
    2.51, 3, 3,3, 3.98, 5.02, 4.0, 7.01, 7, 11.01
]

plt.plot(range(1, len(intervals)+1), intervals, marker='o')
plt.xlabel("retry")
plt.ylabel("interval between retries (s)")
plt.title("Pub/Sub backoff retry intervals")
plt.grid(True)
plt.show()

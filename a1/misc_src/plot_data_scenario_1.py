import matplotlib.pyplot as plt

regions = ['Finland', 'Frankfurt', 'Madrid']
p50_latencies = [28.31, 37.93, 41.52]
avg_latencies = [59.84, 95.86, 96.41]

plt.bar(regions, p50_latencies, label='Median (p50)')
plt.ylabel('Latency (ms)')
plt.title('Comparison of Median Latency by Region')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scenario-b/measurements/performance_results.csv")

baseline = df[df["condition"].str.startswith("baseline")]
baseline_avg = baseline["throughput_mbps"].mean()

degraded = df.loc[
    df["condition"] == "rate_limit_20mbps",
    "throughput_mbps"
].iloc[0]

reduction = (1 - degraded / baseline_avg) * 100

print("Baseline average throughput:", round(baseline_avg, 2), "Mbps")
print("20 Mbps degraded throughput:", degraded, "Mbps")
print("Throughput reduction:", round(reduction, 2), "%")

conditions = ["Baseline average", "20 Mbps rate limit"]
throughputs = [baseline_avg, degraded]

plt.figure(figsize=(8, 5))
plt.bar(conditions, throughputs)
plt.ylabel("Throughput (Mbps)")
plt.title("Scenario B N6 TCP Throughput Comparison")
plt.tight_layout()
plt.savefig(
    "scenario-b/analysis/throughput_comparison.png",
    dpi=200
)

print("Graph saved to scenario-b/analysis/throughput_comparison.png")

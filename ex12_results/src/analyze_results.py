import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('results/results.csv')

# 1. Distribution of mean temperatures (Histogram)
plt.figure(figsize=(10, 6))
df['mean_temp'].hist(bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Mean Interior Temperatures')
plt.xlabel('Mean Temperature (ºC)')
plt.ylabel('Number of Buildings')
plt.savefig('results/mean_temp_distribution.png')

# 2. Average mean temperature
avg_mean = df['mean_temp'].mean()

# 3. Average standard deviation
avg_std = df['std_temp'].mean()

# 4. Buildings with >= 50% area > 18ºC
mold_safe = df[df['pct_above_18'] >= 50].shape[0]

# 5. Buildings with >= 50% area < 15ºC
too_cold = df[df['pct_below_15'] >= 50].shape[0]

print(f"Average Mean Temperature: {avg_mean:.2f}ºC")
print(f"Average Std Deviation: {avg_std:.2f}ºC")
print(f"Buildings with >= 50% area above 18ºC: {mold_safe}")
print(f"Buildings with >= 50% area below 15ºC: {too_cold}")

freezing = df[df['mean_temp'] < 8]

print(freezing)
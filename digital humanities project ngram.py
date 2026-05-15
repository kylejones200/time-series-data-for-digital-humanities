"""Generated from Jupyter notebook: digital humanities project ngram

Magics and shell lines are commented out. Run with a normal Python interpreter."""


# --- code cell ---

import matplotlib.pyplot as plt
import pandas as pd

# --- code cell ---

df = pd.read_csv("/Users/kylejonespatricia/Documents/Combined_sentiment 1840-1963.csv")

df.drop("Unnamed: 0", axis=1, inplace=True)
df["year"] = pd.to_datetime(df["year"], format="%Y")
df = df.sort_values("year")
df.set_index("year", inplace=True)


# --- code cell ---

df.head()


# --- code cell ---

topics = df["Topic"].unique()
colors = plt.get_cmap("tab10", len(topics))

# Plot the data
plt.figure(figsize=(12, 6))
for i, topic in enumerate(topics):
    subset = df[df["Topic"] == topic]
    plt.plot(
        subset.index, subset["composite"], linestyle="-", label=topic, color=colors(i)
    )

plt.xlabel("Year")
plt.ylabel("Composite Score")
plt.title("Composite Score by Topic Over Time")
plt.legend(title="Topic")
plt.grid(True)

# Save the figure
plt.savefig("composite_score_by_topic.png")

# Show the plot
plt.show()


# --- code cell ---

# Apply a rolling mean to smooth the lines (adjust window size as needed)
df["composite_smooth"] = df.groupby("Topic")["composite"].transform(
    lambda x: x.rolling(window=20, min_periods=1).mean()
)

# Generate unique colors for each topic
topics = df["Topic"].unique()
colors = plt.cm.get_cmap("tab10", len(topics))

# Plot the smoothed data
plt.figure(figsize=(12, 6))
for i, topic in enumerate(topics):
    subset = df[df["Topic"] == topic]
    plt.plot(
        subset.index,
        subset["composite_smooth"],
        linestyle="-",
        label=topic,
        color=colors(i),
        alpha=0.8,
    )

plt.xlabel("Year")
plt.ylabel("Composite Score (Smoothed)")
plt.title("Smoothed Composite Score by Topic Over Time")
plt.legend(title="Topic")
plt.grid(True)

# Save the figure
plt.savefig("smoothed_composite_score_by_topic.png")

# Show the plot
plt.show()


# --- code cell ---

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Prepare for anomaly detection
df["anomaly"] = False  # Placeholder

# Initialize Isolation Forest
iso_forest = IsolationForest(contamination=0.05, random_state=42)

# Apply anomaly detection per topic
anomaly_dfs = []
for topic in df["Topic"].unique():
    subset = df[df["Topic"] == topic].copy()

    # Fit Isolation Forest
    subset["anomaly"] = iso_forest.fit_predict(subset[["composite"]]) == -1

    # Store results
    anomaly_dfs.append(subset)

# Merge results
df_anomalies = pd.concat(anomaly_dfs)

# Generate unique colors for each topic
topics = df["Topic"].unique()
colors = plt.cm.get_cmap("tab10", len(topics))

# Plot the data with anomalies
plt.figure(figsize=(12, 6))
for i, topic in enumerate(topics):
    subset = df_anomalies[df_anomalies["Topic"] == topic]

    # Normal points
    plt.plot(
        subset.index,
        subset["composite"],
        linestyle="-",
        label=topic,
        color=colors(i),
        alpha=0.8,
    )

    # Anomalies
    anomalies = subset[subset["anomaly"]]
    plt.scatter(
        anomalies.index,
        anomalies["composite"],
        color=colors(i),
        marker="o",
        edgecolor="black",
        s=100,
        label=f"{topic} (Anomaly)",
    )

plt.xlabel("Year")
plt.ylabel("Composite Score")
plt.title("Anomaly Detection in Composite Score by Topic")
plt.legend(title="Topic", loc="upper left", bbox_to_anchor=(1, 1))
plt.grid(True)

# Save the figure
plt.savefig("anomaly_composite_score_by_topic.png")

# Show the plot
plt.show()


# --- code cell ---

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Pivot the data to get topics as columns
df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")

# Compute rolling correlation (window size can be adjusted)
rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()

# Store years for animation
years = rolling_corr.index.get_level_values(0).unique()


# --- code cell ---

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Pivot the data to get topics as columns
df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")

# Compute rolling correlation (window size can be adjusted)
rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()

# Store years for animation
years = rolling_corr.index.get_level_values(0).unique()

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))


def update(year):
    ax.clear()
    corr_matrix = rolling_corr.loc[year]
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title(f"Rolling Correlation Matrix - Year: {year.year}")


# Create animation
ani = animation.FuncAnimation(fig, update, frames=years, repeat=False)

# Save animation as GIF
ani.save("rolling_correlation.gif", writer="pillow", fps=5)

print("GIF saved as 'rolling_correlation.gif'")


# --- code cell ---

# %matplotlib inline  # Jupyter-only


# --- code cell ---

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Pivot the data to get topics as columns
df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")

# Compute rolling correlation (window size can be adjusted)
rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()

# Store years for animation
years = rolling_corr.index.get_level_values(0).unique()

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Get a sample correlation matrix for setting a fixed structure
initial_corr_matrix = rolling_corr.loc[years[0]]


# Function to update frames
def update(year):
    ax.clear()
    corr_matrix = rolling_corr.loc[year]

    # Plot heatmap without the color bar
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        ax=ax,
        cbar=False,
        vmin=-1,
        vmax=1,  # Keep scale consistent across frames
    )

    ax.set_title(f"Rolling Correlation Matrix - Year: {year.year}")


# Create animation
ani = animation.FuncAnimation(fig, update, frames=years, repeat=False)

# Save animation as GIF
ani.save("rolling_correlation.gif", writer="pillow", fps=5)

print("GIF saved as 'rolling_correlation.gif'")


# --- code cell ---

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Pivot the data to get topics as columns
df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")

# Compute rolling correlation (window size can be adjusted)
rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()

# Store years for animation
years = rolling_corr.index.get_level_values(0).unique()

# Get a sample correlation matrix to define the structure
initial_corr_matrix = rolling_corr.loc[years[0]]

# Create a mask to hide the upper triangle
mask = np.triu(np.ones_like(initial_corr_matrix, dtype=bool))

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))


# Function to update frames
def update(year):
    ax.clear()
    corr_matrix = rolling_corr.loc[year]

    # Plot lower triangle only (masked upper triangle)
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        ax=ax,
        cbar=False,
        vmin=-1,
        vmax=1,
        mask=mask,  # Apply the mask
    )

    ax.set_title(f"Rolling Correlation Matrix - Year: {year.year}")


# Create animation
ani = animation.FuncAnimation(fig, update, frames=years, repeat=False)

# Save animation as GIF
ani.save("rolling_correlation.gif", writer="pillow", fps=5)

print("GIF saved as 'rolling_correlation.gif'")


# --- code cell ---

import matplotlib.pyplot as plt
import pandas as pd

# Pivot the data so each topic is a separate column
df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")

# Plot the time series data
plt.figure(figsize=(12, 6))
for column in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[column], marker="o", linestyle="-", label=column)

plt.xlabel("Year")
plt.ylabel("Composite Score")
plt.title("Composite Score by Topic Over Time")
plt.legend(title="Topic", loc="upper left", bbox_to_anchor=(1, 1))
plt.grid(True)

# Save the figure
plt.savefig("composite_score_time_series.png")

# Show the plot
plt.show()


# --- code cell ---

import matplotlib.pyplot as plt
import pandas as pd

# Pivot the data so each topic is a separate column
df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")

# Compute rolling correlation (window size can be adjusted)
rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr(pairwise=True)

# Extract lower triangle correlations (avoid duplicate pairs)
correlation_over_time = {}
years = rolling_corr.index.get_level_values(0).unique()
for year in years:
    corr_matrix = rolling_corr.loc[year]
    lower_triangle = corr_matrix.where(~np.triu(np.ones(corr_matrix.shape, dtype=bool)))
    mean_corr = lower_triangle.mean().mean()  # Get overall correlation trend
    correlation_over_time[year] = mean_corr

# Convert to DataFrame for plotting
corr_df = pd.DataFrame(
    list(correlation_over_time.items()), columns=["Year", "Mean_Correlation"]
).set_index("Year")

# Plot the correlations over time
plt.figure(figsize=(12, 6))
plt.plot(
    corr_df.index, corr_df["Mean_Correlation"], marker="o", linestyle="-", color="b"
)

plt.xlabel("Year")
plt.ylabel("Mean Correlation")
plt.title("Mean Correlation Over Time")
plt.grid(True)

# Save the figure
plt.savefig("correlation_over_time.png")

# Show the plot
plt.show()


# --- code cell ---

corr_df.head(10)


# --- code cell ---

import statsmodels.api as sm

# Drop NaN values from the correlation dataset
df_corr = corr_df.dropna().copy()

# Prepare the independent (X) and dependent (Y) variables
X = sm.add_constant(df_corr.index.year)  # Add constant for intercept
Y = df_corr["Mean_Correlation"]

# Fit an Ordinary Least Squares (OLS) regression model
model = sm.OLS(Y, X).fit()

# Get summary of the regression
regression_summary = model.summary()

# Display regression results
print(regression_summary)


# --- code cell ---

import matplotlib.pyplot as plt
import numpy as np

# Drop NaN values
df_corr = corr_df.dropna().copy()

# Compute mean and standard deviation
mean_corr = df_corr["Mean_Correlation"].mean()
std_corr = df_corr["Mean_Correlation"].std()

# Calculate +/- 2 standard deviations from the mean
upper_bound = mean_corr + 2 * std_corr
lower_bound = mean_corr - 2 * std_corr

# Plot the correlation over time
plt.figure(figsize=(12, 6))
plt.plot(
    df_corr.index,
    df_corr["Mean_Correlation"],
    marker="o",
    linestyle="-",
    color="b",
    label="Mean Correlation",
)

# Plot the mean as a horizontal red line
plt.axhline(y=mean_corr, color="red", linestyle="-", linewidth=2, label="Mean")

# Plot +/- 2 standard deviations as dashed red lines
plt.axhline(
    y=upper_bound, color="red", linestyle="--", linewidth=1.5, label="+2 Std Dev"
)
plt.axhline(
    y=lower_bound, color="red", linestyle="--", linewidth=1.5, label="-2 Std Dev"
)

plt.xlabel("Year")
plt.ylabel("Mean Correlation")
plt.title("Mean Correlation Over Time with ±2 Std Dev Bounds")
plt.legend()
plt.grid(True)

# Save the figure
plt.savefig("correlation_with_std_bounds.png")

# Show the plot
plt.show()


# --- code cell ---

import matplotlib.pyplot as plt
import pandas as pd
import requests


def get_ngram_data(words, start_year=1800, end_year=2000):
    df = pd.DataFrame(index=range(start_year, end_year + 1))
    for word in words:
        url = f"https://books.google.com/ngrams/json?content={word}&year_start={start_year}&year_end={end_year}&corpus=26&smoothing=3"
        response = requests.get(url)
        data = response.json()
        if data:
            df[word] = pd.Series(
                data[0]["timeseries"], index=range(start_year, end_year + 1)
            )
    return df


# Example usage
words = ["economy", "equality", "democracy", "freedom", "justice", "liberty"]
start_year = 1850
end_year = 1965
df = get_ngram_data(words)
df.to_csv(f"ngram from {start_year}-{end_year}.csv")

# Plot
plt.figure(figsize=(12, 6))
df.plot(figsize=(12, 6))
plt.title("Google Books Ngram Viewer Trends")
plt.xlabel("Year")
plt.ylabel("Frequency (%)")
plt.grid(True)
plt.savefig("ngram_trends.png")
plt.show()


# --- duplicate code cell omitted (identical to earlier cell) ---

"""Generated from Jupyter notebook: digital humanities project ngram

Magics and shell lines are commented out. Run with a normal Python interpreter."""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import statsmodels.api as sm
from sklearn.ensemble import IsolationForest


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


def update(year):
    ax.clear()
    corr_matrix = rolling_corr.loc[year]
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
        mask=mask,
    )
    ax.set_title(f"Rolling Correlation Matrix - Year: {year.year}")


def notebook_step_002() -> None:
    df = pd.read_csv("data/Combined_sentiment 1840-1963.csv")
    df.drop("Unnamed: 0", axis=1, inplace=True)
    df["year"] = pd.to_datetime(df["year"], format="%Y")
    df = df.sort_values("year")
    df.set_index("year", inplace=True)


def notebook_step_003() -> None:
    df.head()


def plot_the_data() -> None:
    topics = df["Topic"].unique()
    colors = plt.get_cmap("tab10", len(topics))
    plt.figure(figsize=(12, 6))
    for i, topic in enumerate(topics):
        subset = df[df["Topic"] == topic]
        plt.plot(
            subset.index,
            subset["composite"],
            linestyle="-",
            label=topic,
            color=colors(i),
        )

    plt.xlabel("Year")
    plt.ylabel("Composite Score")
    plt.title("Composite Score by Topic Over Time")
    plt.legend(title="Topic")
    plt.grid(True)
    plt.savefig("composite_score_by_topic.png")
    plt.show()


def apply_a_rolling_mean_to_smooth_the_lines_adjust() -> None:
    df["composite_smooth"] = df.groupby("Topic")["composite"].transform(
        lambda x: x.rolling(window=20, min_periods=1).mean()
    )
    topics = df["Topic"].unique()
    colors = plt.cm.get_cmap("tab10", len(topics))
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
    plt.savefig("smoothed_composite_score_by_topic.png")
    plt.show()


def prepare_for_anomaly_detection() -> None:
    df["anomaly"] = False
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    anomaly_dfs = []
    for topic in df["Topic"].unique():
        subset = df[df["Topic"] == topic].copy()
        subset["anomaly"] = iso_forest.fit_predict(subset[["composite"]]) == -1
        anomaly_dfs.append(subset)

    df_anomalies = pd.concat(anomaly_dfs)
    topics = df["Topic"].unique()
    colors = plt.cm.get_cmap("tab10", len(topics))
    plt.figure(figsize=(12, 6))
    for i, topic in enumerate(topics):
        subset = df_anomalies[df_anomalies["Topic"] == topic]
        plt.plot(
            subset.index,
            subset["composite"],
            linestyle="-",
            label=topic,
            color=colors(i),
            alpha=0.8,
        )
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
    plt.savefig("anomaly_composite_score_by_topic.png")
    plt.show()


def pivot_the_data_to_get_topics_as_columns() -> None:
    df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")
    rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()
    rolling_corr.index.get_level_values(0).unique()


def pivot_the_data_to_get_topics_as_columns_2() -> None:
    df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")
    rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()
    years = rolling_corr.index.get_level_values(0).unique()
    fig, ax = plt.subplots(figsize=(10, 8))
    ani = animation.FuncAnimation(fig, update, frames=years, repeat=False)
    ani.save("rolling_correlation.gif", writer="pillow", fps=5)
    print("GIF saved as 'rolling_correlation.gif'")


def pivot_the_data_to_get_topics_as_columns_3() -> None:
    df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")
    rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()
    years = rolling_corr.index.get_level_values(0).unique()
    fig, ax = plt.subplots(figsize=(10, 8))
    rolling_corr.loc[years[0]]
    ani = animation.FuncAnimation(fig, update, frames=years, repeat=False)
    ani.save("rolling_correlation.gif", writer="pillow", fps=5)
    print("GIF saved as 'rolling_correlation.gif'")


def pivot_the_data_to_get_topics_as_columns_4() -> None:
    df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")
    rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr()
    years = rolling_corr.index.get_level_values(0).unique()
    initial_corr_matrix = rolling_corr.loc[years[0]]
    np.triu(np.ones_like(initial_corr_matrix, dtype=bool))
    fig, ax = plt.subplots(figsize=(10, 8))
    ani = animation.FuncAnimation(fig, update, frames=years, repeat=False)
    ani.save("rolling_correlation.gif", writer="pillow", fps=5)
    print("GIF saved as 'rolling_correlation.gif'")


def pivot_the_data_so_each_topic_is_a_separate_colum() -> None:
    df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")
    plt.figure(figsize=(12, 6))
    for column in df_pivot.columns:
        plt.plot(
            df_pivot.index, df_pivot[column], marker="o", linestyle="-", label=column
        )

    plt.xlabel("Year")
    plt.ylabel("Composite Score")
    plt.title("Composite Score by Topic Over Time")
    plt.legend(title="Topic", loc="upper left", bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.savefig("composite_score_time_series.png")
    plt.show()


def pivot_the_data_so_each_topic_is_a_separate_colum_2() -> None:
    df_pivot = df.pivot_table(index="year", columns="Topic", values="composite")
    rolling_corr = df_pivot.rolling(window=10, min_periods=5).corr(pairwise=True)
    correlation_over_time = {}
    years = rolling_corr.index.get_level_values(0).unique()
    for year in years:
        corr_matrix = rolling_corr.loc[year]
        lower_triangle = corr_matrix.where(
            ~np.triu(np.ones(corr_matrix.shape, dtype=bool))
        )
        mean_corr = lower_triangle.mean().mean()
        correlation_over_time[year] = mean_corr

    corr_df = pd.DataFrame(
        list(correlation_over_time.items()), columns=["Year", "Mean_Correlation"]
    ).set_index("Year")
    plt.figure(figsize=(12, 6))
    plt.plot(
        corr_df.index, corr_df["Mean_Correlation"], marker="o", linestyle="-", color="b"
    )
    plt.xlabel("Year")
    plt.ylabel("Mean Correlation")
    plt.title("Mean Correlation Over Time")
    plt.grid(True)
    plt.savefig("correlation_over_time.png")
    plt.show()


def notebook_step_014() -> None:
    corr_df.head(10)


def drop_nan_values_from_the_correlation_dataset() -> None:
    df_corr = corr_df.dropna().copy()
    X = sm.add_constant(df_corr.index.year)
    Y = df_corr["Mean_Correlation"]
    model = sm.OLS(Y, X).fit()
    regression_summary = model.summary()
    print(regression_summary)


def drop_nan_values() -> None:
    df_corr = corr_df.dropna().copy()
    mean_corr = df_corr["Mean_Correlation"].mean()
    std_corr = df_corr["Mean_Correlation"].std()
    upper_bound = mean_corr + 2 * std_corr
    lower_bound = mean_corr - 2 * std_corr
    plt.figure(figsize=(12, 6))
    plt.plot(
        df_corr.index,
        df_corr["Mean_Correlation"],
        marker="o",
        linestyle="-",
        color="b",
        label="Mean Correlation",
    )
    plt.axhline(y=mean_corr, color="red", linestyle="-", linewidth=2, label="Mean")
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
    plt.savefig("correlation_with_std_bounds.png")
    plt.show()


def example_usage() -> None:
    words = ["economy", "equality", "democracy", "freedom", "justice", "liberty"]
    start_year = 1850
    end_year = 1965
    df = get_ngram_data(words)
    df.to_csv(f"ngram from {start_year}-{end_year}.csv")
    plt.figure(figsize=(12, 6))
    df.plot(figsize=(12, 6))
    plt.title("Google Books Ngram Viewer Trends")
    plt.xlabel("Year")
    plt.ylabel("Frequency (%)")
    plt.grid(True)
    plt.savefig("ngram_trends.png")
    plt.show()


def main() -> None:
    notebook_step_002()
    notebook_step_003()
    plot_the_data()
    apply_a_rolling_mean_to_smooth_the_lines_adjust()
    prepare_for_anomaly_detection()
    pivot_the_data_to_get_topics_as_columns()
    pivot_the_data_to_get_topics_as_columns_2()
    pivot_the_data_to_get_topics_as_columns_3()
    pivot_the_data_to_get_topics_as_columns_4()
    pivot_the_data_so_each_topic_is_a_separate_colum()
    pivot_the_data_so_each_topic_is_a_separate_colum_2()
    notebook_step_014()
    drop_nan_values_from_the_correlation_dataset()
    drop_nan_values()
    example_usage()


if __name__ == "__main__":
    main()

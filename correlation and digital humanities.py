"""Generated from Jupyter notebook: correlation and digital humanities

Magics and shell lines are commented out. Run with a normal Python interpreter."""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
import ruptures as rpt
import seaborn as sns
from copulas.bivariate import Clayton, Gumbel
from scipy.stats import kendalltau, rankdata


def rolling_correlation(df, method="kendall", window=10):
    rolling_corrs = pd.DataFrame(index=df.index, columns=df.columns[1:])
    for i in range(len(df) - window + 1):
        df_window = df.iloc[i : i + window]
        for topic in df.columns[1:]:
            corr, _ = kendalltau(df_window["gdp_percap"], df_window[topic])
            rolling_corrs.loc[df.index[i + window - 1], topic] = corr
    return rolling_corrs.astype(float)


def update(frame):
    decade = decades[frame]
    df_decade = df_selected[df_selected["decade"] == decade]
    for ax in axes:
        ax.clear()
    for ax, (x_var, y_var) in zip(axes, topic_pairs):
        sns.kdeplot(
            x=df_decade[x_var], y=df_decade[y_var], fill=True, cmap="Blues", ax=ax
        )
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.set_title(f"GDP Per Capital vs {y_var}")
    plt.suptitle(
        f"Sentiment and GDP Per Capital Joint Distribution by Decade: {decade}s"
    )


def install_necessary_packages_run_this_only_if_you() -> None:
    file_path = "Wide_Sentiment_Data.csv"

    df = pd.read_csv(file_path)

    selected_topics = ["Economy", "Freedom", "Liberty", "Democracy"]

    df_selected = df[selected_topics].apply(pd.to_numeric, errors="coerce")

    df_selected = df_selected.dropna()

    df_copula = df_selected.copy()

    for col in selected_topics:
        df_copula[col] = rankdata(df_copula[col]) / (len(df_copula) + 1)

    copula_models = {"Clayton": Clayton(), "Gumbel": Gumbel()}

    copula_results = {}

    for model_name, copula in copula_models.items():
        dependencies = {}
        for topic in selected_topics[1:]:
            try:
                copula.fit(df_copula[["Economy", topic]].values)
                dependencies[topic] = copula.theta
            except Exception as e:
                dependencies[topic] = f"Error: {e}"
        copula_results[model_name] = dependencies

    copula_df = pd.DataFrame(copula_results)

    print("\nCopula-Based Dependency Metrics:")

    print(copula_df)

    copula_df.to_csv("copula_dependency_metrics.csv")

    print("Copula results saved as 'copula_dependency_metrics.csv'.")


def install_necessary_packages_if_needed() -> None:
    file_path = "Wide_Sentiment_Data.csv"

    df = pd.read_csv(file_path)

    selected_topics = ["Economy", "Freedom", "Liberty", "Democracy"]

    df_selected = df[selected_topics].apply(pd.to_numeric, errors="coerce")

    df_selected = df_selected.dropna()

    df_selected["decade"] = df_selected.index // 10 * 10

    decades = sorted(df_selected["decade"].unique())

    copula_models = {"Clayton": Clayton, "Gumbel": Gumbel}

    copula_results = {
        model: {topic: [] for topic in selected_topics[1:]} for model in copula_models
    }

    for decade in decades:
        df_decade = df_selected[df_selected["decade"] == decade]
        df_copula = df_decade.copy()
        for col in selected_topics:
            df_copula[col] = rankdata(df_copula[col]) / (len(df_copula) + 1)
        for model_name, copula_class in copula_models.items():
            for topic in selected_topics[1:]:
                try:
                    copula = copula_class()
                    copula.fit(df_copula[["Economy", topic]].values)
                    copula_results[model_name][topic].append(copula.theta)
                except Exception:
                    copula_results[model_name][topic].append(None)

    copula_clayton_df = pd.DataFrame(copula_results["Clayton"], index=decades)

    copula_gumbel_df = pd.DataFrame(copula_results["Gumbel"], index=decades)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    copula_clayton_df.plot(ax=axes[0], marker="o")

    axes[0].set_title("Clayton Copula (Lower Tail Dependence) Over Time")

    axes[0].set_xlabel("Decade")

    axes[0].set_ylabel("Clayton Theta (Lower Tail Dependence)")

    axes[0].legend(title="Topic")

    axes[0].grid()

    copula_gumbel_df.plot(ax=axes[1], marker="o")

    axes[1].set_title("Gumbel Copula (Upper Tail Dependence) Over Time")

    axes[1].set_xlabel("Decade")

    axes[1].set_ylabel("Gumbel Theta (Upper Tail Dependence)")

    axes[1].legend(title="Topic")

    axes[1].grid()

    plt.tight_layout()

    plt.savefig("copula_dependency_trends.png")

    plt.show()

    copula_clayton_df.to_csv("copula_clayton_dependency_by_decade.csv")

    copula_gumbel_df.to_csv("copula_gumbel_dependency_by_decade.csv")

    print(
        "Results saved as 'copula_clayton_dependency_by_decade.csv' and 'copula_gumbel_dependency_by_decade.csv'."
    )


def install_necessary_packages_if_needed_2() -> None:
    file_path = "Wide_Sentiment_Data.csv"

    df = pd.read_csv(file_path)

    if "year" in df.columns:
        df.set_index("year", inplace=True)

    selected_topics = ["gdp_percap", "Economy", "Freedom", "Liberty", "Democracy"]

    df_selected = df[selected_topics].apply(pd.to_numeric, errors="coerce")

    df_selected = df_selected.dropna()

    rolling_window = 10

    copula_results_clayton = {topic: [] for topic in selected_topics[1:]}

    copula_results_gumbel = {topic: [] for topic in selected_topics[1:]}

    years_list = []

    for year in df_selected.index[:-rolling_window]:
        df_window = df_selected.loc[year : year + rolling_window]
        df_copula = df_window.copy()
        for col in selected_topics:
            df_copula[col] = rankdata(df_copula[col]) / (len(df_copula) + 1)
        years_list.append(year)
        for topic in selected_topics[1:]:
            try:
                clayton_copula = Clayton()
                clayton_copula.fit(df_copula[["gdp_percap", topic]].values)
                copula_results_clayton[topic].append(clayton_copula.theta)
            except Exception:
                copula_results_clayton[topic].append(None)
            try:
                gumbel_copula = Gumbel()
                gumbel_copula.fit(df_copula[["gdp_percap", topic]].values)
                copula_results_gumbel[topic].append(gumbel_copula.theta)
            except Exception:
                copula_results_gumbel[topic].append(None)

    copula_clayton_df = pd.DataFrame(copula_results_clayton, index=years_list)

    copula_gumbel_df = pd.DataFrame(copula_results_gumbel, index=years_list)

    copula_clayton_df = copula_clayton_df.interpolate(method="linear")

    copula_gumbel_df = copula_gumbel_df.interpolate(method="linear")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    copula_clayton_df.plot(ax=axes[0])

    axes[0].set_title(
        "Lower Tail Dependence with gdp_percap Over Time (Clayton Copula)"
    )

    axes[0].set_xlabel("Year")

    axes[0].set_ylabel("Clayton Theta (Lower Tail Dependence)")

    axes[0].spines["top"].set_visible(False)

    axes[0].spines["right"].set_visible(False)

    copula_gumbel_df.plot(ax=axes[1])

    axes[1].set_title("Upper Tail Dependence with gdp_percap Over Time (Gumbel Copula)")

    axes[1].set_xlabel("Year")

    axes[1].set_ylabel("Gumbel Theta (Upper Tail Dependence)")

    axes[1].spines["top"].set_visible(False)

    axes[1].spines["right"].set_visible(False)

    plt.tight_layout()

    plt.savefig("copula_dependency_trends_real_years.png")

    plt.show()

    copula_clayton_df.to_csv("copula_clayton_dependency_by_real_years.csv")

    copula_gumbel_df.to_csv("copula_gumbel_dependency_by_real_years.csv")

    print(
        "Results saved as 'copula_clayton_dependency_by_real_years.csv' and 'copula_gumbel_dependency_by_real_years.csv'."
    )


def notebook_step_004() -> None:
    df.head()


def install_necessary_packages_run_if_needed() -> None:
    file_path = "Wide_Sentiment_Data.csv"

    df = pd.read_csv(file_path)

    df.set_index("year", inplace=True)

    selected_topics = ["gdp_percap", "Economy", "Freedom", "Liberty", "Democracy"]

    df_selected = df[selected_topics].dropna()

    rolling_spearman_10 = rolling_correlation(df_selected, method="spearman", window=10)

    rolling_spearman_np = rolling_spearman_10.dropna().values

    algo = rpt.Binseg(model="l2").fit(rolling_spearman_np)

    change_points = algo.predict(n_bkps=5)

    change_years = rolling_spearman_10.dropna().index[change_points[:-1]]

    plt.figure(figsize=(12, 6))

    for topic in rolling_spearman_10.columns:
        plt.plot(
            rolling_spearman_10.index,
            rolling_spearman_10[topic],
            label=f"Economy vs {topic}",
        )

    for year in change_years:
        plt.axvline(x=year, color="r", linestyle="--", label=f"Break at {year}")

    plt.xlabel("Year")

    plt.ylabel("Rolling Spearman Correlation (10-year window)")

    plt.title("Structural Breaks in Rolling Spearman Correlation")

    plt.legend()

    plt.grid()

    plt.savefig("spearman_regime_switching.png")

    plt.show()

    breakpoints_df = pd.DataFrame({"Breakpoints": change_years})

    breakpoints_df.to_csv("spearman_structural_breaks.csv", index=False)

    print(
        "Results saved as 'spearman_regime_switching.png' and 'spearman_structural_breaks.csv'."
    )


def install_necessary_packages_run_if_needed_2() -> None:
    file_path = "Wide_Sentiment_Data.csv"

    df = pd.read_csv(file_path)

    df.set_index("year", inplace=True)

    selected_topics = ["Economy", "Freedom", "Liberty", "Democracy"]

    df_selected = df[selected_topics].dropna()

    rolling_spearman_10 = rolling_correlation(df_selected, method="spearman", window=10)

    rolling_spearman_np = rolling_spearman_10.dropna().values

    algo = rpt.Binseg(model="l2").fit(rolling_spearman_np)

    change_points = algo.predict(n_bkps=5)

    change_years = rolling_spearman_10.dropna().index[change_points[:-1]]

    plt.figure(figsize=(12, 6))

    for topic in rolling_spearman_10.columns:
        plt.plot(
            rolling_spearman_10.index,
            rolling_spearman_10[topic],
            label=f"Economy vs {topic}",
        )

    for year in change_years:
        plt.axvline(x=year, color="r", linestyle="--")
        plt.text(
            year, plt.ylim()[1], str(year), color="r", fontsize=12, ha="left", va="top"
        )

    plt.gca().spines["top"].set_visible(False)

    plt.gca().spines["right"].set_visible(False)

    plt.xlabel("Year")

    plt.ylabel("Rolling Spearman Correlation (10-year window)")

    plt.title("Structural Breaks in Rolling Spearman Correlation")

    plt.legend()

    plt.savefig("spearman_regime_switching.png")

    plt.show()

    breakpoints_df = pd.DataFrame({"Breakpoints": change_years})

    breakpoints_df.to_csv("spearman_structural_breaks.csv", index=False)

    print(
        "Results saved as 'spearman_regime_switching.png' and 'spearman_structural_breaks.csv'."
    )


def install_necessary_packages_run_if_needed_3() -> None:
    rolling_kendall_10 = rolling_correlation(df_selected, method="kendall", window=10)

    rolling_kendall_np = rolling_kendall_10.dropna().values

    algo_kendall = rpt.Binseg(model="l2").fit(rolling_kendall_np)

    change_points_kendall = algo_kendall.predict(n_bkps=5)

    change_years_kendall = rolling_kendall_10.dropna().index[change_points_kendall[:-1]]

    plt.figure(figsize=(12, 6))

    for topic in rolling_kendall_10.columns:
        plt.plot(
            rolling_kendall_10.index,
            rolling_kendall_10[topic],
            label=f"Economy vs {topic}",
        )

    for year in change_years_kendall:
        plt.axvline(x=year, color="r", linestyle="--")
        plt.text(
            year + 1,
            plt.ylim()[1],
            str(year),
            color="r",
            fontsize=12,
            ha="left",
            va="top",
        )

    plt.gca().spines["top"].set_visible(False)

    plt.gca().spines["right"].set_visible(False)

    plt.xlabel("Year")

    plt.ylabel("Rolling Kendall Tau Correlation (10-year window)")

    plt.title("Structural Breaks in Rolling Kendall Tau Correlation")

    plt.legend()

    plt.savefig("kendall_regime_switching.png")

    plt.show()

    breakpoints_kendall_df = pd.DataFrame({"Breakpoints": change_years_kendall})

    breakpoints_kendall_df.to_csv("kendall_structural_breaks.csv", index=False)

    print(
        "Results saved as 'kendall_regime_switching.png' and 'kendall_structural_breaks.csv'."
    )


def select_relevant_topics_for_joint_distribution_an() -> None:
    selected_topics = ["Economy", "Freedom", "gdp_percap", "Democracy"]

    df_selected = df[selected_topics].apply(pd.to_numeric, errors="coerce")

    df_selected = df_selected.dropna()

    df_selected["decade"] = df_selected.index // 10 * 10

    decades = sorted(df_selected["decade"].unique())

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    topic_pairs = [
        ("gdp_percap", "Freedom"),
        ("gdp_percap", "Economy"),
        ("gdp_percap", "Democracy"),
    ]

    ani = animation.FuncAnimation(fig, update, frames=len(decades), repeat=True)

    animation_path = "sentiment_joint_distribution_animation.gif"

    ani.save(animation_path, writer="pil", fps=1)

    print(f"Animation saved at: {animation_path}")


def main() -> None:
    install_necessary_packages_run_this_only_if_you()
    install_necessary_packages_if_needed()
    install_necessary_packages_if_needed_2()
    notebook_step_004()
    install_necessary_packages_run_if_needed()
    install_necessary_packages_run_if_needed_2()
    install_necessary_packages_run_if_needed_3()
    select_relevant_topics_for_joint_distribution_an()


if __name__ == "__main__":
    main()

from src.config import Config
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_daily_trend(column_name, daily_metrics, title):
    plt.figure(figsize=(10, 5))
    ax = sns.lineplot(
        daily_metrics, x=daily_metrics.index, y=column_name, hue=Config.VARIATION
    )
    plt.legend(title="Group", title_fontsize="25", fontsize="20")
    plt.xticks(fontsize=15, fontfamily="serif")
    plt.yticks(fontsize=15, fontfamily="serif")
    plt.xlabel("")
    plt.ylabel("")

    ax.axvline(
        x=Config.EXPERIMENT_START_DATE,
        ymin=0,
        ymax=1,
        linestyle="dashed",
        color="g",
    )
    plt.text(
        Config.EXPERIMENT_START_DATE,
        daily_metrics[column_name].min(),
        "TREATMENT",
        rotation=90,
    )
    plt.xticks(rotation=30)
    plt.title(title, fontsize=40)


def plot_stats(aggregated_data, stats, title):
    metrics = list(aggregated_data.columns)
    A_avg = aggregated_data.loc["A"].values
    B_avg = aggregated_data.loc["B"].values

    p_values_list = [stats[metric] for metric in metrics]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_height = 0.35
    y = np.arange(len(metrics))
    bars_A = ax.barh(y - bar_height / 2, A_avg, bar_height, label="Group A")
    bars_B = ax.barh(y + bar_height / 2, B_avg, bar_height, label="Group B")

    ax.set_xlabel("Average Value")
    ax.set_ylabel("Metrics")
    ax.set_title(f"Average Metrics Comparison _ {title}")
    ax.set_yticks(y)
    ax.set_yticklabels(metrics)
    ax.invert_yaxis()
    ax.legend()

    for i, (bar_A, bar_B) in enumerate(zip(bars_A, bars_B)):
        ax.text(
            bar_A.get_width() + 0.5,
            bar_A.get_y() + bar_A.get_height() / 2,
            f"p={p_values_list[i]:.3f}",
            va="center",
            ha="left",
            fontsize=10,
        )
        ax.text(
            bar_B.get_width() + 0.5,
            bar_B.get_y() + bar_B.get_height() / 2,
            f"p={p_values_list[i]:.3f}",
            va="center",
            ha="left",
            fontsize=10,
        )

    plt.tight_layout()
    plt.show()

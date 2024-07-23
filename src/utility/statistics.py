from src.config import Config
from scipy.stats import ttest_ind, mannwhitneyu
from scipy.stats import chi2_contingency
import pandas as pd

activity_stat_columns = [
    "activity_ratio",
    "activity_count",
    "purchase_sum",
    "avg_purchase",
    "avg_gameends",
    "converted_days_count",
    "conversion_ratio",
    "motivated_days_ratio",
    "motivated_days_count",
]


def _perform_ttest(df, group_col, value_col, type="ttest"):
    group1 = df[df[group_col] == "A"][value_col]
    group2 = df[df[group_col] == "B"][value_col]
    if type == "ttest":
        return ttest_ind(group1, group2, equal_var=False)
    return mannwhitneyu(group1, group2)


def calc_ttest(data_frame, statt_columns=None):
    if not statt_columns:
        statt_columns = activity_stat_columns

    stat_result = {
        column: (_perform_ttest(data_frame, Config.VARIATION, column, "ttest"))
        for column in statt_columns
    }
    stat_p = {}
    for key in stat_result:
        stat_p[key] = float(stat_result[key].pvalue)

    return data_frame.groupby(Config.VARIATION)[statt_columns].mean(), stat_p


def calc_chiSq_test(data_frame, group_col, value_col):

    contingency_table = pd.crosstab(
        data_frame[group_col], data_frame[value_col]
    )
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    print("Chi-square statistic:", chi2)
    print("p-value:", p)
    print("Degrees of freedom:", dof)
    print("Expected frequencies:", expected)
    return

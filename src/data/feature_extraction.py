import pandas as pd
from datetime import datetime
from src.config import Config

INITIAL_RECORD_MAP = {
    "activity_ratio":0,
    "activity_count":0,
    "purchase_sum":0,
    "avg_purchase":0,
    "avg_gameends":0,
    "converted_days_count":0,
    "conversion_ratio":0,
    "motivated_days_ratio":0,
    "motivated_days_count":0,

}


def get_assignment_features(activity: pd.DataFrame, study_window="treatment"):
    activity["assignment_date"] = pd.to_datetime(activity.assignment_date)
    activity["install_date"] = pd.to_datetime(activity.install_date)
    activity["conversion_date"] = pd.to_datetime(activity.conversion_date)

    activity.set_index("playerid", inplace=True)

    activity["age_in_app"] = (
        activity["assignment_date"] - activity["install_date"]
    ).dt.days

    activity["convert_age"] = (
        activity["conversion_date"] - activity["install_date"]
    ).dt.days

    activity["converted_before_assignment"] = (
        activity["convert_age"] < activity["age_in_app"]
    ) & (activity["convert_age"].isnull() == False)

    activity["converted_after_assignment"] = (
        activity["convert_age"] >= activity["age_in_app"]
    ) & (activity["convert_age"].isnull() == False)

    activity["never_converted"] = activity["convert_age"].isnull()

    if study_window == "treatment":
        last_experiment_date = datetime.strptime(Config.EXPERIMENT_END_DATE, "%Y-%m-%d")
        activity["study_length"] = activity.apply(
            lambda row: (last_experiment_date - row.assignment_date).days + 1, axis=1
        )
    else:
        start_pre_treatment_date = datetime.strptime(
            Config.STUDY_START_DATE, "%Y-%m-%d"
        )
        activity["study_length"] = activity.apply(
            lambda row: (
                (row.assignment_date - start_pre_treatment_date).days + 1
                if start_pre_treatment_date > row.install_date
                else (row.assignment_date - row.install_date).days
            ),
            axis=1,
        )
    activity["activity_ratio"] = activity["activity_count"] / activity["study_length"]

    activity["conversion_ratio"] = (
        activity["converted_days_count"] / activity["activity_count"]
    )

    # activity["converted_per_study_days"] = (
    #     activity["converted_days_count"] / activity["study_length"]
    # )

    # activity["purchase_per_experiment_day"] = (
    #     activity["purchase_sum"] / activity["study_length"]
    # )

    activity["avg_purchase"] = activity["purchase_sum"] / activity["activity_count"]

    activity["avg_gameends"] = activity["gameends_sum"] / activity["activity_count"]

    # activity["motivation_per_experiment_day"] = (
    #     activity["motivated_days_count"] / activity["study_length"]
    # )

    activity["motivated_days_ratio"] = (
        activity["motivated_days_count"] / activity["activity_count"]
    )

    activity.fillna(INITIAL_RECORD_MAP, inplace=True)

    return activity


def get_groups_daily_assignment(assignment_df):
    group_assignment = (
        assignment_df.groupby(["assignment_date", "abtest_group"])
        .size()
        .unstack(fill_value=0)
    )
    group_assignment["total"] = group_assignment.sum(axis=1)

    for group in group_assignment.columns[:-1]:
        group_assignment[f"ratio_{group}"] = (
            group_assignment[group] / group_assignment["total"]
        )
    group_assignment.reset_index(inplace=True)
    group_assignment.columns = [
        "assignment_date",
        "group_A_assignment",
        "group_B_assignment",
        "population_size",
        "ratio_A",
        "ratio_B",
    ]
    group_assignment["group_A_size"] = group_assignment["group_A_assignment"].cumsum()
    group_assignment["group_B_size"] = group_assignment["group_B_assignment"].cumsum()
    return group_assignment


def get_total_daily_features(daily_metrics, assignment_activity):
    group_assignment = get_groups_daily_assignment(assignment_activity)
    daily_metrics = pd.merge(
        daily_metrics,
        group_assignment[["assignment_date", "group_B_size", "group_A_size"]],
        left_on="activity_date",
        right_on="assignment_date",
        how="left",
    )
    daily_metrics["group_A_size"] = daily_metrics["group_A_size"].fillna(0)
    daily_metrics["group_B_size"] = daily_metrics["group_B_size"].fillna(0)

    return daily_metrics


def get_treatment_daily_features(treatment_daily_metrics):
    treatment_daily_metrics["daily_active_player_percentage"] = (
        treatment_daily_metrics.apply(
            lambda row: (
                row.daily_active_player / row.group_B_size
                if row.abtest_group == "B"
                else row.daily_active_player / row.group_A_size
            ),
            axis=1,
        )
    )

    treatment_daily_metrics["total_conversion_rate"] = treatment_daily_metrics.apply(
        lambda row: (
            row.total_num_purhcases / row.group_B_size
            if row.abtest_group == "B"
            else row.total_num_purhcases / row.group_A_size
        ),
        axis=1,
    )
    treatment_daily_metrics["active_player_conversion_rate"] = (
        treatment_daily_metrics.total_num_purhcases
        / treatment_daily_metrics.daily_active_player
    )

    treatment_daily_metrics["total_sum_purchase_per_player"] = (
        treatment_daily_metrics.apply(
            lambda row: (
                row.total_revenue / row.group_B_size
                if row.abtest_group == "B"
                else row.total_revenue / row.group_A_size
            ),
            axis=1,
        )
    )

    treatment_daily_metrics["total_sum_purchase_per_active_player"] = (
        treatment_daily_metrics.total_revenue
        / treatment_daily_metrics.daily_active_player
    )

    treatment_daily_metrics["average_purchase_size"] = (
        treatment_daily_metrics.total_revenue
        / treatment_daily_metrics.total_num_purhcases
    )
    treatment_daily_metrics["total_game_rounds_per_player"] = (
        treatment_daily_metrics.apply(
            lambda row: (
                row.total_game_rounds / row.group_B_size
                if row.abtest_group == "B"
                else row.total_game_rounds / row.group_A_size
            ),
            axis=1,
        )
    )
    return treatment_daily_metrics

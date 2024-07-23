CREATE TABLE
  abtest.historical_activity AS (
  WITH
    experience AS (
    SELECT
      DISTINCT *
    FROM
      `abtest.assignment` AS exp ),
    activity AS (
    SELECT
      DISTINCT act.playerid,
      COUNT(act.purchases) activity_count,
      SUM(act.purchases) purchase_sum,
      SUM(
        CASE
          WHEN act.purchases>0 THEN 1
          ELSE 0
      END
        ) converted_days_count,
      SUM(act.gameends) gameends_sum,
      AVG(act.purchases) purchase_avg,
      AVG(act.gameends) gameends_avg,
      SUM(
        CASE
          WHEN act.gameends>0 THEN 1
          ELSE 0
      END
        ) motivated_days_count,
    FROM
      experience expp
    LEFT JOIN
      `king-ds-recruit-candidate-991.abtest.activity` act
    ON
      expp.playerid=act.playerid
    WHERE
      act.activity_date< expp.assignment_date
    GROUP BY
      act.playerid,
      expp.assignment_date)
  SELECT
    expp.*,
    act.activity_count,
    act.converted_days_count,
    act.purchase_sum,
    act.purchase_avg,
    act.gameends_sum,
    act.gameends_avg,
    act.motivated_days_count
  FROM
    experience expp
  LEFT JOIN
    activity act
  ON
    expp.playerid = act.playerid)
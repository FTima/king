
  CREATE TABLE abtest.assignment_activity
  AS
(WITH
  experience AS (
  SELECT
    DISTINCT *
  FROM
    `abtest.assignment` AS exp ),
  activity AS (
  SELECT
    DISTINCT act.playerid,
    COUNT(act.purchases) count_activity,
    SUM(act.purchases) sum_purchase,
    SUM(act.gameends) sum_gameends,
    AVG(act.purchases) avg_purchase,
    AVG(act.gameends) avg_gameends,
    act.activity_date-expp.assignment_date,
    SUM(
      CASE
        WHEN act.purchases>0 THEN 1
        ELSE 0
    END
      ) converted_days
  FROM
    experience expp
  LEFT JOIN
    `king-ds-recruit-candidate-991.abtest.activity` act
  ON
    expp.playerid=act.playerid
  WHERE
    act.activity_date>= expp.assignment_date
  GROUP BY
    act.playerid)
SELECT
  expp.*,
  act.count_activity,
  act.converted_days,
  act.sum_purchase,
  act.avg_purchase,
  act.sum_gameends,
  act.avg_gameends
FROM
  experience expp
LEFT JOIN
  activity act
ON
  expp.playerid = act.playerid)
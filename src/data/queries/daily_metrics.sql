WITH
  experience AS (
  SELECT
    DISTINCT playerid,
    abtest_group
  FROM
    `abtest.assignment` AS exp )
SELECT
  DISTINCT activity_date,
  expp.abtest_group,
  COUNT(act.playerid) daily_active_player,
  SUM(CASE
      WHEN act.purchases>0 THEN 1
      ELSE 0
  END
    ) AS total_num_purhcases,
  SUM(act.purchases) AS total_revenue,
  SUM(act.gameends) AS total_game_rounds,
  SUM(CASE
      WHEN act.gameends>0 THEN 1
      ELSE 0
  END
    ) AS total_motivated_players
FROM
  experience expp
LEFT JOIN
  `king-ds-recruit-candidate-991.abtest.activity` act
ON
  expp.playerid=act.playerid
WHERE
  act.activity_date>= @study_start_date
GROUP BY
  act.activity_date,
  expp.abtest_group
ORDER BY
  act.activity_date
WITH
  experience AS (
  SELECT
    *
  FROM
    `abtest.assignment` AS exp )
SELECT
  act.playerid,
  act.activity_date,
  act.purchases,
  act.gameends,
  exp.abtest_group,
  exp.assignment_date,
  exp.install_date,
  exp.conversion_date
FROM
  `king-ds-recruit-candidate-991.abtest.activity` act
INNER JOIN
  experience exp
ON
  exp.playerid=act.playerid
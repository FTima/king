# Project Setup
## Install all python dependencies

Poetry is used for python dependency management. To install the necessary python dependencies run the following command.

```bash
poetry install
```

# Code Structure
## Notebooks
1. The experiment_statistics notebook provides an overview of the experiment, including the group sizes and its setup parameters. 
2. The experiment_daily_analysis notebook delves into the daily performance of each group, providing an overview of key metrics on a daily basis.
3. The experiment_statistical_test notebook calculates aggregated metrics and validates the differences using statistical tests.
4. The segmentation_analysis notebook provides detailed analysis for different segments of players. 
5. The experiment_validation notebook performs a sanity check to ensure the validity of the experiment.

## code source
All modules and classes have been implemented in the src package.

## Config
All constants and parameters are presented in the config file.

## Document
The "King A_B Test Use Case.pdf" document offers further explanation and interpretation of the analysis and results. 






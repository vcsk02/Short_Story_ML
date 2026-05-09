# Dataset Notes

This experiment uses a small public univariate weather time-series dataset:

- **Daily Minimum Temperatures in Melbourne**
- Source mirror: https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv
- Columns: `Date`, `Temp`
- Frequency: daily
- Task used here: next-7-day forecasting from the previous 60 days

Why this dataset is used:

- It is small enough to run quickly on a laptop.
- It has real seasonal temporal structure.
- It works well for demonstrating leakage-aware chronological splits.
- It supports a simple reproduction-style experiment without requiring a GPU.

For a stronger final submission, you may replace this dataset with ETT, Weather, Electricity, or Traffic datasets and keep the same code structure.

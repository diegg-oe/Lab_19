
Millivolts = float
Percent = float

import pandas as pd
from pathlib import Path
import numpy

FULL_MV : Millivolts = 4100
EMPTY_MV : Millivolts = 3200


def honor_pledge() -> str:
    """Return the honor pledge string."""
    return 'On our honor, we have neither given nor received any unacknowledged or unauthorized aid on this lab.'





CSV_FILE =  Path(__file__).resolve().parent.parent / "readings.csv"

TIME_GROUP = "10min"


readings = pd.read_csv(CSV_FILE)
readings = readings[(readings["milivolts"] > 3200) & (readings["milivolts"] < 4100)]
readings["timestamp"] = pd.to_datetime(readings["timestamp"])
readings = readings.sort_values("timestamp")

smoothed = readings.resample(TIME_GROUP, on="timestamp")["milivolts"].median() # mean affected by outliers
elapsed_hours = (smoothed.index - smoothed.index[0]).total_seconds() / 3600


regression_coefficients = numpy.polyfit( smoothed, elapsed_hours, 5)
print(regression_coefficients)






def estimate_battery_percent(voltage_mv: Millivolts) -> Percent:
    """Return the charge left, from 0 to 100, for a battery voltage in millivolts.

    At or above FULL_MV the charge is 100, and at or below EMPTY_MV it is 0.
    In between, estimate the percent of the run's time left before the
    battery reaches EMPTY_MV.
    """
    hours = regression_coefficients[0] * voltage_mv ** 5 + regression_coefficients[1] ** voltage_mv ** 4 + regression_coefficients[2] ** voltage_mv ** 3 + regression_coefficients[3] ** voltage_mv ** 2 + regression_coefficients[4] ** voltage_mv + regression_coefficients[5]  




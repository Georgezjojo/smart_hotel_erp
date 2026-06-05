"""
Demand prediction using a simple moving average (pure Python).
Replace with TensorFlow / scikit‑learn in the future.
"""
from datetime import datetime, timedelta

def moving_average(data, window=7):
    if not data:
        return 0
    if len(data) >= window:
        return sum(data[-window:]) / window
    return sum(data) / len(data)

def seasonal_factor(month):
    # Typical hotel demand seasonality (0.7 – 1.3)
    factors = {1:0.8, 2:0.85, 3:0.9, 4:1.0, 5:1.1, 6:1.2,
               7:1.3, 8:1.25, 9:1.0, 10:0.95, 11:0.85, 12:1.0}
    return factors.get(month, 1.0)

def predict_demand(history_occupancies, predict_date=None):
    """
    history_occupancies : list of past occupancy percentages (0-100)
    predict_date        : datetime.date (default: tomorrow)
    Returns predicted occupancy (0-100).
    """
    if predict_date is None:
        predict_date = datetime.now().date() + timedelta(days=1)
    base = moving_average(history_occupancies)
    season = seasonal_factor(predict_date.month)
    predicted = base * season
    return round(min(predicted, 100), 2)
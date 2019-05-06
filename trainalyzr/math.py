import pandas as pd


def max(series):
    max = series.max()
    return None if pd.isna(max) else max


def average(series):
    mean = series.mean()
    return None if pd.isna(mean) else mean


def variance(series):
    mean = series.mean()
    if mean != 0:
        variance = series.std() / mean
        return None if pd.isna(variance) else variance
    return None

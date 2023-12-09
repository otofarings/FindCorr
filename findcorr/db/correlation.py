from datetime import datetime, timedelta
import math

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from .models import Candles


SLIDING_WINDOW_SIZE = 365
STEP_SIZE = 7


def get_candles(secid: str, begin_dt: str, end_dt: str) -> list:
    return Candles.objects.filter(
        secid=secid, 
        begin_dt__gte=begin_dt, 
        end_dt__lte=end_dt
    )


def create_df(candles: list) -> pd.DataFrame:
    return pd.DataFrame.from_records(candles)


def get_mean_ohlc_price(candles_df: pd.DataFrame) -> pd.DataFrame:
    return candles_df[['pr_open', 'pr_close', 'pr_high', 'pr_low']].mean(axis=1)


def scale_min_max_ohlc_price(df_work: pd.DataFrame, df_train: pd.DataFrame) -> pd.DataFrame:
    tranform_columns = ['pr_open', 'pr_close', 'pr_high', 'pr_low']
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    df_work = df_work.copy()
    df_train = df_train.copy()


def calc_spreed(candles_a: pd.Series, candles_b: pd.Series) -> pd.DataFrame:
    return pd.DataFrame({
        'spread': candles_a - candles_b, 
        'candles_a': candles_a, 
        'candles_b': candles_b
    })


def calc_ohlc_corr(ohlc_a_scaled: pd.Series, ohlc_b_scaled: pd.Series) -> float:
    return round(ohlc_a_scaled.corr(ohlc_b_scaled), 4)


def get_min_dt(a_df: pd.DataFrame, b_df: pd.DataFrame) -> tuple[datetime, datetime]:
    max_dt = max(a_df["begin_dt"].max(), b_df["begin_dt"].max())
    min_dt = min(a_df["begin_dt"].min(), b_df["begin_dt"].min())

    weeks_count = math.ceil(max_dt - min_dt).days // STEP_SIZE

    start_dt = min_dt - timedelta(days=weeks_count)
    end_dt = max_dt + timedelta(days=SLIDING_WINDOW_SIZE)

    return start_dt, end_dt


def split_test_train(df_: pd.DataFrame, start_dt: datetime, end_dt: datetime) -> tuple[pd.DataFrame, pd.DataFrame]:
    mask_start_dt = df_["begin_dt"] >= start_dt
    mask_end_dt_1 = df_["begin_dt"] <= (end_dt - timedelta(days=STEP_SIZE))
    mask_end_dt_2 = df_["begin_dt"] <= end_dt

    df_train = df_[mask_start_dt & mask_end_dt_1].copy()
    df_test = df_[mask_start_dt & mask_end_dt_2].copy()

    return df_train, df_test


def calc_corr(candles_a: list, candles_b: list) -> float:
    candles_a_df = create_df(candles_a)
    candles_b_df = create_df(candles_b)

    candles_a_df["ohlc_mean"] = get_mean_ohlc_price(candles_a_df)
    candles_b_df["ohlc_mean"] = get_mean_ohlc_price(candles_b_df)

    df_a_train, df_a_test = split_test_train(candles_a_df, *get_min_dt(candles_a_df, candles_b_df))
    df_b_train, df_b_test = split_test_train(candles_b_df, *get_min_dt(candles_a_df, candles_b_df))

    df_a_train["ohlc_scaled"] = scale_min_max_ohlc_price(df_a_train)
    df_b_train["ohlc_scaled"] = scale_min_max_ohlc_price(df_b_train)

    df_a_test["ohlc_scaled"] = scale_min_max_ohlc_price(df_a_test)
    df_b_test["ohlc_scaled"] = scale_min_max_ohlc_price(df_b_test)





    # spread_scaled_df = calc_spreed(candles_a_df["ohlc_scaled"], candles_b_df["ohlc_scaled"])
    # corr = calc_ohlc_corr(spread_scaled_df["candles_a"], spread_scaled_df["candles_b"])





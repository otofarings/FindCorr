from datetime import datetime, timedelta
import math

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

from .models import Candles


def get_df_to_plot(ticker_A: str, ticker_B: str, begin_dt: str, end_dt: str) -> pd.DataFrame:
    def get_candles(secid: str) -> list:
        return Candles.objects.filter(
            secid=secid, 
            begin_dt__gte=begin_dt, 
            end_dt__lte=end_dt
        )

    def create_df(candles: list) -> pd.DataFrame:
        return pd.DataFrame({
            'secid': [candle.secid for candle in candles],
            'pr_open': [candle.pr_open for candle in candles],
            'pr_close': [candle.pr_close for candle in candles],
            'pr_high': [candle.pr_high for candle in candles],
            'pr_low': [candle.pr_low for candle in candles],
            'val': [candle.val for candle in candles],
            'vol': [candle.vol for candle in candles],
            'begin_dt': [candle.begin_dt for candle in candles],
            'end_dt': [candle.end_dt for candle in candles],
        })
    
    # Функция объединения двух датафреймов пересечением
    def df_merger(df_A_: pd.DataFrame, df_B_: pd.DataFrame) -> pd.DataFrame:
        # Переименовываем столбцы
        df_A_.rename(columns={
            'secid': 'secid_A',
            'pr_open': 'pr_open_A',
            'pr_close': 'pr_close_A',
            'pr_high': 'pr_high_A',
            'pr_low': 'pr_low_A',
            'val': 'val_A',
            'vol': 'vol_A',
            }, inplace=True)

        # Переименовываем столбцы
        df_B_.rename(columns={
            'secid': 'secid_B',
            'pr_open': 'pr_open_B',
            'pr_close': 'pr_close_B',
            'pr_high': 'pr_high_B',
            'pr_low': 'pr_low_B',
            'val': 'val_B',
            'vol': 'vol_B',
            }, inplace=True)
        
        return df_A_.merge(df_B_, how='inner', on=['begin_dt'])

    SLIDING_WINDOW_SIZE = 365
    STEP_SIZE = 7

    print('Тикер B:', ticker_B)
    print('Начальная дата:', begin_dt)
    print('Конечная дата:', end_dt)

    # Делаем запрос в БД
    df_A = create_df(get_candles(ticker_A))
    df_B = create_df(get_candles(ticker_B))

    # Склеиваем полученные датафреймы
    df_AB = df_merger(df_A, df_B)
    del df_A, df_B

    # Задаем усредненную OHLC-цену
    df_AB['OHLC_A'] = (df_AB['pr_open_A'] + df_AB['pr_close_A'] + df_AB['pr_high_A'] + df_AB['pr_low_A'])/4
    df_AB['OHLC_B'] = (df_AB['pr_open_B'] + df_AB['pr_close_B'] + df_AB['pr_high_B'] + df_AB['pr_low_B'])/4

    # Создаем пустые колонки для хранения результата
    df_AB['spread_medium'] = ''
    df_AB['OHLC_A_scaled'] = ''
    df_AB['OHLC_B_scaled'] = ''
    df_AB['spread_scaled'] = ''

    # Задаем размер скользящего окна (в днях)
    SLIDING_WINDOW_SIZE = 365

    # Задаем размер шага, на который мы будем сдвигать скользящее окно (в днях)
    STEP_SIZE = 7

    # Количество недель (включая неполные), которое прошло между началом и концом датасета
    weeks_in_dataset = math.ceil((df_AB.iloc[-1]['begin_dt'] - df_AB.iloc[0]['begin_dt'])/timedelta(weeks=1))

    # Вычисляем точку отсчета, начальную дату.
    # Для этого отмеряем в глубину датасета от его конца недели.
    start_dt = df_AB.iloc[-1]['begin_dt'] - timedelta(weeks=weeks_in_dataset)

    # Вычисляем конечную дату
    end_dt = start_dt + timedelta(days=SLIDING_WINDOW_SIZE)
    # Обучаем линейную регрессию, смещая скользящее окно
    for i in range(math.ceil(weeks_in_dataset - SLIDING_WINDOW_SIZE/STEP_SIZE)+1):

        # Наша обучающая выборка всегда короче на 1 шаг, чем полная
        train_end_dt = end_dt - timedelta(days=STEP_SIZE)

        # Нарезаем датасет с заданным шагом на куски размером со скользящее окно
        # на обучающую и плную выборку
        df_train = df_AB[(df_AB.begin_dt >= start_dt) & (df_AB.begin_dt <= train_end_dt)].copy(deep=True)
        df_work = df_AB[(df_AB.begin_dt >= start_dt) & (df_AB.begin_dt <= end_dt)].copy(deep=True)

    #--------------------------
        # Создаем колонку с масштабированной OHLC-ценой
        scaler = MinMaxScaler(feature_range=(0, 1))
        df_train['OHLC_A_scaled'] = scaler.fit_transform(df_train[['OHLC_A']])
        df_work['OHLC_A_scaled'] = scaler.transform(df_work[['OHLC_A']])
        df_train['OHLC_B_scaled'] = scaler.fit_transform(df_train[['OHLC_B']])
        df_work['OHLC_B_scaled'] = scaler.transform(df_work[['OHLC_B']])

        # Создаем колонку с масштабированным спредом
        df_train['spread_scaled'] = df_train['OHLC_B_scaled'] - df_train['OHLC_A_scaled']
        df_work['spread_scaled'] = df_work['OHLC_B_scaled'] - df_work['OHLC_A_scaled']

        # Создаем список значений X_train и y_train, но без последнего интервала
        X = np.arange(len(df_work)).reshape(-1, 1)
        X_train = np.arange(len(df_train)).reshape(-1, 1)
        y_train = df_train['spread_scaled']

        # Считаем средний спред при помощи линейной регрессии
        reg = LinearRegression().fit(X_train, y_train)
        y_pred = reg.predict(X)

        # Сохраняем результат
        df_work['spread_medium'] = y_pred

        # Обновляем значения в исходном датафрейме, записывая только последний шаг
        df_AB.loc[(df_AB.begin_dt >= train_end_dt) & (df_AB.begin_dt <= end_dt), 'spread_medium'] = df_work.loc[(df_work.begin_dt >= train_end_dt) & (df_work.begin_dt <= end_dt), 'spread_medium'].values
        df_AB.loc[(df_AB.begin_dt >= train_end_dt) & (df_AB.begin_dt <= end_dt), 'OHLC_A_scaled'] = df_work.loc[(df_work.begin_dt >= train_end_dt) & (df_work.begin_dt <= end_dt), 'OHLC_A_scaled'].values
        df_AB.loc[(df_AB.begin_dt >= train_end_dt) & (df_AB.begin_dt <= end_dt), 'OHLC_B_scaled'] = df_work.loc[(df_work.begin_dt >= train_end_dt) & (df_work.begin_dt <= end_dt), 'OHLC_B_scaled'].values
        df_AB.loc[(df_AB.begin_dt >= train_end_dt) & (df_AB.begin_dt <= end_dt), 'spread_scaled'] = df_work.loc[(df_work.begin_dt >= train_end_dt) & (df_work.begin_dt <= end_dt), 'spread_scaled'].values

    #--------------------------
        # Делаем шаг, сдвигая скользящее окно
        start_dt += timedelta(days=STEP_SIZE)
        end_dt += timedelta(days=STEP_SIZE)

    X = np.arange(len(df_AB['spread_scaled'])).reshape(-1, 1)
    y = df_AB['spread_scaled'].replace('', np.nan).dropna()

    # Считаем средний спред при помощи линейной регрессии
    reg = LinearRegression().fit(X, y)
    y_pred = reg.predict(X)

    # Сохраняем результат
    df_AB['spread_medium_line'] = y_pred


    print('Линейная регрессия рассчитана')

    # Для этого отмеряем в глубину датасета от его конца недели.
    start_dt = df_AB.iloc[-1]['begin_dt'] - timedelta(days=SLIDING_WINDOW_SIZE)

    # Вычисляем конечную дату
    end_dt = df_AB.iloc[-1]['begin_dt']

    # Сохраняем подготовленные данные
    df_for_backtest = df_AB[(df_AB.begin_dt >= start_dt) & (df_AB.begin_dt <= end_dt)]
    df_for_backtest.reset_index(drop=True, inplace=True)

    return df_for_backtest

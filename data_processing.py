from pandas import DataFrame as df
from datetime import datetime


def framed_candles(candles):
    candles_data_frame = df(candles)

    candles_data_frame_date = candles_data_frame[0]

    final_date = []

    for time in candles_data_frame_date.unique():
        readable = datetime.fromtimestamp(int(time / 1000))
        final_date.append(readable)

    shortened_candles_data_frame = candles_data_frame.iloc[:, 1:6]

    dataframe_final_date = df(final_date)

    dataframe_final_date.columns = ['Date']

    final_dataframe =\
        shortened_candles_data_frame.join(dataframe_final_date)

    final_dataframe.set_index('Date', inplace=True)
    final_dataframe.astype(float, copy=True, errors='ignore')

    final_dataframe.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    return final_dataframe

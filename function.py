from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm


def functionpredicttemperature(hours):
    df = pd.read_csv('temperature.csv', names=['value'], header=0)
    df["San Francisco"].fillna(0)

    model = pm.auto_arima(df.sanfrancisco, start_p=1, start_q=1,
                          test='adf',  # use adftest to find optimal 'd'
                          max_p=3, max_q=3,  # maximum p and q
                          m=1,  # frequency of series
                          d=None,  # let model determine 'd'
                          seasonal=False,  # No Seasonality
                          start_P=0,
                          D=0,
                          trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

    # Forecast
    n_periods = hours  # One day
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    # fc contains the forecasting for the next 24 hours.
    print(fc)
    return fc


def functionpredicthumidity( hours):
    df = pd.read_csv('humidity.csv', names=['value'], header=0)
    df["San Francisco"].fillna(0)

    model = pm.auto_arima(df.sanfrancisco, start_p=1, start_q=1,
                          test='adf',  # use adftest to find optimal 'd'
                          max_p=3, max_q=3,  # maximum p and q
                          m=1,  # frequency of series
                          d=None,  # let model determine 'd'
                          seasonal=False,  # No Seasonality
                          start_P=0,
                          D=0,
                          trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

    # Forecast
    n_periods = hours  # 2 days
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    # fc contains the forecasting for the next 24 hours.
    print(fc)
    return fc

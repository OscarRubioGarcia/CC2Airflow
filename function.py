from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
import numpy as np
import json
import datetime
import mongoconection as mongoc

def functionpredicttemperature(hours):
    #df = pd.read_csv('temperature.csv')
    df = mongoc.loaddatafrommongo()
    df["DATE"] = pd.to_datetime(df["DATE"])
    sanfrancisco = df[['DATE', 'TEMP']] 
    sanfrancisco = sanfrancisco.dropna()
    sanfrancisco = sanfrancisco.head(1000)
	
    model = pm.auto_arima(sanfrancisco["TEMP"], start_p=1, start_q=1,
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
    n_periods = hours  # X days
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    # fc contains the forecasting for the next X hours.
    return fc

def functionpredicthumidity( hours):
    df = mongoc.loaddatafrommongo()
    df["DATE"] = pd.to_datetime(df["DATE"])
    sanfrancisco = df[['DATE', 'HUM']] 
    sanfrancisco = sanfrancisco.dropna()
    sanfrancisco = sanfrancisco.head(1000)
	
    model = pm.auto_arima(sanfrancisco["HUM"], start_p=1, start_q=1,
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
    n_periods = hours  # X days
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    # fc contains the forecasting for the next X hours.
    return fc

def generateresponse( time, arrayT, arrayH):
    dt = datetime.datetime.now() + datetime.timedelta(hours=1)
    end = datetime.datetime.now() + datetime.timedelta(hours=time)
    step = datetime.timedelta(hours=1)
    
    timelist = []
    
    while dt < end:
        timelist.append(dt.strftime('%H:%M:%S'))
        dt += step

    json_string = '{ "predictions": [ '
    index = 0
    maxl = len(timelist) -1
    while index < len(timelist):
        json_string += '{ "hour": "'+ str(timelist[index])+'","temp":'+str(arrayT[index])+',"hum":'+str(arrayH[index])+' }'
        if index != maxl:
          json_string += ','
        index += 1

    json_string += '] }'
    response = json.loads(json_string)
    return json.dumps(response)

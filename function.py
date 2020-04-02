from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import json
import datetime


def functionpredicttemperature(hours):
    df = pd.read_csv('temperature.csv')
    df["datetime"] = pd.to_datetime(df["datetime"])
    sanfrancisco = df[['datetime', 'San Francisco']]
    sanfrancisco = sanfrancisco.dropna()
    sanfrancisco = sanfrancisco.head(1000)
    sanfrancisco['datetime'] = sanfrancisco['datetime'].apply(datetime_to_float)
    
    y = np.array(sanfrancisco['San Francisco'])
    X = sanfrancisco.drop('San Francisco', axis = 1)
    X = np.array(sanfrancisco)

    # 42 is to ensure same seed results
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rfmodel = RandomForestRegressor(n_estimators=100, random_state=42, max_features=1, oob_score=True)
    rfmodel = rfmodel.fit(X_train, y_train)

    predictThis = pd.DataFrame({"datetime": generateTimeRange(hours)})
    predictThis['datetime'] = pd.to_datetime(predictThis['datetime'], format='%Y-%m-%d %H:%M:%S')
    predictThis['datetime'] = predictThis['datetime'].apply(datetime_to_float)
    topredict = predictThis['datetime'].to_frame()

    pred = rfmodel.predict(X_test)
    
    return pred


def functionpredicthumidity(hours):
    df = pd.read_csv('humidity.csv')
    df["datetime"] = pd.to_datetime(df["datetime"])
    sanfrancisco = df[['datetime', 'San Francisco']]
    sanfrancisco = sanfrancisco.dropna()
    sanfrancisco = sanfrancisco.head(1000)
    sanfrancisco['datetime'] = sanfrancisco['datetime'].apply(datetime_to_float)

    y = np.array(sanfrancisco['San Francisco'])
    X = sanfrancisco.drop('San Francisco', axis = 1)
    X = np.array(sanfrancisco)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rfmodel = RandomForestRegressor(n_estimators=100, random_state=42, max_features=1, oob_score=True)
    rfmodel = rfmodel.fit(X_train, y_train)

    predictThis = pd.DataFrame({"datetime": generateTimeRange(hours)})
    predictThis['datetime'] = pd.to_datetime(predictThis['datetime'], format='%Y-%m-%d %H:%M:%S')
    predictThis['datetime'] = predictThis['datetime'].apply(datetime_to_float)
    topredict = predictThis['datetime'].to_frame()

    pred = rfmodel.predict(X_test)
    
    return pred


def datetime_to_float(d):
    return d.timestamp()

	
def generateTimeRange(time):
    dt = datetime.datetime.now() + datetime.timedelta(hours=1)
    end = datetime.datetime.now() + datetime.timedelta(hours=time)
    step = datetime.timedelta(hours=1)
    
    timelist = []
    
    while dt < end:
        timelist.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
        dt += step
    
    return timelist
	
	
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
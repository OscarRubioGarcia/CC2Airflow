from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import json
import datetime
import mongoconection as mongoc


def functionpredicttemperature(hours):
    # df = pd.read_csv('temperature.csv')
    df = mongoc.loaddatafrommongo()
    df["DATE"] = pd.to_datetime(df["DATE"])
    sanfrancisco = df[['DATE', 'TEMP']]
    sanfrancisco['TEMP'] = pd.to_numeric(df['TEMP'], errors='coerce')
    sanfrancisco = sanfrancisco.dropna()
    sanfrancisco = sanfrancisco.head(1000)
    sanfrancisco['DATE'] = sanfrancisco['DATE'].apply(datetime_to_float)

    y = np.array(sanfrancisco['TEMP'])
    X = sanfrancisco.drop('TEMP', axis=1)
    X = np.array(sanfrancisco)

    # 42 is to ensure same seed results
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rfmodel = RandomForestRegressor(n_estimators=100, random_state=42, max_features=1, oob_score=True)
    rfmodel = rfmodel.fit(X_train, y_train)

    predictThis = pd.DataFrame({"DATE": generateTimeRange(hours)})
    predictThis['DATE'] = pd.to_datetime(predictThis['DATE'], format='%Y-%m-%d %H:%M:%S')
    predictThis['DATE'] = predictThis['DATE'].apply(datetime_to_float)
    topredict = predictThis['DATE'].to_frame()

    pred = rfmodel.predict(X_test)

    return pred


def functionpredicthumidity(hours):
    df = mongoc.loaddatafrommongo()
    df["DATE"] = pd.to_datetime(df["DATE"])
    sanfrancisco = df[['DATE', 'HUM']]
    sanfrancisco['HUM'] = pd.to_numeric(df['HUM'], errors='coerce')
    sanfrancisco = sanfrancisco.dropna()
    sanfrancisco = sanfrancisco.head(1000)
    sanfrancisco['DATE'] = sanfrancisco['DATE'].apply(datetime_to_float)
    
    y = np.array(sanfrancisco['HUM'])
    X = sanfrancisco.drop('HUM', axis=1)
    X = np.array(sanfrancisco)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rfmodel = RandomForestRegressor(n_estimators=100, random_state=42, max_features=1, oob_score=True)
    rfmodel = rfmodel.fit(X_train, y_train)
    
    predictThis = pd.DataFrame({"DATE": generateTimeRange(hours)})
    predictThis['DATE'] = pd.to_datetime(predictThis['DATE'], format='%Y-%m-%d %H:%M:%S')
    predictThis['DATE'] = predictThis['DATE'].apply(datetime_to_float)
    topredict = predictThis['DATE'].to_frame()
    
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


def generateresponse(time, arrayT, arrayH):
    dt = datetime.datetime.now() + datetime.timedelta(hours=1)
    end = datetime.datetime.now() + datetime.timedelta(hours=time)
    step = datetime.timedelta(hours=1)

    timelist = []

    while dt < end:
        timelist.append(dt.strftime('%H:%M:%S'))
        dt += step

    json_string = '{ "predictions": [ '
    index = 0
    maxl = len(timelist) - 1
    while index < len(timelist):
        json_string += '{ "hour": "' + str(timelist[index]) + '","temp":' + str(arrayT[index]) + ',"hum":' + str(
            arrayH[index]) + ' }'
        if index != maxl:
            json_string += ','
        index += 1

    json_string += '] }'
    response = json.loads(json_string)
    return json.dumps(response)
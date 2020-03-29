from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm


def functionpredicttemperature(hours):
    df = pd.read_csv('temperature.csv', names=['value'], header=0)
    df["San Francisco"].fillna(-999)

    y = np.array(df['TEMP'])
    df = df.drop('TEMP', axis=1)
    lb_list = list(df.columns)
    X = np.array(df)

    # 42 is to ensure same seed results
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rfmodel = RandomForestRegressor(n_estimators=100, random_state=42)
    rfmodel.fit(X_train, y_train)

    n_periods = hours  # X days
    predictThis = {"2020-10-01 12:00:00", "2020-10-01 13:00:00", "2020-10-01 14:00:00", "2020-10-01 15:00:00",
               "2012-10-01 16:00:00"}
    pred = rfmodel.predict(predictThis)

    print("The prediction is")
    return pred


def functionpredicthumidity(hours):
    df = pd.read_csv('humidity.csv', names=['value'], header=0)
    df["San Francisco"].fillna(-999)

    y = np.array(df['HUM'])
    df = df.drop('HUM', axis=1)
    lb_list = list(df.columns)
    X = np.array(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rfmodel = RandomForestRegressor(n_estimators=100, random_state=42)
    rfmodel.fit(X_train, y_train)

    n_periods = hours  # X days
    predictThis = {"2020-10-01 12:00:00", "2020-10-01 13:00:00", "2020-10-01 14:00:00", "2020-10-01 15:00:00",
               "2012-10-01 16:00:00"}

    pred = rfmodel.predict(predictThis)

    print("The predction is")
    return pred

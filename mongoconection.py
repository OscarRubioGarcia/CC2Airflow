from pymongo import MongoClient
import pandas as pd


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# debugWindows = 192.168.99.100, release = localhost, virtualMachine = mongodb
def loaddatafrommongo():
    client = MongoClient("mongodb://mongodb:27017")

    db = client.test
    collection = db['Output']

    cursor = collection.find({}, {'_id': False})
    df = pd.DataFrame(list(cursor))
    df = df.drop(labels='field3', axis=1)

    return df
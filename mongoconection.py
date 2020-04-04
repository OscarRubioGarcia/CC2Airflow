from pymongo import MongoClient
import pandas as pd


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# debug = 192.168.99.100, release = localhost
def loaddatafrommongo():
    client = MongoClient("mongodb://localhost:27017")

    db = client.test
    collection = db['Output']

    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    del df['_id']
    df = df.drop(labels='field3', axis=1)

    return df
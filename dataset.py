import pandas as pd
import pymongo as pymongo
from pymongo import MongoClient


def create_dataset_top10(date):
    query = create_query(date)
    data_cols = {"id": 1, "hour": 1, "aerial": 1, "terrain": 1, "man": 1, "district": 1, "concelho": 1,
                 "familiaName": 1, "natureza": 1,
                 "especieName": 1, "status": 1}
    client = MongoClient()
    db = client.vost
    df = pd.DataFrame(list(db.data.find(query, data_cols).sort("created", pymongo.DESCENDING).limit(10)))
    # Change the DType of id to a integer
    df["id"] = df["id"].astype(int)
    # Remove Duplicates if any
    df.drop_duplicates(subset=['id'], inplace=True, keep='last')
    # Create new columns that sums the values of resources for each event
    df['total_meios'] = df['man'] + df['terrain'] + df['aerial']
    return df


def create_query(date):
    if date is None:
        return None
    else:
        return {"date": date}
#!/usr/bin/env python

import os
import requests
import pandas as pd
DATABRICKS_TOKEN = "dapi749bafa84bc0f269de2624e8a6df084b-3"

my_data = [
  {
    "tweet": "@Gladvillian_ dont get that bacon stuffed crust tho its trash"
  },
  {
    "tweet": "suck"
  },
  {
    "tweet": "@user #goodmorning and thanks for the follow. have a   #monday &amp; a good week."
  },
  {
    "tweet": "Y'all trying to use The Lord to sell pussy on this corner... I already know!"
  },
  {
    "tweet": "noooo wtfffff pouseeey died #oitnbspoiler #oitnb #orangeisthenewblack   suprised #omg"
  }
]
df = pd.DataFrame(data=my_data)


def create_tf_serving_json(data):
    return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

def score_model(dataset):
    url = 'https://adb-4167085237468301.1.azuredatabricks.net/model/toxic_best_accuracy/1/invocations'
    headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}'}
    data_json = dataset.to_dict(orient='split') if isinstance(dataset, pd.DataFrame) else create_tf_serving_json(dataset)
    response = requests.request(method='POST', headers=headers, url=url, json=data_json)
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()


if __name__ == "__main__":
    print(score_model(df))

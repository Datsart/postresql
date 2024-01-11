import pandas as pd
import json
import requests


def get_info(hash_id):
    df = pd.read_csv('result.csv')
    result_info = df.loc[df['hash'] == hash_id]

    data = {
        'hash': hash_id,
        f'{result_info["feature"].iloc[0]}': result_info['value'].iloc[0],
        f'{result_info["feature"].iloc[1]}': result_info['value'].iloc[1],
        f'{result_info["feature"].iloc[2]}': result_info['value'].iloc[2],
        f'{result_info["feature"].iloc[3]}': result_info['value'].iloc[3],
        f'{result_info["feature"].iloc[4]}': result_info['value'].iloc[4],
        'datetime': result_info['datetime'].iloc[0]
    }
    res_json = json.dumps(data, ensure_ascii=False, indent=2)
    print(res_json)
    return res_json


def get_response_stat(hash_id):
    url = "http://127.0.0.1:5050/get_stat"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = get_info(hash_id)

    response = requests.post(url, json=payload, headers=headers)
    return f'{response.json()}'


hash_id = '0c476f060ddc927f5145b0b4a5ff7fa9'
# print(get_response_stat(hash_id))

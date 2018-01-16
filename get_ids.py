import os
import json
import click
import requests

VERSION = '20170801'
SEARCH_FOR_VENUE_URL = 'https://api.foursquare.com/v2/venues/search'

def get_venue_id(search_parameter):
    # foursquareのAPIを叩いて指定した条件でvenueIDをとってくる
    search_for_venue_parameters = {'v': VERSION}
    for search_parameter_key in search_parameter:
        search_for_venue_parameters[search_parameter_key] = search_parameter[search_parameter_key]

    # idの取得前に取得条件を表示し、確認する
    search_for_venue_response = requests.get(url=SEARCH_FOR_VENUE_URL, params=search_for_venue_parameters)
    venue_data_json = json.loads(search_for_venue_response.text)
    if 'errorType' in venue_data_json['meta']:
        raise Exception('spam', 'eggs')
    venue_data = venue_data_json['response']['venues']
    #下限よりも多くのtipsがあるvenueのIDを抽出
    venue_ids = {}
    for venue in venue_data:
        venue_ids[venue['name']] = venue['id']
    return venue_ids, search_for_venue_response.text

# idの保存
def save_ids_json(ids, path):
    ids_json = json.dumps(ids, sort_keys=True, ensure_ascii=False, indent=2)
    with open(path, 'w') as fh:
        fh.write(ids_json)

def print_ids_json(ids):
    if not ids:
        return

    ids_json = json.dumps(ids, sort_keys=True, ensure_ascii=False, indent=2)
    print(ids_json)
    return

if __name__ == '__main__':
    main()

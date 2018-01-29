import os
import sys
import json
import random
import requests

VERSION = '20170801'

def get_venues_tips(venue_id):
    # venueidをと結合するためurlを分ける
    first_get_venues_tips_url = 'https://api.foursquare.com/v2/venues/'
    second_get_venues_tips_url = '/tips'

    # 各venueidをapiurlと結合してAPIのget_venue_tipsを叩く
    # 帰ってきたデータを保存する
    get_venues_tips_url = ( first_get_venues_tips_url
                          + venue_id
                          + second_get_venues_tips_url)

    get_venues_tips_params = {'v': VERSION,
                              "client_id": os.environ['FOURSQUARE_CLIENT_ID'],
                              "client_secret": os.environ['FOURSQUARE_CLIENT_SECRET'],
                              'limit': 500}

    get_venues_tips_response = requests.get(url=get_venues_tips_url, params=get_venues_tips_params)
    venue_tips_data = json.loads(get_venues_tips_response.text)

    if 'errorType' in venue_tips_data['meta']:
        raise Exception(venue_tips_data['meta']['errorType'])

    venue_tips_data_dict = {}
    venue_tips_data_dict[second_get_venues_tips_url] = venue_tips_data['response']

    # 各venue_idのtipsをまとめて保管する
    tips = {}
    for venue_id in venue_tips_data_dict:
        one_venue_tips = []
        one_venue_info = {}
        for tips_items_data in venue_tips_data_dict[venue_id]['tips']['items']:
            one_venue_tips += [tips_items_data['text']]
        one_venue_info['tips'] = one_venue_tips
        one_venue_info['count'] = venue_tips_data_dict[venue_id]['tips']['count']
        tips[venue_id] = one_venue_info

    return tips, get_venues_tips_response.text

def save_tips_json(tips, path):
    tips_json = json.dumps(tips, sort_keys=True, ensure_ascii=False, indent=2)
    with open(path, "w") as fh:
        fh.write(tips_json)

def fill_missing_value(search_parameters):
    parameter_keys = ['ll','near','intent','radius', 'sw',
                  'ne', 'query', 'limit', 'categoryId',
                  'llAcc', 'alt', 'altAcc', 'url', 'providerId', 'linkedId']

    for parameter_key in parameter_keys:
        if parameter_key not in search_parameters:
            search_parameters[parameter_key] = None

    return search_parameters
"""
def main():

    # venue検索条件ファイルの取得
    if len(sys.argv) != 2:
        print("検索パラメータくれ")
        return
    search_parameters_file_name = sys.argv[1]

    with open(search_parameters_file_name, 'r') as f:
        search_parameters = json.load(f)

    with open("id.json", 'r') as f:
        token = json.load(f)

    for search_name in search_parameters:
        search_parameters[search_name] = fill_missing_value(search_parameters[search_name])

        # parameterにclientIdとsecretIdを追加
        for key in token:
            search_parameters[search_name][key] = token[key]

        # venue_idの取得
        tips_num_lower_limit = 10
        venue_ids = get_venue_id(search_parameters[search_name],tips_num_lower_limit)
        if not venue_ids:
            continue
        # 取得したvenue_idからtipsを取得
        tips = get_venues_tips(venue_ids, token)

        # 取得してきたtipsの保存先
        path = 'tips/tips_ja/' + search_name + '_tips.json'
        save_tips_json(tips, path)
"""
if __name__ == "__main__":
    main()

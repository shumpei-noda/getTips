import sys
import json
import random
import requests

CLIENT_ID = 'NQY52G1UBPKOQVRR0FOAGZGD55UJCDOKFGOCGGBHUAN5DV5S'
CLIENT_SEACRET = 'CV5QHUMNXUFGFDSRNJ4STH3KBV5G0IVQNKTMXDQTTC23AEY2'
VERSION = '20170801'
RADIUS = '800'

def get_venue_id(search_parameters, tips_num_lower_limit):
    # foursquareのAPIを叩いて指定した条件でvenueIDをとってくる
    search_for_venue_url = 'https://api.foursquare.com/v2/venues/search'
    search_for_venue_parameters = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SEACRET,
        'v': VERSION,
    }
    for search_parameter_key in search_parameters:
        search_for_venue_parameters[search_parameter_key] = search_parameters[search_parameter_key]

    search_for_venue_response = requests.get(url=search_for_venue_url, params=search_for_venue_parameters)
    venue_data = json.loads(search_for_venue_response.text)['response']['venues']

    #下限よりも多くのtipsがあるvenueのIDを抽出
    venue_ids = []
    for venue in venue_data:
        if venue['stats']['tipCount'] > tips_num_lower_limit:
            venue_ids += [venue['id']]

    return venue_ids

def get_venues_tips(venue_ids):
    # venueidをと結合するためurlを分ける
    first_get_venues_tips_url = 'https://api.foursquare.com/v2/venues/'
    third_get_venues_tips_url = '/tips'

    # 各venueidをapiurlと結合してAPIのget_venue_tipsを叩く
    # 帰ってきたデータを保存する
    venue_tips_data_dict = {}
    for second_get_venues_tips_url in venue_ids:
        get_venues_tips_url = (  first_get_venues_tips_url
                               + second_get_venues_tips_url
                               + third_get_venues_tips_url)
        get_venues_tips_params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SEACRET,
            'v': VERSION,
        }
        get_venues_tips_response = requests.get(url=get_venues_tips_url, params=get_venues_tips_params)
        venue_tips_data = json.loads(get_venues_tips_response.text)
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

    return tips

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

def main():

    # venue検索条件ファイルの取得
    if len(sys.argv) != 2:
        return
    search_parameters_file_name = sys.argv[1]
    with open(search_parameters_file_name, 'r') as f:
        search_parameters = json.load(f)

    for search_name in search_parameters:
        search_parameters[search_name] = fill_missing_value(search_parameters[search_name])
        # venue_idの取得
        tips_num_lower_limit = 10
        venue_ids = get_venue_id(search_parameters[search_name],tips_num_lower_limit)

        tips = get_venues_tips(venue_ids)

        # 取得してきたtipsの保存先
        path = 'tips/tips_ja/' + search_name + '_tips.json'
        save_tips_json(tips, path)
    print(tips)
if __name__ == "__main__":
    main()

import sys
import json
import requests

VERSION = '20170801'

def get_venue_id(search_parameters, tips_num_lower_limit):
    # foursquareのAPIを叩いて指定した条件でvenueIDをとってくる
    search_for_venue_url = 'https://api.foursquare.com/v2/venues/search'
    search_for_venue_parameters = {'v': VERSION}
    for search_parameter_key in search_parameters:
        search_for_venue_parameters[search_parameter_key] = search_parameters[search_parameter_key]

    # idの取得前に取得条件を表示し、確認する
    unuse_key = ['client_secret', 'client_id', 'v']
    for key in search_for_venue_parameters:
        if key in unuse_key or search_for_venue_parameters[key] == None:
            continue
        print(key, ":", search_for_venue_parameters[key])
    print("?(y/n)")

    ans = input()
    if ans != 'y':
        return

    search_for_venue_response = requests.get(url=search_for_venue_url, params=search_for_venue_parameters)
    venue_data_json = json.loads(search_for_venue_response.text)
    if 'errorType' in venue_data_json['meta']:
        print("error: " + venue_data_json['meta']['errorDetail'])
        return
    venue_data = venue_data_json['response']['venues']

    #下限よりも多くのtipsがあるvenueのIDを抽出
    venue_ids = {}
    for venue in venue_data:
        venue_ids[venue['name']] = venue['id']

    return venue_ids

# 欠損値の補完
def fill_missing_value(search_parameters):
    parameter_keys = ['ll','near','intent','radius', 'sw',
                  'ne', 'query', 'limit', 'categoryId',
                  'llAcc', 'alt', 'altAcc', 'url', 'providerId', 'linkedId']

    for parameter_key in parameter_keys:
        if parameter_key not in search_parameters:
            search_parameters[parameter_key] = None

    return search_parameters

# idの保存
def save_ids_json(ids, path):
    ids_json = json.dumps(ids, sort_keys=True, ensure_ascii=False, indent=2)
    with open(path, "w") as fh:
        fh.write(ids_json)

def main():
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
        search_parameters[search_name]['ll'] = "35.680910,139.767025"
        # parameterにclientIdとsecretIdを追加
        for key in token:
            search_parameters[search_name][key] = token[key]

        tips_num_lower_limit = 10
        ids = get_venue_id(search_parameters[search_name],tips_num_lower_limit)

        path = "./ids/" + search_name + ".json"
        save_ids_json(ids, path)


if __name__ == '__main__':
    main()

import click
import json
import requests

VERSION = '20170801'

def get_venue_id(search_parameter, tips_num_lower_limit):
    # foursquareのAPIを叩いて指定した条件でvenueIDをとってくる
    search_for_venue_url = 'https://api.foursquare.com/v2/venues/search'
    search_for_venue_parameters = {'v': VERSION}
    for search_parameter_key in search_parameter:
        search_for_venue_parameters[search_parameter_key] = search_parameter[search_parameter_key]

    # idの取得前に取得条件を表示し、確認する
    unuse_key = ['client_secret', 'client_id', 'v']
    for key in search_for_venue_parameters:
        if key in unuse_key or search_for_venue_parameters[key] == None:
            continue
        print(key, ":", search_for_venue_parameters[key])

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

# idの保存
def save_ids_json(ids, path):
    ids_json = json.dumps(ids, sort_keys=True, ensure_ascii=False, indent=2)
    with open(path, "w") as fh:
        fh.write(ids_json)

def print_ids_json(ids):
    if not ids:
        return

    ids_json = json.dumps(ids, sort_keys=True, ensure_ascii=False, indent=2)
    print(ids_json)
    return

@click.command()
@click.argument('parameters_file', type=click.File('r'))
@click.argument('id_file', type=click.File('r'))
def main(parameters_file, id_file):

    search_parameter = json.load(parameters_file)
    token = json.load(id_file)

    ids_list = []

    for search_parameter in search_parameter:
        # parameterにclientIdとsecretIdを追加
        for key in token:
            search_parameter[key] = token[key]

        tips_num_lower_limit = 10
        ids = get_venue_id(search_parameter,tips_num_lower_limit)

        if ids:
            ids_list += [ids]

    print_ids_json(ids_list)

if __name__ == '__main__':
    main()

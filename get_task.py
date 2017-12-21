import os
import json
import requests_table
import locations_table
import venues_table

from time import sleep
from get_ids import get_venue_id

def fetch(row):
    parameters = {'categoryId': "4d4b7105d754a06374d81259",
                  "intent": "browse",
                  "limit": "50",
                  "ll": str(row['north_latitude']) + "," + str(row['east_longitude']),
                  "ne": str(row['north_latitude']) + "," + str(row['east_longitude']),
                  "sw": str(row['south_latitude']) + "," + str(row['west_longitude']),
                  "client_id": os.environ['FOURSQUARE_CLIENT_ID'],
                  "client_secret": os.environ['FOURSQUARE_CLIENT_SECRET']}
    requests_table.update_status(row['locations.id'], 1)
    venue_ids = None
    try:
        venue_ids, raw_data = get_venue_id(parameters)
    except Exception as inst:
        print(inst)
        requests_table.update_status(row['locations.id'], 3)
        return

    if venue_ids == "err":
        requests_table.update_status(row['locations.id'], 3)
    else:
        requests_table.update_status(row['locations.id'], 2)

    json_data = json.loads(raw_data)

    for data in json_data['response']['venues']:
        venues_table.insert(name=data['name'],
                            venue_id=data['id'],
                            raw_data=json.dumps(data, sort_keys=True, ensure_ascii=False)
                           )

def main():
    rows = requests_table.get_waiting_task()
    for row in rows:
        fetch(row)
        sleep(4)

if __name__ == "__main__":
    while True:
        main()

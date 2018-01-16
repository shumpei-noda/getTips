import requests_table
import locations_table

from time import sleep

N_INSERT = 5
WAIT_STATUS = 0

# locationsテーブルに保存されている情報から、venueをある一定間隔で取得して保存をする
def main():
    # 最後に保存したlocation情報のidがわからないのでrequestsテーブルから取得
    requests_rows = requests_table.get()
    last_id = 0
    if len(requests_rows) == 0:
        last_id = 0
    else:
        last_id = requests_rows[-1]['location_id']

    # locationsテーブルから取得した情報をrequestsテーブルに保存する
    locations_rows = locations_table.get()
    for i in range(N_INSERT):
        current_id = last_id + i
        if len(locations_rows) <= current_id:
            return
        else:
            location_id = locations_rows[current_id]['id'];

        requests_table.insert(location_id=location_id, status_code=WAIT_STATUS)

# 5秒間隔でlocationテーブルからrequestsテーブルにリクエストを入れる
if __name__ == "__main__":
    while True:
        main()
        sleep(5)

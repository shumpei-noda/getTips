import os
import re
import json
import venues_table
import tips_requests_table
import tips_table

from time import sleep
from get_tips import get_venues_tips

WAIT_STATUS = 0
RUNNNING_STATUS = 1
DONE_STATUS = 2
ERROR_STATUS = 3

def fetch(row):
    # 取得してくる前にステータスを取得中(1)に変更
    tips_requests_table.update_status(row['venues.id'], 1)
    tips_requests_table.commit()
    venue_ids = None
    # エラーが返ってきた場合、このlocation情報のrequestsテーブルのステータスをエラー(3)にする
    try:
        tips, raw_data = get_venues_tips(row['venues.venue_id'])
    except Exception as inst:
        tips_requests_table.update_status(row['venues.id'], 3)
        raise Exception(inst)

    # venue情報の取得ができたので、取得完了(2)にステータスを更新する
    tips_requests_table.update_status(row['venues.id'], 2)

    # tipsの個数が0であった場合終了
    if tips == row['tip_count']:
        return

    # 取得してきたvenue情報をvenuesテーブルに生データで保存する
    json_data = json.loads(raw_data)
    for data in json_data['response']['tips']['items']:
        try:
            tips_table.insert(venue_id=row['venues.id'],
                              tip=data['text'],
                              raw_data=json.dumps(data, sort_keys=True, ensure_ascii=False)
                             )
        except Exception as inst:
            tips_requests_table.update_status(row['venues.id'], 3)
            return
    return

# 取得待ちlocation情報を取得し、venue情報を取得する
def main():
    tips_requests_table.begin_transaction()
    row = tips_requests_table.get_waiting_task()
    fetch(row)
    sleep(8)

if __name__ == "__main__":
    while True:
        main()

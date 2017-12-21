import requests_table
import locations_table

from time import sleep

N_INSERT = 5
STATUS_WAIT = 0

def main():
    requests_rows = requests_table.get()
    last_id = 0
    if len(requests_rows) == 0:
        last_id = 0
    else:
        last_id = requests_rows[-1]['location_id']

    locations_rows = locations_table.get()

    for i in range(N_INSERT):
        current_id = last_id + i
        if len(locations_rows) <= current_id:
            return
        else:
            location_id = locations_rows[current_id]['id'];

        requests_table.insert(location_id=location_id, status_code=STATUS_WAIT)

if __name__ == "__main__":

    while True:
        main()
        sleep(5)

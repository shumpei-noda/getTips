import tips_requests_table
import venues_table

from time import sleep


N_INSERT = 5
WAIT_STATUS = 0

def main():
    tips_rows = tips_requests_table.get()
    last_id = 0
    if len(tips_rows) == 0:
        last_id = 0
    else:
        last_id = tips_rows[-1]['venue_id']


    venues_rows = venues_table.get()
    for i in range(N_INSERT):
        current_id = last_id + i
        if len(venues_rows) <= current_id:
            return
        else:
            venue_id = venues_rows[current_id]['id']

        tips_requests_table.insert(venue_id=venue_id, status_code=WAIT_STATUS)

if __name__ == "__main__":
    while True:
        main()
        sleep(5)

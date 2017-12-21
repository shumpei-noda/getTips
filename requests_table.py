import datetime

from orator import DatabaseManager

config = {
    'mysql': {
        'driver': 'mysql',
        'host': '127.0.0.1',
        'database': 'tips',
        'user': 'root',
        'password': 'password',
        'prefix': '',
        'port': 3307
    }
}
db = DatabaseManager(config)

def insert(location_id, status_code):
    if db.table('requests').where('location_id',location_id).get():
        update_status(location_id, status_code)
    else:
        db.table('requests').insert({'location_id': location_id,
                                     'status': status_code,
                                     'created_at': datetime.datetime.today(),
                                     'updated_at': datetime.datetime.today()
                                    })

def get():
    rows = db.table('requests').get()
    return rows

def get_join_locations():
    rows = db.table('requests').join('locations', 'requests.location_id', '=', 'locations.id').get()
    return rows

def get_waiting_task():
    rows = db.table('requests').where('status', '=', '0').join('locations', 'requests.location_id', '=', 'locations.id').get()
    return rows

def update_status(location_id, status_code):
    db.table('requests').where('location_id', location_id).update({'status': status_code,
                                                                  'updated_at': datetime.datetime.today()
                                                                 })

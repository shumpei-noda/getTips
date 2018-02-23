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

def insert(venue_id, status_code):
    if db.table('tips_requests').where('venue_id', venue_id).get():
        update_status(venue_id, status_code)
    else:
        db.table('tips_requests').insert({'venue_id': venue_id,
                                          'status': status_code,
                                          'created_at': datetime.datetime.today(),
                                          'updated_at': datetime.datetime.today()
                                         })

def get():
    rows = db.table('tips_requests').get()
    return rows

def get_join_venues():
    rows = db.table('tips_requests').join('venues', 'tips_requests.venue_id', '=', 'venues.id').get()
    return rows

def get_waiting_tasks():
    rows = db.table('tips_requests').where('status', '=', '0').join('venues', 'tips_requests.venue_id', '=', 'venues.id').lock_for_update().get()
    return rows

def get_waiting_task():
    row = db.table('tips_requests').where('status', '=', '0').join('venues', 'tips_requests.venue_id', '=', 'venues.id').lock_for_update().first()
    return row

def update_status(venue_id, status_code):
    db.table('tips_requests').where('venue_id', venue_id).update({'status': status_code,
                                                                  'updated_at': datetime.datetime.today()
                                                                 })
def begin_transaction():
    db.begin_transaction()

def rollback():
    db.rollback()

def commit():
    db.commit()

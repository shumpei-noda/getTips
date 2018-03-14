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

table_name = 'tips_requests2'

def insert(venue_id, status_code):
    if db.table(table_name).where('venue_id', venue_id).get():
        update_status(venue_id, status_code)
    else:
        db.table(table_name).insert({'venue_id': venue_id,
                                          'status': status_code,
                                          'created_at': datetime.datetime.today(),
                                          'updated_at': datetime.datetime.today()
                                         })

def get():
    rows = db.table(table_name).get()
    return rows

def get_join_venues():
    rows = db.table(table_name).join('venues', table_name+'.venue_id', '=', 'venues.id').get()
    return rows

def get_waiting_tasks():
    rows = db.table(table_name).where('status', '=', '0').join('venues', table_name+'.venue_id', '=', 'venues.id').lock_for_update().get()
    return rows

def get_waiting_task():
    row = db.table(table_name).where('status', '=', '0').join('venues', table_name+'.venue_id', '=', 'venues.id').where('tip_count', '!=', '0').lock_for_update().first()
    return row

def update_status(venue_id, status_code):
    db.table(table_name).where('venue_id', venue_id).update({'status': status_code,
                                                                  'updated_at': datetime.datetime.today()
                                                                 })
def begin_transaction():
    db.begin_transaction()

def rollback():
    db.rollback()

def commit():
    db.commit()

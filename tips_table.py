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
        'charset': 'utf8mb4',
        'port': 3307
    }
}
db = DatabaseManager(config)

def insert(venue_id, tip, raw_data):
    db.table('tips').insert({'venue_id': venue_id,
                             'tip': tip,
                             'raw_data': raw_data,
                             'created_at': datetime.datetime.today(),
                             'updated_at': datetime.datetime.today()
                            })

def get():
    rows = db.table('venues').get()
    return rows

def begin_transaction():
    db.begin_transaction()

def rollback():
    db.rollback()

def commit():
    db.commit()

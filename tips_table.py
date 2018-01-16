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

def insert(name, venue_id, raw_data):
    if db.table('tips').where('name', name).get():
        db.table('tips').where('name', name).update({'venue_id': venue_id,
                                                     'raw_data': raw_data,
                                                     'updated_at': datetime.datetime.today()
                                                    })
    else:
        db.table('tips').insert({'name': name,
                                 'venue_id': venue_id,
                                 'raw_data': raw_data,
                                 'created_at': datetime.datetime.today(),
                                 'updated_at': datetime.datetime.today()
                                 })

def get():
    rows = db.table('venues').get()
    return rows

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

def insert(name, venue_id, tip_count, raw_data):
    if db.table('venues').where('name',name).get():
        db.table('venues').where('name', name).update({'venue_id': venue_id,
                                                       'tip_count': tip_count,
                                                       'raw_data': raw_data,
                                                       'updated_at': datetime.datetime.today()
                                                      })
    else:
        db.table('venues').insert({'name': name,
                                   'venue_id': venue_id,
                                   'tip_count': tip_count,
                                   'raw_data': raw_data,
                                   'created_at': datetime.datetime.today(),
                                   'updated_at': datetime.datetime.today()
                                  })

def get():
    rows = db.table('venues').get()
    return rows

def get_tip_count_null():
    return db.table('venues').where_null('tip_count').get()

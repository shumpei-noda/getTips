import json
import click
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
def insert(name, north_latitude, south_latitude, east_longitude, west_longitude):
    if db.table('locations').where('name',name).get():
        db.table('locations').where('name',name).update({'north_latitude': north_latitude,
                                                         'south_latitude': south_latitude,
                                                         'east_longitude': east_longitude,
                                                         'west_longitude': west_longitude,
                                                         'updated_at': datetime.datetime.today()
                                                        })
    else:
        db.table('locations').insert({'name': name,
                                      'north_latitude': north_latitude,
                                      'south_latitude': south_latitude,
                                      'east_longitude': east_longitude,
                                      'west_longitude': west_longitude,
                                      'created_at': datetime.datetime.today(),
                                      'updated_at': datetime.datetime.today()
                                     })

def get():
    rows = db.table('locations').get()
    return rows

def show():
    rows = get_locations()
    for row in rows:
        print("id:", row['id'])
        print("name:", row['name'])
        print("north_latitude:", row['north_latitude'])
        print("south_latitude:", row['south_latitude'])
        print("east_longitude:", row['east_longitude'])
        print("west_longitude:", row['west_longitude'])
        print("created_at:", row['created_at'])
        print("updated_at:", row['updated_at'])

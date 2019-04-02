import sqlite3
import json

db = 'data/RH/rh.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
csr = conn.cursor()

update_list = []

f = open('data/RH/nad27.geojson', 'r')
geojson = json.load(f)
features = geojson['features']
for feature in features:
    new_coord = feature['geometry']['coordinates']
    old_info = feature['properties']
    update_element = (new_coord[0], new_coord[1], old_info['Latitude'], old_info['Longitude'])
    update_list.append(update_element)
f.close()

csr.executemany("UPDATE `f_RH_Monthly` SET `Longitude` = ?, `Latitude` = ?, `Datum` = 'WGS84' WHERE `Latitude` = ? AND `Longitude` = ?;", update_list)
conn.commit()
conn.close()

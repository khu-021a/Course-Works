import sqlite3

db = 'data/Aerosol/haze.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
csr = conn.cursor()

dup_list = []

for row in csr.execute('SELECT `SiteCode`, `Date` FROM (SELECT `SiteCode`, `Date`, COUNT(*) num FROM `HazeCal` GROUP BY `SiteCode`, `Date`) WHERE num > 1;'):
    dup_list.append((row['SiteCode'], row['Date']))

sample_list = ['AmmSO4', 'AmmNO3', 'Soil', 'OC', 'LAC', 'CM', 'SeaSalt']
aux_list = ['SiteCode', 'Date', 'SiteName', 'Latitude', 'Longitude', 'Elevation', 'State', 'CountyFIPS', 'EPACode', 'Unit']
new_row_list = []
for dup_row in dup_list:
    sums = {n: 0 for n in sample_list}
    counts = {n: 0 for n in sample_list}
    aux_info = {n: 0 for n in aux_list}
    #`SiteCode`, `Date`, `SiteName`, `Latitude`, `Longitude`, `Elevation`, `State`, `CountyFIPS`, `EPACode`, `Unit`
    for row in csr.execute('SELECT * FROM `HazeCal` WHERE `SiteCode` = ? AND `Date` = ?;', dup_row):
        aux_info['SiteName'] = row['SiteName']
        aux_info['Latitude'] = row['Latitude']
        aux_info['Longitude'] = row['Longitude']
        aux_info['Elevation'] = row['Elevation']
        aux_info['State'] = row['State']
        aux_info['CountyFIPS'] = row['CountyFIPS']
        aux_info['EPACode'] = row['EPACode']
        aux_info['Unit'] = row['Unit']
        if row['AmmSO4_Status'] == 'V0':
            sums['AmmSO4'] += row['AmmSO4_Value']
            counts['AmmSO4'] += 1

        if row['AmmNO3_Status'] == 'V0':
            sums['AmmNO3'] += row['AmmNO3_Value']
            counts['AmmNO3'] += 1

        if row['Soil_Status'] == 'V0':
            sums['Soil'] += row['Soil_Value']
            counts['Soil'] += 1

        if row['OC_Status'] == 'V0':
            sums['OC'] += row['OC_Value']
            counts['OC'] += 1

        if row['LAC_Status'] == 'V0':
            sums['LAC'] += row['LAC_Value']
            counts['LAC'] += 1

        if row['CM_Status'] == 'V0':
            sums['CM'] += row['CM_Value']
            counts['CM'] += 1

        if row['SeaSalt_Status'] == 'V0':
            sums['SeaSalt'] += row['SeaSalt_Value']
            counts['SeaSalt'] += 1

    if counts['AmmSO4'] == 0:
        amm_so4_status = 'M1'
        amm_so4_value = -999
    else:
        amm_so4_status = 'V0'
        amm_so4_value = sums['AmmSO4'] / counts['AmmSO4']

    if counts['AmmNO3'] == 0:
        amm_no3_status = 'M1'
        amm_no3_value = -999
    else:
        amm_no3_status = 'V0'
        amm_no3_value = sums['AmmNO3'] / counts['AmmNO3']

    if counts['Soil'] == 0:
        soil_status = 'M1'
        soil_value = -999
    else:
        soil_status = 'V0'
        soil_value = sums['Soil'] / counts['Soil']

    if counts['OC'] == 0:
        oc_status = 'M1'
        oc_value = -999
    else:
        oc_status = 'V0'
        oc_value = sums['OC'] / counts['OC']

    if counts['LAC'] == 0:
        lac_status = 'M1'
        lac_value = -999
    else:
        lac_status = 'V0'
        lac_value = sums['LAC'] / counts['LAC']

    if counts['CM'] == 0:
        cm_status = 'M1'
        cm_value = -999
    else:
        cm_status = 'V0'
        cm_value = sums['CM'] / counts['CM']

    if counts['SeaSalt'] == 0:
        sea_salt_status = 'M1'
        sea_salt_value = -999
    else:
        sea_salt_status = 'V0'
        sea_salt_value = sums['SeaSalt'] / counts['SeaSalt']

    new_row_list.append((dup_row[0], dup_row[1], aux_info['SiteName'], aux_info['Latitude'], aux_info['Longitude'], aux_info['Elevation'], aux_info['State'], aux_info['CountyFIPS'], aux_info['EPACode'], aux_info['Unit'], amm_so4_value, amm_so4_status, amm_no3_value, amm_no3_status, soil_value, soil_status, oc_value, oc_status, lac_value, lac_status, cm_value, cm_status, sea_salt_value, sea_salt_status))

csr.executemany('DELETE FROM `HazeCal` WHERE `SiteCode` = ? AND `Date` = ?;', dup_list)
csr.executemany('INSERT INTO `HazeCal` (`SiteCode`, `Date`, `SiteName`, `Latitude`, `Longitude`, `Elevation`, `State`, `CountyFIPS`, `EPACode`, `Unit`, `AmmSO4_Value`, `AmmSO4_Status`, `AmmNO3_Value`, `AmmNO3_Status`, `Soil_Value`, `Soil_Status`, `OC_Value`, `OC_Status`, `LAC_Value`, `LAC_Status`, `CM_Value`, `CM_Status`, `SeaSalt_Value`, `SeaSalt_Status`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', new_row_list)

conn.commit()
conn.close()

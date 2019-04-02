import sqlite3

db = 'data/Aerosol/haze.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
csr = conn.cursor()
record_list = []
for row in csr.execute('SELECT * FROM `haze`'):
    unit = 'ug/m^3 LC'
    if row['Sf_Status'].startswith('V'):
        amm_so4_v = 4.125 * row['Sf_Value']
        amm_so4_s = 'V0'
    elif row['SO4f_Status'].startswith('V'):
        amm_so4_v = 1.375 * row['SO4f_Value']
        amm_so4_s = 'V0'
    else:
        amm_so4_v = -999
        amm_so4_s = 'M1'

    if row['NO3f_Status'].startswith('V'):
        amm_no3_v = 1.29 * row['NO3f_Value']
        amm_no3_s = 'V0'
    else:
        amm_no3_v = -999
        amm_no3_s = 'M1'

    if row['OC1f_Status'].startswith('V') and row['OC2f_Status'].startswith('V') and row['OC3f_Status'].startswith(
            'V') and row['OC4f_Status'].startswith('V') and row['OPf_Status'].startswith('V'):
        oc_v = row['OC1f_Value'] + row['OC2f_Value'] + row['OC3f_Value'] + row['OC4f_Value'] + row['OPf_Value']
        oc_s = 'V0'
    else:
        oc_v = -999
        oc_s = 'M1'

    if row['EC1f_Status'].startswith('V') and row['EC2f_Status'].startswith('V') and row['EC3f_Status'].startswith(
            'V') and row['OPf_Status'].startswith('V'):
        lac_v = row['EC1f_Value'] + row['EC2f_Value'] + row['EC3f_Value'] - row['OPf_Value']
        lac_s = 'V0'
    else:
        lac_v = -999
        lac_s = 'M1'

    if row['ALf_Status'].startswith('V') and row['CAf_Status'].startswith('V') and row['FEf_Status'].startswith('V') and \
            row['SIf_Status'].startswith('V') and row['TIf_Status'].startswith('V'):
        soil_v = 2.2 * row['ALf_Value'] + 1.63 * row['CAf_Value'] + 2.42 * row['FEf_Value'] + 2.49 * row[
            'SIf_Value'] + 1.94 * row['TIf_Value']
        soil_s = 'V0'
    else:
        soil_v = -999
        soil_s = 'M1'

    if row['MT_Status'].startswith('V') and row['MF_Status'].startswith('V'):
        cm_v = row['MT_Value'] - row['MF_Value']
        cm_s = 'V0'
    else:
        cm_v = -999
        cm_s = 'M1'

    if row['CHLf_Status'].startswith('V') and row['CHLf_Value'] >= row['CHLf_MDL']:
        sea_salt_v = 1.8 * row['CHLf_Value']
        sea_salt_s = 'V0'
    elif row['CLf_Status'].startswith('V'):
        sea_salt_v = 1.8 * row['CLf_Value']
        sea_salt_s = 'V0'
    else:
        sea_salt_v = -999
        sea_salt_s = 'M1'

    new_record = (row['SiteCode'], row['Date'], row['SiteName'], row['Latitude'], row['Longitude'], row['Elevation'], row['State'], row['CountyFIPS'], row['EPACode'], unit, amm_so4_v, amm_so4_s, amm_no3_v, amm_no3_s, soil_v, soil_s, oc_v, oc_s, lac_v, lac_s, cm_v, cm_s, sea_salt_v, sea_salt_s)
    record_list.append(new_record)

csr.executemany('INSERT INTO `HazeCal` (`SiteCode`, `Date`, `SiteName`, `Latitude`, `Longitude`, `Elevation`, `State`, `CountyFIPS`, `EPACode`, `Unit`, `AmmSO4_Value`, `AmmSO4_Status`, `AmmNO3_Value`, `AmmNO3_Status`, `Soil_Value`, `Soil_Status`, `OC_Value`, `OC_Status`, `LAC_Value`, `LAC_Status`, `CM_Value`, `CM_Status`, `SeaSalt_Value`, `SeaSalt_Status`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', record_list)
conn.commit()
conn.close()
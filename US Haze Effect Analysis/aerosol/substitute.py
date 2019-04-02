import sqlite3

db = 'data/Aerosol/haze.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
csr = conn.cursor()

sql = "SELECT `SiteCode`,`Date`,`AmmSO4_Value`,`AmmSO4_Status`,`AmmNO3_Value`,`AmmNO3_Status`,`Soil_Value`,`Soil_Status`,`OC_Value`,`OC_Status`,`LAC_Value`,`LAC_Status`,`CM_Value`,`CM_Status`,`SeaSalt_Value`,`SeaSalt_Status` FROM `HazeCal` WHERE `Date` >= '20060101' and `Date` <= '20141231' ORDER BY `Date`;"

records = {}

for row in csr.execute(sql):
    site_code = row['SiteCode']
    year = row['Date'][0:4]
    month = row['Date'][4:6]
    if site_code not in records:
        records[site_code] = {}

    if year not in records[site_code]:
        records[site_code][year] = {}

    quarter = 'q1' if '01' <= month <= '03' else 'q2' if '04' <= month <= '06' else 'q3' if '07' <= month <= '09' else 'q4'


    if quarter not in records[site_code][year]:
        records[site_code][year][quarter] = {}

    amm_so4 = 'AmmSO4'
    amm_no3 = 'AmmNO3'
    soil = 'Soil'
    oc = 'OC'
    lac = 'LAC'
    cm = 'CM'
    sea_salt = 'SeaSalt'

    if amm_so4 not in records[site_code][year][quarter]:
        records[site_code][year][quarter][amm_so4] = []

    if amm_no3 not in records[site_code][year][quarter]:
        records[site_code][year][quarter][amm_no3] = []

    if soil not in records[site_code][year][quarter]:
        records[site_code][year][quarter][soil] = []

    if oc not in records[site_code][year][quarter]:
        records[site_code][year][quarter][oc] = []

    if lac not in records[site_code][year][quarter]:
        records[site_code][year][quarter][lac] = []

    if cm not in records[site_code][year][quarter]:
        records[site_code][year][quarter][cm] = []

    if sea_salt not in records[site_code][year][quarter]:
        records[site_code][year][quarter][sea_salt] = []

    records[site_code][year][quarter][amm_so4].append({'value': row['AmmSO4_Value'], 'valid': row['AmmSO4_Status']})
    records[site_code][year][quarter][amm_no3].append({'value': row['AmmNO3_Value'], 'valid': row['AmmNO3_Status']})
    records[site_code][year][quarter][soil].append({'value': row['Soil_Value'], 'valid': row['Soil_Status']})
    records[site_code][year][quarter][oc].append({'value': row['OC_Value'], 'valid': row['OC_Status']})
    records[site_code][year][quarter][lac].append({'value': row['LAC_Value'], 'valid': row['LAC_Status']})
    records[site_code][year][quarter][cm].append({'value': row['CM_Value'], 'valid': row['CM_Status']})
    records[site_code][year][quarter][sea_salt].append({'value': row['SeaSalt_Value'], 'valid': row['SeaSalt_Status']})

medians = {}
for site, record1 in records.items():
    for year, record2 in record1.items():
        for quarter, record3 in record2.items():
            for constituent, value_list in record3.items():
                if site not in medians:
                    medians[site] = {}

                if year not in medians[site]:
                    medians[site][year] = {}

                if quarter not in medians[site][year]:
                    medians[site][year][quarter] = {}

                if constituent not in medians[site][year][quarter]:
                    medians[site][year][quarter][constituent] = {}

                status_str = ''.join([x['valid'] for x in value_list])
                if status_str.count('V') >= 15 and ('M1' * 11) not in status_str:
                    valid_value_list = [x['value'] for x in value_list if x['valid'] == 'V0']
                    l_len = len(valid_value_list)
                    valid_value_list.sort()
                    medians[site][year][quarter][constituent]['median'] = valid_value_list[(l_len - 1) // 2] if (l_len % 2) == 1 else (0.5 * (valid_value_list[l_len // 2 - 1] + valid_value_list[l_len // 2]))
                    medians[site][year][quarter][constituent]['exclude'] = False
                else:
                    medians[site][year][quarter][constituent]['median'] = 0
                    medians[site][year][quarter][constituent]['exclude'] = True


avgs = {}
used_years = [2010 + i for i in range(0, 5)]
for site, v in medians.items():
    for ty in used_years:
        year = str(ty)
        if site not in avgs:
            avgs[site] = {}

        if year not in avgs[site]:
            avgs[site][year] = {}

        cal_ys = [str(ty - i) for i in range(0, 5)]
        qs = ['q' + str(i) for i in range(1, 5)]
        cs = ['AmmSO4', 'AmmNO3', 'Soil', 'OC', 'LAC', 'CM', 'SeaSalt']
        for c in cs:
            for q in qs:
                sum = 0
                count = 0
                for y in cal_ys:
                    if y in v and q in v[y] and c in v[y][q]:
                        sum += v[y][q][c]['median']
                        if not v[y][q][c]['exclude']:
                            count += 1

                avg = (sum / count) if count >= 1 else 0

                if q not in avgs[site][year]:
                    avgs[site][year][q] = {}

                if c not in avgs[site][year][q]:
                    avgs[site][year][q][c] = {}

                avgs[site][year][q][c]['value'] = avg

new_records = []

for s, o1 in avgs.items():
    for y, o2 in o1.items():
        for q, o3 in o2.items():
            r = (s, y, int(q[1:]), o3['AmmSO4']['value'], o3['AmmNO3']['value'], o3['Soil']['value'], o3['OC']['value'], o3['LAC']['value'], o3['CM']['value'], o3['SeaSalt']['value'])
            new_records.append(r)

insert_sql = "INSERT INTO `Substituent` (`SiteCode`, `Year`, `Quarter`, `AmmSO4_Substitute`, `AmmNO3_Substitute`, `Soil_Substitute`, `OC_Substitute`, `LAC_Substitute`, `CM_Substitute`, `SeaSalt_Substitute`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
csr.executemany(insert_sql, new_records)
conn.commit()
conn.close()
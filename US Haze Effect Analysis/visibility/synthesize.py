import sqlite3
import math

db = 'data/Aerosol/haze.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
csr = conn.cursor()

query = "SELECT tm.`SiteCode` `SiteCode`, tm.`Date` `Date`, tm.`SiteName` `SiteName`, tm.`Latitude` `Latitude`, tm.`Longitude` `Longitude`, tm.`Elevation` `Elevation`, tm.`State` `State`, tm.`CountyFIPS` `CountyFIPS`, tm.`EPACode` `EPACode`, tm.`Unit` `Unit`, tm.`AmmSO4_Value` `AmmSO4_Value`, tm.`AmmSO4_Status` `AmmSO4_Status`, tm.`AmmNO3_Value` `AmmNO3_Value`, tm.`AmmNO3_Status` `AmmNO3_Status`, tm.`Soil_Value` `Soil_Value`, tm.`Soil_Status` `Soil_Status`, tm.`OC_Value` `OC_Value`, tm.`OC_Status` `OC_Status`, tm.`LAC_Value` `LAC_Value`, tm.`LAC_Status` `LAC_Status`, tm.`CM_Value` `CM_Value`, tm.`CM_Status` `CM_Status`, tm.`SeaSalt_Value` `SeaSalt_Value`, tm.`SeaSalt_Status` `SeaSalt_Status`, tm.`SAmmSO4_Value` `SAmmSO4_Value`, tm.`SAmmSO4_Status` `SAmmSO4_Status`, tm.`SAmmNO3_Value` `SAmmNO3_Value`, tm.`SAmmNO3_Status` `SAmmNO3_Status`, tm.`SPOM_Value` `SPOM_Value`, tm.`SPOM_Status` `SPOM_Status`, tm.`LAmmSO4_Value` `LAmmSO4_Value`, tm.`LAmmSO4_Status` `LAmmSO4_Status`, tm.`LAmmNO3_Value` `LAmmNO3_Value`, tm.`LAmmNO3_Status` `LAmmNO3_Status`, tm.`LPOM_Value` `LPOM_Value`, tm.`LPOM_Status` `LPOM_Status`, tm.`flRH_Value` `flRH_Value`, tm.`fssRH_Value` `fssRH_Value`, tm.`S_Rayleigh_Value` `S_Rayleigh_Value`, tm.`fsRH_Value` `fsRH_Value`, tm.`201001` `201001`, tm.`201002` `201002`, tm.`201003` `201003`, tm.`201004` `201004`, tm.`201005` `201005`, tm.`201006` `201006`, tm.`201007` `201007`, tm.`201008` `201008`, tm.`201009` `201009`, tm.`201010` `201010`, tm.`201011` `201011`, tm.`201012` `201012`, tm.`201101` `201101`, tm.`201102` `201102`, tm.`201103` `201103`, tm.`201104` `201104`, tm.`201105` `201105`, tm.`201106` `201106`, tm.`201107` `201107`, tm.`201108` `201108`, tm.`201109` `201109`, tm.`201110` `201110`, tm.`201111` `201111`, tm.`201112` `201112`, tm.`201201` `201201`, tm.`201202` `201202`, tm.`201203` `201203`, tm.`201204` `201204`, tm.`201205` `201205`, tm.`201206` `201206`, tm.`201207` `201207`, tm.`201208` `201208`, tm.`201209` `201209`, tm.`201210` `201210`, tm.`201211` `201211`, tm.`201212` `201212`, tm.`201301` `201301`, tm.`201302` `201302`, tm.`201303` `201303`, tm.`201304` `201304`, tm.`201305` `201305`, tm.`201306` `201306`, tm.`201307` `201307`, tm.`201308` `201308`, tm.`201309` `201309`, tm.`201310` `201310`, tm.`201311` `201311`, tm.`201312` `201312`, tm.`201401` `201401`, tm.`201402` `201402`, tm.`201403` `201403`, tm.`201404` `201404`, tm.`201405` `201405`, tm.`201406` `201406`, tm.`201407` `201407`, tm.`201408` `201408`, tm.`201409` `201409`, tm.`201410` `201410`, tm.`201411` `201411`, tm.`201412` `201412`, tm.`Quarter` `Quarter`, tm.`AmmSO4_Substitute` `AmmSO4_Substitute`, tm.`AmmNO3_Substitute` `AmmNO3_Substitute`, tm.`Soil_Substitute` `Soil_Substitute`, tm.`OC_Substitute` `OC_Substitute`, tm.`LAC_Substitute` `LAC_Substitute`, tm.`CM_Substitute` `CM_Substitute`, tm.`SeaSalt_Substitute` `SeaSalt_Substitute`, tm.`SAmmSO4_Substitute` `SAmmSO4_Substitute`, tm.`SAmmNO3_Substitute` `SAmmNO3_Substitute`, tm.`SPOM_Substitute` `SPOM_Substitute`, tm.`LAmmSO4_Substitute` `LAmmSO4_Substitute`, tm.`LAmmNO3_Substitute` `LAmmNO3_Substitute`, tm.`LPOM_Substitute` `LPOM_Substitute`, tn.`AmmSO4_Flag` `AmmSO4_Flag`, tn.`AmmNO3_Flag` `AmmNO3_Flag`, tn.`Soil_Flag` `Soil_Flag`, tn.`OC_Flag` `OC_Flag`, tn.`LAC_Flag` `LAC_Flag`, tn.`CM_Flag` `CM_Flag`, tn.`SeaSalt_Flag` `SeaSalt_Flag` FROM (SELECT t1.`SiteCode` `SiteCode`, t1.`Date` `Date`, t1.`SiteName` `SiteName`, t1.`Latitude` `Latitude`, t1.`Longitude` `Longitude`, t1.`Elevation` `Elevation`, t1.`State` `State`, t1.`CountyFIPS` `CountyFIPS`, t1.`EPACode` `EPACode`, t1.`Unit` `Unit`, t1.`AmmSO4_Value` `AmmSO4_Value`, t1.`AmmSO4_Status` `AmmSO4_Status`, t1.`AmmNO3_Value` `AmmNO3_Value`, t1.`AmmNO3_Status` `AmmNO3_Status`, t1.`Soil_Value` `Soil_Value`, t1.`Soil_Status` `Soil_Status`, t1.`OC_Value` `OC_Value`, t1.`OC_Status` `OC_Status`, t1.`LAC_Value` `LAC_Value`, t1.`LAC_Status` `LAC_Status`, t1.`CM_Value` `CM_Value`, t1.`CM_Status` `CM_Status`, t1.`SeaSalt_Value` `SeaSalt_Value`, t1.`SeaSalt_Status` `SeaSalt_Status`, t1.`SAmmSO4_Value` `SAmmSO4_Value`, t1.`SAmmSO4_Status` `SAmmSO4_Status`, t1.`SAmmNO3_Value` `SAmmNO3_Value`, t1.`SAmmNO3_Status` `SAmmNO3_Status`, t1.`SPOM_Value` `SPOM_Value`, t1.`SPOM_Status` `SPOM_Status`, t1.`LAmmSO4_Value` `LAmmSO4_Value`, t1.`LAmmSO4_Status` `LAmmSO4_Status`, t1.`LAmmNO3_Value` `LAmmNO3_Value`, t1.`LAmmNO3_Status` `LAmmNO3_Status`, t1.`LPOM_Value` `LPOM_Value`, t1.`LPOM_Status` `LPOM_Status`, t2.`flRH_Value` `flRH_Value`, t2.`fssRH_Value` `fssRH_Value`, t2.`S_Rayleigh_Value` `S_Rayleigh_Value`, t2.`fsRH_Value` `fsRH_Value`, t3.`201001` `201001`, t3.`201002` `201002`, t3.`201003` `201003`, t3.`201004` `201004`, t3.`201005` `201005`, t3.`201006` `201006`, t3.`201007` `201007`, t3.`201008` `201008`, t3.`201009` `201009`, t3.`201010` `201010`, t3.`201011` `201011`, t3.`201012` `201012`, t3.`201101` `201101`, t3.`201102` `201102`, t3.`201103` `201103`, t3.`201104` `201104`, t3.`201105` `201105`, t3.`201106` `201106`, t3.`201107` `201107`, t3.`201108` `201108`, t3.`201109` `201109`, t3.`201110` `201110`, t3.`201111` `201111`, t3.`201112` `201112`, t3.`201201` `201201`, t3.`201202` `201202`, t3.`201203` `201203`, t3.`201204` `201204`, t3.`201205` `201205`, t3.`201206` `201206`, t3.`201207` `201207`, t3.`201208` `201208`, t3.`201209` `201209`, t3.`201210` `201210`, t3.`201211` `201211`, t3.`201212` `201212`, t3.`201301` `201301`, t3.`201302` `201302`, t3.`201303` `201303`, t3.`201304` `201304`, t3.`201305` `201305`, t3.`201306` `201306`, t3.`201307` `201307`, t3.`201308` `201308`, t3.`201309` `201309`, t3.`201310` `201310`, t3.`201311` `201311`, t3.`201312` `201312`, t3.`201401` `201401`, t3.`201402` `201402`, t3.`201403` `201403`, t3.`201404` `201404`, t3.`201405` `201405`, t3.`201406` `201406`, t3.`201407` `201407`, t3.`201408` `201408`, t3.`201409` `201409`, t3.`201410` `201410`, t3.`201411` `201411`, t3.`201412` `201412`, t4.`Quarter` `Quarter`, t4.`AmmSO4_Substitute` `AmmSO4_Substitute`, t4.`AmmNO3_Substitute` `AmmNO3_Substitute`, t4.`Soil_Substitute` `Soil_Substitute`, t4.`OC_Substitute` `OC_Substitute`, t4.`LAC_Substitute` `LAC_Substitute`, t4.`CM_Substitute` `CM_Substitute`, t4.`SeaSalt_Substitute` `SeaSalt_Substitute`, t4.`SAmmSO4_Substitute` `SAmmSO4_Substitute`, t4.`SAmmNO3_Substitute` `SAmmNO3_Substitute`, t4.`SPOM_Substitute` `SPOM_Substitute`, t4.`LAmmSO4_Substitute` `LAmmSO4_Substitute`, t4.`LAmmNO3_Substitute` `LAmmNO3_Substitute`, t4.`LPOM_Substitute` `LPOM_Substitute` FROM `HazeCal` t1, `H_sp` t2, `f_RH_Sites` t3, `Substituent` t4 WHERE t1.`Date` >= '20100101' AND t1.`Date` <= '20141231' AND t1.`SiteCode` = t2.`SiteCode` AND  t1.`Date` = t2.`Date` AND t1.`SiteCode` = t3.`Code` AND t1.`SiteCode` = t4.`SiteCode` AND SUBSTR(t1.`Date`, 1, 4) = t4.`Year` AND ((CAST(SUBSTR(t1.`Date`, 5, 2) AS INTEGER) - 1) / 3 + 1) = t4.`Quarter`) tm LEFT OUTER JOIN (SELECT ta.`SiteCode` `SiteCode`, ta.`Year` `Year`, ta.`Replaceable` `AmmSO4_Flag`, tb.`Replaceable` `AmmNO3_Flag`, tc.`Replaceable` `Soil_Flag`, td.`Replaceable` `OC_Flag`, te.`Replaceable` `LAC_Flag`, tf.`Replaceable` `CM_Flag`, tg.`Replaceable` `SeaSalt_Flag` FROM (SELECT * FROM `ReplaceableMapping` WHERE `Component` = 'AmmSO4') ta, (SELECT * FROM `ReplaceableMapping` WHERE `Component` = 'AmmNO3') tb, (SELECT * FROM `ReplaceableMapping` WHERE `Component` = 'Soil') tc, (SELECT * FROM `ReplaceableMapping` WHERE `Component` = 'OC') td, (SELECT * FROM `ReplaceableMapping` WHERE `Component` = 'LAC') te, (SELECT * FROM `ReplaceableMapping` WHERE `Component` = 'CM') tf, (SELECT * FROM `ReplaceableMapping` WHERE `Component` = 'SeaSalt') tg WHERE ta.`SiteCode` = tb.`SiteCode` AND ta.`SiteCode` = tc.`SiteCode` AND ta.`SiteCode` = td.`SiteCode` AND ta.`SiteCode` = te.`SiteCode` AND ta.`SiteCode` = tf.`SiteCode` AND ta.`SiteCode` = tg.`SiteCode` AND ta.`Year` = tb.`Year` AND ta.`Year` = tc.`Year` AND ta.`Year` = td.`Year` AND ta.`Year` = te.`Year` AND ta.`Year` = tf.`Year` AND ta.`Year` = tg.`Year`) tn ON tm.`SiteCode` = tn.`SiteCode` AND SUBSTR(tm.`Date`, 1, 4) = tn.`Year`;"

refined_records = []

for row in csr.execute(query):
    site_code = row['SiteCode']
    sample_date = row['Date']
    y = sample_date[0:4]
    m = sample_date[4:6]
    d = sample_date[6:8]
    q = row['quarter']
    lat = row['Latitude']
    lon = row['Longitude']
    elev = row['Elevation']
    state = row['State']
    county = row['CountyFIPS']
    flag = False

    amm_so4 = row['AmmSO4_Value'] if row['AmmSO4_Status'] == 'V0' else row['AmmSO4_Substitute']
    s_amm_so4 = row['SAmmSO4_Value'] if row['SAmmSO4_Status'] == 'V0' else row['SAmmSO4_Substitute']
    l_amm_so4 = row['LAmmSO4_Value'] if row['LAmmSO4_Status'] == 'V0' else row['LAmmSO4_Substitute']
    if row['AmmSO4_Flag'] != 1 and (row['AmmSO4_Status'] == 'M1' or row['SAmmSO4_Status'] == 'M1' or row['LAmmSO4_Status'] == 'M1') and not flag:
        flag = True

    amm_no3 = row['AmmNO3_Value'] if row['AmmNO3_Status'] == 'V0' else row['AmmNO3_Substitute']
    s_amm_no3 = row['SAmmNO3_Value'] if row['SAmmNO3_Status'] == 'V0' else row['SAmmNO3_Substitute']
    l_amm_no3 = row['LAmmNO3_Value'] if row['LAmmNO3_Status'] == 'V0' else row['LAmmNO3_Substitute']
    if row['AmmNO3_Flag'] != 1 and (row['AmmNO3_Status'] == 'M1' or row['SAmmNO3_Status'] == 'M1' or row[
        'LAmmNO3_Status'] == 'M1') and not flag:
        flag = True

    oc = row['OC_Value'] if row['OC_Status'] == 'V0' else row['OC_Substitute']
    s_pom = row['SPOM_Value'] if row['SPOM_Status'] == 'V0' else row['SPOM_Substitute']
    l_pom = row['LPOM_Value'] if row['LPOM_Status'] == 'V0' else row['LPOM_Substitute']
    if row['OC_Flag'] != 1 and (row['OC_Status'] == 'M1' or row['SPOM_Status'] == 'M1' or row[
        'LPOM_Status'] == 'M1') and not flag:
        flag = True

    soil = row['Soil_Value'] if row['Soil_Status'] == 'V0' else row['Soil_Substitute']
    if row['Soil_Flag'] != 1 and row['Soil_Status'] == 'M1' and not flag:
        flag = True

    lac = row['LAC_Value'] if row['LAC_Status'] == 'V0' else row['LAC_Substitute']
    if row['LAC_Flag'] != 1 and row['LAC_Status'] == 'M1' and not flag:
        flag = True

    cm = row['CM_Value'] if row['CM_Status'] == 'V0' else row['CM_Substitute']
    if row['CM_Flag'] != 1 and row['CM_Status'] == 'M1' and not flag:
        flag = True

    sea_salt = row['SeaSalt_Value'] if row['SeaSalt_Status'] == 'V0' else row['SeaSalt_Substitute']
    if row['SeaSalt_Flag'] != 1 and row['SeaSalt_Status'] == 'M1' and not flag:
        flag = True

    f_rh = row[sample_date[0:6]]
    f_l_rh = row['flRH_Value']
    f_s_rh = row['fsRH_Value']
    f_ss_rh = row['fssRH_Value']
    s_rayleigh = row['S_Rayleigh_Value']

    b_so4 = 3.0 * f_rh * amm_so4
    b_s_so4 = 2.2 * f_s_rh * s_amm_so4
    b_l_so4 = 4.8 * f_l_rh * l_amm_so4
    b_no3 = 3.0 * f_rh * amm_no3
    b_s_no3 = 2.4 * f_s_rh * s_amm_no3
    b_l_no3 = 5.1 * f_l_rh * l_amm_no3
    b_omc = 4.0 * 1.4 * oc
    b_pom = 4.0 * 1.8 * oc
    b_s_pom = 2.8 * s_pom
    b_l_pom = 6.1 * l_pom
    b_lac = 10.0 * lac
    b_soil = soil
    b_cm = 0.6 * cm
    b_salt = 1.7 * f_ss_rh * sea_salt
    b_rhr_0 = b_so4 + b_no3 + b_omc + b_lac + b_soil + b_cm + 10
    b_rhr_1 = b_so4 + b_no3 + b_pom + b_lac + b_soil + b_salt + b_cm + s_rayleigh
    b_rhr_2 = b_s_so4 + b_s_no3 + b_s_pom + b_l_so4 + b_l_no3 + b_l_pom + b_lac + b_soil + b_salt + b_cm + s_rayleigh
    hi_rhr_0 = 10.0 * math.log(b_rhr_0 / 10)
    hi_rhr_1 = 10.0 * math.log(b_rhr_1 / 10)
    hi_rhr_2 = 10.0 * math.log(b_rhr_2 / 10)
    refined_records.append((site_code, y, m, d, q, lat, lon, elev, state, county, flag, b_so4, b_s_so4, b_l_so4, b_no3, b_s_no3, b_l_no3, b_omc, b_pom, b_s_pom, b_l_pom, b_lac, b_soil, b_cm, b_salt, b_rhr_0, b_rhr_1, b_rhr_2, hi_rhr_0, hi_rhr_1, hi_rhr_2))

print(refined_records)
insert_sql = "INSERT INTO `HazeF` (`SiteCode`, `Year`, `Month`, `Day`, `Quarter`, `Latitude`, `Longitude`, `Elevation`, `State`, `CountyFIPIS`, `Flag`, `LE_SO4`, `LE_S_SO4`, `LE_L_SO4`, `LE_NO3`, `LE_S_NO3`, `LE_L_NO3`, `LE_OMC`, `LE_POM`, `LE_S_POM`, `LE_L_POM`, `LE_LAC`, `LE_Soil`, `LE_CM`, `LE_Salt`, `LE_RHR_0`, `LE_RHR_1`, `LE_RHR_2`, `HI_RHR_0`, `HI_RHR_1`, `HI_RHR_2`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
csr.executemany(insert_sql, refined_records)

conn.commit()
conn.close()


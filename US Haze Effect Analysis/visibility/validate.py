import sqlite3

db = 'data/Aerosol/haze.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
csr = conn.cursor()

sql = "SELECT t1.`SiteCode` `SiteCode`, t1.`Date` `Date`, t1.`SiteName` `SiteName`, t1.`Latitude` `Latitude`, t1.`Longitude` `Longitude`, t1.`Elevation` `Elevation`, t1.`State` `State`, t1.`CountyFIPS` `CountyFIPS`, t1.`EPACode` `EPACode`, t1.`Unit` `Unit`, t1.`AmmSO4_Value` `AmmSO4_Value`, t1.`AmmSO4_Status` `AmmSO4_Status`, t1.`AmmNO3_Value` `AmmNO3_Value`, t1.`AmmNO3_Status` `AmmNO3_Status`, t1.`Soil_Value` `Soil_Value`, t1.`Soil_Status` `Soil_Status`, t1.`OC_Value` `OC_Value`, t1.`OC_Status` `OC_Status`, t1.`LAC_Value` `LAC_Value`, t1.`LAC_Status` `LAC_Status`, t1.`CM_Value` `CM_Value`, t1.`CM_Status` `CM_Status`, t1.`SeaSalt_Value` `SeaSalt_Value`, t1.`SeaSalt_Status` `SeaSalt_Status`, t1.`SAmmSO4_Value` `SAmmSO4_Value`, t1.`SAmmSO4_Status` `SAmmSO4_Status`, t1.`SAmmNO3_Value` `SAmmNO3_Value`, t1.`SAmmNO3_Status` `SAmmNO3_Status`, t1.`SPOM_Value` `SPOM_Value`, t1.`SPOM_Status` `SPOM_Status`, t1.`LAmmSO4_Value` `LAmmSO4_Value`, t1.`LAmmSO4_Status` `LAmmSO4_Status`, t1.`LAmmNO3_Value` `LAmmNO3_Value`, t1.`LAmmNO3_Status` `LAmmNO3_Status`, t1.`LPOM_Value` `LPOM_Value`, t1.`LPOM_Status` `LPOM_Status`, t2.`flRH_Value` `flRH_Value`, t2.`fssRH_Value` `fssRH_Value`, t2.`S_Rayleigh_Value` `S_Rayleigh_Value`, t2.`fsRH_Value` `fsRH_Value`, t3.`201001` `201001`, t3.`201002` `201002`, t3.`201003` `201003`, t3.`201004` `201004`, t3.`201005` `201005`, t3.`201006` `201006`, t3.`201007` `201007`, t3.`201008` `201008`, t3.`201009` `201009`, t3.`201010` `201010`, t3.`201011` `201011`, t3.`201012` `201012`, t3.`201101` `201101`, t3.`201102` `201102`, t3.`201103` `201103`, t3.`201104` `201104`, t3.`201105` `201105`, t3.`201106` `201106`, t3.`201107` `201107`, t3.`201108` `201108`, t3.`201109` `201109`, t3.`201110` `201110`, t3.`201111` `201111`, t3.`201112` `201112`, t3.`201201` `201201`, t3.`201202` `201202`, t3.`201203` `201203`, t3.`201204` `201204`, t3.`201205` `201205`, t3.`201206` `201206`, t3.`201207` `201207`, t3.`201208` `201208`, t3.`201209` `201209`, t3.`201210` `201210`, t3.`201211` `201211`, t3.`201212` `201212`, t3.`201301` `201301`, t3.`201302` `201302`, t3.`201303` `201303`, t3.`201304` `201304`, t3.`201305` `201305`, t3.`201306` `201306`, t3.`201307` `201307`, t3.`201308` `201308`, t3.`201309` `201309`, t3.`201310` `201310`, t3.`201311` `201311`, t3.`201312` `201312`, t3.`201401` `201401`, t3.`201402` `201402`, t3.`201403` `201403`, t3.`201404` `201404`, t3.`201405` `201405`, t3.`201406` `201406`, t3.`201407` `201407`, t3.`201408` `201408`, t3.`201409` `201409`, t3.`201410` `201410`, t3.`201411` `201411`, t3.`201412` `201412`, t4.`Quarter` `Quarter`, t4.`AmmSO4_Substitute` `AmmSO4_Substitute`, t4.`AmmNO3_Substitute` `AmmNO3_Substitute`, t4.`Soil_Substitute` `Soil_Substitute`, t4.`OC_Substitute` `OC_Substitute`, t4.`LAC_Substitute` `LAC_Substitute`, t4.`CM_Substitute` `CM_Substitute`, t4.`SeaSalt_Substitute` `SeaSalt_Substitute`, t4.`SAmmSO4_Substitute` `SAmmSO4_Substitute`, t4.`SAmmNO3_Substitute` `SAmmNO3_Substitute`, t4.`SPOM_Substitute` `SPOM_Substitute`, t4.`LAmmSO4_Substitute` `LAmmSO4_Substitute`, t4.`LAmmNO3_Substitute` `LAmmNO3_Substitute`, t4.`LPOM_Substitute` `LPOM_Substitute` FROM `HazeCal` t1, `H_sp` t2, `f_RH_Sites` t3, `Substituent` t4 WHERE t1.`Date` >= '20100101' AND t1.`Date` <= '20141231' AND t1.`AmmSO4_Status` = 'V0' AND t1.`AmmNO3_Status` = 'V0' AND t1.`Soil_Status` = 'V0' AND t1.`OC_Status` = 'V0' AND t1.`LAC_Status`  = 'V0' AND t1.`CM_Status` = 'V0' AND t1.`SeaSalt_Status` = 'V0' AND t1.`SiteCode` = t2.`SiteCode` AND  t1.`Date` = t2.`Date` AND t1.`SiteCode` = t3.`Code` AND t1.`SiteCode` = t4.`SiteCode` AND SUBSTR(t1.`Date`, 1, 4) = t4.`Year` AND ((CAST(SUBSTR(t1.`Date`, 5, 2) AS INTEGER) - 1) / 3 + 1) = t4.`Quarter`;"

single_replace_list = ['AmmSO4', 'AmmNO3', 'Soil', 'OC', 'LAC', 'CM', 'SeaSalt']

valid_results = {type: {} for type in single_replace_list}

def rhr0(amm_so4, amm_no3, soil, oc, lac, cm, f_rh):
    return (3 * f_rh * (amm_so4 + amm_no3) + soil + 1.4 * 4 * oc + 10 * lac + 0.6 * cm + 10)

def rhr1(amm_so4, amm_no3, soil, oc, lac, cm, sea_salt, f_rh, f_rh_ss, s_rayleigh):
    return (3 * f_rh * (amm_so4 + amm_no3) + soil + 1.8 * 4 * oc + 10 * lac + 0.6 * cm + 1.7 * f_rh_ss * sea_salt + s_rayleigh)

def rhr2(s_amm_so4, s_amm_no3, s_pom, l_amm_so4, l_amm_no3, l_pom, soil, lac, cm, sea_salt, f_rh_s, f_rh_l, f_rh_ss, s_rayleigh):
    return (2.2 * f_rh_s * s_amm_so4 + 4.8 * f_rh_l * l_amm_so4 + 2.4 * f_rh_s * s_amm_no3 + 5.1 * f_rh_l * l_amm_no3 + 2.8 * s_pom + 6.1 * l_pom + 10 * lac + soil + 1.7 * f_rh_ss + sea_salt + 0.6 * cm + s_rayleigh)

for type in single_replace_list:
    for row in csr.execute(sql):
        site_code = row['SiteCode']
        sample_date = row['Date']
        sample_ym = sample_date[0:6]
        sample_y = sample_date[0:4]
        sample_md = sample_date[4:8]
        formula_list = ['RHR' + str(i) for i in range(0, 3)]
        if site_code not in valid_results[type]:
            valid_results[type][site_code] = {}

        if sample_y not in valid_results[type][site_code]:
            valid_results[type][site_code][sample_y] = {}

        if sample_md not in valid_results[type][site_code][sample_y]:
            valid_results[type][site_code][sample_y][sample_md] = {}

        if type == 'SeaSalt':
            b_rhr_1 = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                           row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym], row['fssRH_Value'],
                           row['S_Rayleigh_Value'])
            b_rhr_1_s = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                           row['LAC_Value'], row['CM_Value'], row['SeaSalt_Substitute'], row[sample_ym], row['fssRH_Value'],
                           row['S_Rayleigh_Value'])
            b_rhr_2 = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                           row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                           row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                           row['fssRH_Value'], row['S_Rayleigh_Value'])
            b_rhr_2_s = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                           row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                           row['CM_Value'], row['SeaSalt_Substitute'], row['fsRH_Value'], row['flRH_Value'],
                           row['fssRH_Value'], row['S_Rayleigh_Value'])
            rhr_0_diff_ratio = 0
            rhr_1_diff_ratio = abs((b_rhr_1_s - b_rhr_1) / b_rhr_1)
            rhr_2_diff_ratio = abs((b_rhr_2_s - b_rhr_2) / b_rhr_2)

            valid_results[type][site_code][sample_y][sample_md][formula_list[0]] = rhr_0_diff_ratio
            valid_results[type][site_code][sample_y][sample_md][formula_list[1]] = rhr_1_diff_ratio
            valid_results[type][site_code][sample_y][sample_md][formula_list[2]] = rhr_2_diff_ratio
        else:
            if type == 'AmmSO4':
                b_rhr_0 = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_0_s = rhr0(row['AmmSO4_Substitute'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_1 = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_1_s = rhr1(row['AmmSO4_Substitute'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2 = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                               row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                               row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2_s = rhr2(row['SAmmSO4_Substitute'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Substitute'],
                               row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                               row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])

                rhr_0_diff_ratio = abs((b_rhr_0_s - b_rhr_0) / b_rhr_0)
                rhr_1_diff_ratio = abs((b_rhr_1_s - b_rhr_1) / b_rhr_1)
                rhr_2_diff_ratio = abs((b_rhr_2_s - b_rhr_2) / b_rhr_2)

                valid_results[type][site_code][sample_y][sample_md][formula_list[0]] = rhr_0_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[1]] = rhr_1_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[2]] = rhr_2_diff_ratio
            if type == 'AmmNO3':
                b_rhr_0 = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_0_s = rhr0(row['AmmSO4_Value'], row['AmmNO3_Substitute'], row['Soil_Value'], row['OC_Value'],
                                 row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_1 = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_1_s = rhr1(row['AmmSO4_Value'], row['AmmNO3_Substitute'], row['Soil_Value'], row['OC_Value'],
                                 row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2 = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                               row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                               row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2_s = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Substitute'], row['SPOM_Value'], row['LAmmSO4_Value'],
                                 row['LAmmNO3_Substitute'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                                 row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])

                rhr_0_diff_ratio = abs((b_rhr_0_s - b_rhr_0) / b_rhr_0)
                rhr_1_diff_ratio = abs((b_rhr_1_s - b_rhr_1) / b_rhr_1)
                rhr_2_diff_ratio = abs((b_rhr_2_s - b_rhr_2) / b_rhr_2)

                valid_results[type][site_code][sample_y][sample_md][formula_list[0]] = rhr_0_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[1]] = rhr_1_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[2]] = rhr_2_diff_ratio
            if type == 'Soil':
                b_rhr_0 = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_0_s = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Substitute'], row['OC_Value'],
                                 row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_1 = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_1_s = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Substitute'], row['OC_Value'],
                                 row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2 = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                               row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                               row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2_s = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                                 row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Substitute'], row['LAC_Value'],
                                 row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])

                rhr_0_diff_ratio = abs((b_rhr_0_s - b_rhr_0) / b_rhr_0)
                rhr_1_diff_ratio = abs((b_rhr_1_s - b_rhr_1) / b_rhr_1)
                rhr_2_diff_ratio = abs((b_rhr_2_s - b_rhr_2) / b_rhr_2)

                valid_results[type][site_code][sample_y][sample_md][formula_list[0]] = rhr_0_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[1]] = rhr_1_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[2]] = rhr_2_diff_ratio
            if type == 'OC':
                b_rhr_0 = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_0_s = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Substitute'],
                                 row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_1 = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_1_s = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Substitute'],
                                 row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2 = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                               row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                               row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2_s = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Substitute'], row['LAmmSO4_Value'],
                                 row['LAmmNO3_Value'], row['LPOM_Substitute'], row['Soil_Value'], row['LAC_Value'],
                                 row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])

                rhr_0_diff_ratio = abs((b_rhr_0_s - b_rhr_0) / b_rhr_0)
                rhr_1_diff_ratio = abs((b_rhr_1_s - b_rhr_1) / b_rhr_1)
                rhr_2_diff_ratio = abs((b_rhr_2_s - b_rhr_2) / b_rhr_2)

                valid_results[type][site_code][sample_y][sample_md][formula_list[0]] = rhr_0_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[1]] = rhr_1_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[2]] = rhr_2_diff_ratio
            if type == 'LAC':
                b_rhr_0 = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_0_s = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                                 row['LAC_Substitute'], row['CM_Value'], row[sample_ym])
                b_rhr_1 = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_1_s = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                                 row['LAC_Substitute'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2 = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                               row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                               row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2_s = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                                 row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Substitute'],
                                 row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])

                rhr_0_diff_ratio = abs((b_rhr_0_s - b_rhr_0) / b_rhr_0)
                rhr_1_diff_ratio = abs((b_rhr_1_s - b_rhr_1) / b_rhr_1)
                rhr_2_diff_ratio = abs((b_rhr_2_s - b_rhr_2) / b_rhr_2)

                valid_results[type][site_code][sample_y][sample_md][formula_list[0]] = rhr_0_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[1]] = rhr_1_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[2]] = rhr_2_diff_ratio
            if type == 'CM':
                b_rhr_0 = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row[sample_ym])
                b_rhr_0_s = rhr0(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                                 row['LAC_Value'], row['CM_Substitute'], row[sample_ym])
                b_rhr_1 = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                               row['LAC_Value'], row['CM_Value'], row['SeaSalt_Value'], row[sample_ym],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_1_s = rhr1(row['AmmSO4_Value'], row['AmmNO3_Value'], row['Soil_Value'], row['OC_Value'],
                                 row['LAC_Value'], row['CM_Substitute'], row['SeaSalt_Value'], row[sample_ym],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2 = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                               row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                               row['CM_Value'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                               row['fssRH_Value'], row['S_Rayleigh_Value'])
                b_rhr_2_s = rhr2(row['SAmmSO4_Value'], row['SAmmNO3_Value'], row['SPOM_Value'], row['LAmmSO4_Value'],
                                 row['LAmmNO3_Value'], row['LPOM_Value'], row['Soil_Value'], row['LAC_Value'],
                                 row['CM_Substitute'], row['SeaSalt_Value'], row['fsRH_Value'], row['flRH_Value'],
                                 row['fssRH_Value'], row['S_Rayleigh_Value'])

                rhr_0_diff_ratio = abs((b_rhr_0_s - b_rhr_0) / b_rhr_0)
                rhr_1_diff_ratio = abs((b_rhr_1_s - b_rhr_1) / b_rhr_1)
                rhr_2_diff_ratio = abs((b_rhr_2_s - b_rhr_2) / b_rhr_2)

                valid_results[type][site_code][sample_y][sample_md][formula_list[0]] = rhr_0_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[1]] = rhr_1_diff_ratio
                valid_results[type][site_code][sample_y][sample_md][formula_list[2]] = rhr_2_diff_ratio

valid_day_ratios = {type: {} for type in single_replace_list}

for type, sites in valid_results.items():
    for site, years in sites.items():
        if site not in valid_day_ratios[type]:
            valid_day_ratios[type][site] = {}
        for year, mds in years.items():
            if year not in valid_day_ratios[type][site]:
                valid_day_ratios[type][site][year] = {}

            valid_count = [0, 0, 0]
            total_count = [0, 0, 0]
            for md, formulas in mds.items():
                for formula, value in formulas.items():
                    if formula == 'RHR0':
                        total_count[0] += 1
                        if value < 0.1:
                            valid_count[0] += 1

                    if formula == 'RHR1':
                        total_count[1] += 1
                        if value < 0.1:
                            valid_count[1] += 1

                    if formula == 'RHR2':
                        total_count[2] += 1
                        if value < 0.1:
                            valid_count[2] += 1

            if total_count[0] > 0:
                valid_day_ratios[type][site][year]['RHR0'] = valid_count[0] / total_count[0]

            if total_count[1] > 0:
                valid_day_ratios[type][site][year]['RHR1'] = valid_count[1] / total_count[1]

            if total_count[2] > 0:
                valid_day_ratios[type][site][year]['RHR2'] = valid_count[2] / total_count[2]

valid_years = {}

for type, sites in valid_day_ratios.items():
    if type not in valid_years:
        valid_years[type] = {}
    for site, years in sites.items():
        if site not in valid_years[type]:
            valid_years[type][site] = {}
        for year, formulas in years.items():
            if year not in valid_years[type][site]:
                valid_years[type][site][year] = {}
            replaceable = True
            for value in formulas.values():
                if value >= 0.9:
                    flag = True
                else:
                    flag = False
                replaceable = replaceable and flag
            valid_years[type][site][year]['Replaceable'] = replaceable

#print(valid_years)
insert_list = []
for type, sites in valid_years.items():
    for site, years in sites.items():
        for year, replace in years.items():
            insert_list.append((type, site, year, int(replace['Replaceable'])))

csr.executemany('INSERT INTO `ReplaceableMapping` (`Component`, `SiteCode`, `Year`, `Replaceable`) VALUES (?, ?, ?, ?);', insert_list)

conn.commit()
conn.close()
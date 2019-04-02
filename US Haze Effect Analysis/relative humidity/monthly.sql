INSERT INTO f_RH_Monthly
	SELECT StateCode, StateName, CountyCode, CountyName, SiteNum, Latitude lat, Longitude lon, Datum, strftime('%Y', DateLocal) y, strftime('%m', DateLocal) m, avg(fRHAvg)
	FROM f_RH_Daily
	GROUP BY lat, lon, y, m;
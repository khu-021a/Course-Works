INSERT INTO f_RH_Daily
	SELECT StateCode, StateName, CountyCode,  CountyName, SiteNum, Latitude, Longitude, Datum, DateLocal, fRHAvg
	FROM (SELECT t1.StateCode StateCode, t1.StateName StateName, t1.CountyCode CountyCode, t1.CountyName CountyName, t1.SiteNum SiteNum, t1.Latitude Latitude, t1.Longitude Longitude, t1.Datum Datum, t1.DateLocal DateLocal, COUNT(t1.TimeLocal) ValidHourNum, AVG(t2.fRH) fRHAvg
		FROM hourly_RH t1, f_RH t2
		WHERE CAST(ROUND(t1.SampleMeasurement) AS INTEGER) = t2.RH
		GROUP BY Latitude, Longitude, DateLocal) t3
	WHERE ValidHourNum >= 16;
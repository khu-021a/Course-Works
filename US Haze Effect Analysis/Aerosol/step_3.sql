SELECT `SiteCode`,`Date`,`AmmSO4_Value`,`AmmSO4_Status`,`AmmNO3_Value`,`AmmNO3_Status`,`Soil_Value`,`Soil_Status`,`OC_Value`,`OC_Status`,`LAC_Value`,`LAC_Status`,`CM_Value`,`CM_Status`,`SeaSalt_Value`,`SeaSalt_Status`
FROM `HazeCal`
WHERE `Date` >= '20060101' and `Date` <= '20141231'
ORDER BY `Date`;

CREATE TABLE `Substituent` (
	`SiteCode`	TEXT,
	`Year`	TEXT,
	`Quarter`	INTERGER,
	`AmmSO4_Substitute`	REAL,
	`AmmNO3_Substitute`	REAL,
	`Soil_Substitute`	REAL,
	`OC_Substitute`	REAL,
	`LAC_Substitute`	REAL,
	`CM_Substitute`	REAL,
	`SeaSalt_Substitute`	REAL
);

INSERT INTO `Substituent` (`SiteCode`, `Year`, `Quarter`, `AmmSO4_Substitute`, `AmmNO3_Substitute`, `Soil_Substitute`, `OC_Substitute`, `LAC_Substitute`, `CM_Substitute`, `SeaSalt_Substitute`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
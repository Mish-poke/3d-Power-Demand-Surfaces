
# Brief Description
# this script is adding the raw data from neptune lab into the weather data file for each ship
# when ever one wants to update the weather data per ship, you will have to run this script in the first place to
# add latest lat / long / engine data at the end of the existing ships-weather file

from tkinter import filedialog
import inspect
import os
from playsound import playsound
import math

import pandas as pd

from _CM_Include import *

# region FULL AIDA FLEET
# dict_analyseTheseShips = {
# 	"AIDAvita": 				1
# 	,"AIDAdiva": 				1
# 	,"AIDAluna": 				1
# 	,"AIDAmar": 				1
# 	,"AIDAbella": 				1
# 	,"AIDAblu": 				1
# 	,"AIDAsol": 				1
# 	,"AIDAstella": 				1
# 	,"AIDAprima": 				1
# 	,"AIDAperla": 				1
# 	,"AIDAaura": 				1
# 	,"AIDAcara": 				1
# 	,"AIDAnova": 				1
# 	,"Costa Atlantica": 		0
# 	,"Costa Deliziosa": 		0
# 	,"Costa Diadema": 			0
# 	,"Costa Fascinosa": 		0
# 	,"Costa Favolosa": 			0
# 	,"Costa Fortuna": 			0
# 	,"Costa Luminosa": 			0
# 	,"Costa Magica": 			0
# 	,"Costa Mediterranea": 		0
# 	,"Costa Pacifica": 			0
# 	,"Costa Serena": 			0
# 	,"Costa Smeralda": 			0
# 	,"Costa Toscana": 			0
# 	,"Costa Firenze": 			0
# 	,"Costa Venezia": 			0
# }
# endregion

# region FULL AIDA AND COSTA FLEET
dict_analyseTheseShips = {
	"AIDAaura": 				1
	,"AIDAcara": 				1
	,"AIDAvita": 				1
	,"AIDAdiva": 				1
	,"AIDAluna": 				1
	,"AIDAmar": 				1
	,"AIDAbella": 				1
	,"AIDAblu": 				1
	,"AIDAsol": 				1
	,"AIDAstella": 				1
	,"AIDAprima": 				1
	,"AIDAperla": 				1
	,"AIDAnova": 				1
	,"Costa Atlantica": 		1
	,"Costa Deliziosa": 		1
	,"Costa Diadema": 			1
	,"Costa Fascinosa": 		1
	,"Costa Favolosa": 			1
	,"Costa Fortuna": 			1
	,"Costa Luminosa": 			1
	,"Costa Magica": 			1
	,"Costa Mediterranea": 		1
	,"Costa neoRomantica": 		1
	,"Costa Pacifica": 			1
	,"Costa Serena": 			1
	,"Costa Smeralda": 			1
	,"Costa Toscana": 			1
	,"Costa Firenze": 			1
	,"Costa Venezia": 			1
}
# endregion

# region FULL AIDA AND COSTA FLEET
# dict_analyseTheseShips = {
# 	"AIDAaura": 				0
# 	,"AIDAcara": 				0
# 	,"AIDAvita": 				0
# 	,"AIDAdiva": 				0
# 	,"AIDAluna": 				0
# 	,"AIDAmar": 				0
# 	,"AIDAbella": 				0
# 	,"AIDAblu": 				0
# 	,"AIDAsol": 				0
# 	,"AIDAstella": 				0
# 	,"AIDAprima": 				0
# 	,"AIDAperla": 				0
# 	,"AIDAnova": 				0
# 	,"Costa Atlantica": 		1
# 	,"Costa Deliziosa": 		0
# 	,"Costa Diadema": 			0
# 	,"Costa Fascinosa": 		0
# 	,"Costa Favolosa": 			0
# 	,"Costa Fortuna": 			0
# 	,"Costa Luminosa": 			0
# 	,"Costa Magica": 			0
# 	,"Costa Mediterranea": 		0
# 	,"Costa neoRomantica": 		0
# 	,"Costa Pacifica": 			0
# 	,"Costa Serena": 			0
# 	,"Costa Smeralda": 			0
# 	,"Costa Toscana": 			0
# 	,"Costa Firenze": 			0
# 	,"Costa Venezia": 			0
# }
# endregion

dict_rawDataStructure = {
	"sourceDataStructure_neptuneLab_RawData": 				0
	,"sourceDataStructure_neptuneLab_preparedAverages": 	0
	,"sourceDataStructure_PBI_preparedColumns": 			1
}

fileCopyBeforeSmartAlgo = '_BEFORE_SMART_ALGO_'

masterPath_allShipsWeatherData = r'E:\001_CMG\NASA_ARIS_Data\SHIPs\02 SHIP with OpenWeather\xx'
stringWeatherFileEnhancement = ' SHIP_and_OpenWeather.csv'

# 'ShipCode;SOG;lastupdateutc;DG1POW;DG2POW;DG3POW;DG4POW;DG5POW;DG6POW;Latitude;Longitude;
flag_weatherData_Ship = 'ShipCode'
flag_weatherData_SOG = 'SOG'
flag_weatherData_Date = 'lastupdateutc'
flag_weatherData_DG1POW = 'DG1POW'
flag_weatherData_DG2POW = 'DG2POW'
flag_weatherData_DG3POW = 'DG3POW'
flag_weatherData_DG4POW = 'DG4POW'
flag_weatherData_DG5POW = 'DG5POW'
flag_weatherData_DG6POW = 'DG6POW'
flag_weatherData_Latitude = 'Latitude'
flag_weatherData_Longitude = 'Longitude'

dict_shipShortCodesToLongNames = dict(
	[
		('A-AU', 'AIDAaura'),
		('A-CA', 'AIDAcara'),
		('A-VT', 'AIDAvita'),
		('A-BE', 'AIDAbella'),
		('A-LN', 'AIDAluna'),
		('A-DV', 'AIDAdiva'),
		('A-BL', 'AIDAblu'),
		('A-MR', 'AIDAmar'),
		('A-SL', 'AIDAsol'),
		('A-ST', 'AIDAstella'),
		('A-PM', 'AIDAprima'),
		('A-PL', 'AIDAperla'),
		('A-NV', 'AIDAnova'),
		('C-AT', 'Costa Atlantica'),
		('C-DE', 'Costa Deliziosa'),
		('C-DI', 'Costa Diadema'),
		('C-FA', 'Costa Favolosa'),
		('C-FS', 'Costa Fascinosa'),
		('C-FO', 'Costa Fortuna'),
		('C-LU', 'Costa Luminosa'),
		('C-MG', 'Costa Magica'),
		('C-MD', 'Costa Mediterranea'),
		('C-NR', 'Costa neoRomantica'),
		('C-PA', 'Costa Pacifica'),
		('C-SE', 'Costa Serena'),
		('C-ME', 'Costa Smeralda'),
		('C-TO', 'Costa Toscana'),
		('C-FI', 'Costa Firenze'),
		('C-VZ', 'Costa Venezia')
	]
)

dict_shipShortCodesToLongNames_Reverse = dict(
	[
		('AIDAaura', 			'A-AU'),
		('AIDAcara', 			'A-CA'),
		('AIDAvita', 			'A-VT'),
		('AIDAbella', 			'A-BE'),
		('AIDAluna', 			'A-LN'),
		('AIDAdiva', 			'A-DV'),
		('AIDAblu', 			'A-BL'),
		('AIDAmar', 			'A-MR'),
		('AIDAsol', 			'A-SL'),
		('AIDAstella', 			'A-ST'),
		('AIDAprima', 			'A-PM'),
		('AIDAperla', 			'A-PL'),
		('AIDAnova', 			'A-NV'),
		('Costa Atlantica', 	'C-AT'),
		('Costa Deliziosa', 	'C-DE'),
		('Costa Diadema', 		'C-DI'),
		('Costa Favolosa', 		'C-FA'),
		('Costa Fascinosa', 	'C-FS'),
		('Costa Fortuna', 		'C-FO'),
		('Costa Luminosa', 		'C-LU'),
		('Costa Magica', 		'C-MG'),
		('Costa Mediterranea', 	'C-MD'),
		('Costa neoRomantica', 	'C-NR'),
		('Costa Pacifica', 		'C-PA'),
		('Costa Serena', 		'C-SE'),
		('Costa Smeralda', 		'C-ME'),
		('Costa Toscana', 		'C-TO'),
		('Costa Firenze', 		'C-FI'),
		('Costa Venezia', 		'C-VZ')
	]
)


# ######################################################################################################################
def f_loopAllFilesInThisFolderAndCreateNewSumFile(
):
	f_makeThePrintNiceStructured(True, "### START READING ALL FILES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	df1 = pd.DataFrame()
	
	filesToBeTreated = filedialog.askopenfilenames(
		initialdir="C:\\Users\\TR@FI_02\\Downloads\\Automation Data",
		title='PICK FILES FROM DAY BY DAY RAW DATA')
	
	useFilePicker = True
	# region LOOP Files and bring the together in one dataframe
	if useFilePicker:
		for subFile in filesToBeTreated:
			print("read " + subFile)
			
			if df1.shape[0] == 0:  # df1 is empty
				df1 = pd.read_csv(subFile, sep=',', decimal=".", low_memory=False)
			else:
				df2 = pd.read_csv(subFile, sep=',', decimal=".", low_memory=False)
				
				df1 = pd.concat([df1, df2])
		
		df1 = func_replaceColumnNamesIfNeeded(df1)
		
		df1[flag_weatherData_Date] = pd.to_datetime(df1[flag_weatherData_Date])
		
		df1 = df1.round(decimals=4)
		
		df1 = df1.sort_values(
			[flag_weatherData_Ship, flag_weatherData_Date],
			ascending=[True, True]
		)
		
		df1 = df1[[
			flag_weatherData_Ship,
			flag_weatherData_Date,
			flag_weatherData_SOG,
			flag_weatherData_DG1POW,
			flag_weatherData_DG2POW,
			flag_weatherData_DG3POW,
			flag_weatherData_DG4POW,
			flag_weatherData_DG5POW,
			flag_weatherData_DG6POW,
			flag_weatherData_Latitude,
			flag_weatherData_Longitude
		]]
		
		df1 = df1.reset_index(drop=True)
	# endregion
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return (df1)


# ######################################################################################################################
def func_replaceColumnNamesIfNeeded(
	dfInput
):
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'Ship', flag_weatherData_Ship)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'Speed', flag_weatherData_SOG)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'Date', flag_weatherData_Date)
	
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'DG1_ACTIVE_POWER', flag_weatherData_DG1POW)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'DG2_ACTIVE_POWER', flag_weatherData_DG2POW)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'DG3_ACTIVE_POWER', flag_weatherData_DG3POW)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'DG4_ACTIVE_POWER', flag_weatherData_DG4POW)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'DG5_ACTIVE_POWER', flag_weatherData_DG5POW)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'DG6_ACTIVE_POWER', flag_weatherData_DG6POW)
	
	return dfInput


# ######################################################################################################################
def func_searchAndReplaceThisColumnName(
	dfInput,
	columnNameToBeSearchedFor,
	newColumnName
):
	if columnNameToBeSearchedFor in dfInput.columns:
		dfInput = dfInput.rename(columns={columnNameToBeSearchedFor: newColumnName})
		print("REPLACE COLUMN HEADER (" + columnNameToBeSearchedFor + ") with (" + newColumnName + ")")
	
	return dfInput


# ######################################################################################################################
def f_readExistingMasterFile(
	thisShipOnly
):
	f_makeThePrintNiceStructured(True, "### READ EXISTING MASTER FILE ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	masterFileThisShipDoesExist = True
	
	df_existingMasterFile = pd.DataFrame()
	
	# masterPath_allShipsWeatherData = r'C:\Users\500095\Desktop\NASA_ARIS_Data\SHIPs\02 SHIP with OpenWeather\xx'
	# stringWeatherFileEnhancement = ' SHIP_and_OpenWeather.csv'

	masterFileName = masterPath_allShipsWeatherData.replace(
		'xx',
		(thisShipOnly + stringWeatherFileEnhancement))
	
	print("READ THE Existing Weather FILE for this SHIP:" + masterFileName)
	
	if os.path.exists(masterFileName):
		df_existingMasterFile = pd.read_csv(masterFileName, sep=';', decimal=',', low_memory=False)
	else:
		print("THIS FILE DOES NOT EXIST; NEXT SHIP")
		masterFileThisShipDoesExist = False
	
	if masterFileThisShipDoesExist:
		df_existingMasterFile[flag_weatherData_Date] = pd.to_datetime(
			df_existingMasterFile[flag_weatherData_Date],
			format='%Y-%m-%d %H:%M'
		) #, format='%d.%m.%Y %H:%M') >> needed in some cases with old data format
	
	
	return df_existingMasterFile, masterFileThisShipDoesExist


# ######################################################################################################################
def f_createCopyOfExistingMasterFileBeforeChangingIt(
	dfInput,
	typeFlag,
	thisShipOnly
):
	f_makeThePrintNiceStructured(True, "### CREATE COPY OF MASTER FILE ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	# masterPath_allShipsWeatherData = r'C:\Users\500095\Desktop\NASA_ARIS_Data\SHIPs\02 SHIP with OpenWeather\xx'
	# stringWeatherFileEnhancement = ' SHIP_and_OpenWeather.csv'
	
	masterFileName = masterPath_allShipsWeatherData.replace(
		'xx',
		('PY_CODE_AUTOBACKUPs' + chr(92) + thisShipOnly + stringWeatherFileEnhancement))
	
	# masterFileName = masterFileName.replace('.csv', ("_" + thisShipOnly + '.csv'))
	
	currentDT = datetime.datetime.now()
	thisTimeNow = str(currentDT.strftime("%Y-%m-%d %H-%M-%S"))
	
	finalNewStringAtTheEndOFTheBackupFile = str('_SAFETY_COPY_' + typeFlag + thisTimeNow + '.csv')
	
	fileName = masterFileName.replace('.csv', finalNewStringAtTheEndOFTheBackupFile)
	
	print("CREATE BACKUP FILE FOR THIS SHIP:" + fileName)
	
	dfInput.to_csv(
		fileName,
		sep=';',
		decimal='.',
		index=False)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])


# ######################################################################################################################
def func_addActualEngineDataIntoWeatherFile(
	df_freshEngineSourceData,
	df_thisShipExisitingWeatherFile,
	shipNameShortCode
):
	df_newMasterDF = pd.DataFrame()
	
	maxDateInExistingFile = df_thisShipExisitingWeatherFile[flag_weatherData_Date].max()
	
	print("LAST DATE @ EXISTING WEATHER DATA @ " + str(maxDateInExistingFile))
	
	df_freshDataSubFile = df_freshEngineSourceData[
		(df_freshEngineSourceData[flag_weatherData_Date] > maxDateInExistingFile) &
		(df_freshEngineSourceData[flag_weatherData_Ship] == shipNameShortCode)
		]
	
	if df_freshDataSubFile.shape[0] > 0:
		print("JEA, new data found")
		print(df_freshDataSubFile.head(5))
		
		df_newMasterDF = pd.concat(
			[df_thisShipExisitingWeatherFile, df_freshDataSubFile],
			sort=True,
			ignore_index=True
		)
		
		masterFileName = masterPath_allShipsWeatherData.replace(
			'xx',
			(shipNameShortCode + stringWeatherFileEnhancement))
		
		if 'Temperature' not in df_newMasterDF.columns:
			df_newMasterDF['Temperature'] = -99
		
		df_newMasterDF = \
			df_newMasterDF[
				[
					'ShipCode',
					'SOG',
					'lastupdateutc',
					'DG1POW',
					'DG2POW',
					'DG3POW',
					'DG4POW',
					'DG5POW',
					'DG6POW',
					'Latitude',
					'Longitude',
					'Temperature',
					'SecondsSinceStart_NASA',
					'SecondsSinceStart_UTC',
					'CloseByNasaData_Temperature',
					'CloseByNasaData_relHumidity',
					'CloseByNasaDataEnthalpy',
					'CloseByNasaDataDistance',
					'Corp_ClimateZone'
				]
			]
		
		df_newMasterDF.to_csv(
			masterFileName,
			sep=';',
			decimal='.',
			index=False)
		
	else:
		print("ups, no data found after the existing max data @ " + str(maxDateInExistingFile))
	
	return df_newMasterDF


# ######################################################################################################################
def f_fillSpeedGapsIfOneDGRunningAndNoLatLongChange(
	dfThisData
):
	cnt = 0
	
	for ap in dfThisData.index:
		if ap > 3:
			if math.isnan(dfThisData.loc[ap, flag_weatherData_SOG]):
				if \
					dfThisData.loc[ap, flag_weatherData_Latitude] == \
					dfThisData.loc[ap - 1, flag_weatherData_Latitude] == \
					dfThisData.loc[ap - 2, flag_weatherData_Latitude]:
					if \
						dfThisData.loc[ap, flag_weatherData_Longitude] == \
						dfThisData.loc[ap - 1, flag_weatherData_Longitude] == \
						dfThisData.loc[ap - 2, flag_weatherData_Longitude]:
						
						# # that is not perfect since smaller ships might have power demand below 10MW when sailing slow, but it is fine
						# # to find at least 95% of cases where lat long is frozen while ship is sailing
						# if \
						# 	dfThisData.loc[ap, flag_weatherData_DG1POW] + \
						# 	dfThisData.loc[ap, flag_weatherData_DG2POW] + \
						# 	dfThisData.loc[ap, flag_weatherData_DG3POW] + \
						# 	dfThisData.loc[ap, flag_weatherData_DG4POW] + \
						# 	dfThisData.loc[ap, flag_weatherData_DG5POW] + \
						# 	dfThisData.loc[ap, flag_weatherData_DG6POW] < 10.000:
						#
						cnt+=1
						
						dfThisData.loc[ap, flag_weatherData_SOG] = 0.01
	
	print("total count of missing 0 Speed: " + str(cnt))
	
	return dfThisData

# ######################################################################################################################
dfSourceData = f_loopAllFilesInThisFolderAndCreateNewSumFile()

dfSourceData = f_fillSpeedGapsIfOneDGRunningAndNoLatLongChange(dfSourceData)

for thisUniqueShip in dfSourceData[flag_weatherData_Ship].unique():
	if dict_analyseTheseShips[dict_shipShortCodesToLongNames[thisUniqueShip]] == 1:
		f_makeThePrintNiceStructured(True, "### NEXT SHIP OUT OF SOURCE FILE: " + thisUniqueShip, "Main Function")
		
		df_thisShipExistingWeatherDataFile, masterFileThisShipDoesExist = f_readExistingMasterFile(thisUniqueShip)
		
		f_createCopyOfExistingMasterFileBeforeChangingIt(
			df_thisShipExistingWeatherDataFile,
			fileCopyBeforeSmartAlgo,
			thisUniqueShip
		)
		
		if masterFileThisShipDoesExist:
			df_enhancedShipsData = func_addActualEngineDataIntoWeatherFile(
				dfSourceData,
				df_thisShipExistingWeatherDataFile,
				thisUniqueShip
			)
			
playsound('hammer_hitwall1.wav')
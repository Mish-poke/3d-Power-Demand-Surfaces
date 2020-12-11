import pandas as pd
import datetime as dt
import time
import inspect
import geopy.distance as gp
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog
import os.path
from playsound import playsound

from _CM_Include import *

import numpy

# region different Vars to control this tool
flag_ONLY_THIS_enhanceShipsRawDataWithWeatherData = True
dict_updateWeatherDataFromThatFile = {
	"dailyAPI_Update": 1,
	"bulkData": 0
}

#TODO Step01 Daily after download of latest weather data >> create new RAW file with all exisiting weather data
flag_ONLY_THIS_createNewFileWithDayByDayDataAggregation = 0

#TODO Step02 Daily after download of latest weather data >> enhance new RAW data with Enthalpy and create final weather data api file with Enthalpy
flag_ONLY_THIS_AddEnthalpyIntoOpenWeatherFile = 0

flag_ONLY_THIS_createJustOneFileWithAllHistoricalLocations = False # was only needed when bulk download from openWeather was received
flag_convertImperialToMetric = False
# endregion

progressPrintCounter = 1000

flag_ship_shipCode = "ShipCode"
flag_ship_load_DG1 = 'DG1POW'
flag_ship_load_DG2 = 'DG2POW'
flag_ship_load_DG3 = 'DG3POW'
flag_ship_load_DG4 = 'DG4POW'
flag_ship_load_DG5 = 'DG5POW'
flag_ship_load_DG6 = 'DG6POW'

flag_ship_timeAbsolut = "lastupdateutc"
flag_ship_timeSecondsSinceNasaStart = 'SecondsSinceStart_NASA'
flag_ship_timeSecondsSinceStartOfUTC = 'SecondsSinceStart_UTC'
flag_ship_latitude = 'Latitude'
flag_ship_longitude = 'Longitude'
flag_ship_weatherZone = 'NASA_Zone'
flag_ship_speed = 'SOG'
flag_ship_Enthalpy = 'Enthalpy'
flag_ship_CloseByNasaData_Distance = 'CloseByNasaDataDistance'
flag_ship_CloseByNasaData_Temperature = 'CloseByNasaData_Temperature'
flag_ship_CloseByNasaData_relHumidity = 'CloseByNasaData_relHumidity'
flag_ship_CloseByNasaData_absHumidity = 'CloseByNasaData_absHumidity'
flag_ship_CloseByNasaData_Enthalpy = 'CloseByNasaDataEnthalpy'
flag_ship_CloseByNasaData_ClimateZone = 'Corp_ClimateZone'


flag_openWeather_dt = 'dt'
flag_openWeather_dt_iso = 'dt_iso'
flag_openWeather_timezone = 'timezone'
flag_openWeather_city_name = 'city_name'
flag_openWeather_lat = 'lat'
flag_openWeather_lon = 'lon'
flag_openWeather_temp = 'temp'
flag_openWeather_feels_like = 'feels_like'
flag_openWeather_temp_min = 'temp_min'
flag_openWeather_temp_max = 'temp_max'
flag_openWeather_pressure = 'pressure'
flag_openWeather_sea_level = 'sea_level'
flag_openWeather_grnd_level = 'grnd_level'
flag_openWeather_humidity = 'humidity'
flag_openWeather_wind_speed = 'wind_speed'
flag_openWeather_wind_deg = 'wind_dg'
flag_openWeather_rain_1h = 'rain_1h'
flag_openWeather_rain_3h = 'rain_3h'
flag_openWeather_snow_1h = 'snow_1h'
flag_openWeather_snow_3h = 'snow_3h'
flag_openWeather_clouds_all = 'clouds_all'
flag_openWeather_weather_id = 'weather_id'
flag_openWeather_weather_main = 'weather_main'
flag_openWeather_weather_description = '_weather_description'
flag_openWeather_weather_icon = 'weather_icon'
flag_openWeather_Enthalpy = 'Enthalpy'

openWeatherMasterFilePath = \
	r'C:\Users\500095\Desktop\NASA_ARIS_Data\OpenWeather\OpenWeather_MASTER_FILE_WithEnthalpy_WithoutDailyUpdateData.csv'


flag_owAPI_DayByDay_Ship = 'Ship'
flag_owAPI_DayByDay_Date = 'Date'
flag_owAPI_DayByDay_hour = 'hour'
flag_owAPI_DayByDay_minute = 'minute'
flag_owAPI_DayByDay_UTC_Seconds = 'UTC_Seconds'
flag_owAPI_DayByDay_Latitude = 'Latitude'
flag_owAPI_DayByDay_Longitude = 'Longitude'
flag_owAPI_DayByDay_ow_temp = 'ow_temp'
flag_owAPI_DayByDay_ow_humidity = 'ow_humidity'
flag_owAPI_DayByDay_ow_pressure = 'ow_pressure'
flag_owAPI_DayByDay_ow_dewPoint = 'ow_dewPoint'
flag_owAPI_DayByDay_ow_feelsLike = 'ow_feelsLike'
flag_owAPI_DayByDay_ow_dt = 'ow_dt'

openWeather_API_MasterFilePath = \
	r'C:\Users\500095\Desktop\NASA_ARIS_Data\OpenWeather\OpenWeather_MASTER_FILE_API_RAW.csv'

openWeather_API_inclEnth_MasterFilePath = \
	r'C:\Users\500095\Desktop\NASA_ARIS_Data\OpenWeather\OpenWeather_MASTER_FILE_API_inclEnthalpy.csv'


flag_owAPI_MasterFile_Ship = "Ship"
flag_owAPI_MasterFile_dt_iso = "dt_iso"
flag_owAPI_MasterFile_hour = "hour"
flag_owAPI_MasterFile_minute = "minute"
flag_owAPI_MasterFile_dt = "dt"
flag_owAPI_MasterFile_lat = "lat"
flag_owAPI_MasterFile_lon = "lon"
flag_owAPI_MasterFile_temp = "temp"
flag_owAPI_MasterFile_humidity = "humidity"
flag_owAPI_MasterFile_pressure = "pressure"
flag_owAPI_MasterFile_ow_dewPoint = "ow_dewPoint"
flag_owAPI_MasterFile_ow_feelsLike ="ow_feelsLike"
flag_owAPI_MasterFile_ow_dt = "ow_dt"
flag_owAPI_MasterFile_temp_max = "temp_max"
flag_owAPI_MasterFile_temp_min = "temp_min"
flag_owAPI_MasterFile_Enthalpy = "Enthalpy"

# print(numpy.version)

dict_doTheDataMatchingWith = {
	'matchWith_NASA': 0,
	'matchWith_OpenWeather': 1
}

from _NASA_Matching_Variables import *

toleranceInSeconds = 5400 #60min
maxAllowedDistance = 150

toleranceInSeconds_openWeatherData = 600
maxAllowedDistance_openWeatherData = 50

filter_MIN_Speed = -0.5
filter_MAX_Speed = 0.5

# ######################################################################################################################
def f_makeThePrintNiceStructured(
	doThePrint,
	printThisText,
	recentFunction
):
	if FORCE_fullDebugAllComments or \
		(doThePrint and avoidAnyComments == False):
		print("############################################")
		print(printThisText + " in f: " + recentFunction)


# ######################################################################################################################
def f_doTheTimeMeasurementInThisFunction(
	startTime,
	flagType,
	timeMeasurementDoneForThisFunction
):
	if flagType == flag_timeStart:
		startTime = time.perf_counter()
	else:
		endTime = time.perf_counter()
		print(f" TIME ELAPSED {endTime - startTime:0.4f} seconds in Function: " + timeMeasurementDoneForThisFunction)
	
	return startTime

# ######################################################################################################################
def func_findCorrectZoneForEveryShipsSample(
	df,
	dataFlag
):
	df[flag_ship_weatherZone] = df.apply(lambda x: func_detect_NASA_AIRS_ZoneFile(
		x[flag_ship_latitude],
		x[flag_ship_longitude]
	), axis=1)
	
	return df


# ######################################################################################################################
def func_detect_NASA_AIRS_ZoneFile(
	latitude,
	longitude
):
	detected_zone = ''
	
	if pd.isnull(latitude) or pd.isnull(longitude):
		detected_zone = flag_noZoneDetected
	else:
		for zone in list(dict_zones_areas.keys()):
			left_longitude = dict_zones_areas[zone][0][0]
			right_longitude = dict_zones_areas[zone][1][0]
			lower_latitude = dict_zones_areas[zone][0][1]
			upper_latitude = dict_zones_areas[zone][1][1]
			if \
				func_thisPointIsInsideTheZoneBoundary(latitude, lower_latitude, upper_latitude) and \
				func_thisPointIsInsideTheZoneBoundary(longitude, left_longitude, right_longitude):
				
				detected_zone = zone
				break
			else:
				detected_zone = flag_noZoneDetected
	
	return detected_zone


# ######################################################################################################################
def func_thisPointIsInsideTheZoneBoundary(point, left_boundary, right_boundary):
	verification = False
	if left_boundary <= point <= right_boundary:
		verification = True
	return verification


# ######################################################################################################################
def func_addSecondsSinceStartOfNasaCounting(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### func_addSecondsSinceStartOfNasaCounting ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_ship_timeSecondsSinceNasaStart] = dfInput.apply(lambda x: func_countSecondsThisDP(
		x[flag_ship_timeAbsolut],
		'nasa'
	), axis=1)
	
	dfInput[flag_ship_timeSecondsSinceStartOfUTC] = dfInput.apply(lambda x: func_countSecondsThisDP(
		x[flag_ship_timeAbsolut],
		'utc'
	), axis=1)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_countSecondsThisDP(
	thisDate,
	secondFlag
):
	if secondFlag == 'nasa':
		timeDelta = thisDate - initial_date
	
	if secondFlag == 'utc':
		timeDelta = thisDate - initial_date_utc
	
	seconds = round(timeDelta.total_seconds(), 0)
	
	return seconds


# ######################################################################################################################
def func_doSomeTypeCasts(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	# dfInput[flag_ship_timeAbsolut] = pd.to_datetime(dfInput[flag_ship_timeAbsolut])
	
	# dfInput[flag_ship_timeAbsolut] = dfInput[flag_ship_timeAbsolut].astype('datetime64[ns]')
	
	# dfInput[flag_ship_timeAbsolut] = pd.to_datetime(dfInput[flag_ship_timeAbsolut], format='%d.%m.%Y %H:%M')
	
	dfInput[flag_ship_timeAbsolut] = pd.to_datetime(dfInput[flag_ship_timeAbsolut], format='%Y-%m-%d %H:%M')
	
	dfInput[flag_ship_latitude] = dfInput[flag_ship_latitude].astype(float)
	dfInput[flag_ship_longitude] = dfInput[flag_ship_longitude].astype(float)
	dfInput[flag_ship_speed] = dfInput[flag_ship_speed].astype(float)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_readMasterFile(
):
	f_makeThePrintNiceStructured(True, "### ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	thisDF = pd.DataFrame()
	
	root = tk.Tk()
	root.withdraw()
	file = filedialog.askopenfilenames(
		initialdir="C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\SHIPs\\02 SHIP with OpenWeather",
		title='Pick raw data that should be updated with weather data'
	)
	
	list_file_root = list(root.tk.splitlist(file))
	file_root = list_file_root[0]
	thisDF = pd.read_csv(file_root, sep=";", decimal=",", low_memory=False)
	# thisDF = pd.read_csv(file_root, sep=",", decimal=".", low_memory=False)
	
	thisDF[flag_ship_speed] = thisDF[flag_ship_speed].astype(str)
	thisDF[flag_ship_speed] = thisDF[flag_ship_speed].str.replace("'", '')
	thisDF[flag_ship_speed] = thisDF[flag_ship_speed].astype(float)
	
	thisDF = f_doTheTypeCastForThisColumn(thisDF, flag_ship_latitude)
	thisDF = f_doTheTypeCastForThisColumn(thisDF, flag_ship_longitude)
	thisDF = f_doTheTypeCastForThisColumn(thisDF, flag_ship_speed)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return thisDF


# ######################################################################################################################
def f_doTheTypeCastForThisColumn(
   dfInput,
   thisFlag
):
	if thisFlag in dfInput.columns:
		dfInput[thisFlag] = dfInput[thisFlag].astype(str)
		dfInput[thisFlag] = dfInput[thisFlag].str.replace("'", '')
		dfInput[thisFlag] = dfInput[thisFlag].str.replace(',', '.')
		dfInput[thisFlag] = dfInput[thisFlag].astype(float)
	
	return dfInput


# ######################################################################################################################
def func_loadThisZoneFile(
	thisZone
):
	dfZone = pd.DataFrame()
	
	print("LOAD ZONE DATA for: ", thisZone)
	# print("This zone path: " + dict_zone_paths[thisZone])
	selfMadePath = masterPath + chr(92) + thisZone + ".csv"
	# print("self made path: " + selfMadePath)
	
	dfZone = pd.read_csv(
		# dict_zone_paths[thisZone],
		selfMadePath,
		sep=';', decimal='.',
		low_memory=False
		#dtype={flag_zone_Enthalpy: float}
	)

	print(dfZone.head(5))
	
	dfZone = dfZone[dfZone[flag_zone_SurfTemperature] >= -10]
	
	dfZone = f_doTheTypeCastForThisColumn(dfZone, flag_zone_SurfTemperature)
	dfZone = f_doTheTypeCastForThisColumn(dfZone, flag_zone_SurfRelHumidity)
	dfZone = f_doTheTypeCastForThisColumn(dfZone, flag_zone_SurfAbsHumidity)
	dfZone = f_doTheTypeCastForThisColumn(dfZone, flag_zone_Enthalpy)
	dfZone = f_doTheTypeCastForThisColumn(dfZone, flag_zone_Latitude)
	dfZone = f_doTheTypeCastForThisColumn(dfZone, flag_zone_Longitude)
	
	return dfZone
   

# ######################################################################################################################
def func_matchShipAndNasaData(
	dfShip,
	dfZone,
	thisZone
):
   f_makeThePrintNiceStructured(True, "### func_matchShipAndNasaData for " + thisZone, inspect.stack()[0][3])
   startTime = time
   startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
   print("ZONE Length:", str(len(dfZone)))
	
   validSamplesFound = 0
   
   dfShip = dfShip[dfShip[flag_ship_weatherZone] == thisZone]
   
   dfShip, dfZone = func_MatchFileLengths(dfShip, dfZone)
   
   apIncreaseIfNotFound = 10
   
   for ap in dfShip.index:
      subZone = func_getSubZoneAroundThisShipsTimeStamp(ap, dfShip, dfZone)
      
      if len(subZone) == 0:
         ap = ap + apIncreaseIfNotFound
         continue
      
      # print("found something ")
      closestPoint_Distance, \
      closestPoint_Temperature, \
      closestPoint_relativeHumidity, \
      closestPoint_AbsolutHumidity, \
      closestPoint_Enthalpy = func_getWeatherDataOfClosestPoint(ap, dfShip, subZone)
      
      if closestPoint_Distance < maxAllowedDistance:
         validSamplesFound += 1
      	
         dfShip.loc[ap, flag_ship_CloseByNasaData_Distance] = round(closestPoint_Distance, 3)
         dfShip.loc[ap, flag_ship_CloseByNasaData_Temperature] = round(closestPoint_Temperature, 3)
         dfShip.loc[ap, flag_ship_CloseByNasaData_relHumidity] = round(closestPoint_relativeHumidity, 3)
         dfShip.loc[ap, flag_ship_CloseByNasaData_absHumidity] = round(closestPoint_AbsolutHumidity, 3)
         dfShip.loc[ap, flag_ship_CloseByNasaData_Enthalpy] = round(closestPoint_Enthalpy, 3)
         dfShip.loc[ap, flag_ship_CloseByNasaData_ClimateZone] = \
            func_getClimateZone(closestPoint_Temperature, closestPoint_Enthalpy)
   
   print("VALID samples found for zone " + thisZone + " = " + str(validSamplesFound))
   
   startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])

   return dfShip


# ######################################################################################################################
def func_getClimateZone(
	temp,
	h
):
   if temp <= 13:
      return 1
   
   if 13 < temp <= 25 and h <= 12:
      return 2
   
   if 18 < temp <= 25 and 12 < h <= 15:
      return 3
   
   if 25 < temp <= 30 and h <= 15:
      return 3
   
   if 21.5 < temp <= 30 and 15 < h <= 18:
      return 4
   
   if temp > 30 and h <= 18:
      return 4
      
   if h > 18:
      return 5
   
   return 99


# ######################################################################################################################
def func_getWeatherDataOfClosestPoint(
	ap,
	dfShip,
	subZone
):
	origin = (dfShip.loc[ap, flag_ship_latitude], dfShip.loc[ap, flag_ship_longitude])
	
	closestPoint_Distance = maxAllowedDistance
	closestPoint_Temperature = 0
	closestPoint_relativeHumidity = 0
	closestPoint_AbsolutHumidity = 0
	closestPoint_Enthalpy = 0
	
	for apZone in subZone.index:
		dist = (subZone.loc[apZone, flag_zone_Latitude], subZone.loc[apZone, flag_zone_Longitude])
		
		thisDistance = gp.geodesic(origin, dist).miles / 1.15078
		
		if thisDistance < closestPoint_Distance:
			# print("FOUND something! with a distance of only " + str(thisDistance))
			closestPoint_Distance = thisDistance
			closestPoint_Temperature = subZone.loc[apZone, flag_zone_SurfTemperature]
			closestPoint_relativeHumidity = subZone.loc[apZone, flag_zone_SurfRelHumidity]
			closestPoint_AbsolutHumidity = subZone.loc[apZone, flag_zone_SurfAbsHumidity]
			closestPoint_Enthalpy = subZone.loc[apZone, flag_zone_Enthalpy]
	
	return \
		closestPoint_Distance, \
		closestPoint_Temperature, \
		closestPoint_relativeHumidity, \
		closestPoint_AbsolutHumidity, \
		closestPoint_Enthalpy


# ######################################################################################################################
def func_getSubZoneAroundThisShipsTimeStamp(
	ap,
	dfShip,
	dfZone
):
	shipsTimeInSeconds = dfShip.loc[ap, flag_ship_timeSecondsSinceNasaStart]
	
	subZone = dfZone[
		(dfZone[flag_zone_timeSeconds] >= shipsTimeInSeconds - toleranceInSeconds) & \
		(dfZone[flag_zone_timeSeconds] <= shipsTimeInSeconds + toleranceInSeconds)
		]
	
	return subZone


# ######################################################################################################################
def func_thisSetDoesNotBelongIntoCurrentZone(
	thisSampleZone,
	currentMasterZone
):
	if thisSampleZone is not currentMasterZone:
		return False
	
	return True

# ######################################################################################################################
def func_MatchFileLengths(
	dfInput,
	dfZone
):
	dfZone = dfZone[
		(dfZone[flag_zone_timeSeconds] >= dfInput[flag_ship_timeSecondsSinceNasaStart].min()) &
		(dfZone[flag_zone_timeSeconds] <= dfInput[flag_ship_timeSecondsSinceNasaStart].max())
		]
	
	dfInput = dfInput[
		(dfInput[flag_ship_timeSecondsSinceNasaStart] >= dfZone[flag_zone_timeSeconds].min()) &
		(dfInput[flag_ship_timeSecondsSinceNasaStart] <= dfZone[flag_zone_timeSeconds].max())
		]
	
	# print("START DATE SHIP: " + str(dfInput[flag_ship_timeAbsolut].min()))
	# print("END DATE SHIP: " + str(dfInput[flag_ship_timeAbsolut].max()))
	#
	# print("START DATE NASA ZONE: " + str(dfZone[flag_zone_Date].min()))
	# print("END DATE NASA ZONE: " + str(dfZone[flag_zone_Date].max()))
	
	return dfInput, dfZone


# ######################################################################################################################
def func_readShipsDataMasterFileAndDoInitialTypeCasts(

):
	f_makeThePrintNiceStructured(True, "### ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfFinal = func_readMasterFile()
	
	dfFinal = func_doSomeTypeCasts(dfFinal)
	
	dfFinal = dfFinal[(dfFinal[flag_ship_speed] >= filter_MIN_Speed) & (dfFinal[flag_ship_speed] <= filter_MAX_Speed)]
	
	dfFinal.dropna(axis=0, subset=[flag_ship_latitude], inplace=True)
	dfFinal = dfFinal.reset_index(drop=True)
	
	dfFinal = dfFinal.sort_values(by=[flag_ship_timeAbsolut])
	dfFinal = dfFinal.reset_index(drop=True)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfFinal


# ######################################################################################################################
def func_readShipsDataMasterFileAndDoInitialTypeCastsNew(
	file_root
):
	f_makeThePrintNiceStructured(True, "### ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfFinal = pd.read_csv(file_root, sep=";", decimal=",", low_memory=False)
	# dfFinal = pd.read_csv(file_root, sep=",", decimal=".", low_memory=False)
	
	dfFinal[flag_ship_speed] = dfFinal[flag_ship_speed].astype(str)
	dfFinal[flag_ship_speed] = dfFinal[flag_ship_speed].str.replace("'", '')
	dfFinal[flag_ship_speed] = dfFinal[flag_ship_speed].astype(float)
	
	dfFinal = f_doTheTypeCastForThisColumn(dfFinal, flag_ship_latitude)
	dfFinal = f_doTheTypeCastForThisColumn(dfFinal, flag_ship_longitude)
	dfFinal = f_doTheTypeCastForThisColumn(dfFinal, flag_ship_speed)
	
	dfFinal = func_doSomeTypeCasts(dfFinal)
	
	dfFinal = dfFinal[(dfFinal[flag_ship_speed] >= filter_MIN_Speed) & (dfFinal[flag_ship_speed] <= filter_MAX_Speed)]
	
	dfFinal.dropna(axis=0, subset=[flag_ship_latitude], inplace=True)
	dfFinal = dfFinal.reset_index(drop=True)
	
	dfFinal = dfFinal.sort_values(by=[flag_ship_timeAbsolut])
	dfFinal = dfFinal.reset_index(drop=True)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfFinal

# ######################################################################################################################
def func_addSecondsAndZone(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### START ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput = func_addSecondsSinceStartOfNasaCounting(dfInput)
	
	if dict_doTheDataMatchingWith['matchWith_NASA']:
		dfInput = func_findCorrectZoneForEveryShipsSample(dfInput, flag_historic)
	
		dfInput = func_findCorrectZoneForEveryShipsSample(dfInput, flag_NearRealTime)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_loopAllZonesAndAddValuesIntoMasterDF(
   dfInput
):
	dfFinal = pd.DataFrame()
	
	for thisZone in dfInput[flag_ship_weatherZone].unique():
		print(thisZone)
	
	for thisZone in dfInput[flag_ship_weatherZone].unique():
		if thisZone is not flag_noZoneDetected:
			thisZoneFilePath = masterPath + chr(92) + thisZone + ".csv"
			print(chr(10) + " >>> NEXT ZONE : " + thisZone)
			print("   READ FILE IN PATH: " + thisZoneFilePath)
			if os.path.exists(thisZoneFilePath):
				dfZone = func_loadThisZoneFile(thisZone)
			
				# if thisZone == 'SA_Buenos_Aires' or thisZone == 'Canaries_Main':
				dfFinalSubset = func_matchShipAndNasaData(dfInput, dfZone, thisZone)
				dfFinal = pd.concat([dfFinal, dfFinalSubset])
			else:
				print("FILE DOES NOT EXIST!! NEXT FILE")
	
	return dfFinal


# ######################################################################################################################
def func_exportFinalDataset(
	dfFinal
):
	dfFinal[flag_ship_load_DG1] = dfFinal[flag_ship_load_DG1].astype(float)
	dfFinal[flag_ship_load_DG2] = dfFinal[flag_ship_load_DG2].astype(float)
	dfFinal[flag_ship_load_DG3] = dfFinal[flag_ship_load_DG3].astype(float)
	dfFinal[flag_ship_load_DG4] = dfFinal[flag_ship_load_DG4].astype(float)
	dfFinal[flag_ship_load_DG5] = dfFinal[flag_ship_load_DG5].astype(float)
	dfFinal[flag_ship_load_DG6] = dfFinal[flag_ship_load_DG6].astype(float)
	
	dfFinal[flag_ship_load_DG1] = round(dfFinal[flag_ship_load_DG1], 0)
	dfFinal[flag_ship_load_DG2] = round(dfFinal[flag_ship_load_DG2], 0)
	dfFinal[flag_ship_load_DG3] = round(dfFinal[flag_ship_load_DG3], 0)
	dfFinal[flag_ship_load_DG4] = round(dfFinal[flag_ship_load_DG4], 0)
	dfFinal[flag_ship_load_DG5] = round(dfFinal[flag_ship_load_DG5], 0)
	dfFinal[flag_ship_load_DG6] = round(dfFinal[flag_ship_load_DG6], 0)
	
	dfFinal.to_csv(
		'SHIP_and_NASA.csv',
		sep=';',
		decimal='.',
		index=False
	)


# ######################################################################################################################
def func_getIndexRangeForThisShipsDate(
	dfInput
):
	subDF = dfInput
	
	print("   data index this ship between " + str(subDF.index.min()) + " and " + str(subDF.index.max()))
	
	return subDF.index.min(), subDF.index.max()


# ######################################################################################################################
def func_printProgress(
	ap,
	minIndexThisShip,
	maxIndexThisShip,
	functionName
):
	print(functionName + " progress @ " + str(ap) + " RANGE: (" + str(minIndexThisShip) + " to " + str(maxIndexThisShip) + ")")


# ######################################################################################################################
def func_divisonPossible(number, divisor):
	return number % divisor == 0


######################################################################################################################
def func_replaceNanInThisColumn(
	dfInput,
	columnFlag,
	newNanValue
):
	dfInput[columnFlag].fillna(newNanValue, inplace=True)
	
	return dfInput


# ######################################################################################################################
def func_loopActualDataWithOpenWeather(
	df_thisShipData,
	shipShortCode
):
	f_makeThePrintNiceStructured(True, "### ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	df_openWeather = func_readOpenWeatherSourceFile(shipShortCode)
	
	if flag_ship_CloseByNasaData_Temperature in df_thisShipData.columns:
		df_thisShipData = func_replaceNanInThisColumn(df_thisShipData, flag_ship_CloseByNasaData_Temperature, -99)
	else:
		df_thisShipData[flag_ship_CloseByNasaData_Temperature] = -99
	
	minIndexThisShip, maxIndexThisShip = func_getIndexRangeForThisShipsDate(df_thisShipData)
	
	datapointsFound = 0
	
	for ap in df_thisShipData.index:
		if func_divisonPossible(ap, progressPrintCounter):
			func_printProgress(ap, minIndexThisShip, maxIndexThisShip, inspect.stack()[0][3])
			print("datapointsFound so far " + str(datapointsFound))
		
		if df_thisShipData.loc[ap, flag_ship_CloseByNasaData_Temperature] == - 99:
			dfSubsetWeather = func_getSubsetOfWeatherDataThisTimeframe(
				df_thisShipData.loc[ap, flag_ship_timeSecondsSinceStartOfUTC],
				df_thisShipData.loc[ap, flag_ship_latitude],
				df_thisShipData.loc[ap, flag_ship_longitude],
				df_openWeather
			)
			
			if dfSubsetWeather.shape[0] != 0:
				# print("YEA, some data @ " + str(dfInput.loc[ap, flag_ship_timeAbsolut]))
				
				df_thisShipData, datapointsFound = \
					func_findMatchingWeatherDataIfAny(ap, df_thisShipData, dfSubsetWeather, datapointsFound)
				
			# else:
			# 	print("no data @ " + str(dfInput.loc[ap, flag_ship_timeAbsolut]))
	
	df_thisShipData = df_thisShipData[df_thisShipData[flag_ship_CloseByNasaData_Temperature] != -99]
	
	df_thisShipData = df_thisShipData.sort_values(by=[flag_ship_timeSecondsSinceStartOfUTC])
	
	print("TOTAL datapointsFound " + str(datapointsFound))
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return df_thisShipData


# ######################################################################################################################
def func_readOpenWeatherSourceFile(
	shipShortCode
):

	print("READ THE weather file including Enthalpy from here " + openWeatherMasterFilePath)
	if dict_updateWeatherDataFromThatFile["dailyAPI_Update"] == 1:
		df_openWeather = pd.read_csv(openWeather_API_inclEnth_MasterFilePath, sep=";", decimal=".")
		print("LEN TOTAL API WEATHER MASTER FILE: " + str(len(df_openWeather[flag_owAPI_MasterFile_Ship])))
		df_openWeather = df_openWeather[df_openWeather[flag_owAPI_MasterFile_Ship] == shipShortCode]
		print("LEN TOTAL API WEATHER MASTER FILE FOR THIS SHIP " + shipShortCode + " only: " + str(
			len(df_openWeather[flag_owAPI_MasterFile_Ship])))
	
	if dict_updateWeatherDataFromThatFile["bulkData"] == 1:
		df_openWeather = pd.read_csv(openWeatherMasterFilePath, sep=";", decimal=".")
	
	return df_openWeather


# ######################################################################################################################
def func_findMatchingWeatherDataIfAny(
	ap,
	dfInput,
	dfSubsetWeather,
	datapointsFound
):
	thisSecond = dfInput.loc[ap, flag_ship_timeSecondsSinceStartOfUTC]
	
	origin = (dfInput.loc[ap, flag_ship_latitude], dfInput.loc[ap, flag_ship_longitude])
	
	for thisAP in dfSubsetWeather.index:
		dist = (dfSubsetWeather.loc[thisAP, flag_openWeather_lat], dfSubsetWeather.loc[thisAP, flag_openWeather_lon])
		
		thisDistance = gp.geodesic(origin, dist).miles / 1.15078
		
		# print("thisDistance: " + str(thisDistance))
		
		if thisDistance < maxAllowedDistance_openWeatherData:
			datapointsFound += 1
			# print(str(dfInput.loc[ap, flag_ship_timeAbsolut]) +  " >>> PROPER WEATHER DATA FOUND")
			dfInput.loc[
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] >= thisSecond) &
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] <= thisSecond + toleranceInSeconds_openWeatherData),
				flag_ship_CloseByNasaData_Temperature
			] = round(dfSubsetWeather.loc[thisAP, flag_openWeather_temp], 2)
			
			dfInput.loc[
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] >= thisSecond) &
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] <= thisSecond + toleranceInSeconds_openWeatherData),
				flag_ship_CloseByNasaData_relHumidity
			] = round(dfSubsetWeather.loc[thisAP, flag_openWeather_humidity], 2)
			
			dfInput.loc[
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] >= thisSecond) &
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] <= thisSecond + toleranceInSeconds_openWeatherData),
				flag_ship_CloseByNasaData_Enthalpy
			] = round(dfSubsetWeather.loc[thisAP, flag_openWeather_Enthalpy], 2)
			
			dfInput.loc[
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] >= thisSecond) &
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] <= thisSecond + toleranceInSeconds_openWeatherData),
				flag_ship_CloseByNasaData_Distance
			] = thisDistance
			
			dfInput.loc[
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] >= thisSecond) &
				(dfInput[flag_ship_timeSecondsSinceStartOfUTC] <= thisSecond + toleranceInSeconds_openWeatherData),
				flag_ship_CloseByNasaData_ClimateZone
			] = func_getClimateZone(
					dfSubsetWeather.loc[thisAP, flag_openWeather_temp],
					dfSubsetWeather.loc[thisAP, flag_openWeather_Enthalpy]
				)
		# else:
		# 	print("DISTANCE TOOO BIG")
	
	return dfInput, datapointsFound
	
# ######################################################################################################################
def func_getSubsetOfWeatherDataThisTimeframe(
	refSeconds,
	refLatitude,
	refLongitude,
	df_fullSetWeatherData
):
	dfWeatherSubset = df_fullSetWeatherData[
		(df_fullSetWeatherData[flag_openWeather_dt] >= refSeconds - toleranceInSeconds_openWeatherData) & \
		(df_fullSetWeatherData[flag_openWeather_dt] < refSeconds + toleranceInSeconds_openWeatherData) & \
		(df_fullSetWeatherData[flag_openWeather_lat] >= refLatitude - 1) & \
		(df_fullSetWeatherData[flag_openWeather_lat] <= refLatitude + 1) & \
		(df_fullSetWeatherData[flag_openWeather_lon] >= refLongitude - 1) & \
		(df_fullSetWeatherData[flag_openWeather_lon] <= refLongitude + 1)
	]
	
	return dfWeatherSubset


# ######################################################################################################################
def f_readAllOWFilesAndCreateOneDF():
	df1 = pd.DataFrame()
	
	filesToBeTreated = filedialog.askopenfilenames()
	
	useFilePicker = True
	# region LOOP Files and bring the together in one dataframe
	if useFilePicker:
		for subFile in filesToBeTreated:
			print("read " + subFile)
			
			if df1.shape[0] == 0:  # df1 is empty
				df1 = pd.read_csv(subFile, sep=',', low_memory=False)
					
			else:
				df2 = pd.read_csv(subFile, sep=',', low_memory=False)
					
				df1 = pd.concat([df1, df2])
		
		df1 = df1[df1['dt'] >= 1546300800]
		
		df1 = df1.reset_index(drop=True)
		
		if flag_convertImperialToMetric:
			df1[flag_openWeather_temp] = df1[flag_openWeather_temp]-273.15
			df1[flag_openWeather_feels_like] = df1[flag_openWeather_feels_like] - 273.15
			df1[flag_openWeather_temp_min] = df1[flag_openWeather_temp_min] - 273.15
			df1[flag_openWeather_temp_max] = df1[flag_openWeather_temp_max] - 273.15
			
		print(df1.head(10))
		
		df1 = df1 [
			[
				flag_openWeather_dt,
				flag_openWeather_dt_iso,
				flag_openWeather_city_name,
				flag_openWeather_lat,
				flag_openWeather_lon,
				flag_openWeather_temp,
				flag_openWeather_temp_min,
				flag_openWeather_temp_max,
				flag_openWeather_pressure,
				flag_openWeather_humidity
			]
		]
		
		df1.to_csv(
			"allData.csv",
			sep=';',
			index=False)
		
	return df1


# ######################################################################################################################
def func_addOrUpdateEnthalpy(
):
	print(chr(10) + " ADD ENTHALPY INTO OPEN WEATHER RAW DATA. NOTHING ELSE")
	
	root = tk.Tk()
	root.withdraw()
	file = filedialog.askopenfilenames(parent=root, title='Choose a file')
	list_file_root = list(root.tk.splitlist(file))
	file_root = list_file_root[0]
	df_openWeather = pd.read_csv(file_root, sep=";", decimal=".", low_memory=False)
	
	df_openWeather[flag_openWeather_Enthalpy] = \
		(
			(1.007 * df_openWeather[flag_openWeather_temp] - 0.026) + \
			(2502 - 0.538 * df_openWeather[flag_openWeather_temp]) * \
			0.622 / (
				(df_openWeather[flag_openWeather_pressure] * 100) /
				(df_openWeather[flag_openWeather_humidity] / 100 * pow(10, (
					0.7859 + 0.03477 * df_openWeather[flag_openWeather_temp]) / (1 + 0.00412 * df_openWeather[
					flag_openWeather_temp]) + 2) - 0.378)
			)
		) / 4.184
	
	df_openWeather.to_csv(
		openWeather_API_inclEnth_MasterFilePath,
		sep=';',
		decimal='.',
		index=False
	)
	
# ######################################################################################################################
def func_loopAllDayByDayFilesAndCreateNewSummaryFile():
	df1 = pd.DataFrame()
	
	filesToBeTreated = filedialog.askopenfilenames(
		initialdir="C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\OpenWeather\\Daily_API_Updates",
		title='pick files that you want to aggregate into the aggregated open weather file'
	)
	
	useFilePicker = True
	# region LOOP Files and bring the together in one dataframe
	if useFilePicker:
		for subFile in filesToBeTreated:
			print("read " + subFile)
			
			if df1.shape[0] == 0:  # df1 is empty
				df1 = pd.read_csv(subFile, sep=';', decimal=",", low_memory=False)
			else:
				df2 = pd.read_csv(subFile, sep=';', decimal=",", low_memory=False)
				
				df1 = pd.concat([df1, df2])
		
		df1[flag_owAPI_DayByDay_Date] = pd.to_datetime(df1[flag_owAPI_DayByDay_Date])
		
		df1 = df1.round(decimals=5)
		
		df1 = df1.sort_values(
			[flag_owAPI_DayByDay_Ship, flag_owAPI_DayByDay_Date],
			ascending=[True, True]
		)
		
		df1 = df1.reset_index(drop=True)
	# endregion
	
	df1 = func_convertColumnNamesToPreviousStandard(df1)
	
	if flag_openWeather_temp_max not in df1.columns:
		df1[flag_openWeather_temp_max] = -99
	
	if flag_openWeather_temp_min not in df1.columns:
		df1[flag_openWeather_temp_min] = -99
		
	
	df1.to_csv(
		openWeather_API_MasterFilePath,
		sep=";",
		decimal=".",
		index=False
	)
	

# ######################################################################################################################
def func_convertColumnNamesToPreviousStandard(
	dfInput
):
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'UTC_Seconds', flag_openWeather_dt)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'Date', flag_openWeather_dt_iso)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'Latitude', flag_openWeather_lat)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'Longitude', flag_openWeather_lon)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'ow_humidity', flag_openWeather_humidity)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'ow_pressure', flag_openWeather_pressure)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, 'ow_temp', flag_openWeather_temp)
	
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


# #####################################################################################################################
def func_hardStopRightNow():
	playsound('hammer_hitwall1.wav')
	
	print("### END OF EVERYTHING >>> EXIT CALL")
	exit()
	
	
# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################

if flag_ONLY_THIS_createNewFileWithDayByDayDataAggregation:
	func_loopAllDayByDayFilesAndCreateNewSummaryFile()
	func_hardStopRightNow()

if flag_ONLY_THIS_createJustOneFileWithAllHistoricalLocations:
	df_allDataFromOW = f_readAllOWFilesAndCreateOneDF()
	func_hardStopRightNow()

if flag_ONLY_THIS_AddEnthalpyIntoOpenWeatherFile:
	func_addOrUpdateEnthalpy()
	func_hardStopRightNow()

if flag_ONLY_THIS_enhanceShipsRawDataWithWeatherData:
	
	listOfShipsToBeUpdated = filedialog.askopenfilenames(
		initialdir="C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\SHIPs\\02 SHIP with OpenWeather",
		title='Pick raw data that should be updated with weather data'
	)
	
	for df_thisShip in listOfShipsToBeUpdated:
		print(chr(10))
		print("############################################")
		print("### TREAT THE NEXT SHIP >>> " + df_thisShip)
		# df_thisShip = func_readShipsDataMasterFileAndDoInitialTypeCasts()
		
		df_thisShip = func_readShipsDataMasterFileAndDoInitialTypeCastsNew(df_thisShip)
		
		df_thisShip = func_addSecondsAndZone(df_thisShip)
		
		if dict_doTheDataMatchingWith['matchWith_NASA']:
			df_thisShip = func_loopAllZonesAndAddValuesIntoMasterDF(dfFinal)
		
		if dict_doTheDataMatchingWith['matchWith_OpenWeather']:
			shipShortCode = df_thisShip.loc[1, flag_ship_shipCode]
			
			df_thisShip = func_loopActualDataWithOpenWeather(df_thisShip, shipShortCode)
			
			fileName = \
				"C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\SHIPs\\02 SHIP with OpenWeather\\" + \
				shipShortCode + " " + \
				"SHIP_and_OpenWeather.csv"
			
			df_thisShip.to_csv(
				fileName,
				sep=';',
				decimal='.',
				index=False
			)
		
	# func_exportFinalDataset(df_thisShip)
	
	func_hardStopRightNow()

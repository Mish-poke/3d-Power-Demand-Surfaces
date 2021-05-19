# Brief Description
# This script is needed daily (at least not later than 5 days after the download from the Neptune source) to update
# the lat long values with the respective weather at this point in time. this script is using the rapid-api interface
# into the openweather api

import pandas as pd
import requests
from tkinter import filedialog
import time
from playsound import playsound

from _DAILY_AAQS_Variables import *

flag_finalFile_UTC = "UTC_Seconds"
flag_finalFile_Minute = "minute"
flag_finalFile_Hour = "hour"

flag_viaApiCall_Temp = "ow_temp"
flag_viaApiCall_Humidity = "ow_humidity"
flag_viaApiCall_Pressure = "ow_pressure"
flag_viaApiCall_dewPoint = "ow_dewPoint"
flag_viaApiCall_feelsLike = "ow_feelsLike"
flag_viaApiCall_dt = "ow_dt"

firstTimeTick = datetime.datetime(1970, 1, 1, 0, 0, 0)

# ######################################################################################################################
def func_readWeatherDataViaApiCall(
   dfInput
):
    url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"
    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "376b166a5amsh5a2867fbb758b0dp1c22cejsn222c776ad087"
    }
    # querystring = {"lat":"37.774929","lon":"-122.419418","dt":"1593610932", "units":"metric"}
    
    dateStringForFileName = ""
    
    dfInput[flag_viaApiCall_Temp] = 0
    dfInput[flag_viaApiCall_Humidity] = 0
    dfInput[flag_viaApiCall_Pressure] = 0
    dfInput[flag_viaApiCall_dewPoint] = 0
    dfInput[flag_viaApiCall_feelsLike] = 0
    dfInput[flag_viaApiCall_dt] = 0
    
    print(str(len(dfInput)))
    
    apStart = -1
    apCount = 999
    
    for ap in dfInput.index:
        if ap > apStart and ap <= apStart + apCount:
            time.sleep(0.75)
            
            print(chr(10) + str(ap) + " SHIP: " + dfInput.loc[ap, flag_finalFile_Ship] + " @ " + str(dfInput.loc[ap, flag_finalFile_Date]))
            
            if dateStringForFileName == "":
                dateStringForFileName = str(dfInput.loc[ap, flag_finalFile_Date])[:10]
                print("dateStringForFileName: " + dateStringForFileName)
            
            querystring = {
                "lat": dfInput.loc[ap, flag_finalFile_Latitude],
                "lon": dfInput.loc[ap, flag_finalFile_Longitude],
                "dt": dfInput.loc[ap, flag_finalFile_UTC],
                "units": "metric"}
            
            print(querystring)
            
            response = requests.request("GET", url, headers=headers, params=querystring)
            
            thisResult = response.json()
            
            print(thisResult)
            
            # print(chr(10) + " ### response.headers")
            # print(response.headers)
            # # print(response(lat))
            # print(chr(10) + " ### response.text")
            # print(response.text)
            #
            # print(chr(10) + " ### thisResult[hourly]: ")
            # print(thisResult["hourly"])
            #
            # print(chr(10) + " ### thisResult[hourly][0]: ")
            # print(thisResult["hourly"][0])
            #
            # print(chr(10) + " ### thisResult[hourly][0][temp]: ")
            # print(thisResult["hourly"][0]['temp'])
            #
            # print(chr(10) + " ### thisResult[hourly][1]: ")
            # print(thisResult["hourly"][1])
            #
            # print(chr(10) + " ### thisResult[hourly][1][temp]: ")
            # print(thisResult["hourly"][1]['temp'])
            
            print(
                "TEMP: " + str(thisResult["hourly"][dfInput.loc[ap, flag_finalFile_Hour]]['temp']) +
                "// Humidity: " + str(thisResult["hourly"][dfInput.loc[ap, flag_finalFile_Hour]]['humidity']) +
                "// pressure: " + str(thisResult["hourly"][dfInput.loc[ap, flag_finalFile_Hour]]['pressure']) +
                "// dew_point: " + str(thisResult["hourly"][dfInput.loc[ap, flag_finalFile_Hour]]['dew_point'])
            )
            
            dfInput.loc[ap, flag_viaApiCall_Temp] = thisResult['hourly'][dfInput.loc[ap, flag_finalFile_Hour]]['temp']
            dfInput.loc[ap, flag_viaApiCall_Humidity] = thisResult['hourly'][dfInput.loc[ap, flag_finalFile_Hour]]['humidity']
            dfInput.loc[ap, flag_viaApiCall_Pressure] = thisResult['hourly'][dfInput.loc[ap, flag_finalFile_Hour]]['pressure']
            dfInput.loc[ap, flag_viaApiCall_dewPoint] = thisResult['hourly'][dfInput.loc[ap, flag_finalFile_Hour]]['dew_point']
            dfInput.loc[ap, flag_viaApiCall_feelsLike] = thisResult['hourly'][dfInput.loc[ap, flag_finalFile_Hour]]['feels_like']
            dfInput.loc[ap, flag_viaApiCall_dt] = thisResult['hourly'][dfInput.loc[ap, flag_finalFile_Hour]]['dt']
            
    return dfInput, dateStringForFileName, apStart
       

# ######################################################################################################################
def func_readAllSelectedFilesAndExtractHourlyTimeStamps():

    df1 = pd.DataFrame()
    
    filesToBeTreated = filedialog.askopenfilenames(
        initialdir="Downloads",
    )
    
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
    # endregion
    
    df1 = df1.sort_values([flag_finalFile_Ship, flag_finalFile_Date],
                          ascending=[True, True])

    df1[flag_finalFile_Date] = pd.to_datetime(df1[flag_finalFile_Date])
    
    df1[flag_finalFile_UTC] = df1.apply(lambda x: func_countSecondsThisDP(
        x[flag_finalFile_Date],
        'utc'
    ), axis=1)

    df1 = df1.reset_index(drop=True)

    df1[flag_finalFile_Minute] = df1.apply(lambda x: func_getThisTimeMinute(
        x[flag_finalFile_Date]
    ), axis=1)

    df1 = df1[(df1[flag_finalFile_Minute] == 0)]
    
    df1[flag_finalFile_Hour] = df1.apply(lambda x: func_getThisTimeHour(
        x[flag_finalFile_Date]
    ), axis=1)

    df1 = df1.reset_index(drop=True)
    
    df1 = df1[[
        flag_finalFile_Ship,
        flag_finalFile_Date,
        flag_finalFile_Hour,
        flag_finalFile_Minute,
        flag_finalFile_UTC,
        flag_finalFile_Latitude,
        flag_finalFile_Longitude
    ]]
    
    return df1


# ######################################################################################################################
def func_getThisTimeMinute(
    thisTime
):
    return thisTime.minute


# ######################################################################################################################
def func_getThisTimeHour(
    thisTime
):
    return thisTime.hour


# ######################################################################################################################
def func_countSecondsThisDP(
   thisDate,
   secondFlag
):
    if secondFlag == 'utc':
        timeDelta = thisDate - firstTimeTick
    
    seconds = int(timeDelta.total_seconds())
    
    return seconds


# ######################################################################################################################
df_master = func_readAllSelectedFilesAndExtractHourlyTimeStamps()

df_master.to_csv(
		'preparedDataForThatDay.csv',
		sep=';',
		decimal='.',
		index=False)

df_master, dateStringForFileName, apStart = func_readWeatherDataViaApiCall(df_master)

df_master.to_csv(
		dateStringForFileName + ' finalHourlyDataIncludingWeather ' + str(apStart) + '.csv',
		sep=';',
		decimal='.',
		index=False)

playsound('hammer_hitwall1.wav')
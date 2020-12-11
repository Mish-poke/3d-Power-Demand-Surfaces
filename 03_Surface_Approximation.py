import pandas as pd
import numpy as np
import scipy
from sklearn.preprocessing import PolynomialFeatures
import tkinter as tk
from tkinter import filedialog
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import datetime as dt
import os
from playsound import playsound

#######################################################################################################################

approximationLevel = 3

flag_createNewFile = True

flag_timePeriod_approximationBeforeLayUpStart = False
flag_timePeriod_approximationAfterLayUpStart = True

flag_useFullPeriodSinceStartOfLayUp = False
flag_LayUpSurfaceApproximationInDaysRolling = 7



dict_layUpStartDate = {
    'A-BE': dt.datetime(2020, 3, 4, 0, 0, 0),
    'A-BL': dt.datetime(2020, 3, 15, 0, 0, 0),
    'A-DV': dt.datetime(2020, 3, 10, 0, 0, 0),
    'A-LN': dt.datetime(2020, 3, 14, 0, 0, 0),
    'A-NV': dt.datetime(2020, 3, 12, 0, 0, 0),
    'A-PL': dt.datetime(2020, 3, 14, 0, 0, 0),
    'A-PM': dt.datetime(2020, 3, 9, 0, 0, 0),
    'A-ST': dt.datetime(2020, 3, 12, 0, 0, 0),
    'A-SL': dt.datetime(2020, 3, 10, 0, 0, 0),
    'A-MR': dt.datetime(2020, 3, 12, 0, 0, 0),
    'C-AT': dt.datetime(2019, 12, 31, 0, 0, 0),
    'C-DE': dt.datetime(2020, 4, 21, 0, 0, 0),
    'C-DI': dt.datetime(2020, 4, 2, 0, 0, 0),
    'C-FA': dt.datetime(2020, 3, 27, 0, 0, 0),
    'C-FO': dt.datetime(2020, 3, 23, 0, 0, 0),
    'C-FS': dt.datetime(2020, 1, 31, 0, 0, 0), #'C-FS': dt.datetime(2020, 3, 14, 0, 0, 0),
    'C-LU': dt.datetime(2020, 3, 19, 0, 0, 0),
    'C-MD': dt.datetime(2020, 3, 11, 0, 0, 0),
    'C-ME': dt.datetime(2020, 2, 1, 0, 0, 0),
    'C-MG': dt.datetime(2020, 3, 26, 0, 0, 0),
    'C-PA': dt.datetime(2020, 4, 1, 0, 0, 0),
    'C-SE': dt.datetime(2020, 1, 25, 0, 0, 0)
}


# ### FILTER clouds that are outside of any acceptable distance
use_FilterOutsiders = 0
filterOutsiders_maxAllowedDistanceDeviationFromNormal = 0.75

filter_minLoadDuringLayupTime = 500

useFilter_minTemp = 1
filter_minimumTemperature = 0

useFilter_maxTemp = 0
filter_maximumTemperature = 33

useFilter_MaxHumidity = 1
filter_maxRelHumidity = 100

useFilter_minLoad = 1
dict_filterMinLoad_ORDINARY_Business = {
    
    'A-BE': 4000, #checked
    'A-BL': 3500, #checked
    'A-DV': 4000, #checked
    'A-LN': 3500, #checked
    'A-MR': 3500, #checked
    'A-NV': 8000, #checked
    'A-PM': 5000, #checked
    'A-PL': 5000, #checked
    'A-SL': 3500, #checked
    'A-ST': 3500, #checked
    'C-AT': 3000, #checked
    'C-DE': 3750, #checked
    'C-DI': 5500, #checked
    'C-FS': 4500, #checked
    'C-FA': 4750, #checked
    'C-FO': 3000, #checked
    'C-LU': 3750, #checked
    'C-MG': 3750, #checked
    'C-MD': 3000, #checked
    'C-ME': 6000, #checked
    'C-PA': 4000, #checked
    'C-SE': 3750  #checked
}

useFilter_maxLoad = 1
dict_filterMaxLoad = {
    'A-BE': 7200, #checked
    'A-BL': 7250,
    'A-LN': 6500,
    'A-DV': 6500,
    'A-MR': 6500,
    'A-NV': 9500,
    'A-PL': 8500, #checked
    'A-PM': 7800, #checked
    'A-ST': 6500,
    'A-SL': 6000,
    'C-AT': 8500, #checked
    'C-DE': 8500, #checked
    'C-DI': 9000, #checked
    'C-FS': 8000, #checked
    'C-FA': 9200, #checked
    'C-FO': 8500, #checked
    'C-LU': 8750, #checked
    'C-MD': 5000, #checked
    'C-ME': 9000, #checked
    'C-MG': 7000, #checked
    'C-PA': 9000, #checked
    'C-SE': 8000  #checked
}

# ### FILTER OUT TEMP SPIKES
flag_tempSpikes_useTemperatureSpikeFiltering = 1

flag_tempSpikes_temperatureStepForFilter = 2
flag_tempSpikes_maxDeviationPerTempPercent = 15

usePerlaData = 0

flag_shipCode = 'ShipCode'
flag_time = 'lastupdateutc'
flag_engineLoad = 'TOTAL_PW'

name_column_x = 'CloseByNasaData_Temperature'
name_column_y = 'CloseByNasaDataEnthalpy' #CloseByNasaDataEnthalpy #CloseByNasaData_relHumidity
name_column_z = flag_engineLoad
name_column_approximation = name_column_z+'_Approx'+str(approximationLevel)
name_column_deviation = name_column_approximation+'_Deviation'+str(approximationLevel)

# CloseByNasaData_Temperature
# CloseByNasaData_relHumidity
# CloseByNasaData_absHumidity
# CloseByNasaDataEnthalpy

# column_x = 'Temperature'
# column_y = 'Humidity'
# column_z = 'TOTAL_PW'




########################################################################################################################
def func_filterOutUselessLoadSpikes(
   data_df,
   filterColumn
):
    dfFinal = pd.DataFrame()
    
    printDetailsAboutTempFilter = False
    
    if printDetailsAboutTempFilter:
        print(data_df.head(5))
        print("this set min temp: " + str(data_df[filterColumn].min()))
        print("this set max temp: " + str(data_df[filterColumn].max()))
    
    thisTemp = data_df[filterColumn].min() # flag_tempSpikes_temperatureStepForFilter
    
    while thisTemp < data_df[filterColumn].max():
        if printDetailsAboutTempFilter:
            print(chr(10) + " NEXT TEMPERATURE RANGE with middle @ " +str(thisTemp))
        
        subDF = data_df[
            (data_df[filterColumn] >= thisTemp - flag_tempSpikes_temperatureStepForFilter) &
            (data_df[filterColumn] < thisTemp + flag_tempSpikes_temperatureStepForFilter)
            ]
        
        avgLoadThisTemp = float(subDF[flag_engineLoad].mean())
        if printDetailsAboutTempFilter:
            print("   avgLoadThisTemp " + str(avgLoadThisTemp))
        
        elementsBefore = len(subDF[flag_engineLoad])
        if printDetailsAboutTempFilter:
            print("   ELEMENTS BEFORE FILTER FOR ENGINE LOAD " + str(len(subDF[flag_engineLoad])))
        
        lowerLoadLevel = avgLoadThisTemp - avgLoadThisTemp * flag_tempSpikes_maxDeviationPerTempPercent / 100
        upperMaxLoadLevelThisTemp = avgLoadThisTemp + avgLoadThisTemp * flag_tempSpikes_maxDeviationPerTempPercent / 100

        if printDetailsAboutTempFilter:
            print("   lowerLoadLevel " + str(lowerLoadLevel))
            print("   upperMaxLoadLevelThisTemp " + str(upperMaxLoadLevelThisTemp))
            print("   MIN LOAD THIS TEMP " + str(subDF[flag_engineLoad].min()))
        
        subDF = subDF[subDF[flag_engineLoad] >= lowerLoadLevel]
        subDF = subDF[subDF[flag_engineLoad] < upperMaxLoadLevelThisTemp]

        elementsAfter = len(subDF[flag_engineLoad])

        if printDetailsAboutTempFilter:
            print("   ELEMENTS AFTER FILTER FOR ENGINE LOAD " + str(len(subDF[flag_engineLoad])))
            print(">>> DATA POINTS kicked because being out of acceptable load range: " + str(elementsBefore - elementsAfter))
        
        if len(subDF) > 0:
            dfFinal = pd.concat([dfFinal, subDF])

        thisTemp += flag_tempSpikes_temperatureStepForFilter
    
    return dfFinal


######################################################################################################################
def func_replaceNanInThisColumn(
   dfInput,
   columnFlag,
   newNanValue
):
    dfInput[columnFlag].fillna(newNanValue, inplace=True)
    
    return dfInput


########################################################################################################################
def func_getTotalPower(
   data_df
):
    # if 'DG1POW' in data_df.columns:
    
    # add missing DG load columns for ships with less than 6 engines
    if 'DG5POW' not in data_df.columns:
        data_df["DG5POW"] = 0
    
    if 'DG6POW' not in data_df.columns:
        data_df["DG6POW"] = 0

    data_df = func_replaceNanInThisColumn(data_df, "DG1POW", 0)
    data_df = func_replaceNanInThisColumn(data_df, "DG2POW", 0)
    data_df = func_replaceNanInThisColumn(data_df, "DG3POW", 0)
    data_df = func_replaceNanInThisColumn(data_df, "DG4POW", 0)
    data_df = func_replaceNanInThisColumn(data_df, "DG5POW", 0)
    data_df = func_replaceNanInThisColumn(data_df, "DG6POW", 0)
    
    data_df['DG1POW'] = data_df['DG1POW'].astype(float)
    data_df['DG2POW'] = data_df['DG2POW'].astype(float)
    data_df['DG3POW'] = data_df['DG3POW'].astype(float)
    data_df['DG4POW'] = data_df['DG4POW'].astype(float)
    data_df['DG5POW'] = data_df['DG5POW'].astype(float)
    data_df['DG6POW'] = data_df['DG6POW'].astype(float)
    
    data_df.to_csv("TEST", sep=";"
                   )
    
    data_df[flag_engineLoad] = \
        data_df['DG1POW'] + data_df['DG2POW'] + data_df['DG3POW'] + \
        data_df['DG4POW'] + data_df['DG5POW'] + data_df['DG6POW']
    
    return data_df


# ######################################################################################################################
def func_applyVariousFilters(
   data_df,
   shipShortCode
):
    printDetailsForVariousFilters = False
    
    if printDetailsForVariousFilters:
        print(chr(10) + "#########################################")
        print("### LEN of data_df BEFORE various filter " + str(len(data_df[name_column_x])))
    
    data_df.dropna(axis=0, subset=[name_column_x, name_column_y, flag_engineLoad], inplace=True)

    if printDetailsForVariousFilters:
        print("LEN after dropna: " + str(len(data_df[name_column_x])))

    # region useFilter_minTemp
    data_df = data_df[data_df[flag_engineLoad] >= 500]
    
    #region useFilter_minTemp
    if useFilter_minTemp and name_column_x in data_df.columns:
        if printDetailsForVariousFilters:
            print(chr(10) + " FILTER: useFilter_minTemp in column " + name_column_x)
        
        beforeThisFilter = len(data_df[name_column_x])
        
        data_df = data_df[data_df[name_column_x] >= filter_minimumTemperature]
        
        afterThisFilter = len(data_df[name_column_x])
        if printDetailsForVariousFilters:
            print(">>> DATA POINTS kicked @ useFilter_minTemp: " + str(afterThisFilter - beforeThisFilter))
            print("LEN remaining dataset: " + str(len(data_df[name_column_x])))
    #endregion
    
    #region useFilter_maxTemp
    if useFilter_maxTemp and name_column_x in data_df.columns:
        if printDetailsForVariousFilters:
            print(chr(10) + " FILTER: useFilter_maxTemp")
           
        beforeThisFilter = len(data_df[name_column_x])
        
        data_df = data_df[data_df[name_column_x] < filter_maximumTemperature]
        
        afterThisFilter = len(data_df[name_column_x])
        if printDetailsForVariousFilters:
            print(">>> DATA POINTS kicked @ useFilter_maxTemp: " + str(afterThisFilter - beforeThisFilter))
            print("LEN remaining dataset: " + str(len(data_df[name_column_x])))
    #endregion
    
    #region useFilter_MaxHumidity
    if useFilter_MaxHumidity and 'CloseByNasaData_relHumidity' in data_df.columns:
        if printDetailsForVariousFilters:
            print(chr(10) + " FILTER: CloseByNasaData_relHumidity")
        
        beforeThisFilter = len(data_df['CloseByNasaData_relHumidity'])
        
        data_df = data_df[data_df['CloseByNasaData_relHumidity'] <= filter_maxRelHumidity]
        
        afterThisFilter = len(data_df['CloseByNasaData_relHumidity'])

        if printDetailsForVariousFilters:
            print(">>> DATA POINTS kicked @ useFilter_MaxHumidity: " + str(afterThisFilter - beforeThisFilter))
            print("LEN remaining dataset: " + str(len(data_df[name_column_x])))
    #endregion
    
    #region useFilter_minLoad
    if useFilter_minLoad and flag_timePeriod_approximationBeforeLayUpStart:
        if printDetailsForVariousFilters:
            print(chr(10) + " FILTER: useFilter_minLoad")
        beforeThisFilter = len(data_df[flag_engineLoad])

        if printDetailsForVariousFilters:
            print("LEN dataset before useFilter_minLoad" + str(beforeThisFilter))
        
        data_df = data_df[data_df[flag_engineLoad] > dict_filterMinLoad_ORDINARY_Business[shipShortCode]]
    
        afterThisFilter = len(data_df[flag_engineLoad])

        if printDetailsForVariousFilters:
            print("LEN dataset after useFilter_minLoad: " + str(afterThisFilter))
            print(">>> DATA POINTS kicked @ useFilter_minLoad: " + str(afterThisFilter - beforeThisFilter))
    else:
        if printDetailsForVariousFilters:
            print(chr(10) + " FILTER: filter_minLoadDuringLayupTime")
        
        beforeThisFilter = len(data_df[flag_engineLoad])

        if printDetailsForVariousFilters:
            print("LEN dataset before filter_minLoadDuringLayupTime" + str(beforeThisFilter))
        
        data_df = data_df[data_df[flag_engineLoad] >= filter_minLoadDuringLayupTime]

        afterThisFilter = len(data_df[flag_engineLoad])

        if printDetailsForVariousFilters:
            print("LEN dataset after filter_minLoadDuringLayupTime: " + str(afterThisFilter))
            print(">>> DATA POINTS kicked @ filter_minLoadDuringLayupTime: " + str(afterThisFilter - beforeThisFilter))
    #endregion
    
    #region useFilter_maxLoad
    if useFilter_maxLoad:
        if printDetailsForVariousFilters:
            print(chr(10) + " FILTER: useFilter_maxLoad")
        
        beforeThisFilter = len(data_df[flag_engineLoad])

        if printDetailsForVariousFilters:
            print("LEN dataset before useFilter_maxLoad: " + str(beforeThisFilter))
        
        data_df = data_df[data_df[flag_engineLoad] < dict_filterMaxLoad[shipShortCode]]

        afterThisFilter = len(data_df[flag_engineLoad])

        if printDetailsForVariousFilters:
            print("LEN dataset after useFilter_maxLoad: " + str(afterThisFilter))
            print(">>> DATA POINTS kicked @ useFilter_maxLoad: " + str(afterThisFilter - beforeThisFilter))
    #endregion
    
    #region flag_tempSpikes_useTemperatureSpikeFiltering
    if flag_tempSpikes_useTemperatureSpikeFiltering:
        if usePerlaData:
            print(chr(10) + " AIDAperla FILTER: flag_tempSpikes_useTemperatureSpikeFiltering")
            beforeThisFilter = len(data_df['Temperature_C'])
            
            data_df = func_filterOutUselessLoadSpikes(data_df, 'Temperature_C')

            afterThisFilter = len(data_df['Temperature_C'])
            
            print(">>> TOTAL DATA POINTS kicked: " + str(afterThisFilter - beforeThisFilter))
            print("LEN remaining dataset: " + str(len(data_df[name_column_x])))
        else:
            if printDetailsForVariousFilters:
                print(chr(10) + " FILTER: flag_tempSpikes_useTemperatureSpikeFiltering")
            
            beforeThisFilter = len(data_df['CloseByNasaData_Temperature'])

            if printDetailsForVariousFilters:
                print("LEN dataset before flag_tempSpikes_useTemperatureSpikeFiltering" + str(beforeThisFilter))
            
            data_df = func_filterOutUselessLoadSpikes(data_df, 'CloseByNasaData_Temperature')
            
            afterThisFilter = len(data_df['CloseByNasaData_Temperature'])

            if printDetailsForVariousFilters:
                print("LEN dataset after flag_tempSpikes_useTemperatureSpikeFiltering " + str(afterThisFilter))
                print(">>> TOTAL DATA POINTS kicked: " + str(afterThisFilter - beforeThisFilter))
    #endregion

    if printDetailsForVariousFilters:
        print(chr(10) + "### FINAL LEN AFTER ALL FILTERS: " + str(len(data_df['CloseByNasaData_Temperature'])))
        print("#########################################" + chr(10))
    
    return data_df


# ######################################################################################################################
def func_filterOutOutsider(
   dfInput,
   shipShortCode
):
    arrayFlag_Temp = 0
    arrayFlag_Ent = 1
    arrayFlag_PWR = 2
    
    finalPoints = np.array([[0,0,0]]).astype(float)
    
    for thisTemp in dfInput[name_column_x].unique():
        for thisEnt in dfInput[dfInput[name_column_x] == thisTemp][name_column_y].unique():
            avgLoadThisPoint = round(dfInput[
                               (dfInput[name_column_x] == thisTemp) &
                               (dfInput[name_column_y] == thisEnt)][name_column_z].mean(), 1)

            print("TEMP: " + str(thisTemp) + " // ENT: " + str(thisEnt) + " // AVG LOAD: " + str(avgLoadThisPoint))
            
            finalPoints = np.append(finalPoints, [[thisTemp, thisEnt, avgLoadThisPoint/1000]], axis = 0)
            # print(finalPoints)
    
    
    print("AND NOW THE FINAL ARRAY")
    # print(finalPoints)
    
    finalShortestDistances = np.array([[0]]).astype(float)
    
    ap1 = -1
    for firstPoint in finalPoints:
        ap1 +=1
        p1 = np.array(
            [finalPoints[ap1][arrayFlag_Temp],
             finalPoints[ap1][arrayFlag_Ent],
             finalPoints[ap1][arrayFlag_PWR]]
        )

        ap2 = -1
        lowestDistance = 9999
        dist = 0
        cnt = 0
        ap_lowestDistance = 0
        for secondPoint in finalPoints:
            ap2 += 1
            if ap1 != ap2:
                cnt += 1
                p2 = np.array(
                    [finalPoints[ap2][arrayFlag_Temp],
                     finalPoints[ap2][arrayFlag_Ent],
                     finalPoints[ap2][arrayFlag_PWR]]
                )
                
                squared_dist = np.sum((p1 - p2) ** 2, axis=0)
                dist = np.sqrt(squared_dist)
                
                if dist < lowestDistance:
                    lowestDistance = dist
                    ap_lowestDistance = ap2

        # finalShortestDistances = np.append(finalShortestDistances, [lowestDistance], axis=0)+
        # print("PLACES CHECKED " + str(cnt))
        print("LOwEST DIST " + str(finalPoints[ap1]) + " = " + str(lowestDistance))
        print("Lowest Distance from ("+str(ap1)+")" + str(finalPoints[ap1]) + " to ("+str(ap_lowestDistance) + ")" + str(finalPoints[ap_lowestDistance]))
        finalShortestDistances = np.append(finalShortestDistances, [[lowestDistance]], axis=0)

    finalShortestDistances = np.delete(finalShortestDistances, 0, axis = 0)
    # print(finalShortestDistances)
    # print(finalPoints)
    # finalPoints = np.delete(finalPoints, 0, axis=0)
    
    finalPoints = np.append(finalPoints, finalShortestDistances, axis=1)
    
    flag_distance_temp = 'TEMP'
    flag_distance_ENT = 'ENT'
    flag_distance_PWR = 'PWR'
    flag_distance_DIST = 'DIST'
    flag_distance_ERASE_or_Keep = 'ERASE_KEEP'
    
    distance_df = pd.DataFrame({
        flag_distance_temp: finalPoints[:, 0],
        flag_distance_ENT: finalPoints[:, 1],
        flag_distance_PWR: finalPoints[:, 2],
        flag_distance_DIST: finalPoints[:, 3]
    })
    
    distance_df = distance_df[distance_df['ENT'] > 0]
    
    avgDistance = distance_df[flag_distance_DIST].mean()
    distStdDev =  distance_df[flag_distance_DIST].std()
    
    print("avgDistance: " + str(avgDistance))
    print("distStdDev: " + str(distStdDev))
    print("erase everything above distance of : " + str(avgDistance + filterOutsiders_maxAllowedDistanceDeviationFromNormal*distStdDev))
    
    distance_df[flag_distance_ERASE_or_Keep] = 0
    
    distance_df.loc[ \
        (distance_df[flag_distance_DIST] > avgDistance + filterOutsiders_maxAllowedDistanceDeviationFromNormal*distStdDev),
        flag_distance_ERASE_or_Keep
    ] = 1
    
    # print(distance_df)
    
    df_toBeErased = distance_df[distance_df[flag_distance_ERASE_or_Keep] == 1]
    
    # print(df_toBeErased)
    
    print("LEN BEFORE FILTER: " + str(len(dfInput)))
    
    for ap in df_toBeErased.index:
        thisTempToBeErased = df_toBeErased.loc[ap, flag_distance_temp]
        thisEntToBeErased = df_toBeErased.loc[ap, flag_distance_ENT]

        # print("ERASE THIS COMBI of Temnp " + str(thisTempToBeErased) + " and Ent: " + str(thisEntToBeErased))
        
        dfInput = dfInput.drop(
            dfInput[
                (dfInput[name_column_x] == thisTempToBeErased) &
                (dfInput[name_column_y] == thisEntToBeErased)
            ].index)

        # print("LEN AFTER FILTER x: " + str(len(dfInput)))

    print("FINAL LEN AFTER FILTER: " + str(len(dfInput)))
    
    # df_finalDataset = func_removeOutsiders(data_df, df_toBeErased)
    
    # print(df_finalDataset)
    
    return dfInput

        
# ######################################################################################################################
def func_exportFinalDataframe(
   data_df,
   shipShortCode,
   dayCounter,
   fileDateString
):
    if not flag_createNewFile:
        data_df.to_csv(file_root, sep=';', index=None, header=True, decimal='.')
    else:
        
        fileName = shipShortCode + "_ALL_DATA_SHIP_NASA_surface_approximation.csv"
        
        if \
           flag_timePeriod_approximationBeforeLayUpStart and \
            not flag_timePeriod_approximationAfterLayUpStart:
            
            fileName = \
                "C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\Results\\Surfaces Reference\\" + \
                shipShortCode + \
                "_beforeLayUp_SHIP_NASA_surface_approximation.csv"
            
        if \
            not flag_timePeriod_approximationBeforeLayUpStart and \
              flag_timePeriod_approximationAfterLayUpStart:
            
            if dayCounter < 10:
                finalDayCounter = str("00" + str(dayCounter))
            elif dayCounter >= 10 and dayCounter < 100:
                finalDayCounter = str("0" + str(dayCounter))
            else:
                finalDayCounter = str(dayCounter)
            
            if flag_useFullPeriodSinceStartOfLayUp:
                fileName = \
                    "C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\Results\\Surfaces Layup Full Length\\" + \
                    shipShortCode + "_" + \
                    "duringLayUp_FullDataset_SHIP_NASA_surface_approximation.csv"
            else:
                pathName = "C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\Results\\Surfaces Layup Rolling\\" + shipShortCode + "\\" + str(flag_LayUpSurfaceApproximationInDaysRolling) + "-days"
                if not os.path.exists(pathName):
                    print("sub folder for " + shipShortCode + " does not exist >> create folder")
                    os.mkdir(pathName)
                
                fileName = \
                    "C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\Results\\Surfaces Layup Rolling\\" + shipShortCode + "\\" + str(flag_LayUpSurfaceApproximationInDaysRolling) + "-days" + "\\" + \
                    shipShortCode + "_" + \
                    str(flag_LayUpSurfaceApproximationInDaysRolling) + "_DayRolling_" + \
                    "_Day_" + str(finalDayCounter) + \
                    "_duringLayUp_SHIP_NASA_surface_approximation_" + \
                    str(fileDateString) + ".csv"
            
        
        print("save final file right here:" + fileName)
        
        data_df.to_csv(fileName , sep=';', index=None, header=True, decimal='.')
   

# ######################################################################################################################
def func_filterForProperTimePeriod(
   dfInput,
   shipShortCode
):
    printDetailsForTimeFilter = False
    
    if shipShortCode not in dict_layUpStartDate:
        print("LAY-UP START TIME MISSING in dict_layUpStartDate !!! "
              "Surface Approximation for the time before Lay-Up not possible. END")
        exit()
    else:
        if \
           flag_timePeriod_approximationBeforeLayUpStart and \
           not flag_timePeriod_approximationAfterLayUpStart:
            
            shipLayUpStartTime = dict_layUpStartDate[shipShortCode]
            print("Lay-Up Start-Time " + str(shipLayUpStartTime) + " FILTER OUT EVERYTHING AFTER THAT TIME!!")
        
            dfInput = dfInput[dfInput[flag_time] <= shipLayUpStartTime]
           
            print("LEN AFTER TIME FILTER: " + str(len(dfInput[flag_time])))

        if \
           not flag_timePeriod_approximationBeforeLayUpStart and \
            flag_timePeriod_approximationAfterLayUpStart:
            
            shipLayUpStartTime = dict_layUpStartDate[shipShortCode]
            
            if printDetailsForTimeFilter:
                print("Lay-Up Start-Time " + str(shipLayUpStartTime) + " FILTER OUT EVERYTHING BEFORE THAT TIME!!")
    
            dfInput = dfInput[dfInput[flag_time] >= shipLayUpStartTime]

            if printDetailsForTimeFilter:
                print("LEN AFTER TIME FILTER: " + str(len(dfInput[flag_time])))
          
    return dfInput

# ######################################################################################################################
def find_polynomial_approximation_2d(
   data_df,
   polynomial_degree,
   name_column_x,
   name_column_y,
   column_name_z,
   dayCounter,
   fileDateString
):
    shipShortCode = data_df.loc[1, flag_shipCode]

    flag_printDetailsWhileDoingTheSurfaceApproximation = False
    
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print(chr(10) + "****FUNCTION TO MAKE AN 2D APPROXIMATION SURFACE IN THE HILBERT SPACE"
              " OF POLYNOMIAL OF TWO VARIABLES WITH DEGREE LESS OR EQUAL THAN ", end='')
        
        print(str(polynomial_degree) + ' *****')
        
        print(data_df.head(5))
        
        print(">> SHIP: " + shipShortCode)
    
    data_df[flag_time] = pd.to_datetime(data_df[flag_time])
    
    data_df = func_filterForProperTimePeriod(data_df, shipShortCode)
    
    if shipShortCode not in dict_filterMinLoad_ORDINARY_Business:
        if flag_printDetailsWhileDoingTheSurfaceApproximation:
            print("no ship data in dictionaries, please fill this important data")
        
        exit()
    
    data_df[name_column_x] = round(data_df[name_column_x], 1)
    data_df[name_column_y] = round(data_df[name_column_y], 1)
    
    data_df = func_getTotalPower(data_df)
    
    data_df = func_applyVariousFilters(data_df, shipShortCode)
    
    if use_FilterOutsiders:
        data_df = func_filterOutOutsider(data_df, shipShortCode)
    
    #region Setting Data for the Regression Process
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("Setting Data for the Regression Process: ")
        print("     - setting independent variables: ", end='')
    
    # array_independent_points = data_df[[name_column_x, name_column_y]].to_numpy()  # (x,y)
    list_x = list(data_df[name_column_x])
    list_y = list(data_df[name_column_y])
    
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("done ##################")
    #endregion
    
    #region setting dependent variable
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("... setting dependent variable: ", end='')
       
    array_z = data_df[column_name_z].to_numpy()  # b

    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("done ##################")
    #endregion
    
    #region setting multivariables Vandermonde matrix
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("... setting multivariables Vandermonde matrix: ", end='')
       
    # polynomial = PolynomialFeatures(degree=polynomial_degree)
    # multi_vandermonde_matrix = polynomial.fit_transform(array_independent_points)  # A
    multi_vandermonde_matrix = np.polynomial.polynomial.polyvander2d(list_x, list_y, [polynomial_degree, polynomial_degree])
    
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print(multi_vandermonde_matrix)
        print("done ##################")
    #endregion
    
    #region Performing Regression Process
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("... Performing Regression Process: ", end='')
    
    coefficients, residual, rank, singular_values =\
        np.linalg.lstsq(multi_vandermonde_matrix, array_z, rcond=None)
    
    amount_rows_in_df = len(data_df)
    if residual:
        least_squared_error = residual/amount_rows_in_df
    else:
        least_squared_error = 'No information available.'

    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("done ##################")
    #endregion
    
    #region Execute Approximiation
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("Results from the Regression Process: ")
        print("     -Coefficientes = ", end='')
        print(coefficients)
        print("     -Least Squared Error = ", end='')
        print(least_squared_error)
    
    function_approximated = lambda x, y: sum(coefficients*np.polynomial.polynomial.polyvander2d(x, y, [polynomial_degree, polynomial_degree])[0])
    
    data_df[name_column_approximation] = \
        data_df.apply(lambda dtf: function_approximated(
            dtf[name_column_x],
            dtf[name_column_y]
        ), axis=1
    )
    
    if flag_printDetailsWhileDoingTheSurfaceApproximation:
        print("done ##################")
    #endregion
    
    data_df[name_column_deviation] = data_df[column_name_z] - data_df[name_column_approximation]
    
    func_exportFinalDataframe(data_df, shipShortCode, dayCounter, fileDateString)
    
    # matrix_3dData = func_createMatrixForPlotly3dSurface(data_df)
    
    return function_approximated, data_df


########################################################################################################################
def func_plotTheDotsIn3dOrbit(
    data_df
):
    # PLOTTING SCATTERED DATA POINT IN A 3D PLOT
    dictionary_data_columns_in_list = {
        name_column_x: list(data_df[name_column_x]),
        name_column_y: list(data_df[name_column_y]),
        name_column_z: list(data_df[name_column_z]),
        name_column_approximation: list(data_df[name_column_approximation]),
        name_column_deviation: list(data_df[name_column_deviation])
    }
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = dictionary_data_columns_in_list[name_column_x]
    y = dictionary_data_columns_in_list[name_column_y]
    z = dictionary_data_columns_in_list[name_column_z]
    z_approx = dictionary_data_columns_in_list[name_column_approximation]
    
    ax.scatter(x, y, z, c='r', marker='.')
    # ax.scatter(x, y, z_approx, c='b', marker='.')
    
    ax.set_xlabel(name_column_x)
    ax.set_ylabel(name_column_y)
    ax.set_zlabel(name_column_z)
    
    plt.show()


########################################################################################################################
if usePerlaData:
    name_column_x = 'Temperature_C'
    name_column_y = 'Enthalpy_Kcal_per_Kgad'  # CloseByNasaDataEnthalpy #CloseByNasaData_relHumidity
    name_column_z = flag_engineLoad
    

########################################################################################################################
def func_prepareThisShipData(
   data_df
):
    data_df['lastupdateutc'] = pd.to_datetime(data_df['lastupdateutc'], format='%Y-%m-%d %H:%M:%S')
    
    print("LEN OF MASTER DF BEFORE ANY FILTER: " + str(len(data_df['lastupdateutc'])))
    print(data_df.head(3))

    data_df.dropna(axis=0, subset=["CloseByNasaDataEnthalpy"], inplace=True)
    data_df = data_df.reset_index(drop=True)
    
    print("LEN OF MASTER DF AFTER dropna for missing Enthalpy data " + str(len(data_df['lastupdateutc'])))
    
    return data_df


########################################################################################################################
def func_readFileToBeTreated():
    
    print('Reading File: ', end='')
    
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilenames(
        initialdir="C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\SHIPs\\02 SHIP with OpenWeather",
        title='Pick a ship file to do the surface approximation'
    )
    
    list_file_root = list(root.tk.splitlist(file))
    file_root = list_file_root[0]
    data_df = pd.read_csv(file_root, sep=";", decimal=".")
    
    return data_df

########################################################################################################################
########################################################################################################################
########################################################################################################################

# df_sourceData = func_readFileToBeTreated()
listOfShipsToBeUpdated = filedialog.askopenfilenames(
    initialdir="C:\\Users\\500095\\Desktop\\NASA_ARIS_Data\\SHIPs\\02 SHIP with OpenWeather",
    title='Pick a ship file to do the surface approximation'
)

for df_thisShip in listOfShipsToBeUpdated:
    
    df_sourceData = pd.read_csv(df_thisShip, sep=";", decimal=".")
    
    df_sourceData = func_prepareThisShipData(df_sourceData)
    
    if \
       flag_timePeriod_approximationBeforeLayUpStart or \
       (flag_timePeriod_approximationAfterLayUpStart and flag_useFullPeriodSinceStartOfLayUp):
        
        function_approximated_example, data_df = \
            find_polynomial_approximation_2d(
                df_sourceData,
                approximationLevel,
                name_column_x,
                name_column_y,
                name_column_z,
                1,
                0
            )
        
        print(function_approximated_example(25, 14.69))
        
        # func_plotTheDotsIn3dOrbit(data_df)
    
    else:
        oneMoreCyclePossible = True
        shipShortCode = df_sourceData.loc[1, flag_shipCode]
        
        if not shipShortCode in dict_layUpStartDate:
            print(chr(10) + shipShortCode + " MISSING IN dict_layUpStartDate >>> enhance dict and restart algo")
            exit()
        
        shipLayUpStartTime = dict_layUpStartDate[shipShortCode]
    
        # df_sourceData['lastupdateutc']
        
        veryLastDataPointInActualData = df_sourceData['lastupdateutc'].max()
        print("veryLastDataPointInActualData " + str(veryLastDataPointInActualData))
        
        nextPeriodStart = shipLayUpStartTime
        nextPeriodEnd = shipLayUpStartTime
        dayCounter = 0
        
        while nextPeriodEnd < veryLastDataPointInActualData:
            dayCounter += 1
            nextPeriodEnd = nextPeriodStart + dt.timedelta(seconds=flag_LayUpSurfaceApproximationInDaysRolling * 24 * 60 * 60)
            print(chr(10) + " SURFACE Approximation between " + str(nextPeriodStart) + " and " + str(nextPeriodEnd))
            
            fileDateString = str(str(nextPeriodStart)[:10]) + " to " + str(str(nextPeriodEnd)[:10])
            
            subDF = df_sourceData[
                (df_sourceData['lastupdateutc'] >= nextPeriodStart) & \
                (df_sourceData['lastupdateutc'] < nextPeriodEnd)
            ]
            
            # print("LEN OF SUB DF: " + str(len(subDF['lastupdateutc'])))
            
            if len(subDF['lastupdateutc']) > 250:
                subDF = subDF.reset_index(drop=True)
                
                function_approximated_example, data_df = \
                    find_polynomial_approximation_2d(
                        subDF,
                        approximationLevel,
                        name_column_x,
                        name_column_y,
                        name_column_z,
                        dayCounter,
                        fileDateString
                    )
            else:
                print(
                    "no surface approximation for this period of time, only " +
                    str(len(subDF['lastupdateutc'])) + " samples during this period"
                )
                
            nextPeriodStart = nextPeriodStart + dt.timedelta(seconds=1 * 24 * 60 * 60)
            
playsound('hammer_hitwall1.wav')
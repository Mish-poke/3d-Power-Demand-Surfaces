
#region Possible Color Codes
# 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
# 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r',
# 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r',
# 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r',
# 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r',
# 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r',
# 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r',
# 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r',
# 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r',
# 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r',
# 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r',
# 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r',
# 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r',
# 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r',
# 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r',
# 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r',
# 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r',
# 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r',
# 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r',
# 'vlag', 'vlag_r', 'winter', 'winter_r'
# endregion

import time
import csv
import math
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import datetime as dt
import tkinter as tk
from tkinter import filedialog
import os
import pyautogui
# import mpld3 as mp
from playsound import playsound
import numpy as np
import inspect

import pandas as pd

from _CM_Include import *

playSoundAtTheEnd = True
useInitialDirs = True

approximationLevel = 3

totalSurfacesInJustOneGraph = 2
forceToDoSimpleClassComparison = 0

zAxis_minPowerDemandInGraph = 4000
zAxis_maxPowerDemandInGraph = 9000

flag_showNoOtherHeaderLineThanThisOne = ''#"Power Demand in Port Costa Diadema" + chr(10) + \
    # "June 20 to June 27 2020  = ~3.600kW (red surface)" + chr(10) + \
    # "June 20 to June 27 2021 = ~3.700kW (blue surface)"

flag_commentFirstLineOfChartHeader = "" # "Power Demand in Port during normal operations"
#"Power Demand in lay-up with only ~130 crew June 23 to June 30"
#"Power demand during port stay during normal operation before start of Layup" # "Normal Business 2019 until start of Lay-Up"


flag_print_Temp_Ent_PWR = 0
flag_print_Temp_Ent_PWRSurface = 0
flag_print_Temp_Ent_PWRSurface_per_Zone = 0
filter_showThisClimateZoneOnly = 0


flag_print_BEFORE_and_DURING_LayUp = 1 # set it
flag_showOnlyMatchingSurfaces = 0

flag_createFileWithLoadReductionHistory = 0 # set it both to True to create long term performance trend file
DO_NOT_SHOW_ANY_GRAPH_ONLY_STATs = 0 # needed to create time series for lay up reporting

flag_printQuattroView = 1
flag_showColorScalingBarRightHandSide_ReferenceSurface = 0
flag_showColorScalingBarRightHandSide_DuringLayupSurface = False

flag_plotConnectionLineBetweenSurfaces = 0

flag_createPlotSavescreenshotAndClosePlot = 0

flag_loadReduction_Ship = "Ship"
flag_loadReduction_PeriodStart = "Period Start"
flag_loadReduction_PeriodEnd = "Period End"
flag_loadReduction_avgTempSameTempAreaBeforeLayUp = "avgTempSameTempAreaBeforeLayUp"
flag_loadReduction_avgEnthalpySameTempAreaBeforeLayUp = "avgEnthalpySameTempAreaBeforeLayUp"
flag_loadReduction_avgLoadSameTempAreaBeforeLayUp = "avgLoadSameTempAreaBeforeLayUp"
flag_loadReduction_absoluteReduction_kW = "absoluteReduction_kW"
flag_loadReduction_relativeReduction_Percent = "relativeReduction_Percent"



cb_refArea = 'referenceSurface'
cb_layUpArea = 'layUpSurface'

flag_ship_Enthalpy = 'Enthalpy'
flag_ship_CloseByNasaData_Distance = 'CloseByNasaDataDistance'
flag_ship_CloseByNasaData_Temperature = 'CloseByNasaData_Temperature'
flag_ship_CloseByNasaData_relHumidity = 'CloseByNasaData_relHumidity'
flag_ship_CloseByNasaData_absHumidity = 'CloseByNasaData_absHumidity'
flag_ship_CloseByNasaData_Enthalpy = 'CloseByNasaDataEnthalpy'
flag_ship_CloseByNasaData_ClimateZone = 'Corp_ClimateZone'




filter_minimumTemperature = 5 #5
filter_maximumTemperature = 35 #35

filter_maxRelHumidity = 100

filter_minimumEnthalpy = 0
filter_maximumEnthalpy = 99

filter_maximumLoad = 9000

flag_engineLoad = 'TOTAL_PW'


name_column_x = 'CloseByNasaData_Temperature'
name_column_y = 'CloseByNasaDataEnthalpy' #CloseByNasaData_relHumidity # CloseByNasaDataEnthalpy
name_column_z = 'TOTAL_PW'
name_column_approximation = name_column_z+'_Approx' + str(approximationLevel)
name_column_deviation = name_column_approximation+'_Deviation' + str(approximationLevel)

dict_shipAP = {
    "ship1": 0,
    "ship2": 1,
    "ship3": 2,
    "ship4": 3,
    "ship5": 4,
    "ship6": 5,
    "ship7": 6,
    "ship8": 7,
    "ship9": 8
}

surface_colors = ["Red", "Blue", "Green", "Purple", "Yellow"]

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
		('C-VZ', 'Costa Venezia')
	]
)

# layUpStartDate = dt.datetime(2020, 3, 19, 0, 0, 0)

# ######################################################################################################################
def move_figure_absolut(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = plt.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


# ######################################################################################################################
def func_doTheProperShipRanking(
   avgLoadWholeSurface,
   shipNames
):
    f_makeThePrintNiceStructured(True, "### DO THE PROPER SHIP RANKING ", inspect.stack()[0][3])
    
    maxAP = len(avgLoadWholeSurface)
    print("maxAP " + str(maxAP))
    
    thisAP = 0
    while thisAP < maxAP:
        print("avgLoadWholeSurface["+str(thisAP)+"] = " +str(avgLoadWholeSurface[thisAP]))
        if avgLoadWholeSurface[thisAP+1] > 0:
            if avgLoadWholeSurface[thisAP+1] > avgLoadWholeSurface[thisAP]:
                print("SWAP PLACES between " + shipNames[thisAP] + " and " + shipNames[thisAP + 1])
                avgLoadWholeSurface, shipNames = func_swapValues(avgLoadWholeSurface, shipNames, thisAP)
                thisAP = -1
        else:
            break
        
        thisAP+= 1
    
    return avgLoadWholeSurface, shipNames


# ######################################################################################################################
def func_getProperHeaderForShipColors(
    firstPartOfTheTitle,
    shipHeaderLine,
    avgLoadWholeSurface
):
    f_makeThePrintNiceStructured(True, "### GET HEADER FOR SHIPs & Colors ", inspect.stack()[0][3])
    
    thisAP = 0
    while thisAP < len(avgLoadWholeSurface):
        print("avgLoadWholeSurface[" + str(thisAP) + "] = " + str(avgLoadWholeSurface[thisAP]))
        if avgLoadWholeSurface[thisAP] > 0:
            shipHeaderLine[thisAP] = \
                chr(10) + dict_shipShortCodesToLongNames[shipNames[thisAP]] + " @ " + \
                str(round(avgLoadWholeSurface[thisAP], 0)) + "kW (" + surface_colors[thisAP] + ")"
            
            firstPartOfTheTitle += shipHeaderLine[thisAP]
        
        thisAP = thisAP + 1
    
    print("firstPartOfTheTitle: " + firstPartOfTheTitle)

    return firstPartOfTheTitle


# ######################################################################################################################
def func_swapValues(
   avgLoadWholeSurface,
   shipNames,
   thisAP
):
    temp_value_load = avgLoadWholeSurface[thisAP]
    temp_value_ship = shipNames[thisAP]
    temp_value_color = surface_colors[thisAP]
    
    avgLoadWholeSurface[thisAP] = avgLoadWholeSurface[thisAP + 1]
    shipNames[thisAP] = shipNames[thisAP + 1]
    surface_colors[thisAP] = surface_colors[thisAP + 1]
    
    avgLoadWholeSurface[thisAP + 1] = temp_value_load
    shipNames[thisAP + 1] = temp_value_ship
    surface_colors[thisAP + 1] = temp_value_color
    
    return avgLoadWholeSurface, shipNames


# ######################################################################################################################
def func_defineSurfacePlotArea(
   shipNames,
   timePeriod,
   plotAreaNumber,
   absoluteReduction_kW,
   relativeReduction_Percent,
   avgLoadWholeSurface,
   avgLoadSameTempAreaBeforeLayUp = 0,
   avgLoadLayUp = 0
):
    f_makeThePrintNiceStructured(True, "### CREATE PLOT AREA in ", inspect.stack()[0][3])
    
    print("shipNames[dict_shipAP[ship1]] " + shipNames[dict_shipAP["ship1"]])
    
    shipLongName = dict_shipShortCodesToLongNames[shipNames[dict_shipAP["ship1"]]]
    if shipNames[dict_shipAP["ship2"]] != "":
        shipLongNameInCaseOfComparison = dict_shipShortCodesToLongNames[shipNames[dict_shipAP["ship2"]]]
    
    if flag_printQuattroView:
        fig = plt.figure(figsize=(14, 6.75), dpi=70)
    else:
        fig = plt.figure(figsize=(27, 13.5), dpi=70)
    
    plt.subplots_adjust(left=0.0, bottom=0.0, right=0.98, top=0.9)
    
    fig.tight_layout()
    
    ax = fig.gca(projection='3d')
    
    headerTitleDone = False
    
    if shipNames[dict_shipAP["ship3"]] != "" or forceToDoSimpleClassComparison:
    
        shipHeaderLine = np.empty(len(dict_shipAP) + 1, dtype=object)
        shipHeaderLine.fill('')
        
        avgLoadWholeSurface, shipNames = func_doTheProperShipRanking(avgLoadWholeSurface, shipNames)
        
        firstPartOfTheTitle = (
           "Power Demand Port/Anchorage [kW] over Temperature and Enthalpy (" + timePeriod + ")"
        )

        firstPartOfTheTitle = func_getProperHeaderForShipColors(firstPartOfTheTitle, shipHeaderLine, avgLoadWholeSurface)
        
        # print("START TITLE")
        # print((firstPartOfTheTitle))
        # print("END TITLE")
        
        ax.set_title(firstPartOfTheTitle)
        
        headerTitleDone = True
    
    if not headerTitleDone:
        if len(flag_showNoOtherHeaderLineThanThisOne) > 0:
            ax.set_title(flag_showNoOtherHeaderLineThanThisOne)
        else:
            if flag_print_BEFORE_and_DURING_LayUp:
                if absoluteReduction_kW == 0:
                    ax.set_title(shipName + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) + " Normal Business vs Period between " + timePeriod)
                else:
                    if avgLoadSameTempAreaBeforeLayUp > 0 and avgLoadLayUp > 0:
                        if shipNames[dict_shipAP["ship1"]] == shipNames[dict_shipAP["ship2"]]:
                            ax.set_title(
                                shipLongName + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) +
                                " Normal Business vs Period between " + timePeriod + chr(10) +
                                str(round(absoluteReduction_kW, 0)) + "kW load reduction = " + " - " +(str(round(relativeReduction_Percent*100,1))) + "%" + chr(10) +
                                "weight adjusted load during normal business " + str(round(avgLoadSameTempAreaBeforeLayUp,0)) + "kW (Red-Surface)" + chr(10) +
                                "weight adjusted load during pause " + str(round(avgLoadLayUp, 0)) + "kW (Blue-Surface)"
                            )
                        else:
                            ax.set_title(
                                flag_commentFirstLineOfChartHeader + chr(10) +
                                shipLongName + " vs " + shipNames[dict_shipAP["ship2"]] + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) +
                                shipLongNameInCaseOfComparison + " " + str(round(absoluteReduction_kW, 0)) + "kW load difference = " + " - " + (str(round(relativeReduction_Percent * 100, 1))) + "%" + chr(10) +
                                shipLongName + " avg load within matching surface area " + str(round(avgLoadSameTempAreaBeforeLayUp, 0)) + "kW (Red-Surface)" + chr(10) +
                                shipLongNameInCaseOfComparison + " avg load within matching surface area " + str(round(avgLoadLayUp, 0)) + "kW (Blue-Surface)"
                            )
                    else:
                        if shipNames[dict_shipAP["ship1"]] == shipNames[dict_shipAP["ship2"]]:
                            if plotAreaNumber != 3:
                                ax.set_title(
                                    shipLongName + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) +
                                    " Normal Business vs Period between " + timePeriod + chr(10) +
                                    str(round(absoluteReduction_kW, 0)) + "kW load reduction = " + " - " + (
                                        str(round(relativeReduction_Percent * 100, 1))) + "%"
                                )
                            else:
                                ax.set_title(
                                    shipLongName + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) +
                                    " Normal Business vs period between " + timePeriod + chr(10) +
                                    str(round(absoluteReduction_kW, 0)) + "kW load reduction = " + " - " + (
                                        str(round(relativeReduction_Percent * 100, 1))) + "%" + chr(10) +
                                    "view from below the surfaces"
                                )
                        else:
                            if plotAreaNumber != 3:
                                ax.set_title(
                                    flag_commentFirstLineOfChartHeader + chr(10) +
                                    shipLongName + " vs " + shipLongNameInCaseOfComparison + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) +
                                    shipLongNameInCaseOfComparison + " " + str(round(absoluteReduction_kW, 0)) + "kW load difference within matching surface area = " + " - " + (str(round(relativeReduction_Percent * 100, 1))) + "%"
                                )
                            else:
                                ax.set_title(
                                    flag_commentFirstLineOfChartHeader + chr(10) +
                                    shipLongName + " vs " + shipLongNameInCaseOfComparison + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) +
                                    shipLongNameInCaseOfComparison + " " + str(round(absoluteReduction_kW, 0)) + "kW load difference within matching surface area = " + " - " + (str(round(relativeReduction_Percent * 100, 1))) + "%" + chr(10) +
                                    "view from below the surfaces"
                                )
            else:
                ax.set_title(shipLongName + " Power Demand Port/Anchorage [kW] over Temperature and Enthalpy" + chr(10) +
                             flag_commentFirstLineOfChartHeader
                )
    
    ax.set_xlabel('Temperature [°C]')
    ax.set_ylabel('Enthalpy [kcal/kg]')
    ax.set_zlabel('PORT LOAD [kW]')
    
    ax.set_zlim(zAxis_minPowerDemandInGraph, zAxis_maxPowerDemandInGraph)
    
    plt.xlim(0, 35)
    plt.ylim(0, 30)
    
    if plotAreaNumber == 1:
        ax.view_init(elev=0, azim=-90)
        move_figure_absolut(fig,0,0)
       
    if plotAreaNumber == 2:
        ax.view_init(elev=0, azim=0) #00
        move_figure_absolut(fig, 950, 0)

    if plotAreaNumber == 3:
        ax.view_init(elev=-90, azim=-90) #ax.view_init(elev=45, azim=-45)
        move_figure_absolut(fig, 0, 500)

    if plotAreaNumber == 4:
        ax.view_init(elev=36, azim=-70)
        move_figure_absolut(fig, 950, 500)
    
    return fig, ax


# ######################################################################################################################
def func_getMinMaxAvgThisDfThisValue(
   refDF,
   flagItem
):
    if flagItem == "load":
        minValue = refDF[name_column_approximation].min()
        maxValue = refDF[name_column_approximation].max()
        avgValue = refDF[name_column_approximation].mean()
    
    if flagItem == "temp":
        minValue = refDF[name_column_x].min()
        maxValue = refDF[name_column_x].max()
        avgValue = refDF[name_column_x].mean()
    
    if flagItem == "ent":
        minValue = refDF[name_column_y].min()
        maxValue = refDF[name_column_y].max()
        avgValue = refDF[name_column_y].mean()
       
    return minValue, maxValue, avgValue


# ######################################################################################################################
def func_getSurfaceBeforeLayupMatchingTheseParas(
   df_referenceSurface,
   minTempLayup, maxTempLayup,
   minEnthalpyLayup, maxEnthalpyLayup
):
    beforeLayupSubDfSameRange = df_referenceSurface[
        (df_referenceSurface[name_column_x] >= minTempLayup - 0.5) &
        (df_referenceSurface[name_column_x] <= maxTempLayup + 0.5) &
        (df_referenceSurface[name_column_y] >= minEnthalpyLayup - 0.5) &
        (df_referenceSurface[name_column_y] <= maxEnthalpyLayup + 0.5)
        ]
    
    return beforeLayupSubDfSameRange


# ######################################################################################################################
def func_getLoadBeforeLayupSameClimateConditions(
   df_referenceSurface,
   avgTempLayup, avgEnthalpyLayup
):
    avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface = df_referenceSurface[
            (df_referenceSurface[name_column_x] >= avgTempLayup - 1) &
            (df_referenceSurface[name_column_x] <= avgTempLayup + 1) &
            (df_referenceSurface[name_column_y] >= avgEnthalpyLayup - 1) &
            (df_referenceSurface[name_column_y] <= avgEnthalpyLayup + 1)
            ][name_column_approximation].mean()

    print(" >>> avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface: " + str(
        round(avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface, 2)))
    
    return avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface


# ######################################################################################################################
def func_compareThisSurfaceAgainstRefSurface(
   df_layupSurface,
   df_referenceSurface
):
    minLoadLayUp, maxLoadLayUp, avgLoadLayUp = func_getMinMaxAvgThisDfThisValue(df_layupSurface, "load")
    minTempLayup, maxTempLayup, avgTempLayup = func_getMinMaxAvgThisDfThisValue(df_layupSurface, "temp")
    minEnthalpyLayup, maxEnthalpyLayup, avgEnthalpyLayup = func_getMinMaxAvgThisDfThisValue(df_layupSurface, "ent")
    
    beforeLayupSubDfSameRange = func_getSurfaceBeforeLayupMatchingTheseParas(df_referenceSurface,
                                                                             minTempLayup, maxTempLayup,
                                                                             minEnthalpyLayup, maxEnthalpyLayup)
    
    avgTempSameTempAreaBeforeLayUp = beforeLayupSubDfSameRange[name_column_x].mean()
    avgEnthalpySameTempAreaBeforeLayUp = beforeLayupSubDfSameRange[name_column_y].mean()
    avgLoadSameTempAreaBeforeLayUp = beforeLayupSubDfSameRange[name_column_approximation].mean()
    
    print(chr(10) + " ### Reference Surface Stats")
    print("avgTempSameTempAreaBeforeLayUp: " + str(round(avgTempSameTempAreaBeforeLayUp, 2)))
    print("avgEnthalpySameTempAreaBeforeLayUp: " + str(round(avgEnthalpySameTempAreaBeforeLayUp, 2)))
    print("avgLoadSameTempAreaBeforeLayUp: " + str(round(avgLoadSameTempAreaBeforeLayUp, 2)))
    
    avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface = func_getLoadBeforeLayupSameClimateConditions(
        df_referenceSurface, avgTempLayup, avgEnthalpyLayup
    )
    
    absoluteReduction_kW = avgLoadSameTempAreaBeforeLayUp - avgLoadLayUp
    relativeReduction_Percent = absoluteReduction_kW / avgLoadSameTempAreaBeforeLayUp
    
    print(chr(10) + " ### LOAD REDUCTION Stats")
    print("absoluteReduction_kW: " + str(round(absoluteReduction_kW, 2)))
    print("relativeReduction_Percent: " + str(round(relativeReduction_Percent * 100, 2)) + "%")
    
    return \
        minLoadLayUp, maxLoadLayUp, avgLoadLayUp, \
        minTempLayup, maxTempLayup, avgTempLayup, \
        minEnthalpyLayup, maxEnthalpyLayup, avgEnthalpyLayup, \
        avgTempSameTempAreaBeforeLayUp, avgEnthalpySameTempAreaBeforeLayUp, avgLoadSameTempAreaBeforeLayUp, \
        beforeLayupSubDfSameRange, avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface, \
        absoluteReduction_kW, relativeReduction_Percent


# ######################################################################################################################
def func_initialiseSomeLists():
    absoluteReduction_kW = np.empty(len(dict_shipAP) + 1, dtype=float)
    absoluteReduction_kW.fill(0)
    
    relativeReduction_Percent = np.empty(len(dict_shipAP) + 1, dtype=float)
    relativeReduction_Percent.fill(0)
    
    avgLoadWholeSurface = np.empty(len(dict_shipAP) + 1, dtype=float)
    avgLoadWholeSurface.fill(0)
    
    return absoluteReduction_kW, relativeReduction_Percent, avgLoadWholeSurface


# ######################################################################################################################
def func_createPowerDemandSurfacePlots(
   shipNames,
   df_referenceSurface,
   df_layupSurface,
   df_loadReductionHistory,
   timePeriod = '',
   fileName = '',
   startDateThisPeriod = "", endDateThisPeriod = "",
   df_ship3 = pd.DataFrame(), df_ship4 = pd.DataFrame(), df_ship5 = pd.DataFrame(),
   df_ship6 = pd.DataFrame(), df_ship7 = pd.DataFrame(), df_ship8 = pd.DataFrame(), df_ship9 = pd.DataFrame()
):
    avgLoadSameTempAreaBeforeLayUp = 0
    avgLoadLayUp = 0
    ax2 = ''
    fig2 = ''
    ax3 = ''
    fig3 = ''
    ax4 = ''
    fig4 = ''

    absoluteReduction_kW, relativeReduction_Percent, avgLoadWholeSurface = func_initialiseSomeLists()

    avgLoadWholeSurface[dict_shipAP["ship1"]] = round(df_referenceSurface[name_column_approximation].mean(), 1)
    
    #region compare Reference Surface (Ship 1) against layup surface (Ship 2)
    if df_layupSurface.shape[0] > 0:
        shipKey = dict_shipAP["ship2"]
        df_subSurface = df_layupSurface

        avgLoadWholeSurface[shipKey] = round(df_subSurface[name_column_approximation].mean(), 1)
        print("avgLoadWholeSurface for " + shipNames[dict_shipAP["ship2"]] + " = " + str(avgLoadWholeSurface[shipKey]))
        
        minLoadLayUp, maxLoadLayUp, avgLoadLayUp, \
        minTempLayup, maxTempLayup, avgTempLayup, \
        minEnthalpyLayup, maxEnthalpyLayup, avgEnthalpyLayup, \
        avgTempSameTempAreaBeforeLayUp, avgEnthalpySameTempAreaBeforeLayUp, avgLoadSameTempAreaBeforeLayUp, \
        beforeLayupSubDfSameRange, avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface, \
        absoluteReduction_kW[shipKey], relativeReduction_Percent[shipKey] = func_compareThisSurfaceAgainstRefSurface(
            df_subSurface, df_referenceSurface
        )
        
        if flag_createFileWithLoadReductionHistory:
            df_newLineInWithThisData = [
                {
                    flag_loadReduction_Ship: shipNames[dict_shipAP["ship1"]],
                    flag_loadReduction_PeriodStart: startDateThisPeriod,
                    flag_loadReduction_PeriodEnd: endDateThisPeriod,
                    flag_loadReduction_avgTempSameTempAreaBeforeLayUp: round(avgTempSameTempAreaBeforeLayUp,2),
                    flag_loadReduction_avgEnthalpySameTempAreaBeforeLayUp: round(avgEnthalpySameTempAreaBeforeLayUp, 2),
                    flag_loadReduction_avgLoadSameTempAreaBeforeLayUp: round(avgLoadSameTempAreaBeforeLayUp, 2),
                    flag_loadReduction_absoluteReduction_kW: round(absoluteReduction_kW[dict_shipAP["ship2"]], 2),
                    flag_loadReduction_relativeReduction_Percent: round(relativeReduction_Percent[dict_shipAP["ship2"]], 2),
                }
            ]
            
            df_loadReductionHistory = df_loadReductionHistory.append(df_newLineInWithThisData, ignore_index=True, sort=False)
        
        # Creating arrays with coordinates for surface connection
        x = [avgTempLayup, avgTempSameTempAreaBeforeLayUp]
        y = [avgEnthalpyLayup, avgEnthalpySameTempAreaBeforeLayUp]
        z = np.array([[avgLoadLayUp, avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface]])
        
        if flag_showOnlyMatchingSurfaces:
            df_referenceSurface = beforeLayupSubDfSameRange
    #endregion

    #region in case of more than 2 surfaces in just one graph, analyse the surfaces values
    absoluteReduction_kW, relativeReduction_Percent, avgLoadWholeSurface = func_shipByShipAnalysis(
        df_referenceSurface, avgLoadWholeSurface, absoluteReduction_kW, relativeReduction_Percent,
        df_ship3, df_ship4, df_ship5, df_ship6, df_ship7, df_ship8, df_ship9
    )
    #endregion
    
    if DO_NOT_SHOW_ANY_GRAPH_ONLY_STATs == False:
        fig, ax = func_defineSurfacePlotArea(
            shipNames, timePeriod, 1,
            absoluteReduction_kW[dict_shipAP["ship2"]], relativeReduction_Percent[dict_shipAP["ship2"]],
            avgLoadWholeSurface,
            avgLoadSameTempAreaBeforeLayUp, avgLoadLayUp
        )
        
        if flag_printQuattroView:
            fig2, ax2 = func_defineSurfacePlotArea(
                shipNames, timePeriod, 2,
                absoluteReduction_kW[dict_shipAP["ship2"]], relativeReduction_Percent[dict_shipAP["ship2"]],
                avgLoadWholeSurface
            )
            
            fig3, ax3 = func_defineSurfacePlotArea(
                shipNames, timePeriod, 3,
                absoluteReduction_kW[dict_shipAP["ship2"]], relativeReduction_Percent[dict_shipAP["ship2"]],
                avgLoadWholeSurface
            )
            
            fig4, ax4 = func_defineSurfacePlotArea(
                shipNames, timePeriod, 4,
                absoluteReduction_kW[dict_shipAP["ship2"]], relativeReduction_Percent[dict_shipAP["ship2"]],
                avgLoadWholeSurface
            )
        
        if flag_print_Temp_Ent_PWR:
            surf = ax.plot_trisurf(
                df_referenceSurface[name_column_x],
                df_referenceSurface[flag_engineLoad],
                df_referenceSurface[flag_engineLoad],
                cmap=plt.cm.viridis,
                linewidth=0.2
            )
        else:
            if flag_print_Temp_Ent_PWRSurface_per_Zone:
                maxSurfacePlotViews = 1
    
                if flag_printQuattroView:
                    maxSurfacePlotViews = 4
    
                thisView = 0
                while thisView < maxSurfacePlotViews:
                    thisView += 1
                    this_ax, this_fig = func_getProperPlotArea(thisView, ax, fig, ax2, fig2, ax3, fig3, ax4, fig4)
                    
                    thisLoop = 0
                    maxLoops = 1
                    
                    if flag_print_BEFORE_and_DURING_LayUp:
                        maxLoops = 2
                    
                    while thisLoop < maxLoops:
                        if thisLoop == 0:
                            thisDF = df_referenceSurface
                            thisArea = cb_refArea
                        else:
                            thisDF = df_layupSurface
                            thisArea = cb_layUpArea
                        
                        if thisLoop == 1 and flag_plotConnectionLineBetweenSurfaces:
                            this_ax.plot_wireframe(x, y, z, cmap='cool', linewidth=2)
                        
                        thisClimateZone = 1
                        if func_showThisClimateZone(thisDF, thisClimateZone):
                            func_printThisClimateZoneSurface(thisDF, thisClimateZone, 'winter',
                                                             this_ax, this_fig, showColorBar(thisArea))
    
                        thisClimateZone = 2
                        if func_showThisClimateZone(thisDF, thisClimateZone):
                            func_printThisClimateZoneSurface(thisDF, thisClimateZone, 'spring',
                                                             this_ax, this_fig, showColorBar(thisArea))
    
                        thisClimateZone = 3
                        if func_showThisClimateZone(thisDF, thisClimateZone):
                            func_printThisClimateZoneSurface(thisDF, thisClimateZone, 'summer',
                                                             this_ax, this_fig, showColorBar(thisArea))
    
                        thisClimateZone = 4
                        if func_showThisClimateZone(thisDF, thisClimateZone):
                            func_printThisClimateZoneSurface(thisDF, thisClimateZone, 'hot',
                                                             this_ax, this_fig, showColorBar(thisArea))
    
                        thisClimateZone = 5
                        if func_showThisClimateZone(thisDF, thisClimateZone):
                            func_printThisClimateZoneSurface(thisDF, thisClimateZone, 'magma',
                                                             this_ax, this_fig, showColorBar(thisArea))
                        
                        thisLoop += 1
                        
            else:
                print(chr(10) + " ### SHOW Full Scale Surface without Climate Zones")
                maxSurfacePlotViews = 1
                
                if flag_printQuattroView:
                    maxSurfacePlotViews = 4
                
                thisView = 0
                while thisView < maxSurfacePlotViews:
                    thisView += 1
                    this_ax, this_fig = func_getProperPlotArea(thisView, ax, fig, ax2, fig2, ax3, fig3, ax4, fig4)

                    # region Possible Color Codes
                    # 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
                    # 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r',
                    # 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r',
                    # 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r',
                    # 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r',
                    # 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r',
                    # 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r',
                    # 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r',
                    # 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r',
                    # 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r',
                    # 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r',
                    # 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r',
                    # 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r',
                    # 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r',
                    # 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r',
                    # 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r',
                    # 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r',
                    # 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r',
                    # 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r',
                    # 'vlag', 'vlag_r', 'winter', 'winter_r'
                    # endregion
                    surface_colors = ["Red", "Blue", "Green", "Purple", "Yellow"]
                    func_printThisClimateZoneSurface(df_referenceSurface, 0, 'magma', this_ax, this_fig,
                                                     showColorBar(cb_refArea))
                    
                    if flag_print_BEFORE_and_DURING_LayUp:
                        func_printThisClimateZoneSurface(df_layupSurface, 0, 'PuBuGn_r', this_ax, this_fig,
                                                         showColorBar(cb_layUpArea))
                        
                        if df_ship3.shape[0] > 0:
                            func_printThisClimateZoneSurface(df_ship3, 0, 'Greens_r', this_ax, this_fig,
                                                         showColorBar(cb_layUpArea))
                        
                        if df_ship4.shape[0] > 0:
                            func_printThisClimateZoneSurface(df_ship4, 0, 'Purples_r', this_ax, this_fig,
                                                         showColorBar(cb_layUpArea))
                        
                        if df_ship5.shape[0] > 0:
                            func_printThisClimateZoneSurface(df_ship5, 0, 'YlGnBu_r', this_ax, this_fig,
                                                         showColorBar(cb_layUpArea))
                        
                        if flag_plotConnectionLineBetweenSurfaces:
                            this_ax.plot_wireframe(x, y, z, cmap='cool', linewidth=2)
                        
        # mp.fig_to_html(fig=fig)
        func_showPlotAndSaveScreenshotIfNeeded(plt, shipNames[dict_shipAP["ship1"]], fileName)
    
    return df_loadReductionHistory


# ######################################################################################################################
def func_shipByShipAnalysis(
   df_referenceSurface,
   avgLoadWholeSurface,
   absoluteReduction_kW,
   relativeReduction_Percent, df_ship3, df_ship4, df_ship5, df_ship6, df_ship7, df_ship8, df_ship9
):
    absoluteReduction_kW, \
    relativeReduction_Percent, \
    avgLoadWholeSurface = func_analyseThisSurface(
        df_referenceSurface, dict_shipAP["ship3"], df_ship3, avgLoadWholeSurface, absoluteReduction_kW,
        relativeReduction_Percent
    )

    absoluteReduction_kW, \
    relativeReduction_Percent, \
    avgLoadWholeSurface = func_analyseThisSurface(
        df_referenceSurface, dict_shipAP["ship4"], df_ship4, avgLoadWholeSurface, absoluteReduction_kW,
        relativeReduction_Percent
    )

    absoluteReduction_kW, \
    relativeReduction_Percent, \
    avgLoadWholeSurface = func_analyseThisSurface(
        df_referenceSurface, dict_shipAP["ship5"], df_ship5, avgLoadWholeSurface, absoluteReduction_kW,
        relativeReduction_Percent
    )

    absoluteReduction_kW, \
    relativeReduction_Percent, \
    avgLoadWholeSurface = func_analyseThisSurface(
        df_referenceSurface, dict_shipAP["ship6"], df_ship6, avgLoadWholeSurface, absoluteReduction_kW,
        relativeReduction_Percent
    )

    absoluteReduction_kW, \
    relativeReduction_Percent, \
    avgLoadWholeSurface = func_analyseThisSurface(
        df_referenceSurface, dict_shipAP["ship7"], df_ship7, avgLoadWholeSurface, absoluteReduction_kW,
        relativeReduction_Percent
    )

    absoluteReduction_kW, \
    relativeReduction_Percent, \
    avgLoadWholeSurface = func_analyseThisSurface(
        df_referenceSurface, dict_shipAP["ship8"], df_ship8, avgLoadWholeSurface, absoluteReduction_kW,
        relativeReduction_Percent
    )

    absoluteReduction_kW, \
    relativeReduction_Percent, \
    avgLoadWholeSurface = func_analyseThisSurface(
        df_referenceSurface, dict_shipAP["ship9"], df_ship9, avgLoadWholeSurface, absoluteReduction_kW,
        relativeReduction_Percent
    )
    
    return absoluteReduction_kW, relativeReduction_Percent, avgLoadWholeSurface

# ######################################################################################################################
def func_analyseThisSurface(
   df_referenceSurface,
   shipKey,
   df_subSurface,
   avgLoadWholeSurface,
   absoluteReduction_kW,
   relativeReduction_Percent
):
    if df_subSurface.shape[0] > 0:
        avgLoadWholeSurface[shipKey] = round(df_subSurface[name_column_approximation].mean(), 1)
        print("avgLoadWholeSurface for " + shipNames[shipKey] + " = " + str(avgLoadWholeSurface[shipKey]))
        
        minLoadLayUp, maxLoadLayUp, avgLoadLayUp, \
        minTempLayup, maxTempLayup, avgTempLayup, \
        minEnthalpyLayup, maxEnthalpyLayup, avgEnthalpyLayup, \
        avgTempSameTempAreaBeforeLayUp, avgEnthalpySameTempAreaBeforeLayUp, avgLoadSameTempAreaBeforeLayUp, \
        beforeLayupSubDfSameRange, avgLoadAtRefSurfaceAboveMiddlePointOfLayUpSurface, \
        absoluteReduction_kW[shipKey], relativeReduction_Percent[shipKey] = func_compareThisSurfaceAgainstRefSurface(
            df_subSurface, df_referenceSurface
        )
        
        print("POWER demand diff between " +
              shipNames[dict_shipAP["ship1"]] + " and " +
              shipNames[shipKey] + " = " + str(absoluteReduction_kW[shipKey])
              )
    
    return absoluteReduction_kW, relativeReduction_Percent, avgLoadWholeSurface
    

# ######################################################################################################################
def showColorBar(
   refArea
):
    if refArea == cb_refArea and flag_showColorScalingBarRightHandSide_ReferenceSurface:
        return True

    if refArea == cb_layUpArea and flag_showColorScalingBarRightHandSide_DuringLayupSurface:
        return True
    
    return False
    

# ######################################################################################################################
def func_showPlotAndSaveScreenshotIfNeeded(
   plt,
   shipName,
   fileName
):
    print(chr(10) + "START func_showPlotAndSaveScreenshotIfNeeded")
    print("shipName " + shipName)
    print("fileName " + fileName)
    
    if flag_createPlotSavescreenshotAndClosePlot:
        # plt.show()
        plt.draw()
        plt.pause(0.001)
        plt.show(block=False)

        # if fileName == '':
        #     if not flag_showOnlyMatchingSurfaces:
        #         if not flag_print_Temp_Ent_PWRSurface_per_Zone:
        #             screenshotName = file_name[2:4] + " " + file_name[5:7] + "_FullAreas.png"
        #         else:
        #             screenshotName = file_name[2:4] + " " + file_name[5:7] + "_FullAreasPerClimateZone.png"
        #     else:
        #         if not flag_print_Temp_Ent_PWRSurface_per_Zone:
        #             screenshotName = file_name[2:4] + " " + file_name[5:7] + "_MatchingAreas.png"
        #         else:
        #             screenshotName = file_name[2:4] + " " + file_name[5:7] + "_MatchingAreasPerClimateZone.png"
        #
        # print("screenshotName " + screenshotName)
        
        if fileName == "":
            if flag_printQuattroView:
                fileName = shipName + " Quadro PWR DEMAND SURFACE.csv"
            else:
                fileName = shipName + " Simple PWR DEMAND SURFACE.csv"
        
        finalScreenshotName = "E:\\001_CMG\\NASA_ARIS_Data\\Results\\PNGs\\" + fileName

        finalScreenshotName = finalScreenshotName.replace("csv", 'png')
        
        print(">>> jea " + finalScreenshotName)
        
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(finalScreenshotName)
    else:
        plt.show()
    
       
# ######################################################################################################################
def func_getProperPlotArea(
   thisView,
   ax,
   fig,
   ax2,
   fig2,
   ax3,
   fig3,
   ax4,
   fig4
):
    if thisView == 1:
        print("view 1")
        return ax, fig
    
    if thisView == 2:
        print("view 2")
        return ax2, fig2
    
    if thisView == 3:
        print("view 3")
        return ax3, fig3
    
    if thisView == 4:
        print("view 4")
        return ax4, fig4
    
    return ax, fig
    

# ######################################################################################################################
def func_printThisClimateZoneSurface(
   thisDF,
   thisClimateZone,
   thisColorPalette,
   ax,
   fig,
   plotLoadBar
):
    if thisClimateZone > 0:
        print("LEN F"+str(thisClimateZone) +" TEMP " +
              str(len(thisDF[thisDF['Corp_ClimateZone'] == thisClimateZone][name_column_x]))
        )
        
        surf1 = ax.plot_trisurf(
            thisDF[thisDF['Corp_ClimateZone'] == thisClimateZone][name_column_x],
            thisDF[thisDF['Corp_ClimateZone'] == thisClimateZone][name_column_y],
            thisDF[thisDF['Corp_ClimateZone'] == thisClimateZone][name_column_approximation],
            cmap=thisColorPalette,
            linewidth=0.2, label='F'+str(thisClimateZone),
            # antialiased=False, rstride=10, cstride=10,
        )
        
        print("### Climate Zone F"+str(thisClimateZone))
        
        print("F"+str(thisClimateZone) +" AVG LOAD: " +
              str(thisDF[thisDF['Corp_ClimateZone'] == thisClimateZone][flag_engineLoad].mean()))
        
        print("F"+str(thisClimateZone) +" StdDev: " +
              str(thisDF[thisDF['Corp_ClimateZone'] == thisClimateZone][flag_engineLoad].std()))
    else:
        surf_all = ax.plot_trisurf(
            thisDF[name_column_x],
            thisDF[name_column_y],
            thisDF[name_column_approximation],  # name_column_approximation #flag_engineLoad
            cmap=thisColorPalette,
            linewidth=0.2
        )
        
        if plotLoadBar:
            fig.colorbar(surf_all, shrink=0.5, aspect=5)
       
    return ax


# ######################################################################################################################
def func_showThisClimateZone(
   df,
   thisClimateZone
):
    print(chr(10) + "### check if it is possible to plot any surface for F" + str(thisClimateZone))
    
    if filter_showThisClimateZoneOnly == 0 or filter_showThisClimateZoneOnly == thisClimateZone:
        
        if len(df[df['Corp_ClimateZone'] == thisClimateZone][name_column_x]) > 50:
            return True
        else:
            print("DO NOT SHOW F" + str(thisClimateZone) +
                  " to little datapoints, only: " +
                  str(len(df[df['Corp_ClimateZone'] == thisClimateZone][name_column_x])))
            
    return False


# ######################################################################################################################
def func_prepareDatasetBeforeDrawingSurface(
   df
):
    print(str(len(df[flag_engineLoad])) + " = LEN of DF BEFORE DATA PREPARED AND FILTERED ")
    
    if 'lastupdateutc' in df.columns:
        df['lastupdateutc'] = pd.to_datetime(df['lastupdateutc'])
    
    if \
       flag_ship_CloseByNasaData_Temperature in df.columns and \
          flag_ship_CloseByNasaData_Enthalpy in df.columns:
        df.dropna(axis=0, subset=[flag_ship_CloseByNasaData_Temperature, flag_ship_CloseByNasaData_Enthalpy],
                  inplace=True)
    
    if flag_ship_CloseByNasaData_Temperature in df.columns:
        df[flag_ship_CloseByNasaData_Temperature] = df[flag_ship_CloseByNasaData_Temperature].astype('float')
    
    if flag_ship_CloseByNasaData_Enthalpy in df.columns:
        df[flag_ship_CloseByNasaData_Enthalpy] = df[flag_ship_CloseByNasaData_Enthalpy].astype('float')
    
    if flag_engineLoad not in df.columns:
        # print("total load is missing")
        df[flag_engineLoad] = df['DG1POW'] + df['DG2POW'] + df['DG3POW'] + df['DG4POW'] + df['DG5POW'] + df['DG6POW']
    
    if 'DG1POW' in df.columns:
        # print("add amount of engines running for every data point")
        df["enginesRunning"] = df.apply(lambda x: func_getEngineCount(
            x['DG1POW'],
            x['DG2POW'],
            x['DG3POW'],
            x['DG4POW'],
            x['DG5POW'],
            x['DG6POW']
        ), axis=1)
    
    
    df = df[df[flag_ship_CloseByNasaData_Temperature] >= filter_minimumTemperature]
    df = df[df[flag_ship_CloseByNasaData_Temperature] <= filter_maximumTemperature]
    df = df[df[flag_ship_CloseByNasaData_Enthalpy] >= filter_minimumEnthalpy]
    df = df[df[flag_ship_CloseByNasaData_Enthalpy] <= filter_maximumEnthalpy]
    
    df = df[df[flag_ship_CloseByNasaData_relHumidity] <= filter_maxRelHumidity]
    df = df[df[flag_engineLoad] <= filter_maximumLoad]
    
    
    print(str(len(df[flag_engineLoad])) + " = LEN DF AFTER FILTER ")
    
    return df


# ######################################################################################################################
def func_getEngineCount(
   dg1, dg2, dg3, dg4, dg5, dg6
):
    engineCount = 0
    if dg1 > 1500:
        engineCount += 1

    if dg2 > 1500:
        engineCount += 1

    if dg3 > 1500:
        engineCount += 1

    if dg4 > 1500:
        engineCount += 1

    if dg5 > 1500:
        engineCount += 1

    if dg6> 1500:
        engineCount += 1

    return engineCount


# ######################################################################################################################
root = tk.Tk()
root.withdraw()

def func_readMainFile(
):
    if useInitialDirs:
        file = filedialog.askopenfilenames(
            initialdir="E:\\001_CMG\\NASA_ARIS_Data\\Results",
            title='Pick a file to show surface'
        )
    else:
        file = filedialog.askopenfilenames(
            title='Pick a file to show surface'
        )
    
    list_file_root = list(root.tk.splitlist(file))
    file_root = list_file_root[0]
    file_name = os.path.basename(file_root)
    
    shipName = file_name[:4]
    print("file_name " + file_name)
    print("shipName " + shipName)
    df = pd.read_csv(file_root, sep=";", decimal=".")
    
    return df, shipName


# ######################################################################################################################
def f_doTheExportOfThisLoadReductionHistory(
   df_loadReductionHistory,
   shipNameThisFile
):
    # print("LEN " + str(df_loadReductionHistory.shape[0]))
    # print(df_loadReductionHistory.head(5))

    fileName = \
        "E:\\001_CMG\\NASA_ARIS_Data\\Results\\Load Reduction History\\" + \
        shipNameThisFile + " Load-Reduction-Layup" + ".csv"

    print("save final file right here:" + fileName)

    df_loadReductionHistory.to_csv(fileName, sep=';', index=None, header=True, decimal='.')
    
    
# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################
df_ship1 = pd.DataFrame()
df_ship2 = pd.DataFrame()
df_ship3 = pd.DataFrame()
df_ship4 = pd.DataFrame()
df_ship5 = pd.DataFrame()
df_ship6 = pd.DataFrame()
df_ship7 = pd.DataFrame()
df_ship8 = pd.DataFrame()
df_ship9 = pd.DataFrame()

df_loadReductionHistory = pd.DataFrame()

shipNames = np.empty(len(dict_shipAP) + 1, dtype=object)
shipNames.fill('')

if flag_createFileWithLoadReductionHistory:
    DO_NOT_SHOW_ANY_GRAPH_ONLY_STATs = True
    totalSurfacesInJustOneGraph = 2
    forceToDoSimpleClassComparison = False
    flag_print_BEFORE_and_DURING_LayUp = True

if forceToDoSimpleClassComparison:
    flag_print_BEFORE_and_DURING_LayUp = True
    
    flag_createFileWithLoadReductionHistory = False
    DO_NOT_SHOW_ANY_GRAPH_ONLY_STATs = False
    flag_showOnlyMatchingSurfaces = False

# ######################################################################################################################

df_Ship1, shipNames[dict_shipAP["ship1"]] = func_readMainFile()
df_Ship1 = func_prepareDatasetBeforeDrawingSurface(df_Ship1)
print("shipNames[dict_shipAP[ship1]] " + shipNames[dict_shipAP["ship1"]])

print("totalSurfacesInJustOneGraph = " + str(totalSurfacesInJustOneGraph) + " read one more ship")

if totalSurfacesInJustOneGraph >= 3:
    print(chr(10) + "### LOAD DATA FOR SHIP # " + str(dict_shipAP["ship3"] + 1))
    
    df_ship3, shipNames[dict_shipAP["ship3"]] = func_readMainFile()
    print("data loaded in dataframe for " + shipNames[dict_shipAP["ship3"]])
    df_ship3 = func_prepareDatasetBeforeDrawingSurface(df_ship3)

if totalSurfacesInJustOneGraph >= 4:
    print(chr(10) + "### LOAD DATA FOR SHIP # " + str(dict_shipAP["ship4"] + 1))
    
    df_ship4, shipNames[dict_shipAP["ship4"]] = func_readMainFile()
    print("data loaded in dataframe for " + shipNames[dict_shipAP["ship4"]])
    df_ship4 = func_prepareDatasetBeforeDrawingSurface(df_ship4)

if totalSurfacesInJustOneGraph >= 5:
    print(chr(10) + "### LOAD DATA FOR SHIP # " + str(dict_shipAP["ship5"] + 1))
    
    df_ship5, shipNames[dict_shipAP["ship5"]] = func_readMainFile()
    print("data loaded in dataframe for " + shipNames[dict_shipAP["ship5"]])
    df_ship5 = func_prepareDatasetBeforeDrawingSurface(df_ship5)

if totalSurfacesInJustOneGraph >= 6:
    print(chr(10) + "### LOAD DATA FOR SHIP # " + str(dict_shipAP["ship6"] + 1))
    
    df_ship6, shipNames[dict_shipAP["ship6"]] = func_readMainFile()
    print("data loaded in dataframe for " + shipNames[dict_shipAP["ship6"]])
    df_ship6 = func_prepareDatasetBeforeDrawingSurface(df_ship6)

if totalSurfacesInJustOneGraph >= 7:
    print(chr(10) + "### LOAD DATA FOR SHIP # " + str(dict_shipAP["ship7"] + 1))
    
    df_ship7, shipNames[dict_shipAP["ship7"]] = func_readMainFile()
    print("data loaded in dataframe for " + shipNames[dict_shipAP["ship7"]])
    df_ship7 = func_prepareDatasetBeforeDrawingSurface(df_ship7)

if totalSurfacesInJustOneGraph >= 8:
    print(chr(10) + "### LOAD DATA FOR SHIP # " + str(dict_shipAP["ship8"] + 1))
    
    df_ship8, shipNames[dict_shipAP["ship8"]] = func_readMainFile()
    print("data loaded in dataframe for " + shipNames[dict_shipAP["ship8"]])
    df_ship8 = func_prepareDatasetBeforeDrawingSurface(df_ship8)

if totalSurfacesInJustOneGraph >= 9:
    print(chr(10) + "### LOAD DATA FOR SHIP # " + str(dict_shipAP["ship9"] + 1))
    
    df_ship9, shipNames[dict_shipAP["ship9"]] = func_readMainFile()
    print("data loaded in dataframe for " + shipNames[dict_shipAP["ship9"]])
    df_ship9 = func_prepareDatasetBeforeDrawingSurface(df_ship9)
    
    
if flag_print_BEFORE_and_DURING_LayUp:
    if useInitialDirs:
        filesToBeTreated = filedialog.askopenfilenames(
            initialdir="E:\\001_CMG\\NASA_ARIS_Data\\Results",
            title='Pick one file or many files during the lay up period'
        )
    else:
        filesToBeTreated = filedialog.askopenfilenames(
            title='Pick file to be shown as surface'
        )
    
    for subFile in filesToBeTreated:
        list_file_root = list(root.tk.splitlist(subFile))
        file_root = list_file_root[0]
        file_name = os.path.basename(subFile)
    
        print("fileName " + file_name)
        shipNames[dict_shipAP["ship2"]] = file_name[:4]
        startDateThisPeriod = file_name[len(file_name)-28:len(file_name)-18]
        endDateThisPeriod = file_name[len(file_name)-14:len(file_name)-4]
        
        # print("startDateThisPeriod: " + str(startDateThisPeriod))
        # print("endDateThisPeriod: " + str(endDateThisPeriod))
        
        if shipNames[dict_shipAP["ship2"]] is not shipNames[dict_shipAP["ship1"]]:
            print("!!! SHIP vs SHIP comparison !!! >>> " +
                  shipNames[dict_shipAP["ship1"]] + " compared to " + shipNames[dict_shipAP["ship2"]]
            )
        
        timePeriod = file_name[len(file_name) - 28:-4]
        
        print("timePeriod " + timePeriod)
        
        df_ship2 = pd.read_csv(subFile, sep=";", decimal=".")
        df_ship2 = func_prepareDatasetBeforeDrawingSurface(df_ship2)

        df_loadReductionHistory = \
            func_createPowerDemandSurfacePlots(
                shipNames, df_Ship1, df_ship2, df_loadReductionHistory,
                timePeriod, file_name, startDateThisPeriod, endDateThisPeriod,
                df_ship3,
                df_ship4,
                df_ship5,
                df_ship6,
                df_ship7,
                df_ship8,
                df_ship9
            )
else:
    df_loadReductionHistory = \
        func_createPowerDemandSurfacePlots(
            shipNames, df_Ship1, df_ship2, df_loadReductionHistory
        )

if df_loadReductionHistory.shape[0] > 0:
    f_doTheExportOfThisLoadReductionHistory(df_loadReductionHistory, shipNames[dict_shipAP["ship2"]])


if playSoundAtTheEnd:
    playsound('hammer_hitwall1.wav')
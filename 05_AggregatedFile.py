

import tkinter as tk
from tkinter import filedialog

import pandas as pd
import os
import datetime

from datetime import date

DATE_layUpInitialDate = datetime.date(2020, 3, 1)

flag_rawData_Ship = "Ship"
flag_rawData_Period_Start = "Period Start"
flag_rawData_Period_End = "Period End"
flag_rawData_avgTempSameTempAreaBeforeLayUp = "avgTempSameTempAreaBeforeLayUp"
flag_rawData_avgEnthalpySameTempAreaBeforeLayUp = "avgEnthalpySameTempAreaBeforeLayUp"
flag_rawData_avgLoadSameTempAreaBeforeLayUp = "avgLoadSameTempAreaBeforeLayUp"
flag_rawData_absoluteReduction_kW = "absoluteReduction_kW"
flag_rawData_relativeReduction_Percent = "relativeReduction_Percent"





# ######################################################################################################################
def func_createBlancDf():
	print(date.today())
	
	thisDay = DATE_layUpInitialDate
	
	df_thisSet = pd.DataFrame()
	
	df_thisSet[flag_file_Date] = ""
	df_thisSet[flag_file_absoluteReduction] = 0
	df_thisSet[flag_file_relativeReduction] = 0
	
	while thisDay <= date.today():
		# print(thisDay)
		thisDay = thisDay + datetime.timedelta(days=1)
		
		df_newLineInWithThisData = [
			{
				flag_file_Date: thisDay
			}
		]
		
		
		df_thisSet = df_thisSet.append(df_newLineInWithThisData, ignore_index=True)
	
	df_thisSet[flag_file_absoluteReduction] = 0
	df_thisSet[flag_file_relativeReduction] = 0
	
	df_thisSet[flag_file_Date] = pd.to_datetime(df_thisSet[flag_file_Date])
	
	return df_thisSet


# ######################################################################################################################
def func_readAllFilesAndAggregateData(
	df_allShips
):
	
	filesToBeTreated = filedialog.askopenfilenames(
		initialdir="E:\\001_CMG\\NASA_ARIS_Data\\Results\\Load Reduction History",
		title='Pick ship files that should be used for fleet total file'
	)
	
	for subFile in filesToBeTreated:
		if df_allShips.shape[0] == 0:
			df_allShips = pd.read_csv(subFile, sep=';', decimal=".", low_memory=False)
		else:
			df_thisShip = pd.read_csv(subFile, sep=';', decimal=".", low_memory=False)
			
			df_allShips = pd.concat([df_allShips, df_thisShip])
	
	return df_allShips


# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################

df_allShips = pd.DataFrame()

# df_allShips = func_createBlancDf()

df_allShips = func_readAllFilesAndAggregateData(df_allShips)

df_allShips.to_csv("LayUpPerformance.csv", sep = ";", decimal=".", index=False)

print(df_allShips.head(10))
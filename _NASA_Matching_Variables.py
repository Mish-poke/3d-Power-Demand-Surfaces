import datetime as dt



masterFile = r'C:\Users\500095\Desktop\NASA_ARIS_Data\SHIPs\_ PA MASTER.csv'
# masterFile = r'C:\Users\500095\Desktop\NASA_ARIS_Data\SHIPs\_ DI MASTER.csv'

flag_zone_timeSeconds = 'Time'
flag_zone_Latitude = 'Latitude'
flag_zone_Longitude = 'Longitude'
flag_zone_SurfTemperature = 'SurfTemperature'
flag_zone_SurfRelHumidity = 'SurfRelHumidity'
flag_zone_SurfAbsHumidity = 'SurfAbsHumidity'
flag_zone_Date = 'Date'
flag_zone_Enthalpy = 'Enthalpy'

flag_noZoneDetected = "no zone found"

flag_historic = 'flag_historic'
flag_NearRealTime = 'flag_NearRealTime'

dict_zones_areas = {
     '_________NORTH EUROPE_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_Greenland': ((-52.229, 59.678), (-42.649, 64.38)),
     'NASA_AIRS_L2_Iceland': ((-24.829, 62.842), (-12.964, 66.973)),
     'NASA_AIRS_L2_Baltic_NorthEast': ((17.446,58.667),(30.41,60.82)),
     'NASA_AIRS_L2_Baltic_SouthEast': ((9.778,53.877),(21.511,55.767)),
     'NASA_AIRS_L2_Norway_SouthWest': ((4.636,57.7),(6.526,62.886)),
     'NASA_AIRS_L2_Norway_SouthWest_2': ((6.531,62.062),(8.773,63.523)),
     'NASA_AIRS_L2_Norway_SouthWest_3': ((8.8,63.171),(14.227,66.467)),
     'NASA_AIRS_L2_Norway_NorthWest': ((12.415,66.533),(20.017,70.488)),
     'NASA_AIRS_L2_North_Sea_Denmark_WestBaltic': ((3.01, 50.537), (13.206, 59.985)),
     'NASA_AIRS_L2_NorthSea_SouthEngland': ((-4.9,47.681),(2.966,51.372)),
     'NASA_AIRS_L2_England_Ireland': ((-10.942,50.098),(-2.593,59.854)),
     '_________SOUTH EUROPE_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_West_France': ((-5.669, 43.066), (-0.923, 48.428)),
     'NASA_AIRS_L2_Portugal': ((-10.151, 36.738), (-7.603, 44.121)),
     'NASA_AIRS_L2_Southern_Spain': ((-7.515, 35.42), (0.044, 37.881)),
     'NASA_AIRS_L2_Canaries_Main': ((-18.853, 27.334), (-12.964, 29.795)),
     'NASA_AIRS_L2_Canaries_Funchal': ((-17.46, 32.531), (-16.543, 32.953)),
     'NASA_AIRS_L2_Capo_Verde': ((-26.18, 14.436), (-22.225, 17.644)),
     'NASA_AIRS_L2_WestMed_Malle_BCN': ((-0.813,37.925),(4.504,42.451)),
     'NASA_AIRS_L2_WestMed_North': ((2.834,42.231),(11.711,44.517)),
     'NASA_AIRS_L2_WestMed_East': ((7.8,38.848),(16.238,42.188)),
     'NASA_AIRS_L2_WestMed_Sicily': ((11.36,35.508),(16.238,38.804)),
     'NASA_AIRS_L2_ADRIA_North': ((11.975,42.1),(16.458,46.274)),
     'NASA_AIRS_L2_ADRIA_South': ((16.414,36.079),(23.269,43.726)),
     'NASA_AIRS_L2_Greece_Turkey': ((23.093,35.024),(27.62,41.704)),
     '_________DUBAI PACIFIC_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_Dubai_Region': ((49.812,23.423), (59.216,26.543)),
     'NASA_AIRS_L2_India_Mumbai': ((72.537, 18.413), (73.098, 19.512)),
     'NASA_AIRS_L2_India_Cochin': ((75.597, 8.833), (76.937, 10.701)),
     'NASA_AIRS_L2_Male': ((73.1, 4.0), (73.886, 4.7)),
     'NASA_AIRS_L2_Madagascar': ((47.417,-18.797),(51.228,-11.5)),
     'NASA_AIRS_L2_Mauritius': ((53.262,-22.236),(59.238,-18.809)),
     'NASA_AIRS_L2_Seychelles': ((53.35,-5.537),(57.393,-3.516)),
     '_________JAPAN CHINA_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_Japan_North': ((131.704, 32.695), (141.724, 37.529)),
     'NASA_AIRS_L2_Japan_South': ((129.353, 30.981), (131.902, 34.233)),
     'NASA_AIRS_L2_South_Korea': ((125.87, 34.08), (129.496, 37.969)),
     'NASA_AIRS_L2_Bohai_Rim': ((117.367, 36.958), (122.684, 40.298)),
     'NASA_AIRS_L2_Naha_Ishigaki': ((123.245, 23.994), (128.43, 27.202)),
     'NASA_AIRS_L2_Shanghai_Region': ((119.993, 27.642), (122.454, 33.574)),
     'NASA_AIRS_L2_Hongkong_Shenzen': ((111.802, 21.478), (116.241, 23.159)),
     '_________SOUTH EAST ASIA_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_Vietnam_Sanya': ((105.359, 18.105), (111.16, 21.709)),
     'NASA_AIRS_L2_Vietnam_East_coast': ((107.622, 10.107), (109.731, 16.875)),
     'NASA_AIRS_L2_SouthThailand_Kambodscha': ((99.141,9.141),(104.106,13.711)),
     'NASA_AIRS_L2_Malysia_EAST': ((102.656,0.483), (105.073,6.021)),
     'NASA_AIRS_L2_Malysia_WEST': ((98.569,1.934),(102.612,8.35)),
     'NASA_AIRS_L2_Northern_Indonesia': ((113.401, 3.911), (117.62, 7.515)),
     'NASA_AIRS_L2_Indonesia_Surabaya': ((104.106, -9.404), (123.003, -5.098)),
     'NASA_AIRS_L2_Philippines': ((118.411, 9.316), (122.454, 18.677)),
     '_________AUSTRALIA & PACIFIC_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_Hawaii': ((-92.186, -1.516), (-88.978, 0.681)),
     'NASA_AIRS_L2_Papeetee': ((-150.038, -17.979), (-148.939, -17.353)),
     'NASA_AIRS_L2_Newzeeland_Northern_Island': ((171.167, -42.187), (179.077, -33.486)),
     'NASA_AIRS_L2_South_East_Australia': ((135.396, -43.77), (151.831, -33.662)),
     '_________NORTH AMERICA & CARIBBEAN_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_US_East_Coast': ((-74.5, 40.178), (-62.677, 45.791)),
     'NASA_AIRS_L2_Caribbean_North': ((-78.684,17.578),(-63.962,20.171)),
     'NASA_AIRS_L2_Caribbean_East': ((-63.171, 11.865), (-60.754, 18.633)),
     'NASA_AIRS_L2_Caribbean_South': ((-83.892,8.701),(-63.062,12.48)),
     'NASA_AIRS_L2_Caribbean_West': ((-88.989,15.645),(-80.552,22.148)),
     'NASA_AIRS_L2_Caribbean_Florida_Freeport_Nassau': ((-82.177, 23.467), (-74.751, 30.146)),
     '_________SOUTH AMERICA & CARIBBEAN_________': ((0,0), (0, 0)),
     'NASA_AIRS_L2_SA_Buenos_Aires': ((-59.315, -35.991), (-53.668, -33.464)),
     'NASA_AIRS_L2_SA_Santos_Rio': ((-46.912, -24.302), (-40.408, -21.665)),
     'NASA_AIRS_L2_SA_East_Coast': ((-49.153, -28.828), (-47.966, -24.961)),
     'NASA_AIRS_L2_SA_Salvador_de_Bahia': ((-39.364, -13.755), (-37.672, -12.437)),
     'NASA_AIRS_L2_Ushuaia_RioGrande': ((-71.115,-55.129),(-66.302,-52.91))
}

# dict_zones_areas_NRT = {
#      'x_NASA_AIRS_L2_WestMed_North_NRT': ((2.834,42.231),(11.711,44.517))
# }

masterPath = r'D:\NASA_AIRS_DATA\NASA_AIRS_CSV_incl_Enthalpy\NASA_FINAL_REGIONS'

# ### DEBUG VARs ##############
FORCE_fullDebugAllComments = False
avoidAnyComments = False
flag_timeStart = 'FunctionTimeMeasurementStart'
flag_timeEnd = 'FunctionTimeMeasurementEnd'

initial_date = dt.datetime(1993, 1, 1, 0, 0, 0)
initial_date_utc = dt.datetime(1970, 1, 1, 0, 0, 0)
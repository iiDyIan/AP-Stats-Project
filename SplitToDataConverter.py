from netCDF4 import Dataset
import os
import csv
import sys

# gross code but neccessary to stop weird error

maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

mainDirectory = "SplitDataDirectory"

parametersOfInterest = [

  "rogue_data",

  "wave_height", 
  "sea_state_30m_significant_wave_height_direct", 

  "wave_ursell_number", 

  "sea_state_30m_mean_period_direct",
  "sea_state_30m_mean_period_spectral",

  "sea_state_30m_skewness",
  "sea_state_30m_kurtosis",

  "sea_state_30m_peak_wave_period",
  "sea_state_30m_peak_wavelength",

  "sea_state_30m_steepness",
  "sea_state_30m_bandwidth_peakedness",
  "sea_state_30m_bandwidth_narrowness",

  "sea_state_30m_benjamin_feir_index_peakedness",
  "sea_state_30m_benjamin_feir_index_narrowness",

  "sea_state_30m_crest_trough_correlation",

  "direction_peak_wave_direction",
  "direction_directionality_index"

  ]

for parameter in parametersOfInterest:
    parameterOutput = []

    for filename in os.listdir(mainDirectory):
        with open(mainDirectory+"\\"+filename, 'r') as data:
            for line in csv.reader(data):
                if line != []:
                    mainLine = list(line)
                    if mainLine[0] == parameter and len(mainLine[1]) > 2:
                        mainData = (mainLine[1])
                        mainData = mainData.replace('[', "")
                        mainData = mainData.replace(']', "")
                        res = [float(idx) for idx in mainData.split(', ')]
                        parameterOutput += res
                        

    w = csv.writer(open(str(parameter)+".csv", "w"))
    w.writerow(parameterOutput)

    print(len(parameterOutput))

from netCDF4 import Dataset
import numpy
import os
import math
import csv

mainDirectory = "DataDirectory"

parametersOfInterest = [

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

for filename in os.listdir(mainDirectory):
  f = os.path.join(mainDirectory, filename)

  if os.path.isfile(f):
    ncdf = Dataset(f)
    variables = ncdf.variables
    
    dataExport = {}

    dataExport[filename] = {}

    print("Firing up "+f+"!")

    parameterArray = variables["wave_height"][:]

    splitNum = parameterArray.size/10000
    if math.ceil(splitNum) % 2 != 0:
      splitNum = math.floor(splitNum)
    else:
      splitNum = math.ceil(splitNum)
    
    currentSplitCount = 0
    currentWaveCount = 0
    currentSplitRogueCount = 0

    splitRogueData = []

    for h, sh in numpy.nditer([variables["wave_height"][:], variables["sea_state_30m_significant_wave_height_direct"][:]]):

      currentWaveCount += 1

      if h > sh:
        currentSplitRogueCount += 1

      if currentWaveCount > (currentSplitCount+1)*10000:

        splitRogueData.append([currentWaveCount-(currentSplitCount*10000), currentSplitRogueCount])        
        currentSplitCount += 1
        currentSplitRogueCount = 0

        if int(currentSplitCount) % 10 == 0:
            print("   Rogue data iterated to split "+str(currentSplitCount)+" of "+str(splitNum)+" total splits.")

    dataExport[filename]["rogue_data"] = splitRogueData

    for parameter in parametersOfInterest:

      dataExport[filename][parameter] = []

      parameterArray = (numpy.ma.MaskedArray.filled(variables[parameter][:]))
      parameterArrayRaw = (numpy.ma.MaskedArray.filled(variables[parameter][:]))[0]

      # calculate split number, round up/down to make integer even
      splitNum = parameterArray.size/10000
      if math.ceil(splitNum) % 2 != 0:
        splitNum = math.floor(splitNum)
      else:
        splitNum = math.ceil(splitNum)

      currentSplitCount = 0
      currentWaveCount = 0

      splitData = []

      for x in parameterArrayRaw:

        currentWaveCount += 1

        # check if need to iterate to next split (excluding split 0)
        if currentWaveCount > (currentSplitCount+1)*10000:

          # update split count and declare array for upcoming split
          currentSplitCount += 1
          splitData.append(numpy.array([]))        
          splitData[currentSplitCount] = numpy.append(splitData[currentSplitCount], x)

          # export current split count
          if int(currentSplitCount) % 10 == 0:
            print("   Parameter "+str(parameter)+" iterated to split "+str(currentSplitCount)+" of "+str(splitNum)+" total splits.")

        elif currentSplitCount == 0 and len(splitData) == 0:

          # declare array for upcoming split if split is 0 and undeclared
          splitData.append(numpy.array([]))

        else:

          # append data to current split if split count doesn't need changing
          splitData[currentSplitCount] = numpy.append(splitData[currentSplitCount], x)
      
      parameterData = []

      for x in splitData:
        parameterData.append(numpy.mean(x))

      dataExport[filename][parameter] = parameterData

    # finally export the appropriate split data to a csv

    for key, val in dataExport.items():
      w = csv.writer(open((str(key)+"output.csv"), "w"))
      for key2, val2 in val.items():
          w.writerow([key2, val2])

    # reset all vars to hopefully not mem leak too much

    parameterData = []
    dataExport[filename][parameter] = []
    splitData = []

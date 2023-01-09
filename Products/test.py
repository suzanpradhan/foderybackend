
from typing import List


dataOld = {"data":"dkfjgjh"}

def ulala(data):
    tempData = []
    if isinstance(data, List):
        for i in data:
            return ulala(i)
    else:
        tempSplits = data.split(".")
        if len(tempSplits) > 1:
            for j in tempSplits:
                tempData['j'] = dataOld['j']
        else:
            print(tempSplits[0])
            if (not isinstance(tempData, List)):
                tempData = {}
                tempData[tempSplits[0]] = dataOld[tempSplits[0]]
    return 
ulala(['data'])
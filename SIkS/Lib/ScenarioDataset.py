##################################
#                                # 
# Author: Gavin Moore            #
# Date: 06/23/2023               #
#                                #
# File that contains the dataset #
# to be used to store scenarios  #
#                                #
##################################
import ScenarioData as SData
import json as js



# WIP outline to show how dataset will be designed and considered
# TODO: Define API that stores datasets of this form in JSON files and loads them
x, y = 0, 0

xi, yi = 0, 0

HomogenousDataset = {
    "size":        [x, y],
    "obstacles":   [SData.Shape()],
    "roi":         [SData.Shape()],
    "sensor_data": SData.SensorData(),
    "sensors":     [SData.Shape()],
    "paths":       [SData.Path()]
}

HeterogenousDataset = {
    "size":      [x, y],
    "obstacles": [SData.Shape()],
    "roi":       [SData.Shape()],
    "sensors":   [SData.Sensor()],
    "paths":     [SData.Path()]
}



class ScenarioDataset():
    def __init__(self, datasetMode="homo", filename="default.json") -> None:
        '''
        @ARGS
        datasetMode => Can be either hetero or homo; not case sensitive
        filename => Defines the filename that the file will be stored under 
        '''
        self.DatasetType = datasetMode.upper()
        
        assert self.DatasetType in ("HOMO", "HETERO"), \
           f"Invalid datasetMode parameter {datasetMode} set as {self.DatasetType}" 
        
        
            
        
        pass
    
    
    def LoadDataset():
        # LoadingDict = js.
        
        
        pass
    
    def StoreDataset():
        pass
    
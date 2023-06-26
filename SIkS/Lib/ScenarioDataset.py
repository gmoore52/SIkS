##################################
#                                # 
# Author: Gavin Moore            #
# Date: 06/23/2023               #
#                                #
# File that contains the dataset #
# to be used to store scenarios  #
#                                #
##################################
from . import ScenarioData as SData
import json as js



# WIP outline to show how dataset will be designed and considered
# TODO: Define API that stores datasets of this form in JSON files and loads them
x, y = 0, 0

HomogenousDataset = {
    "size":        [x, y],
    "obstacles":   [SData.Shape],
    "roi":         [SData.Shape],
    "sensor_data": SData.SensorData(),
    "sensors":     [SData.Shape],
    "paths":       [SData.Path]
}

HeterogenousDataset = {
    "size":        [x, y],
    "obstacles":   [SData.Shape],
    "roi":         [SData.Shape],
    "sensors":     [SData.Sensor],
    "paths":       [SData.Path]
}



class ScenarioDataset():
    def __init__(self, datasetMode="homo", filename="default.json", areaSize=(64, 64)):
        '''
        @ARGS
        datasetMode => Can be either hetero or homo or load; not case sensitive
        filename => Defines the filename that the file will be stored under 
        '''
        self.Dataset = {
                        "size":        [areaSize[0], areaSize[1]],
                        "obstacles":   [],
                        "roi":         [],
                        "paths":       []
            }
        if datasetMode.upper() == "LOAD":
            self.LoadDataset()
            self.DatasetType = "HOMO" if "sensor_data" in self.Dataset.keys() \
                          else "HETERO"
                          
                          
        
        self.DatasetType = datasetMode.upper()
        self.FileName = filename
        
        assert self.DatasetType in ("HOMO", "HETERO"), \
           f"Invalid datasetMode parameter {datasetMode} set as {self.DatasetType}" 
           
        assert self.FileName[-5:] == ".json", \
            f"Invalid filename, please use .json extension; Set filename is {filename}"
            
        assert len(areaSize) == 2 ,\
            f"Invalid areaSize param; use a tuple/list of length 2 to contain each \
            dimension; object passed: {areaSize}"
           
           
        
        
        
        if self.DatasetType == "HOMO":
            self.Dataset["sensor_data"] = []
            self.Dataset["sensors"]     = []
        
        if self.DatasetType == "HETERO":
            self.Dataset["sensors"]     = []
        
        
        self.StoreDataset()
            
        
        
    
    
    def LoadDataset(self):
        with open(self.FileName, 'r') as infile:
            self.Dataset = js.load(infile)
            assert all(key in self.Dataset.keys() \
                       for key in ["size", "obstacles", "roi", "paths", "sensors"]) \
                    and len(self.Dataset.keys()) in (5, 6), \
                    f"Invalid Data loaded at file {self.FileName}; Data not in proper format"
            self.DatasetType = "HOMO" if "sensor_data" in self.Dataset.keys() \
                          else "HETERO"
            infile.close()
        
        
    
    def StoreDataset(self, p: list[SData.Shape]):
        with open(self.FileName, 'w') as outfile:
            js.dump(self.Dataset, outfile, indent=4)
            outfile.close()
            
    def AddSensor(self, param: SData.Sensor):
        pass
        
    
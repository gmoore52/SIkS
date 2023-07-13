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
import os
import pickle

class ScenarioDataset():
    def __init__(self, areaSize=(64,64)):
    
        self.Size = areaSize
        self.SensorData = SData.SensorData()
        self.Obstacles = []
        self.FOI = []
        self.Sensors = []
        
    
    def SetSize(self, param=(64,64)):
        self.Size = param
    
    def SetSensorData(self, param: SData.SensorData):
        self.SensorData = param
            
    def AddSensor(self, param: SData.Sensor):
        self.Sensors.append(param)
    
    def AddObstacle(self, param: SData.Shape):
        self.Obstacles.append(param)
    
    def AddFieldOfInterest(self, param: SData.FieldOfInterest):
        self.FOI.append(param)
        
class ScenarioDatasetAPI():
    def __init__(self, filename: str ="default.ksce", filepath: str =os.path.curdir):
        '''
        @ARGS
        filename => Defines the filename that the file will be stored under 
        '''
        self.Filepath = filepath
        self.FileName = os.path.join(self.Filepath, filename)
            
        assert self.FileName[-5:] == ".ksce", \
            f"Invalid filename, please use .ksce extension; Set filename is {filename}"
            
        assert self.FileName != "default.ksce", \
            "Filename is set to default, please pass a filename on initilization of dataset API"
            
            
        self.Dataset = ScenarioDataset()
        if os.path.exists(filename):
            self.LoadDataset()
        else:
            self.StoreDataset()
            
            
    def LoadDataset(self):
        result = ScenarioDataset()
        with open(self.FileName, 'rb') as infile:
            result = pickle.load(infile)
            infile.close()
        
        return result
    
    def StoreDataset(self):
        with open(self.FileName, 'wb') as outfile:
            pickle.dump(self.Dataset, outfile)
            outfile.close()
            
    def SetFilepath(self, filepath: str):
        self.Filepath = filepath
            
    def SetFilename(self, filename: str):
        assert self.FileName[-5:] == ".ksce", \
            f"Invalid filename, please use .ksce extension; Set filename is {filename}"
        self.FileName = os.path.join(self.Filepath, filename)
            
    def SetDataset(self, dataset: ScenarioDataset):
        self.Dataset = dataset
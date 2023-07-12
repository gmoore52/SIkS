import Lib.ScenarioDataset as SData
import Lib.ScenarioData as SD
import numpy as np


class ScenarioSimulator:
    def __init__(self, dataset: SData.ScenarioDataset) -> None:
        self.ScenarioDim = dataset.Size
        # self.Sensors = dataset.Sensors
        
        self.Sensors = {}
        self.Actions = {}
        self.SenseData = dataset.SensorData
        # Make the sensors a map storing their respective ID and their sensor object
        for id, sensor in enumerate(dataset.Sensors):
            self.Sensors[id] = sensor
            
        # Randomly deploy sensors immediately
        self.RandomlyDeploySensors()
        
        # Deployment field will cotnain valid, invalid, and taken positions
        # 0 => valid; 1 => taken; 2=> invalid
        self.DeploymentField = np.zeros(self.ScenarioDim)
        self.ComputeDeploymentField()
    # change int type to int32 for 2^32 degrees of coverage, current 255 max coverage
        self.CoverageMatrix = np.zeros(self.ScenarioDim, dtype=np.int8)
        
        
        
        
    def CalculateCircularIntersection(self, sensor: SD.Sensor, position: SD.Point):
        '''
        Uses Euclidean Distance formula to determine if the point in question is inside
        the sensing range of the sensor in question and returns the boolean result
        '''
        return (((position.xPos-sensor.Position.xPos)**2 + 
                (position.yPos-sensor.Position.yPos)**2) ** 0.5) \
                <= self.SenseData.SensingRange
        
        
    def ComputeCoverage(self):
        # Reset coverage matrix
        self.CoverageMatrix = np.zeros(self.ScenarioDim, dtype=np.int8)
        
        # Loop through every element of the coverage matrix and compute if its distance
        # shows that it is inside the range of each sensor
        # The coverage matrix will show the coverage degree of each respective point in
        # the finite field in question, the field will be considered with only integer 
        # distances for simplicities sake
        for y in range(self.ScenarioDim[1]):
            for x in range(self.ScenarioDim[0]):
                for id, sensor in self.Sensors.items():
                    if self.CalculateCircularIntersection(sensor, SD.Point(x=x, y=y)):
                        self.CoverageMatrix[y][x] += 1
                        
                        
    def ComputeDeploymentField(self):
        '''
        Function to compute deployment field based on sensor positions
        '''
        for sensor in self.Sensors.values():
            x, y = sensor.Position.xPos, sensor.Position.yPos
            self.DeploymentField[y, x] = 2
            
        
                        
                        
    def RandomlyDeploySensors(self):
        for id, sensor in self.Sensors.items():
            validPos = np.random.choice(np.argwhere(self.DeploymentField==0))
            self.Sensors[id].Position.xPos, self.Sensors[id].Position.yPos = \
                validPos[0], validPos[1]
            self.DeploymentField[validPos[0], validPos[1]] = 2
        
        self.ComputeDeploymentField()
        self.ComputeCoverage()
    
    def GetSensorObsFromID(self, senseID):
        # Get Sensor data for each sensor that contains the proper 
        sensor = self.Sensors[senseID]
        senseRange, moveRange = self.SenseData.SenseRange, self.SenseData.MoveRange
        obsSize = ((senseRange+moveRange)*2, (senseRange+moveRange)*2)
        obsPos = (sensor.Position.xPos - obsSize[0], sensor.Position.yPos - obsSize[1])
        
        # TODO: Currently do not account for valid ranges of indices
        CovObsMatrix = \
        self.CoverageMatrix[obsPos[1]-1:obsPos+obsSize[0], obsPos[0]-1:obsPos+obsSize[1]]
        PosObsMatrix = \
        self.DeploymentField[obsPos[1]-1:obsPos+obsSize[0], obsPos[0]-1:obsPos+obsSize[1]]
        
        
        return CovObsMatrix, PosObsMatrix
    
    def GetGlobalObs(self):
        # self.ComputeCoverage()
        # self.ComputeDeploymentField()
        return self.CoverageMatrix, self.DeploymentField
    

    def GetValidActions(self):
        '''
        Function returns a dictionary containing each sensor ID mapped to 
        the valid action list for each sensor ID
        '''
        actions = {}
        for id in self.Sensors.keys():
            actions[id] = self.GetValidActionForID(id)
        
        return actions
    
    
    def GetValidActionForID(self, ID):
        '''
        Function returns an action list that contains valid movement positions
        for the sensor with the id ID
        '''
        actionList = []
        # We will use the midpoint-circle algorithm to calculate valid action indices
        sensor = self.Sensors[ID]
        xPos, yPos = sensor.Position.xPos, sensor.Position.yPos
        radius = self.SenseData.SensingRange
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        actionList.append([xPos, yPos+radius])
        actionList.append([xPos, yPos-radius])
        actionList.append([xPos+radius, yPos])
        actionList.append([xPos-radius, yPos])

        while x < y:
            if f >= 0: 
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x    
            actionList.append([xPos + x, yPos + y])
            actionList.append([xPos - x, yPos + y])
            actionList.append([xPos + x, yPos - y])
            actionList.append([xPos - x, yPos - y])
            actionList.append([xPos + y, yPos + x])
            actionList.append([xPos - y, yPos + x])
            actionList.append([xPos + y, yPos - x])
            actionList.append([xPos - y, yPos - x])
            
        return actionList
    

    def LoadActionToID(self, ID, action):
        '''
        Function loads the action to the action list
        '''
        assert action not in self.GetValidActionForID(ID), \
            "Invalid action passed as action"
            
        self.Actions[ID] = action
        
    
    def GenerateNewScenario(self):
        '''
        Function generates new scenario based on the actions list
        can be seen as version of step() function
        '''
        assert self.Actions.keys() == self.Sensors.Keys, \
            "Not enough actions loaded to actions list or invalid actions"
            
            
        for id in self.Actions.keys():
            self.DeploymentField[self.Sensors[id].xPos, self.Sensors[id].yPos] = 0
            self.Sensors[id].xPos = self.Actions[id][0]
            self.Sensors[id].yPos = self.Actions[id][1]
            self.DeploymentField[self.Sensors[id].xPos, self.Sensors[id].yPos] = 1
            
        self.ComputeCoverage()
    

           
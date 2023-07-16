import sys
sys.path.append("/home/gavin/Dev/SIkS/SIkS/")

import Lib.ScenarioDataset as SData
import Lib.ScenarioData as SD
import numpy as np
import skimage.draw as skd


class ScenarioSimulator:
    def __init__(self, dataset: SData.ScenarioDataset):
        self.ScenarioDim = dataset.Size
        
        self.Sensors = {}
        self.Actions = {}
        self.SenseData = dataset.SensorData
        # Make the sensors a map storing their respective ID and their sensor object
        for id, sensor in enumerate(dataset.Sensors):
            self.Sensors[id] = sensor
            
        
        # Deployment field will cotnain valid, invalid, and taken positions
        # 0 => valid; 1 => taken; 2=> invalid
        self.DeploymentField = np.zeros(self.ScenarioDim)
        # Randomly deploy sensors immediately
        self.RandomlyDeploySensors()
        self.ComputeDeploymentField()
    # change int type to int32 for 2^32 degrees of coverage, current 255 max coverage
        self.CoverageMatrix = np.zeros(self.ScenarioDim, dtype=np.int8)
        self.ComputeCoverage()
        
        
        
    def ComputeCoverage(self):
        '''
        Method that will compute our coverage matrix based on current sensor data
        and on current sensor positions
        '''
        # Reset coverage matrix to be all zeros
        self.CoverageMatrix = np.zeros(self.ScenarioDim, dtype=np.int8)
        # We will use the disk method from skimage.draw that will help draw a disk of
        # appropriate size and position in our coverage matrix relative to each sensor
        # each sensor will increase the coverage of each point inside its disk by 1 
        for id, sensor in self.Sensors.items():
            x, y = \
                sensor.Position.xPos, sensor.Position.yPos
            rr, cc = skd.disk((x, y), self.SenseData.SensingRange, shape=None)
            rr, cc = np.clip(rr, 0, self.ScenarioDim[0]-1), np.clip(cc, 0, self.ScenarioDim[1]-1)
            self.CoverageMatrix[rr, cc] += 1
                        
                        
    def ComputeDeploymentField(self):
        '''
        Function to compute deployment field based on sensor positions
        '''
        for sensor in self.Sensors.values():
            x, y = sensor.Position.xPos, sensor.Position.yPos
            self.DeploymentField[x, y] = 1
            
        
                        
                        
    def RandomlyDeploySensors(self):
        '''
        Function that can be used to reset the simulation via randomly deploying sensors
        will check for valid indices each time it deploys a sensor
        '''
        for id, sensor in self.Sensors.items():
            validIndices = np.argwhere(self.DeploymentField==0)
            validPos = validIndices[np.random.choice(len(validIndices))]
            self.Sensors[id].Position.xPos, self.Sensors[id].Position.yPos = \
                validPos[0], validPos[1]
            self.DeploymentField[validPos[0], validPos[1]] = 1
        
        self.ComputeDeploymentField()
        self.ComputeCoverage()
    
    def GetSensorObsFromID(self, senseID):
        '''
        Function that gets observation data for each respective sensor with id senseID
        '''
        # Get Sensor data for each sensor that contains the proper 
        sensor = self.Sensors[senseID]
        senseRange, moveRange = self.SenseData.SensingRange, self.SenseData.MoveRange
        # Make size and position of the observations in relation to the sensor data
        # and to each respective sensors position
        obsSize = ((senseRange+moveRange)*2, (senseRange+moveRange)*2)
        obsPos = [sensor.Position.xPos - (obsSize[0]//2), sensor.Position.yPos - (obsSize[1]//2)]
        # Make the observation matrices to be returned at the end of the function
        covMatrix = np.zeros(obsSize)
        posMatrix = np.zeros(obsSize)
        
        borderSize = ((obsSize[0]*2)+self.ScenarioDim[0], (obsSize[1]*2)+self.ScenarioDim[1])
        # Use -1 for coverageMatrix as negative is nonexistent coverage
        BorderCoverageMatrix   = np.full(borderSize, -1)
        # Use 2 for deploymentMatrix as 2 is invalid index for deployment
        BorderDeploymentMatrix = np.full(borderSize,  2)
        
        # Fill the proper areas in the border matrices
        BorderCoverageMatrix[obsSize[0]:-obsSize[0], obsSize[1]:-obsSize[1]]   = self.CoverageMatrix
        BorderDeploymentMatrix[obsSize[0]:-obsSize[0], obsSize[1]:-obsSize[1]] = self.DeploymentField
        
        # TODO: Debug if the positions are valid or if they need pushed over by a constant
        # Make new positions for the border matrices
        borderPos = (obsPos[0]+obsSize[0], obsPos[1]+obsSize[1])
        # Calculate the coverage and positon matrix based on the border matrices
        covMatrix = \
        BorderCoverageMatrix[borderPos[0]-1:borderPos[0]+obsSize[0],
                             borderPos[1]-1:borderPos[1]+obsSize[1]]
        
        posMatrix = \
            BorderDeploymentMatrix[borderPos[0]-1:borderPos[0]+obsSize[0], 
                                   borderPos[1]-1:borderPos[1]+obsSize[1]]
            
        return covMatrix, posMatrix
    
    
    def GetGlobalObs(self):
        '''
        Function that will return the global state/observations in the form
        of the covreage matrix and the deployment field
        '''
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
            
        # Trim the actions list to only account for valid movements
        trimmedActions = \
            np.clip(actionList, [0, 0], [self.ScenarioDim[0]-1, self.ScenarioDim[1]-1])
        # Return only the trimmed valid movements that are available positions
        # according to the deployment field
        trimmedActions = [a for a in trimmedActions if self.DeploymentField[a[0], a[1]] == 0]
        return trimmedActions
        return [a for a in trimmedActions if self.DeploymentField[a[0], a[1]] == 0]
    

    def LoadActionToID(self, ID, action):
        '''
        Function loads the action to the action list
        '''
        assert np.any(np.all(action == self.GetValidActionForID(ID), axis=1)), \
            "Invalid action passed as action"
            
        self.Actions[ID] = action
        
    
    def GenerateNewScenario(self):
        '''
        Function generates new scenario based on the actions list
        can be seen as version of step() function
        '''
        assert self.Actions.keys() == self.Sensors.keys(), \
            "Not enough actions loaded to actions list or invalid actions"
            
            
        for id in self.Actions.keys():
            self.DeploymentField[self.Sensors[id].Position.xPos, self.Sensors[id].Position.yPos] = 0
            self.Sensors[id].Position.xPos = self.Actions[id][0]
            self.Sensors[id].Position.yPos = self.Actions[id][1]
            self.DeploymentField[self.Sensors[id].Position.xPos, self.Sensors[id].Position.yPos] = 1
            
        self.ComputeDeploymentField()
        self.ComputeCoverage()
    

           
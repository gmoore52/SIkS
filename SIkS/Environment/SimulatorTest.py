# import sys
# sys.path.append("/home/gavin/Dev/SIkS/SIkS/")
import ScenarioSimulator as ss
import Lib.ScenarioDataset as sd
from matplotlib import pyplot as plt
import numpy as np







if __name__ == "__main__":
    API = sd.ScenarioDatasetAPI(filename="newTest2.ksce", filepath="/home/gavin/Dev/SIkS/SIkS/Environment/")
    
    API.SetFilename("test58.ksce")
    Dataset = API.LoadDataset()
    
    
    STEPS = 25
    # Dataset.Sensors = []
    
    print(Dataset.SensorData)
    
    
    # Dataset.SensorData.SensingRange = 30
    # Dataset.SensorData.CommRange = 60
    Dataset.SensorData.MoveRange = 25
    
    
    Sim = ss.ScenarioSimulator(dataset=Dataset)
    
    n_agents = len(Sim.Sensors)
    
    plt.ion()
    fig = plt.figure()
    
    for _ in range(STEPS):
        
        
        actions = []
        for a_id in range(n_agents):
            avail_actions = Sim.GetValidActionForID(a_id)
            avail_action_ind = np.nonzero(avail_actions)[0]
            action = avail_actions[np.random.choice(avail_action_ind)]
            Sim.LoadActionToID(a_id, action)
            obs = Sim.GetSensorObsFromID(a_id)
    
        Sim.GenerateNewScenario() # like step
    
        ax =  fig.add_subplot(3, 2, 1)
        ax2 = fig.add_subplot(3, 2, 2)
        ax3 = fig.add_subplot(3, 2, 3)
        ax4 = fig.add_subplot(3, 2, 4)
        ax5 = fig.add_subplot(3, 2, 5)
        ax6 = fig.add_subplot(3, 2, 6)
        covMat, depField = Sim.GetGlobalObs()
        aField1, aField1_2 = Sim.GetSensorObsFromID(3)
        aField2, aField2_2 = Sim.GetSensorObsFromID(2)
        ax.matshow(depField)
        ax2.matshow(covMat)
        ax3.matshow(aField1)
        ax4.matshow(aField2)
        ax5.matshow(aField1_2)
        ax6.matshow(aField2_2)
        plt.pause(0.000001)
        
        
        plt.draw()

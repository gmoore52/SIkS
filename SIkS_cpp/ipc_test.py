import SimulatorServerWrapper as SW
import matplotlib.pyplot as plt
import time
import numpy as np

# plt.ion()
# fig = plt.figure()
#
# ax =  fig.add_subplot(3, 2, 1)
# ax2 = fig.add_subplot(3, 2, 2)
# ax3 = fig.add_subplot(3, 2, 3)
# # ax4 = fig.add_subplot(3, 2, 4)
# # ax5 = fig.add_subplot(3, 2, 5)
# # ax6 = fig.add_subplot(3, 2, 6)
#
#
# server = SW.SimulatorServer("./cmake-build-debug/newTest12.json")
#
# cov_mat = server.GetCoverageMatrix()
# dep_field = server.GetDeploymentField()
# des_mat = server.GetDesiredMatrix()
#
# server.Reset()
# acts = server.GetAvailActions()
#
# # server.Step()
#
# ax.matshow(cov_mat)
# ax2.matshow(dep_field)
# ax3.matshow(des_mat)
#
# plt.draw()
# plt.cla()
#
# plt.show()

STEPS = 10
# Dataset.Sensors = []

# print(Dataset.SensorData)


# Dataset.SensorData.SensingRange = 10
# Dataset.SensorData.CommRange = 60
# Dataset.SensorData.MoveRange = 2
for x in range(1, 11):
    seconds = time.time()
    # Sim = ss.ScenarioSimulator(datasetName="newTest12.json",
    #                            filepath="./cmake-build-debug",
    #                            episode_limit=50,
    #                            randomly_deploy=False)
    server = SW.SimulatorServer("./cmake-build-debug/newTest12.json")

    # Sim = ss.ScenarioSimulator(dataset=Dataset)

    n_agents = server.GetNAgents()

    # plt.ion()
    # fig = plt.figure()
    #
    # ax =  fig.add_subplot(3, 2, 1)
    # ax2 = fig.add_subplot(3, 2, 2)
    # ax3 = fig.add_subplot(3, 2, 3)
    # ax4 = fig.add_subplot(3, 2, 4)
    # ax5 = fig.add_subplot(3, 2, 5)
    # ax6 = fig.add_subplot(3, 2, 6)

    for _ in range(STEPS*x):


        actions = []
        for a_id in range(n_agents):
            avail_actions = server.GetAvailAgentActions(a_id)
            avail_action_ind = np.nonzero(avail_actions)[0]
            action = avail_actions[np.random.choice(avail_action_ind)]
            # Sim.LoadActionToID(a_id, action)
            actions.append(action)
            obs = server.GetObsAgent(a_id)

        server.Step(actions) # like step
        covMat, depField, desMat = server.GetState()
        server.GetObs()
        # a_id1, a_id2 = np.random.choice(range(n_agents)), np.random.choice(range(n_agents))
        # aField1, aField1_2 = Sim.get_obs_agent(a_id1)
        # aField2, aField2_2 = Sim.get_obs_agent(a_id2)
        # ax.matshow(depField)
        # ax2.matshow(covMat)
        # ax3.matshow(aField1)
        # ax4.matshow(aField2)
        # ax5.matshow(aField1_2)
        # ax6.matshow(desMat)
        # plt.pause(0.000001)


        # plt.draw()
        # plt.cla()

        print(f"Step {_} completed")

    time_since = time.time() - seconds
    print(f"Took approximatly {time_since} seconds to run {STEPS*x} steps ")

# print(server.GetCoverageMatrix())




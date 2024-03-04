import SimulatorServerWrapper as SW
import matplotlib.pyplot as plt

# plt.ion()
fig = plt.figure()

ax =  fig.add_subplot(3, 2, 1)
ax2 = fig.add_subplot(3, 2, 2)
ax3 = fig.add_subplot(3, 2, 3)
# ax4 = fig.add_subplot(3, 2, 4)
# ax5 = fig.add_subplot(3, 2, 5)
# ax6 = fig.add_subplot(3, 2, 6)


server = SW.SimulatorServer("./cmake-build-debug/newTest12.json")

cov_mat = server.GetCoverageMatrix()
dep_field = server.GetDeploymentField()
des_mat = server.GetDesiredMatrix()

server.Reset()
acts = server.GetAvailActions()

# server.Step()

ax.matshow(cov_mat)
ax2.matshow(dep_field)
ax3.matshow(des_mat)

plt.draw()
plt.cla()

# print(server.GetCoverageMatrix())




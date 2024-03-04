import subprocess
import time
import os
import socket
import numpy as np

class SimulatorServer:
    PORT_NUM = 8080
    BUFFER_SIZE = 2**20
    def __init__(self, fileName):
        self.ServerProcess = subprocess.Popen(["./cmake-build-debug/SMAWS", str(SimulatorServer.PORT_NUM),
                                               fileName], stdout=subprocess.PIPE)
        # self.ClientSocket

        while True:
            try:
                self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.ClientSocket.connect(("localhost", SimulatorServer.PORT_NUM))
                break
            except ConnectionRefusedError:
                time.sleep(1)

        response = self.ClientSocket.recv(SimulatorServer.BUFFER_SIZE).decode()
        if response == "Connection with Python Received!":
            print("Connection to C++ server successful!")

    def SendRequest(self, request, *args):
        self.ClientSocket.send(f"{request} {len(args)} {' '.join(map(str, args))}".encode())

    def GetResponse(self):
        chunks = []
        bytes_recd = 0
        msg_len = 2048
        while bytes_recd < msg_len:
            chunk = self.ClientSocket.recv(min(msg_len - bytes_recd, 2048)).decode()
            msg_len = int(chunk.split()[0]) if bytes_recd == 0 else msg_len
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        # Don't return the first value indicating size
        ret_data = ''.join(chunks)
        # return ''.join(chunks)
        return ' '.join(ret_data.split()[1:])
        # return self.ClientSocket.recv(SimulatorServer.BUFFER_SIZE).decode()

    def GetObs(self):
        self.SendRequest("get_obs")
        return self.DeserializeObs(self.GetResponse())

    def GetObsAgent(self, a_id):
        self.SendRequest("get_obs_agent", a_id)
        return self.DeserializeMatrix(self.GetResponse())

    def GetObsSize(self):
        self.SendRequest("get_obs_size")
        return self.DeserializeVector(self.GetResponse())

    def GetState(self):
        self.SendRequest("get_state")
        return self.DeserializeState(self.GetResponse())

    def GetStateSize(self):
        self.SendRequest("get_state_size")
        return self.DeserializeUnsigned(self.GetResponse())

    def GetAvailAgentActions(self, a_id):
        self.SendRequest("get_avail_agent_actions", a_id)
        return self.DeserializeVector(self.GetResponse())

    def GetAvailActions(self):
        self.SendRequest("get_avail_actions")
        return self.DeserializeActionVector(self.GetResponse())

    def Reset(self):
        self.SendRequest("reset")
        return self.DeserializeResetVector(self.GetResponse())

    def Step(self, actions):
        self.SendRequest("step", *actions)
        return self.DeserializeResetVector(self.GetResponse())

    def GetTotalActions(self):
        self.SendRequest("get_total_actions")
        return self.DeserializeUnsigned(self.GetResponse())

    def GetNActions(self):
        self.SendRequest("get_n_actions")
        return self.DeserializeUnsigned(self.GetResponse())

    def GetDeploymentField(self):
        self.SendRequest("get_deployment_field")
        return self.DeserializeMatrix(self.GetResponse())

    def GetCoverageMatrix(self):
        self.SendRequest("get_coverage_matrix")
        return self.DeserializeMatrix(self.GetResponse())

    def GetDesiredMatrix(self):
        self.SendRequest("get_desired_matrix")
        return self.DeserializeMatrix(self.GetResponse())

    def Shutdown(self):
        self.SendRequest("shutdown")
        print(self.GetResponse())




    def DeserializeObs(self, resp):
        serial_parts = resp.split()
        num_mats = int(serial_parts.pop(0))
        rows = int(serial_parts.pop(0))
        cols = int(serial_parts.pop(0))
        data = np.array(serial_parts, dtype=np.int32)
        return data.reshape(num_mats, rows, cols)


    def DeserializeMatrix(self, resp):
        serial_parts = resp.split()
        rows = int(serial_parts.pop(0))
        cols = int(serial_parts.pop(0))
        data = np.array(serial_parts, dtype=np.int32)
        return data.reshape(rows, cols)

    def DeserializeState(self, resp):
        serial_parts = resp.split()
        cov_rows = int(serial_parts.pop(0))
        cov_cols = int(serial_parts.pop(0))
        cov_mat = np.array(serial_parts[:cov_cols*cov_rows-1], dtype=np.int32)
        cov_mat.reshape(cov_rows, cov_cols)
        serial_parts = serial_parts[:cov_cols*cov_rows-1]

        dep_rows = int(serial_parts.pop(0))
        dep_cols = int(serial_parts.pop(0))
        dep_field = np.array(serial_parts[:dep_cols*dep_rows-1], dtype=np.int32)
        dep_field.reshape(dep_rows, dep_cols)
        serial_parts = serial_parts[:dep_cols*dep_rows-1]

        des_rows = int(serial_parts.pop(0))
        des_cols = int(serial_parts.pop(0))
        des_mat = np.array(serial_parts, dtype=np.int32)
        des_mat.reshape(des_rows, des_cols)

        return cov_mat, dep_field, des_mat

    def DeserializeResetVector(self, resp):
        serial_parts = resp.split()

        num_obs = int(serial_parts.pop(0))
        num_obs_rows = int(serial_parts.pop(0))
        num_obs_cols = int(serial_parts.pop(0))
        obs = np.array(serial_parts[:num_obs*num_obs_rows*num_obs_cols], dtype=np.int32)
        obs.reshape(num_obs, num_obs_rows, num_obs_cols)

        serial_parts = serial_parts[num_obs*num_obs_rows*num_obs_cols:]

        cov_rows = int(serial_parts.pop(0))
        cov_cols = int(serial_parts.pop(0))
        cov_mat = np.array(serial_parts[:cov_cols*cov_rows-1], dtype=np.int32)
        cov_mat.reshape(cov_rows, cov_cols)
        serial_parts = serial_parts[cov_cols*cov_rows:]

        dep_rows = int(serial_parts.pop(0))
        dep_cols = int(serial_parts.pop(0))
        dep_field = np.array(serial_parts[:dep_cols*dep_rows-1], dtype=np.int32)
        dep_field.reshape(dep_rows, dep_cols)
        serial_parts = serial_parts[dep_cols*dep_rows:]

        des_rows = int(serial_parts.pop(0))
        des_cols = int(serial_parts.pop(0))
        des_mat = np.array(serial_parts, dtype=np.int32)
        des_mat.reshape(des_rows, des_cols)
        serial_parts = serial_parts[des_cols*des_rows:]

        num_vecs = int(serial_parts.pop(0))
        num_acts = int(serial_parts.pop(0))
        actions = np.array(serial_parts, dtype=np.int32)
        actions.reshape(num_vecs, num_acts)



        return obs, cov_mat, dep_field, des_mat, actions

    def DeserializeUnsigned(self, resp):
        return int(resp)

    def DeserializeVector(self, resp):
        serial_parts = resp.split()
        num_vecs = int(serial_parts.pop(0))
        num_elems = int(serial_parts.pop(0))
        vec = np.array(serial_parts, dtype=np.int32)

        return vec

    def DeserializeActionVector(self, resp):
        serial_parts = resp.split()
        num_vecs = int(serial_parts.pop(0))
        num_acts = int(serial_parts.pop(0))
        actions = np.array(serial_parts, dtype=np.int32)
        actions.reshape(num_vecs, num_acts)

        return actions
#include "Server.h"
#include "ScenarioSimulator.h"

Server::Server(int port) : m_Port(port), m_ServerUp(true)
{

}

void Server::StartServer(const std::string& fileName)
{

    m_Simulator = std::make_shared<SMAWS::ScenarioSimulator>(fileName);

    m_ServerSocket = socket(AF_INET, SOCK_STREAM, 0);
    m_ServerAddress.sin_family = AF_INET;
    m_ServerAddress.sin_port = htons(m_Port);
    m_ServerAddress.sin_addr.s_addr = INADDR_ANY;

    // Bind the address
    bind(m_ServerSocket, (sockaddr*)&m_ServerAddress, sizeof(m_ServerAddress));

    // Listen for connections
    listen(m_ServerSocket, 3);

    // Accept a new connection
    m_ServerAddrSize = sizeof(m_ServerStorage);
    m_ClientSocket = accept(m_ServerSocket, (sockaddr*)&m_ServerStorage, &m_ServerAddrSize);

    // Send a response back to the client
    std::string response = "Connection with Python Received!";
    send(m_ClientSocket, response.c_str(), response.length(), 0);

    RunServer();
}

void Server::RunServer()
{
    while(m_ServerUp)
    {
        char buffer[1024] = {0};
        recv(m_ClientSocket, buffer, 1024, 0);
        std::string response(buffer);
//        std::stringstream iss(response);
        std::stringstream iss(response);
        std::string msg;
        iss >> msg;
        int num_args = 0;
        iss >> num_args;
//        std::string response;
        if(msg == "get_obs")
        {
            response = SerializeVector(m_Simulator->GetObs());
        }
        if(msg == "get_obs_agent")
        {
            if(num_args != 1)
                perror("Invalid number of arguments");

            int a_id = 0;
            iss >> a_id;
            response = SerializeMatrix(m_Simulator->GetObsAgent(a_id));
        }
        if(msg == "get_obs_size")
        {
            response = SerializeVector(m_Simulator->GetObsSize());
        }
        if(msg == "get_state")
        {
            response = SerializeState(m_Simulator->GetState());
        }
        if(msg == "get_state_size")
        {
            response = SerializeVector(m_Simulator->GetStateSize());
        }
        if(msg == "get_avail_agent_actions")
        {
            if(num_args != 1)
                perror("Invalid number of arguments");
            int a_id;
            iss >> a_id;
            response = SerializeVector(m_Simulator->GetAvailableAgentActions(a_id));

        }
        if(msg == "get_avail_actions")
        {
            response = SerializeVector(m_Simulator->GetAvailableActions());
        }
        if(msg == "reset")
        {
            response = SerializeResetVector(m_Simulator->Reset());
        }
        if(msg == "step")
        {
            if(num_args != m_Simulator->Get_n_Agents())
                perror("Invalid number of arguments");

            std::vector<unsigned> arg_vector;
            for(int i = 0; i < num_args; i++)
            {
                int arg;
                iss >> arg;
                arg_vector.emplace_back(arg);
            }
            response = SerializeResetVector(m_Simulator->Step(arg_vector));
        }
        if(msg == "get_total_actions")
        {
            response = std::to_string(m_Simulator->GetTotalActions());
        }
        if(msg == "get_n_actions")
        {
            response = std::to_string(m_Simulator->Get_n_Actions());
        }
        if(msg == "get_deployment_field")
        {
            response = SerializeMatrix(m_Simulator->GetDeploymentField());
        }
        if(msg == "get_coverage_matrix")
        {
            response = SerializeMatrix(m_Simulator->GetCoverageMatrix());
        }
        if(msg == "get_desired_matrix")
        {
            response = SerializeMatrix(m_Simulator->GetDesiredMatrix());
        }
        if(msg == "shutdown")
        {
            response = "Client called Shutdown\nShutting down...";
            m_ServerUp = false;
            m_Simulator.reset();
        }

        response = std::to_string(response.size()+std::string(" ").size()+std::to_string(response.size()).size()) + " " + response;
        const char* response_data = response.data();
        int bytes_sent = 0;
        while (bytes_sent < response.size()) {
            int bytes_to_send = std::min<unsigned>(2048, response.size() - bytes_sent);
            int bytes_sent_now = send(m_ClientSocket, response_data + bytes_sent, bytes_to_send, 0);
            if (bytes_sent_now < 0) {
                perror("Send failed");
                return;
            }
            bytes_sent += bytes_sent_now;
        }

        send(m_ClientSocket, response.c_str(), response.size(), 0);
    }

    close(m_ClientSocket);
    close(m_ServerSocket);
}


std::string Server::SerializeMatrix(const Eigen::MatrixXi& matrix)
{
    std::ostringstream oss;
    oss << matrix.rows() << " " << matrix.cols() << " ";
    for (int i = 0; i < matrix.rows(); ++i) {
        for (int j = 0; j < matrix.cols(); ++j) {
            oss << matrix(i, j) << " ";
        }
    }
    return oss.str();
}

std::string Server::SerializeVector(const Eigen::Vector3i& vec)
{
    std::ostringstream oss;
    oss << 1 << " " << vec.size() << " ";
    for (int i = 0; i < vec.size(); ++i) {
        oss << vec(i) << " ";
    }
    return oss.str();
}

std::string Server::SerializeVector(const std::vector<unsigned>& vec)
{
    std::ostringstream oss;
    oss << 1 << " " << vec.size() << " ";
    for (int i = 0; i < vec.size(); ++i) {
        oss << vec[i] << " ";
    }
    return oss.str();
}

std::string Server::SerializeVector(const std::vector<Eigen::MatrixXi>& vec)
{
    std::ostringstream oss;
    oss << vec.size() << " " << vec[0].rows() << " " << vec[0].cols() << " ";
    for(const auto& mat : vec)
        oss << SerializeMatrix(mat) << " ";

    return oss.str();
}

std::string Server::SerializeVector(const std::vector<std::vector<unsigned>>& vec)
{
    std::ostringstream oss;
    oss << vec.size() << " " << vec[0].size() << " ";
    for(const auto& v : vec)
        oss << SerializeVector(v) << " ";

    return oss.str();
}

std::string Server::SerializeState(const State& state)
{
    std::ostringstream oss;
    oss << SerializeMatrix(state.CovMat) + " ";
    oss << SerializeMatrix(state.DepField) + " ";
    oss << SerializeMatrix(state.DesMat);

    return oss.str();
}

std::string Server::SerializeResetVector(const ResetVector& reset_vector)
{
    std::string obs_string;
    std::string state;
    std::string actions;

    obs_string = SerializeVector(reset_vector.obs);

    state = SerializeState(reset_vector.state);

    for(const auto& act : reset_vector.actions)
    {
        actions += SerializeVector(act) + " ";
    }

    return obs_string + " " + state + " " + actions;
}
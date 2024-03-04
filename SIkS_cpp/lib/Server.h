#include <string>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sstream>
#include <memory>
#include <algorithm>
#include "ScenarioSimulator.h"



//
//#include <iostream>
//#include <string>
//#include <vector>
//#include <memory>
//#include <boost/asio.hpp>

#ifndef IPC_TEST_SERVER_H
#define IPC_TEST_SERVER_H


class Server {

public:
    Server(int);

    void StartServer(const std::string&);
    void RunServer();
private:
    int m_Port;
    int m_ClientSocket;
    int m_ServerSocket;

    bool m_ServerUp;

    socklen_t m_ServerAddrSize;
    sockaddr_in m_ServerAddress;
    sockaddr_storage m_ServerStorage;

    std::shared_ptr<SMAWS::ScenarioSimulator> m_Simulator;

    std::string SerializeMatrix(const Eigen::MatrixXi&);
    std::string SerializeVector(const Eigen::Vector3i&);
    std::string SerializeVector(const std::vector<unsigned>&);
    std::string SerializeVector(const std::vector<Eigen::MatrixXi>&);
    std::string SerializeVector(const std::vector<std::vector<unsigned>>&);
    std::string SerializeState(const State&);
    std::string SerializeResetVector(const ResetVector&);
//    char m_Buffer[256];


    void HandleRequest();

};

//class Server
//{
//public:
//    Server(boost::asio::io_service &io_service, unsigned short port);
//private:
//
//
//    boost::asio::ip::tcp::acceptor acceptor_;
//    boost::asio::ip::tcp::socket socket_;
//};


#endif //IPC_TEST_SERVER_H

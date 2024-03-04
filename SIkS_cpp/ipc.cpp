////#include <boost/
////#include <iostream>
////#include <boost/asio.hpp>
//
//#include <iostream>
//#include <sys/types.h>
//#include <sys/socket.h>
//#include <netinet/in.h>
//#include <netdb.h>
//#include <unistd.h>
//#include <string>
//#include <arpa/inet.h>
//#include <stdio.h>
//#include <string.h>
//
////using namespace boost::asio;
//
////std::string read_msg(boost::asio::ip::tcp::socket& sock)
////{
////    boost::asio::streambuf buf;
////    boost::asio::read_until(sock, buf, '\n');
////    std::string data = boost::asio::buffer_cast<const char *>(buf.data());
////    return data;
////}
//
//int main(int argc, const char** argv)
//{
//
//    int portNum;
//    if(argc >=0)
//        portNum = atoi(argv[0]);
//
//
//
//    char buffer[1000];
//    int n;
//
//    int serverSock=socket(AF_INET, SOCK_STREAM, 0);
//
//    sockaddr_in serverAddr;
//    serverAddr.sin_family = AF_INET;
//    serverAddr.sin_port = portNum;
//    serverAddr.sin_addr.s_addr = INADDR_ANY;
//
//    /* bind (this socket, local address, address length)
//       bind server socket (serverSock) to server address (serverAddr).
//       Necessary so that server can use a specific port */
//    bind(serverSock, (struct sockaddr*)&serverAddr, sizeof(struct sockaddr));
//
//    // wait for a client
//    /* listen (this socket, request queue length) */
//    listen(serverSock,1);
//
//    while (1 == 1) {
//        bzero(buffer, 1000);
//
//        sockaddr_in clientAddr;
//        socklen_t sin_size=sizeof(struct sockaddr_in);
//    int clientSock=accept(serverSock,(struct sockaddr*)&clientAddr, &sin_size);
//
//        //receive a message from a client
//        n = read(clientSock, buffer, 500);
//        std::cout << "Confirmation code  " << n << std::endl;
//        std::cout << "Server received:  " << buffer << std::endl;
//
//        strcpy(buffer, "test");
//        n = write(clientSock, buffer, strlen(buffer));
//        std::cout << "Confirmation code  " << n << std::endl;
//    }
//
//
//
//    return 0;
////    boost::asio::io_service ioService;
////
////    boost::asio::ip::tcp::acceptor acceptor(ioService,
////                                            boost::asio::ip::tcp::endpoint(
////                                                    boost::asio::ip::tcp::v4(), portNum));
////
////    boost::asio::ip::tcp::socket socket1(ioService);
////
////    acceptor.accept(socket1);
//
//
//
//
////    std::string message = read_msg(socket1);
////    std::cout << message << std::endl;
//
//
//    return 0;
//}
//
//
//



// C++ Server
//#include <iostream>
//#include <string>
//#include <cstring>
//#include <sys/socket.h>
//#include <netinet/in.h>
//#include <arpa/inet.h>
//#include <unistd.h>
#include "lib/Server.h"

int main(int argc, char** argv) {
    int portNum;
    std::string file_path;
    if(argc >=1)
        portNum = atoi(argv[1]);
    if(argc >= 2)
        file_path = argv[2];



//    std::cout << portNum << std::endl;

//    int serverSocket, newSocket;
//    struct sockaddr_in serverAddr;
//    struct sockaddr_storage serverStorage;
//    socklen_t addr_size;
//
//    // Create the socket
//    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
//    serverAddr.sin_family = AF_INET;
//    serverAddr.sin_port = htons(portNum);
//    serverAddr.sin_addr.s_addr = INADDR_ANY;
//
//    // Bind the address
//    bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
//
//    // Listen for connections
//    listen(serverSocket, 10);
//
//    while (true) {
//        // Accept a new connection
//        addr_size = sizeof(serverStorage);
//        newSocket = accept(serverSocket, (struct sockaddr*)&serverStorage, &addr_size);
//
//        // Receive data from the client
//        char buffer[1024] = {0};
//        recv(newSocket, buffer, 1024, 0);
//        std::string msg = buffer;
//
//        // Print the received message
//        std::cout << "Received message from client: " << msg << std::endl;
//
//        // Send a response back to the client
//        std::string response = "even bigger balls";
//        send(newSocket, response.c_str(), response.length(), 0);
//
//        // Close the socket
//        close(newSocket);
//    }

    Server server(portNum);
    server.StartServer(file_path);

    return 0;
}

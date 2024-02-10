from socket import *

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# Assign a port number
serverPort = 18830
# Bind the socket to server address and server port
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

try: 
    while True:
        # Establish the connection
        print("The server is ready to receive")
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open("./html_files/" + filename[1:])
            outputdata = f.read()
            # Send HTTP OK and the Set-Cookie header into the socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Set-Cookie: session=18831\r\n\r\n".encode())
            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            #connectionSocket.send("\r\n".encode())
            # Close the client connection socket
            connectionSocket.close()
        except IOError:
            # Send HTTP NotFound response
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())

            # Close client socket
            connectionSocket.close()
except KeyboardInterrupt:
    print("closing server...")
    serverSocket.close()

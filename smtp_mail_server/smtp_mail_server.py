from socket import *
import base64

# choose a mail server (NYU mail server) and call it mailserver
# dig command used: 'dig nyu.edu MX +short' (MX for mail exchange, +short to retreive only MX info)   
mailserver = 'mxb-00256a01.gslb.pphosted.com'
serverPort = 25

# create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))

tcp_resp = clientSocket.recv(1024).decode()
print("tcp resp:",tcp_resp)

# Send HELO command to begin SMTP handshake
helloCommand = 'HELO Alice\r\n'
clientSocket.send(helloCommand.encode())
helo_resp = clientSocket.recv(1024).decode()
print("helo resp:",helo_resp)

# Send MAIL FROM command and print server response
mailFromCommand = 'MAIL FROM: <sg7569@nyu.edu> \r\n'
clientSocket.send(mailFromCommand.encode())
mail_from_resp = clientSocket.recv(1024).decode()
print("mail from:",mail_from_resp)

# Send RCPT TO command and print server response
rcptToCommand = 'RCPT TO: <sg7569@nyu.edu> \r\n'
clientSocket.send(rcptToCommand.encode())
rcpt_to_resp = clientSocket.recv(1024).decode()

# Send DATA command and print server response
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
data_resp = clientSocket.recv(1024).decode()
print("data: ",data_resp)

# Send email data
subject = 'Subject: SMTP Mail Client Test\r\n'
clientSocket.send(subject.encode())
clientSocket.send('\r\n'.encode())
clientSocket.send('I love computer networks!\r\n'.encode())

# Message ends with a single period
endMessage = '.\r\n'
clientSocket.send(endMessage.encode())
end_resp = clientSocket.recv(1024).decode()
print("end: ", end_resp)

# Send QUIT command and get server response
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
quit_resp = clientSocket.recv(1024).decode()
print("quit msg: ",quit_resp)

# Close connection
clientSocket.close()




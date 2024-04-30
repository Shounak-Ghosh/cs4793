import socket

listen_ip = "216.165.95.183"  # Listen on all available interfaces
listen_port = 12345    # Choose the port to listen on

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((listen_ip, listen_port))

print(f"Listening for UDP traffic on {listen_ip}:{listen_port}")

while True:
    data, addr = udp_socket.recvfrom(1024)  # Adjust the buffer size as needed
    print(f"Received data from {addr}: {data.decode('utf-8')}")
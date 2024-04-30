import socket
import time

target_ip = "142.251.40.206"  # Replace with the receiver's IP address
target_port = 12346      # Replace with the receiver's port

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = "Your UDP message"
    udp_socket.sendto(message.encode(), (target_ip, target_port))
    time.sleep(1)  # Adjust the delay as needed
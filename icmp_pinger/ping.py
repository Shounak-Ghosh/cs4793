from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii

# run using "sudo python3 ping.py" (MacOS)

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

# Dont worry about this method
def checksum(string):
    csum = 0
    countTo = (len(string) / 2) * 2

    count = 0
    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum = int(csum) + int(thisVal)
        csum = csum & 0xFFFFFFFF
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xFFFFFFFF

    csum = (csum >> 16) + (csum & 0xFFFF)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xFFFF
    answer = answer >> 8 | (answer << 8 & 0xFF00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    time_left = timeout
    while 1:
        time_start = time.time()
        # Wait for the socket to receive a reply
        buffer = select.select([mySocket], [], [], time_left)

        # If we do not get a response within the timeout
        if not buffer[0]:
            return "Request timed out."
        time_received = time.time()

        # Receive the packet and address from the socket
        recPacket, addr = mySocket.recvfrom(1024)

        # Extract the ICMP header from the IP packet
        icmpHeader = recPacket[20:28]

        # Use struct.unpack to get the data that was sent via thestruct.pack method below
        imcpType, imcpCode, imcpChecksum, imcpPacketID, imcpSequence = struct.unpack(
            "bbHHh", icmpHeader
        )

        # Verify Type/Code is an ICMP echo reply
        if imcpPacketID == ID:
            bytesInDouble = struct.calcsize("d")
            # Extract the time in which the packet was sent
            time_sent = struct.unpack("d", recPacket[28 : 28 + bytesInDouble])[0]
            # Return the delay in ms: 1000 * (time received - time sent)
            return 1000 * (time_received - time_sent)

        # If we got a response but it was not an ICMP echo reply
        time_left = time_received - time_start
        if time_left <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence(16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data

    # Define icmpEchoRequestType and icmpEchoRequestCode, which are both used below
    icmpEchoRequestType = 8  # ICMP type code for echo request
    icmpEchoRequestCode = 0  # ICMP code for echo request

    header = struct.pack(
        "bbHHh", icmpEchoRequestType, icmpEchoRequestCode, myChecksum, ID, 1
    )

    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == "darwin":
        myChecksum = socket.htons(myChecksum) & 0xFFFF
    # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack(
        "bbHHh", icmpEchoRequestType, icmpEchoRequestCode, myChecksum, ID, 1
    )
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.ord/papers/sock_raw
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    numPackets = 0
    minRTT = doOnePing(dest,timeout) # minimum round trip time
    maxRTT = 0 # maximum round trip time
    totalRTT = 0
    print("Pinging " + dest + " using Python:\n")
    # Send ping requests to a server separated by approximately one second
    try:
        while 1:
            delay = doOnePing(dest, timeout)
            numPackets += 1
            minRTT = min(minRTT, delay)
            maxRTT = max(maxRTT, delay)
            totalRTT += delay
            print(delay)
            time.sleep(1)  # one second
        return delay
    except KeyboardInterrupt:
        print("\nExiting...")
        print("Packets sent:", numPackets, "Min RTT:", minRTT, "Max RTT:", maxRTT, "Avg RTT:", totalRTT/numPackets)
        sys.exit(0)


# ping("127.0.0.1")  # localhost
# ping("google.com") # 142.251.40.110
# ping("bing.com") #13.107.21.200
ping("gov.uk") #151.101.192.144
#!/usr/bin/env python
from socket import socket                  # The Socket library
from socket import AF_INET, SOCK_STREAM    # Specific constants from socket
from sys    import exit                    # Import the exit function 
AGENT_IP    = "192.168.1.129"              # The Agent IP Address
AGENT_PORT  = 1100                         # The Agent Port number 
BUFFER      = 14336 # 14k                  # The size of the TCP Buffer
tcpSocket = socket(AF_INET, SOCK_STREAM)   # Create an object of type socket
tcpSocket.connect((AGENT_IP,AGENT_PORT))   # Establish a connection
tcpSocket.send("TA:version")               # Send the TA:version command 
response = tcpSocket.recv(BUFFER)          # Get the response from the agent
print response                             # Print the response
tcpSocket.send("OS:/home/test/automation/bin/testmaster.py")   # Send the TA:version command 
response = tcpSocket.recv(BUFFER)          # Get the response from the agent
print response
tcpSocket.send("TA:bye")                   # End the session with the agent 
response = tcpSocket.recv(BUFFER)          # Get the closing notice 
print response                             # Print the closing response 
exit(0)          

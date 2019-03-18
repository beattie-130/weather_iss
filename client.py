#!/usr/bin/env python3
import socket

PORT = 43768        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = input("Enter host to connect to\n>>> ")

s.connect((host, PORT))
print("Connected to server on port", PORT)
response_data = s.recv(1024).decode()

while True:
    print(response_data)
    user_command = input(">>>")

    # Send initial command to server
    s.send(user_command.encode())
    if(user_command == 'EXIT' or user_command == 'exit'):
        print("Closing connection to server...")
        break

    # Receive instructions from server for command entered if command was "WEAT"
    if(user_command[0:4] == 'WEAT'):
        instr = s.recv(1024).decode()
        print(instr)
        user_input = input(">>>")
        s.send(user_input.encode())

    # Receive result from server
    response_data = s.recv(2048).decode()

s.close()
print("Connection to server closed.\nGoodbye!")

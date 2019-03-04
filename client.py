#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = socket.socket()

s.connect((HOST, PORT))
print("Connected to ser on port", PORT)
response_data = s.recv(1024).decode()


while True:
    print(response_data)
    user_command = input(">>>")

    # Send initial command to server
    s.send(user_command.encode())
    if(user_command == 'EXIT'):
        print("Closing connection to server...")
        break

    # Receive instructions from server for command entered
    instr = s.recv(1024).decode()
    print(instr)
    user_input = input(">>>")
    s.send(user_input.encode())

    # Receive result from server
    response_data = s.recv(1024).decode()


s.close()
print("Connection to server closed.\nGoodbye!")

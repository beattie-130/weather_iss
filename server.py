#!/usr/bin/env python3.7
import socket
import string
from weather_iss import get_weather
from weather_iss import get_ISS

HOST = socket.gethostbyname(socket.gethostname())
PORT = 43768
PROMPT = "[WEAT] [SUMM] = current weather information\n[WEAT] [3DAY] = 3 day forecast\n[ISS] = ISS Location (lat,lng)\n[EXIT] = close connection\n[HELP] = list of commands"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created successfully")

s.bind((HOST, PORT))

# Allow the socket to backlog up to 5 connections
s.listen(5)
print("Socket listening on " + HOST + " port " + str(PORT))

# Accepts connection from client
conn, addr = s.accept()
print("Connection established from ", addr)
conn.send(('Welcome to the weather server!\n' + PROMPT).encode())

# Loop until the server is closed
while True:

    # Receive command from client
    data = conn.recv(1024).decode()
    data = data.upper()

    print("Recieved from client:\n", data)

    # Prepare message to be sent back to client
    result_msg = ""

    # If the client sent "EXIT", close the server
    if (data == 'EXIT'):
        result_msg = "Closing connection to client..."
        break
    # If the first 4 characters in the clients command were "WEAT", get weather data
    elif data[0:4] == 'WEAT':

        # Get location information from client to get weather data
        instr_msg = "\nEnter an address, city & state, or ZIP Code for weather data"
        conn.send(instr_msg.encode())
        location = conn.recv(1024).decode()
        print("Recieved from client:\n", location)
        try:
            print("get weather called")
            result_msg = get_weather(data[5:9], location)
        except:
            result_msg = "ERROR while generating weather data\n"
    # If the client sent "ISS", get ISS location data
    elif data == 'ISS':
        try:
            result_msg = get_ISS()['msg']
            print("get ISS called")
        except:
            result_msg = "ERROR while generating ISS data\n"
    # If client sent "HELP", send the prompt wtih the list of commands
    elif data == 'HELP':
        result_msg = PROMPT
    # If client sends anything else then send "INVALID COMMAND"
    else:
        result_msg = "INVALID COMMAND"

    # Send message back to client
    conn.send(result_msg.encode())

# Closes connection and socket to client
conn.close()
s.close()
print("Connection to client closed")
print("Socket closed.\nGoodbye!")

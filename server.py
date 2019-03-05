#!/usr/bin/env python3.7
import socket
import string
from weather_iss import get_weather
from weather_iss import get_ISS

HOST = socket.gethostbyname(socket.gethostname())
PORT = 43768
PROMPT = "[WEAT = weather] [ISS = ISS] [EXIT = close connection] [HELP = list of commands]"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created successfully")

s.bind((HOST, PORT))

# Allow the socket to backlog up to 5 connections
s.listen(5)
print("Socket listening on " + HOST + " port " + str(PORT))

conn, addr = s.accept()
print("Connection established from ", addr)
conn.send(('Welcome to the weather server!\n' + PROMPT).encode())

while True:

    data = conn.recv(1024).decode()
    data = data.upper()
    result_msg = ""
    print("Recieved from client:\n", data)
    if (data == 'EXIT'):
        result_msg = "Closing connection to client..."
        break
    elif data == 'WEAT':
        instr_msg = "\nEnter an address, city & state, or ZIP Code for weather data"
        conn.send(instr_msg.encode())
        location = conn.recv(1024).decode()
        try:
            print("get weather called")
            result_msg = get_weather(location)
        except:
            result_msg = "ERROR while generating weather data\n"
    elif data == 'ISS':
        try:
            result_msg = get_ISS()['msg']
            print("get ISS called")
        except:
            result_msg = "ERROR while generating ISS data\n"
    elif data == 'HELP':
        result_msg = PROMPT
    else:
        result_msg = "INVALID COMMAND"

    conn.send(result_msg.encode())


conn.close()
s.close()
print("Connection to client closed")
print("Socket closed.\nGoodbye!")

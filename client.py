## Base for code taken from Tech With Tim

import socket
import pickle
import re
import threading
import os

HEADERLENGTH = 8
PORT = 5000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/disconnect"

def ask_name():
    user = input("Username: ")
    return user

def ask_ip():
    reg = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    ip = input("Server IP:")
    ip = re.search(reg, ip)
    if (ip):
        ip = ip.string()
    else:
        ip = socket.gethostbyname(socket.gethostname())

    reg = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    port = input("Server port:")
    port = re.search(reg, port)
    
    if (port):
        port.string()
    else:
        port = PORT

    return (ip, port)

def connect():
    address = ask_ip()
    print("Connecting to server...")
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        os.system('cls' if os.name == 'nt' else 'clear')
        return client
    except:
        print("CONNECTION ERROR")

def disconnect(client, user):
    '''     msg_length = client.recv(HEADERLENGTH).decode(FORMAT)
    if (msg_length):
        msg_length = int(msg_length)

    data = client.recv(msg_length)
    p = pickle.loads(data)

    print(p["msg"]) '''

    client.close()

def send(client, user, message):
    p = {"username": user, "msg": message }
    p = pickle.dumps(p)

    msg_length = len(p)
    msg = bytes(f'{msg_length:<{HEADERLENGTH}}', FORMAT) + p

    client.send(msg)

    if (message == DISCONNECT_MESSAGE):
        disconnect(client, user)

    ## print(client.recv(2048).decode(FORMAT)) ##Debug print

def receive(socket):
    try:
        msg_length = socket.recv(HEADERLENGTH).decode(FORMAT)
        if (msg_length):
            msg_length = int(msg_length)

            data = socket.recv(msg_length)
            p = pickle.loads(data)

            username = p["username"]
            msg = p["msg"]
    except socket.error:
        pass

def chat_handler(socket):
    while True:
        receive(socket)

def start():
    user = ask_name()
    socket = connect()

    thread = threading.Thread(target=chat_handler, args=(socket,))
    thread.start()

    while socket:
        msg = input(f"{user}: ")
        send(socket, user, msg)
    

start()
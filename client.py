## Base for code taken from Tech With Tim

import socket
import pickle
import re
import threading
import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from venv import create

HEADERLENGTH = 8
PORT = 5000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/disconnect"

## UI
WIDTH = 160
HEIGHT = 80

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_name():
    user = input("Username: ")
    # TODO: Add sanitisation
    clear_terminal()
    return user

def ask_ip():
    reg = "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    ip = input("Server IP:")
    ip = re.search(reg, ip)
    if (ip):
        ip = ip.string()
    else:
        ip = socket.gethostbyname(socket.gethostname())

    port = input("Server port:")
    port = re.search(reg, port)
    
    if (port):
        port.string()
    else:
        port = PORT

    return (ip, port)

def connect():
    address = ask_ip()
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        os.system('cls' if os.name == 'nt' else 'clear')
        return client
    except BaseException:
        print("CONNECTION ERROR")

def disconnect(client, user):
    # TODO: Add logging
    client.close()
    sys.exit(0)

def send(client, user, message):
    p = {"username": user, "msg": message }
    p = pickle.dumps(p)

    msg_length = len(p)
    msg = bytes(f'{msg_length:<{HEADERLENGTH}}', FORMAT) + p

    client.send(msg)

    if (message == DISCONNECT_MESSAGE):
        disconnect(client, user)

def receive(socket):
    try:
        msg_length = socket.recv(HEADERLENGTH).decode(FORMAT)
        if (msg_length):
            msg_length = int(msg_length)

            data = socket.recv(msg_length)
            p = pickle.loads(data)

            username = p["username"]
            msg = p["msg"]

            print(f"{username}: {msg}")
    except Exception:
        pass

def chat_handler(socket):
    while True:
        receive(socket)

''' def create_ui(socket, user):
    root = tk.Tk()
    #canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)

    label = tk.Label(root, text="Chat:")
    label.pack(padx=5, pady=5)

    chat = tk.scrolledtext.ScrolledText(root)
    chat.pack(padx=5, pady=5)
    chat.configure(state="disabled")

    entry_box = tk.Entry(root, width=WIDTH)
    entry_box.pack()

    send_btn = tk.Button(root, text="Send", command=send(socket, user, entry_box.get()))
    send_btn.pack()

    ##root.protocol("WM_DELETE_WINDOW", disconnect(socket, user))

    root.mainloop() '''

def start():
    socket = connect()
    user = ask_name()
    send(socket, user, "")

    thread = threading.Thread(target=chat_handler, args=(socket,))
    thread.start()

    while socket:
        msg = input(f"{user}: ")
        send(socket, user, msg)
        
    #create_ui(socket, user)
    

start()
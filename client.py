# Base for code taken from NeuralNine
import pickle
import socket
import sys
import threading
import tkinter as tk
from tkinter import simpledialog
import tkinter.scrolledtext
from typing import Protocol

HEADERLENGTH = 8
PORT = 5000
IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

## UI
WIDTH = 160
HEIGHT = 80

class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        msg = tkinter.Tk()
        msg.withdraw()

        self.server_ip = simpledialog.askstring("IP", "Enter the server IP", parent=msg) or IP
        try:
            self.server_port = int(simpledialog.askstring("port", "Enter the server port", parent=msg))
        except ValueError:
            self.server_port = PORT

        self.username = simpledialog.askstring("username", "Username:", parent=msg)

        try:
            self.sock.connect((self.server_ip, self.server_port))
            self.sock.send(self.serialise("start"))
        except BaseException as err:
            print(err)

        self.running = True
        self.gui_done = False

        gui_thread = threading.Thread(target=self.gui_handler)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        self.receive()

    def disconnect(self):
        # TODO: Add logging
        self.running = False
        self.sock.close()
        self.root.destroy()
        sys.exit(0)

    def serialise(self, msg):
        p = {"username": self.username, "msg": msg }
        p = pickle.dumps(p)
        print(msg)

        msg_length = len(p)
        return bytes(f'{msg_length:<{HEADERLENGTH}}', FORMAT) + p

    def send(self):
        msg = self.serialise(self.entry_box.get())
        
        print(self.sock)
        self.sock.send(msg)
        self.entry_box.delete(0, 'end')

    '''         if (message == DISCONNECT_MESSAGE):
            disconnect(client, user) '''

    def receive(self):
        while self.running:
            try:
                msg_length = self.sock.recv(HEADERLENGTH).decode(FORMAT)
                if (msg_length):
                    msg_length = int(msg_length)

                    data = self.sock.recv(msg_length)
                    p = pickle.loads(data)

                    print(p)
                    username = p["username"]
                    msg = p["msg"]

                    if (self.gui_done):
                        self.chat.config(state="normal")
                        self.chat.insert("end", f"{username}: {msg}\n")
                        self.chat.yview("end")
                        self.chat.config(state="disabled")

                    print(f"\n{username}: {msg}")
            except ConnectionAbortedError:
                break
            except Exception as err:
                print(err)
                self.sock.close()

    def gui_handler(self):
        self.root = tkinter.Tk()

        self.label = tk.Label(self.root, text="Chat:")
        self.label.pack(padx=5, pady=5)

        self.chat = tk.scrolledtext.ScrolledText(self.root)
        self.chat.pack(padx=5, pady=5)
        self.chat.configure(state="disabled")

        self.entry_box = tk.Entry(self.root, width=WIDTH)
        self.entry_box.pack()

        self.send_btn = tk.Button(self.root, text="Send", command=self.send)
        self.send_btn.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.disconnect)

        self.gui_done = True
        self.root.mainloop()

Client()
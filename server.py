## Base for code taken from Tech With Tim

import socket
import threading

HEADERLENGTH = 8
PORT = 5000
IP = socket.gethostbyname(socket.gethostname())
ADDRESS = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "/disconnect"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##IPV4 TCP

s.bind(ADDRESS)

def client_thread(conn, addr):
    print(f"[CONNECTION] Client {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADERLENGTH).decode(FORMAT)
        if (msg_length):
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()

def start():
    s.listen()
    print(f"[STARTING] Server listening on {IP}:{PORT}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=client_thread, args=(conn, addr))
        thread.start()
        print(f"[STATUS] Client connections: {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
## Base for code taken from Tech With Tim

from http import client
import socket
import threading
import pickle

HEADERLENGTH = 8
PORT = 5000
IP = socket.gethostbyname(socket.gethostname())
ADDRESS = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "/disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##IPV4 TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDRESS)

SOCKET_LIST = [server]
CLIENTS = []

def send(client, user, message):
    p = {"username": user, "msg": message }
    p = pickle.dumps(p)
    print(pickle.dumps(p))

    msg_length = len(p)
    print(msg_length)
    msg = bytes(f'{msg_length:<{HEADERLENGTH}}', FORMAT) + p

    client.send(msg)

def receive(client_socket):
    try:
        msg_length = client_socket.recv(HEADERLENGTH).decode(FORMAT)
        if (msg_length):
            msg_length = int(msg_length)

            data = client_socket.recv(msg_length)
            p = pickle.loads(data)

            if p["msg"] == DISCONNECT_MESSAGE:
                return None
            else:
                return p
                ##client_socket.send("Msg received".encode(FORMAT))
    except socket.error:
        #getpeername()
        print(f"[CONNECTION] {client_socket.getpeername()[0]} disconnected unexpectedly")
        return None

def client_thread(client_socket, addr):
    print(f"[CONNECTION] Client {addr[0]} connected")
    print(f"[STATUS] Client connections: {threading.active_count() - 1}")

    send(client_socket, "SERVER", "Welcome to the server!")
    connected = True
    while connected:
        p = receive(client_socket)
        if (not p):
            connected = False
        else:
            print("{}: {}".format(p["username"], p["msg"]))
    print(f"[CONNECTION] {client_socket.getpeername()[0]} disconnected")
    client_socket.close()

def start():
    server.listen()
    print(f"[STARTING] Server listening on {IP}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        SOCKET_LIST.append(client_socket)
        CLIENTS.append(client_socket)

        thread = threading.Thread(target=client_thread, args=(client_socket, addr))
        thread.start()

print("[STARTING] Server is starting...")
start()
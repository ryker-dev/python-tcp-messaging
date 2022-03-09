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
SERVER_NAME = "CHAT SERVER 1"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##IPV4 TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDRESS)

SOCKET_LIST = [server]
CLIENTS = {}

def send(client, user, message):
    p = {"username": user, "msg": message }
    p = pickle.dumps(p)

    msg_length = len(p)
    msg = bytes(f'{msg_length:<{HEADERLENGTH}}', FORMAT) + p

    client.send(msg)

def propagate(clients, user, msg):
    try:
        for client in clients:
            send(client, user, msg)
    except Exception:
        return

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

def get_name(client_socket):
    data = receive(client_socket)
    try:
        user = data["username"]

        if (user in CLIENTS.keys()):
            send(client_socket, SERVER_NAME, "Username is already taken")
            return None
        ip = client_socket.getpeername()[0]
        CLIENTS[ip] = user
        print(f"[CONNECTION] {ip} connected as '{user}'")
        return user
    except KeyError:
        send(client_socket, SERVER_NAME, "ERROR 400: Missing username")
    except Exception:
        send(client_socket, SERVER_NAME, "GENERIC ERROR")

def client_thread(client_socket, addr):
    print(f"[CONNECTION] Client {addr[0]} connected")
    print(f"[STATUS] Client connections: {threading.active_count() - 1}") #Fix bad counter

    user = get_name(client_socket)

    ## MODT 
    send(client_socket, SERVER_NAME, f"Welcome to {SERVER_NAME}")
    ##

    connected = True
    while connected:
        p = receive(client_socket)
        if (not p):
            connected = False
        else:
            l = SOCKET_LIST.copy()
            l.remove(client_socket)
            l.remove(server)
            print(l)
            propagate(l, p["username"], p["msg"])
            print("{}: {}".format(p["username"], p["msg"]))

    print(f"[CONNECTION] {client_socket.getpeername()[0]} disconnected")
    client_socket.close()

def start():
    server.listen()
    print(f"[STARTING] Server listening on {IP}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        SOCKET_LIST.append(client_socket)
        print(SOCKET_LIST)

        thread = threading.Thread(target=client_thread, args=(client_socket, addr))
        thread.start()

print("[STARTING] Server is starting...")
start()
import socket
import os
from os import listdir
from os.path import isfile, join
import threading
from time import sleep

# create tcp socket with ignore delay for fill buffers
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setblocking(True)
tcp.setsockopt(socket.SOL_TCP, socket.TCP_QUICKACK, 1)
tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# useful variable
port = 55000
buffer = 1024
tcp.bind(('', port))
tcp.listen(15)
inputs = {}
names = {}
print("ready to serve...")
# global answer
# answer = 0

# accept new connections
def accept():
    while True:
        client, address = tcp.accept()
        inputs[client] = address
        name = welcome(client)
        # check if there is already that name
        if name in names.values():
            msg = "importent! this is a message from the server - your name is already taken, please try to connect again with a different name, the taken names is all the online mamber below:"
            msg = msg.encode()
            client.send(msg)
            # send taken names
            onlineList(client)
            # kick him
            gentlyKick(client, 1, name)

            continue
        print("new user detected! " + name + " connected")
        names[address] = name
        broadcast(name.encode() + f" entered the chat".encode(), [tcp, client])
        start = threading.Thread(target=recive, args=(client, name))
        start.start()

def recive(client, name):
    while True:
        message = "null"
        try:
            # get adress details
            id = client.getpeername()
            nickname = names[id]
            try:
                # try because maybe his dissconected...
                data = client.recv(buffer)
                data = data.decode('UTF-8')
                try:
                    # check if that a 2 part message
                    command, message = data.split(',', 1)
                    data = str(nickname + " >>> " + message)
                except:
                    command = data
                # recat by command
                if command == 'broadcast':
                    broadcast(data.encode(), [tcp, client])
                elif command == "online":
                    onlineList(client)
                elif command == "files":
                    filesList(client)
                # elif command == "555":
                #      answer = 2
                # elif command == "666":
                #      answer = 1
                elif command == "download" and message != "null":
                    down = threading.Thread(target=download, args=(client, message, id, name))
                    down.start()
                elif command == "exit":
                    kick(id, name, client)
                else:
                    port = getClient(command)
                    if port == "exep" or data.find(">>>") == -1:
                        msg = "there is no such user name / command ! try again, pay intention to spaces or correct name!"
                        msg = msg.encode()
                        client.send(msg)
                    else:
                        chatWith(port, data)
            except:
                try:
                    gentlyKick(id, 0, name)
                except:
                    pass
        except:
            pass

# broadcast to all new connection and welcome the new client
def welcome(client):
    name = client.recv(buffer)
    name = name.decode('UTF-8')
    if len(names) < 1:
        greetMsg = name + ", you are the first client so...how you doing?"
        client.send(greetMsg.encode())
    else:
        onlineList(client)
    return name

# send the list of clients to requested client
def onlineList(client):
    msg = "list of who is online:\n"
    msg = msg.encode()
    client.send(msg)
    data = names.items()
    for nickname in data:
        nickname = (nickname[1] + "\n").encode()
        client.send(nickname)

# check if there is client with that name
def getClient(name):
    for key, value in names.items():
        if name == value:
            return key
    return "exep"

#broadcast to all
def broadcast(msg, notClients):
    for connection in inputs:
        if connection not in notClients:
            try:
                connection.send(msg)
            except:
                pass

# to chat in private
def chatWith (port, msg):
    print(port)
    for connection in inputs:
        if msg.find(">>>") == -1:
            break
        try:
            connection.getpeername()
        except:
            continue
        if connection.getpeername() == port:
            msg = msg.encode()
            connection.send(msg)
            break

# send the file list in the folder
def filesList(client):
    path = os.path.abspath("")
    files = [file for file in listdir(path) if isfile(join(path, file))]
    msg = "list of available files:"
    msg = msg.encode()
    client.send(msg)
    for file in files:
        file = (file + "\n").encode()
        client.send(file)

# split the file to packages
def splitToPacket(file):
    packets = []
    with open(file, "rb") as f:
        package = f.read(buffer - 256)
        while (package):
            packets.append(package)
            package = f.read(buffer - 256)
        return packets

# udp connection
def udp(file, id):
    packets = splitToPacket(file)
    UDPSEND = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPRECV = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPRECV.settimeout(3)
    UDPSEND.settimeout(3)
    UDPSEND.bind(('', 56000))
    UDPRECV.bind(('', 57000))
    address = ('127.0.0.1', id[1] + 1000)
    ack = 0
    print("udp start")
    # half = int(len(packets))
    flag = 0
    #seperate recive and send UDP socket
    # while didnt send all packages
    while ack < len(packets):
            msg = (packets[ack].decode() + "," + str(ack)).encode()
            UDPSEND.sendto(msg, address)
            data = UDPRECV.recvfrom(buffer)
            temp = int(data[0].decode())
            if temp != -2:
                ack += 1
                # tried to stop, didnt hespaknu all so in comment
            # if half < ack:
            #     tcp.send("continue?")
            #     cont.start()
            #     cont.join()
            #     if answer == 1:
            #         break
        # if all acks are fine
    msg = ("-1" + "," + str(-1)).encode()
    # close the sending seqtion
    while True:
        UDPSEND.sendto(msg, address)
        data = UDPRECV.recvfrom(buffer)
        if data[0].decode() == -1:
            break

#all previus data before send the file on UDP
def download(client, file, id, name):
    path = os.path.abspath("")
    files = [file for file in listdir(path) if isfile(join(path, file))]
    if file not in files:
        msg = "no such a file in the server!"
        msg = msg.encode()
        client.send(msg)
        print("no such a file!")
    else:
        print(f"sending {file} to {name}")
        msg = "-sending-"
        msg = msg.encode()
        client.send(msg)
        sleep(0.1)
        size = os.path.getsize(file)
        size = str(size)
        msg = "serverFile-" + file + "," + size
        msg = msg.encode()
        client.send(msg)
        udp(file, id)

# def cont():
#     while answer == 0:
#         if answer == 2:
#             answer = 0
#             break
#         elif answer == 1:
#             pass


#kick method
def kick(id, name, client):
    msg = "-exit-"
    msg = msg.encode()
    try:
        for key, value in names.items():
            if value == name:
                id = key
                del names[key]
                break
        client.send(msg)
        del names[id]
        print(f"client {name} has left the chat, port {id[1]} free now ")
    except:
        print(f"client {name} has left the chat, port {id[1]} free now ")
    del inputs[client]
    broadcast(f"{name} has left the chat".encode(), [tcp])
    client.close()

def gentlyKick(client, flag, name):
    id = client.getpeername()
    try:
        del names[id]
        if flag == 0:
            broadcast(f"{name} has left the chat".encode(), [tcp])
            print(f"client {name} has left the chat, port {id} free now ")
    except:
        pass
    if flag != 0:
        print(f"client {name} has kicked from the chat (same name) , port {id[1]} is free now ")
    del inputs[client]
    print(1)
    msg = "-exit-"
    msg = msg.encode()
    client.send(msg)
    print(2)


start = threading.Thread(target=accept())
# cont = threading.Thread(target=cont())
start.start()
start.join()
tcp.close()



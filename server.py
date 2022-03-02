import socket
import select
import os
from os import listdir
from os.path import isfile, join

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setblocking(1)
tcp.setsockopt(socket.SOL_TCP, socket.TCP_QUICKACK, 1)
tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

port = 55000
buffer = 1024
tcp.bind(('', port))
tcp.listen(15)
inputs = [tcp]
names = {}
print("ready to serve...")

def welcome(client):
    name = client.recv(buffer)
    name = name.decode('UTF-8')
    users = [n.getpeername() for n in inputs if n is not client and n is not tcp]
    if len(users) < 1:
        greetMsg = name + ", you are the first client so...how you doing?"
        client.send(greetMsg.encode())
    else:
        onlineList(client)
    return name

def onlineList(i):
    msg = "list of who is online:\n"
    msg = msg.encode()
    i.send(msg)
    data = names.items()
    for name in data:
        name = (name[1] + "\n").encode()
        i.send(name)

def getClient(name):
    for key, value in names.items():
        if name == value:
            return key
    return "exep"

def broadcast(msg, non_receptors):
    for connection in inputs:
        if connection not in non_receptors:
            connection.send(msg)

def chatWith (port, msg):
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

def filesList(i):
    path = os.path.abspath("")
    files = [file for file in listdir(path) if isfile(join(path, file))]
    msg = "list of available files:"
    msg = msg.encode()
    i.send(msg)
    for file in files:
        file = (file + "\n").encode()
        i.send(file)


def udp(file):
    msgFromServer = "Hello UDP Client"
    bytesToSend = str.encode(msgFromServer)
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    address = (id[0], id[1])
    print(address)
    while (True):
        UDPServerSocket.sendto(bytesToSend, address)



def download(i, file):
    path = os.path.abspath("")
    files = [file for file in listdir(path) if isfile(join(path, file))]
    if file not in files:
        msg = "no such a file in the server!"
        msg = msg.encode()
        i.send(msg)
        print("no such a file!")
    else:
        print(f"sending {file} to {nickname}")
        msg = "-sending-"
        msg = msg.encode()
        i.send(msg)
        size = os.path.getsize(file)
        size = str(size)
        msg = "serverFile-" + file + "," + size
        msg = msg.encode()
        i.send(msg)
        udp(file)


def kick(i):
    msg = "-exit-"
    msg = msg.encode()
    try:
        for key, value in names.items():
            if value == nickname:
                id = key
                del names[key]
                break
        i.send(msg)
        id = i.getpeername()
        del names[id]
        print(f"client {nickname} has left the chat, port {id[1]} free now ")
    except:
        try:
            print(f"client {nickname} has left the chat, port {id[1]} free now ")
        except:
            pass
    inputs.remove(i)
    broadcast(f"{nickname} has left the chat".encode(), [tcp])
    i.close()

def gentlyKick(i, flag):
    id = i.getpeername()
    try:
        del names[id]
        if flag == 0:
            broadcast(f"{nickname} has left the chat".encode(), [tcp])
            print(f"client {nickname} has left the chat, port {id} free now ")

    except:
        pass
    if flag != 0:
        print(f"client {nickname} has kicked from the chat (same name) , the ip and port {id[1]} are free now ")
    inputs.remove(i)
    i.close()


while True:
    readables, _, _ = select.select(inputs, [], [])
    for i in readables:
        if i is tcp:
            client, address = tcp.accept()
            inputs.append(client)
            name = welcome(client)
            if name in names.values():
                msg = "importent! this is a message from the server - your nickname is already taken, please try to connect again with a different name, the taken names is all the online mamber below:"
                msg = msg.encode()
                client.send(msg)
                onlineList(client)
                gentlyKick(client, 1)
                continue
            print("new user detected! " + name + " connected")
            names[address] = name
            broadcast(name.encode() + f" entered the chat".encode(), [tcp, client])
        else:
            try:
                id = i.getpeername()
                nickname = names[id]
                try:
                    data = i.recv(buffer)
                    data = data.decode('UTF-8')
                    try:
                        command, message = data.split(',', 1)
                        data = str(nickname + " >>> " + message)
                    except:
                        command = data
                    if command == 'broadcast':
                        broadcast(data.encode(), [tcp, i])
                    elif command == "online":
                        onlineList(i)
                    elif command == "files":
                        filesList(i)



                    elif command == "d":
                        download(i, "text.txt")




                    elif command == "download":
                        download(i, message)
                    elif command == "exit":
                        kick(i)
                    else:
                        port = getClient(command)
                        if port == "exep" or data.find(">>>") == -1:
                            msg = "there is no such user name / command ! try again, pay intention to spaces or correct name!"
                            msg = msg.encode()
                            i.send(msg)
                        else:
                            chatWith(port, data)
                except:
                    try:
                        gentlyKick(i, 0)
                    except:
                        pass
            except:
                kick(i)

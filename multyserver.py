import socket
import select

server = socket.socket()
port = 55000
server.bind(('', port))
server.listen(15)
inputs = [server]
names = {}
files = ("mygif.gif", "text.txt", "photo.jpg")
print("ready to serve...")

def welcome(client):
    name = client.recv(1024)
    name = name.decode('UTF-8')
    users = [n.getpeername() for n in inputs if n is not client and n is not server]
    if len(users) < 1:
        greetMsg = name + ", you are the first client and no one online yet..so...how you doing?"
        client.send(greetMsg.encode())
    else:
        onlineList(client)
    client.getsockname()
    return name

def onlineList(i):
    msg = "list of who is online:"
    msg = msg.encode()
    i.send(msg)
    data = names.items()
    for name in data:
        name = (name[1]+ "\n").encode()
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

def chatWith (msg, port):
    for connection in inputs:
        try:
            connection.getpeername()[1]
        except:
            continue
        if connection.getpeername()[1] == port:
            connection.send(msg)

def filesList(i):
    msg = "list of available files:"
    msg = msg.encode()
    i.send(msg)
    for file in files:
        file = (file + "\n").encode()
        i.send(file)

def kick(i):


    # not muhan


    msg = "exit"
    msg = msg.encode()
    i.send(msg)
    id = i.getpeername()[1]
    del names[id]
    inputs.remove(i)
    print(f"client {nickname} has left the chat ")
    broadcast(f"{nickname} has left the chat".encode(), [server])
    i.close()

while inputs:
    readables, _, _ = select.select(inputs, [], [])
    for i in readables:
        if i is server:
            client, address = server.accept()
            inputs.append(client)
            name = welcome(client)
            print("new user detected! " + name + " connected")
            names[address[1]] = name
            broadcast(name.encode() + f" entered the chat".encode(), [server, client])

        else:
            id = i.getpeername()[1]
            nickname = names[id]
            try:
                data = i.recv(1024)
                data = data.decode('UTF-8')
                try:
                    command, message = data.split(',', 1)
                    data = str(nickname + " >>> " + message).encode()
                except:
                    command = data
                if command == 'broadcast':
                    broadcast(data, [server, i])
                elif command == "online":
                    onlineList(i)
                elif command == "files":
                    filesList(i)
                elif command == "exit":
                    kick(i)
                else:
                    port = getClient(command)
                    if port == "exep":
                        msg = "there is no such user name / command ! try again, pay intention to spaces or correct name!"
                        msg = msg.encode()
                        i.send(msg)
                    else:
                        chatWith(data, port)

            except Exception as e:
                kick(i)

import socket
import select

server = socket.socket()
port = 55000
server.bind(('', port))
server.listen(15)
inputs = [server]
clients = []
names = {}
print("ready to serve...")

def welcome(client):
    name = client.recv(1024)
    name = name.decode('UTF-8')
    users = [n.getpeername() for n in inputs if n is not client and n is not server]
    if len(users) < 1:
        greetMsg = "hello " + name + "! \n you are the first client and no one online yet..so...how you doing?"
    else:
        greetMsg = "hello " + name + "! \n users online: " + str(users)
    client.send(greetMsg.encode())
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

while inputs:
    readables, _, _ = select.select(inputs, [], [])
    for i in readables:
        if i is server:
            client, address = server.accept()
            inputs.append(client)
            print("connected to new client")
            name = welcome(client)
            names[address[1]] = name
            broadcast(name.encode() + f" enterd".encode(), [server, client])

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
                elif command == "list":
                    onlineList(i)
                else:
                    port = getClient(command)
                    if port == "exep":
                        msg = " there is no such user name / command ! try again, pay intention to spaces or correct name!"
                        msg = msg.encode()
                        i.send(msg)
                    else:
                        chatWith(data, port)

            except Exception as e:
                print(e)
                inputs.remove(i)
                print(f"client {nickname} has left the chat ")
                broadcast(f"{nickname} has left the chat".encode(), [server])
                i.close()
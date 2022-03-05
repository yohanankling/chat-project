import tkinter
from socket import socket
from time import sleep
from tkinter import messagebox
import socket
import threading
import os
# answer = 0
# starting to setting the useful variable
buffer = 1024
ip = input("enter server IP: or press enter for locall ip")
name = input("enter your nickname please:")
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# to send tcp immideatlly (disable Nagle's algorithm) - more transferring but more convenient to track packet
tcp.setsockopt(socket.SOL_TCP, socket.TCP_QUICKACK, 0)
tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
host_name = socket.gethostname()
if ip == "":
    ip = socket.gethostbyname(host_name)
port = 55001
# connect to free port and ip
for i in range(14):
    try:
        tcp.bind(("", port))
        break
    except:
        port = port + 1
try:
    tcp.connect((ip, 55000))
except:
    print("cant connect to server")

# write recived file
def write(packets, filename):
    # if answer == 1:
    #     return
    file = open(filename, 'wb')
    for packet in packets:
        file.write(packet)
    file.close()

def udp(filename, size):
    print("udp start")
    if os.path.exists(filename):
        os.remove(filename)
    else:
        pass
    #set two UDP socket to recive and send
    UDPSEND = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPRECV = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    address = ('127.0.0.1', port + 1000)
    UDPRECV.bind(address)
    sendto = (ip, 57000)
    packets = []
    ack = 0
    UDPSEND.sendto("-2".encode(), sendto)
    while True :
        data = UDPRECV.recvfrom(buffer)[0]
        data = data.decode()
        data = data.split(',')
        # if its a good ack, continue, else send again
        if int(data[1]) == ack:
            packets.append(data[0].encode())
            UDPSEND.sendto(str(ack).encode(), sendto)
            ack += 1
            #if finished
        if int(data[1]) == -1:
            UDPSEND.sendto(str(-1).encode(), sendto)
            break
    frame.insert(tkinter.END, "sucssfully recived the file!")
    data = "the last package is: ".encode() + packets[ack-1]
    frame.insert(tkinter.END, "we printed the last package in the terminal(its might be long to show you that here so...")
    print(data.decode())
    write(packets, filename)

def files():
    data = tcp.recv(buffer).decode()
    data = data.split(',')
    filename = data[0]
    size = data[1]
    frame.insert(tkinter.END, "filename :" + filename)
    frame.insert(tkinter.END, "\n")
    frame.insert(tkinter.END, filename + " size : " + size)
    size = int(size)
    # thread to keep the tcp socket also in action
    udpThread = threading.Thread(target=udp, args=(filename, size))
    udpThread.start()

# tried to de an break point in download, in comment for now...
# def continueD():
#     frame.insert(tkinter.END, "to stop the download , send '1', to continue - send '0' *in the terminal!*")
#     while True:
#         answer = input("enter your decision please:")
#         try :
#             if answer == 0:
#                 tcp.send("555".encode())
#                 break
#             elif answer == 1:
#                 tcp.send("666".encode())
#                 break
#             else:
#                 frame.insert(tkinter.END, "wrong type..try again")
#         except:
#             frame.insert(tkinter.END, "wrong type..try again")

# recive method in thread
def recive():
    while True:
        try:
            data = tcp.recv(buffer).decode()
            if data == "-exit-":
                tcp.detach()
                tcp.close()
                print("you successfully disconnected from the server, bye bye " + name)
                os._exit(0)
            elif data == "-sending-":
                files()
            # elif data == "continue?":
            #     ans.start()
            #     ans.join()
            else:
                frame.insert(tkinter.END, data)
        except:
            print("cannot to connect the server, try different name, or running the server")
            tcp.detach()
            tcp.close()
            os._exit(0)


def online():
    tcp.send("online".encode())
    message.set("")


def filesList():
    tcp.send("files".encode())
    message.set("")


def disconnect():
    tcp.send("exit".encode())
    message.set("")


def exit():
    if messagebox.askyesno("Exit", "Do you want to quit the application?"):
        tcp.send("exit".encode())
        sleep(0.1)
        gui.destroy()
    else:
        msg = "lucky for us..."
        frame.insert(tkinter.END, msg)


def send2():
    text = message.get()
    tcp.send(text.encode())
    try:
        to, msg = text.split(',', 1)
        data = str(name + " >>> " + to + ":  " + msg)
        frame.insert(tkinter.END, data)
    except:
        pass
    message.set("")

try:
    tcp.send(name.encode())
except:
    pass

# GUi
gui = tkinter.Tk()
gui.title("icq2")
gui.resizable(False, False)
gui['bg'] = 'cyan'
window = tkinter.Frame(gui)
scrollbar = tkinter.Scrollbar(window)
frame = tkinter.Listbox(window, height=20, width=50, yscrollcommand=scrollbar.set)
frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
frame.pack()
window.pack()
menu = tkinter.Label(gui, text="menu:")
menu.pack()
send = tkinter.Label(gui, text="enter your message:")
send.pack()
message = tkinter.StringVar()
message.set("")
text = tkinter.Entry(gui, textvariable=message, foreground="Black")
text.bind(send2())
text.pack()
send = tkinter.Button(gui, text="Send", command=send2)
send.pack(side=tkinter.LEFT)
online = tkinter.Button(gui, text="online list", command=online)
online.pack(side=tkinter.RIGHT)
filesList = tkinter.Button(gui, text="files list", command=filesList)
filesList.pack(side=tkinter.RIGHT)
disconnect = tkinter.Button(gui, text="disconnect", command=disconnect)
disconnect.pack(side=tkinter.LEFT)
gui.protocol("WM_DELETE_WINDOW", exit)

# some welcome messgae
msg = "hello " + name + "!"
frame.insert(tkinter.END, msg)
msg = "here is the commands manual : "
frame.insert(tkinter.END, msg)
msg = 'to send a message to everyone enter - "broadcast,text"'
frame.insert(tkinter.END, msg)
msg = 'to send a message to a person enter - "person name,text"'
frame.insert(tkinter.END, msg)
msg = 'to download a file from the server enter - "download,file_name.type"'
frame.insert(tkinter.END, msg)

# thread to run recive and send in parallel
recive = threading.Thread(target=recive)
# ans = threading.Thread(target=continueD)
recive.start()
tkinter.mainloop()

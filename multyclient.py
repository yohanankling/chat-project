import socket
import threading
import sys
name = input("enter your nickname please:")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 55001
for i in range(14):
      try:
            s.bind(("", port))
            break
      except:
            port = port + 1
s.connect((ip, 55000))
print("hello " + name + "!")
print("here is the commands manual : ")
print('to send a message to everyone enter - "broadcast,text"')
print('to send a message to a person enter - "person name,text"')
print('to see who is online enter - "online"')
print('to see the available online file list enter - "files"')
print('to disconnect enter - "exit"')

def send():
      s.send(name.encode())
      while True:
            s.send(input().encode())

t = threading.Thread(target=send)
t.start()

while True:
      try:
            data = s.recv(1024).decode()

            #not muhan

            if data == "exit":
                  s.close()
            else:
                  print(data)
      except:
            pass

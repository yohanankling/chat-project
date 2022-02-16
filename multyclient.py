#client code:
import socket
import threading
name = input("enter your nickname please:")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
s.connect((ip, 55000)) #enter server address & port number
print("commands manual : ")
print('to send a message to everyone enter - "broadcast,text"')
print('to send a message to a person enter - "person name,text"')
print('to see who is online enter - "list"')


def job():
      s.send(name.encode())
      while True:
            s.send(input().encode())

t = threading.Thread(target=job)
t.start()

while True:
      try:
            print(s.recv(1024).decode())
      except:
            pass
import socket
import threading
import os
buffer = 1024
ip = input("enter server IP: or press enter for locall ip")
name = input("enter your nickname please:")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_name = socket.gethostname()
if ip =="":
      ip = socket.gethostbyname(host_name)
port = 55001
print(ip)
for i in range(14):
      try:
            s.bind(("", port))
            udp.bind("", port)
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
print('to download a file from the server enter - "download,file_name.type"')
print('to disconnect enter - "exit"')

def send():
      s.send(name.encode())
      while True:
            s.send(input().encode())

t = threading.Thread(target=send)
t.start()

#
# def files():
#       print("download request accepted")
#       filename = s.recv(buffer).decode()
#       size = s.recv(buffer).decode()
#       size = 80
#       print("starting downloading...")
#       if os.path.exists(filename):
#             os.remove(filename)
#       with open(filename, 'wb') as fw:
#             recived = 0
#             print(1)
#             while recived < size:
#                   print(2)
#                   data = s.recv(buffer)
#                   fw.write(data)
#                   recived = recived + len(data)
#       fw.close()
#       print("the file was successfully downloaded.")





# def files():
#       print("download request accepted")
#       filename = s.recv(buffer).decode()
#       # size = s.recv(buffer).decode()
#       size = 80
#       print("starting downloading...")
#       if os.path.exists(filename):
#             os.remove(filename)
#       with open(filename, 'wb') as fw:
#             recived = 0
#             while recived < size:
#                   data = udp.recvfrom(buffer)
#                   fw.write(data)
#                   recived = recived + len(data)
#       fw.close()
#       print("the file was successfully downloaded.")

def files():
      filename = s.recv(buffer).decode()
      size = s.recv(buffer).decode()
      print(1)
      msg = udp.recvfrom(buffer)
      print(2)
      print(msg)


while True:
      try:
            data = s.recv(buffer).decode()
            if data == "-exit-":
                  s.detach()
                  s.close()
                  print("you successfully disconnected from the server, bye bye " + name)
                  os._exit(0)
            elif data == "-sending-":
                  files()
            else:
                  print(data)
      except:
            pass
# download,text.txt

# -* encoding:utf-8 *-
# python 2.7.9
# __author__="zjx"
#
import socket
import sys
import Queue

s = socket.socket()
port = 1236

s.bind(("",port)) # Bind the ip and the port
s.listen(10)
x = 1
queue = Queue.Queue()
num = 1269
while x <= num:
    queue.put(x)
    x += 1

while True:
    c,addr=s.accept()
    print "Get connection from:",addr
    if queue.empty() == False:
        z = str(queue._get())
        c.send(z)
        print z
        i = 1
        while i<= 7:
            try:
                queue._get()
                i += 1
            except Exception,e:
                break
    else:
        c.send("You can't get the task")
        print "The task have stop"
        break
    c.close()
s.close()
sys.exit()

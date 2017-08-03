'''
Created on Jul 25, 2017

@author: Steven Proctor
'''
import socket
import time
from threading import Thread
class Node(object):
    '''
    classdocs
    '''
    def __init__(self, addr, ports):
        self.buffer = []
        self.portlink(addr,ports)
        
    def send(self, message):
        try:
            self.conn.sendto(message, self.addr)
        except:
            time.sleep(0.01)
            self.send(message)
    def portlink(self,addr,ports):
        while True:
            s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto("t", (socket.gethostbyname(socket.gethostname()), 5555))
            
            if s.getsockname()[1] in ports:
                sock = s
                break
            else:
                s.close()  
            time.sleep(0.01)
        for p in ports:
            sock.sendto("t",(addr,p))
            time.sleep(0.01)
        
        addr2bind = sock.getsockname()
        sock.close()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn.bind(addr2bind)
        data, address = self.conn.recvfrom(64)
        if address != None:
            print str(address) + data
            self.addr = address
            self.online = True
            return
        else:
            self.online = False
        print "check"
        self.open = True
        t = Thread(self.__listen__())
        t.start()
    def __listen__(self):
        while self.open:
            data, address = self.conn.recvfrom(64)
            if address == self.addr:
                self.buffer.append(data)
            
ports = range(30000,65000,300)

node = Node("73.172.209.102", ports)
node.send("THIS MEANS THAT IT WORKS")
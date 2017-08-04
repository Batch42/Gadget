'''
Created on Jul 25, 2017

@author: Steven Proctor
grab +port        grab +port
spit packets    
recieve
'''
import socket
import time
from threading import Thread
class Node(object):
    '''
    classdocs
    '''
    def __init__(self, addr, ports,female):
        self.buffer = []
        self.portlink(addr,ports,female)
        
    def send(self, message):
        try:
            self.outbound.sendto(message, self.toaddr)
        except:
            time.sleep(0.01)
            self.send(message)
            
    def portlink(self,addr,ports,start):
        if start:
            self.inbound = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
            flower = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            flower.bind(addr2bind)
            data, address = flower.recvfrom(64)
            self.toaddr = address
            self.fromaddr = (addr,int(data))
            flower.close()
            self.outbound = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.outbound.bind(addr2bind)
            self.outbound.sendto(self.inbound.getsockname()[1],self.toaddr)
            self.open = True
            t = Thread(self.__listen__())
            t.start()
        else:
            self.outbound = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            time.sleep(0.02*len(ports))
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
                sock.sendto(self.outbound.getsockname()[1],(addr,p))
                time.sleep(0.01)
        
            
            addr2bind = sock.getsockname()
            sock.close()
            self.inbound = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.inbound.bind(addr2bind)
            data, address = self.inbound.recvfrom(64)
            self.fromaddr = address
            self.toaddr = (addr,int(data))
            self.outbound.sendto("check",self.toaddr)
            self.open = True
            t = Thread(self.__listen__())
            t.start()
    def __listen__(self):
        while self.open:
            data, address = self.inbound.recvfrom(64)
            if address == self.fromaddr:
                self.buffer.append(data)
            
ports = range(30000,65000,300)

node = Node("73.172.209.102", ports, False)
node.send("THIS MEANS THAT IT WORKS")
time.sleep(3)
print node.buffer[0]
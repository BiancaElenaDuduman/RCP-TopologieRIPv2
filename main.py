import socket
import struct

#########------------------Pachet RIP---------------###########
class pachetRip:
    def __init__(self):
        self.command = b'\x00'
        self.version = b'\x02'
        self.addrFam = b'\x00\x02'
        self.routeTag = b'\x00\x00'
        self.ipAddress = b'\x00\x00\x00\x00'
        self.netMask = b'\x00\x00\x00\x00'
        self.nextHop = b'\x00\x00\x00\x00'
        self.metric = b'\x00\x00\x00\x00'

        self.pachet = b''

    def packet(self):
        self.pachet += (self.command[0:1] +
                      self.version[0:1] +
                      self.addrFam[0:2] +
                      self.routeTag[0:2] +
                      self.ipAddress[0:4] +
                      self.netMask[0:4] +
                      self.nextHop[0:4] +
                      self.metric[0:4])

    #transform adresa in int
    def toInt(self, ip):
        v = ip.split('.')
        for i in range(0, len(v)):
            v[i] = int(v[i])
        return struct.pack("BBBB", v[0], v[1], v[2], v[3])


    def addEntry(self, ip, masca):
        self.pachet += (self.addrFam[0:2] +
                        self.routeTag[0:2] +
                        self.toInt(ip) +
                        self.toInt(masca) +
                        self.nextHop[0:4] +
                        self.metric[0:4])

    def setIp(self, ip):
        self.ipAdress = self.toInt(ip)

    def setMasca(self, masca):
        self.netMask = self.toInt(masca)

def Send(self, udp_ip, udp_port):
    grp= (udp_ip, udp_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(grp)

    sock.send(self.pachet, grp)

    sock.close()

def receive(self, udp_ip, udp_port):
    format=''
    grp= (udp_ip, udp_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(grp)
    message, address = sock.recv(1024)
    #message
    sock.close()



ip1 = '192.168.1.1'
port1 = 12001
ip2 = '192.168.2.1'
port2 = 12002

ob = pachetRip()
ob.setIp('192.168.2.1')
ob.setMasca('255.255.255.0')


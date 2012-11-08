import os, sys
import socket
import struct
import threading
import SocketServer
import random
import signal

# DNS Server List
# DNS_SERVS = ['8.8.8.8',
#          '8.8.4.4',
#          '208.67.222.222',
#          '208.67.220.220',
#          ]

LOCAL_DNS_IP = "127.0.0.1"
REMOTE_DNS_IP = "8.8.8.8"

DNS_PORT = 53           # default dns port 53
TIMEOUT = 20            # set timeout 20 second

    
def QueryDnsByTcp(dns_ip, dns_port, query_data):
    dns_serv = (dns_ip, dns_port);
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(TIMEOUT) # set socket timeout
        
        s.sendto(query_data, dns_serv)
        data, addr = s.recvfrom(2048)
    except:
        return

    endata = ""
    for i in range(len(data)):
        endata += chr(~ord(data[i]) % 256)
    return endata

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True
    
    def __init__(self, s, t):
        SocketServer.UDPServer.__init__(self, s, t)

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        query_data = self.request[0]
        udp_sock = self.request[1]
        addr = self.client_address

        response = QueryDnsByTcp(REMOTE_DNS_IP, DNS_PORT, query_data)
        if response:
            # udp dns packet no length
            udp_sock.sendto(response[:], addr)
        
        
if __name__ == "__main__":
    dns_server = ThreadedUDPServer((LOCAL_DNS_IP, DNS_PORT), ThreadedUDPRequestHandler)
    try:
        dns_server.serve_forever()
    except KeyboardInterrupt:
        dns_server.shutdown()
        sys.exit()

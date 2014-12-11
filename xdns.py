#!/usr/bin/python

import os, sys, getopt
import socket
import struct
import threading
import SocketServer

DNS_PORT = 53           # default dns port 53
TIMEOUT = 20            # set timeout 5 second

LOCAL_LISTEN_IP = '127.0.0.1'   # listen ip
REMOTE_SERV_IP = '8.8.8.8'      # remote dns server ip

def DNSQuery(dns_ip, dns_port, query_data):
    # simply encrypt socket data
    qdata = query_data[::-1]
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.settimeout(TIMEOUT) # set socket timeout
    
        s.sendto(qdata, (dns_ip, dns_port))
        data, addr = s.recvfrom(2048)
    except:
        return None
    finally:
        if s: s.close()

    return data

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True
    
    def __init__(self, s, t):
        socket.setdefaulttimeout(TIMEOUT)
        SocketServer.UDPServer.__init__(self, s, t)

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        query_data = self.request[0]
        udp_sock = self.request[1]
        addr = self.client_address

        response = DNSQuery(REMOTE_SERV_IP, DNS_PORT, query_data)
        if response:
            # udp dns packet no length
            udp_sock.sendto(response, addr)
        
def help():
    print 'Usage: xdns.py -s <serverip> -l <listenip>'
    print 'options:'
    print '  -h  show help'
    print '  -l  explicitly set listen ip, default 127.0.0.1'
    print '  -s  explicitly set remote DNS ip, default 8.8.8.8'
        
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:s:")
    except getopt.GetoptError:
        help()
        sys.exit(-1)

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        if opt == '-s':
            REMOTE_SERV_IP = arg
        if opt == '-l':
            LOCAL_LISTEN_IP = arg


    print "---------------------------------------------------------------"
    print "  Listen IP : ", LOCAL_LISTEN_IP, " |  Remote IP ", REMOTE_SERV_IP
    print "---------------------------------------------------------------"
    
    dns_server = ThreadedUDPServer((LOCAL_LISTEN_IP, DNS_PORT), ThreadedUDPRequestHandler)
    dns_server.serve_forever()


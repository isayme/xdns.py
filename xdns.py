#!/usr/bin/python

import os, sys, getopt
import socket
import struct
import threading
import SocketServer

import threadpool

REMOTE_SERV_IP = ''      # remote dns server ip
#REMOTE_SERV_IP = '8.8.8.8'
    
class ThreadPoolMixIn:
    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        self.tp.add_task(self.process_request_thread, request, client_address)

    def serve_forever(self, poll_interval=0.5):
        try:
            SocketServer.UDPServer.serve_forever(self, poll_interval)
        finally:
            self.tp.stop()
            

class DNSProxy(ThreadPoolMixIn, SocketServer.UDPServer):
    # much faster rebinding
    allow_reuse_address = True
    
    def __init__(self, s, t):        
        self.tp = threadpool.ThreadPool(20)
        SocketServer.UDPServer.__init__(self, s, t)
  
  
class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        query_data = self.request[0]
        udp_sock = self.request[1]
        addr = self.client_address

        response = self.dns_query(REMOTE_SERV_IP, 53, query_data)
        if response:
            # udp dns packet no length
            udp_sock.sendto(response, addr)
 
    def dns_query(self, dns_ip, dns_port, query_data):
        # simply encrypt socket data
        qdata = query_data[::-1]
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(5) # set socket timeout = 5s
        
            s.sendto(qdata, (dns_ip, dns_port))
            data, addr = s.recvfrom(2048)
        except:
            return None
        finally:
            if s: s.close()

        return data
    
    
def help():
    print('Usage: xdns.py -s <serverip>')
    print('options:')
    print('  -h  show help')
    print('  -s  explicitly set remote DNS ip, default 8.8.8.8')
        
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:')
    except getopt.GetoptError:
        help()
        sys.exit(-1)

    if not REMOTE_SERV_IP:
        REMOTE_SERV_IP = '8.8.8.8'
    
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        if opt == '-s':
            REMOTE_SERV_IP = arg
    
    print('REMOTE_SERV_IP: ' + REMOTE_SERV_IP)
    
    dns_server = DNSProxy(('0.0.0.0', 53), ThreadedUDPRequestHandler)
    dns_server.serve_forever()

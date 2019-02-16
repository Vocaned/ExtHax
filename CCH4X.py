import socket 
import os
import sys
import struct
import nonCPEparser
import CPEparser
import importlib

def eth_addr(a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b

s=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

while True:

    dat=s.recvfrom(65565)
    packet=dat[0]
    eth_header = packet[:14]
    eth = struct.unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    
    ip_header = packet[14:34]
    iph = struct.unpack('!BBHHHBBH4s4s' , ip_header)
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    iph_length = ihl * 4
    ttl = iph[5]
    protocol = iph[6]
    src_addr = socket.inet_ntoa(iph[8])
    dest_addr = socket.inet_ntoa(iph[9])
    if protocol == 6 :
        # s_addr = socket.inet_ntoa(iph[8])
        # d_addr = socket.inet_ntoa(iph[9])

        # print('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))
        t = iph_length + 14
        tcp_header = packet[t:t+20]
    
        tcph = struct.unpack('!HHLLBBHHH' , tcp_header)

        src_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4

        # print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length))

        h_size = 14 + iph_length + tcph_length * 4
        data_size = len(packet) - h_size

        #get data from the packet
        data = packet[h_size:]
        if src_port == 25565 or dest_port == 25565:
            if data == b'':
                continue
            try:
                importlib.reload(CPEparser)
                CPEparser.parse(src_port, dest_port, data)
            except Exception as e:
                print('[ERROR] ' + str(e)) 
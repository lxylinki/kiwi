import sys
import json
import socket
import bases
from sys import maxsize

# this file contains: 
# agent skeleton
# TODO:scheduling algorithms

class agent:
    # fixed len msgs
    MSGLEN = 2048
    listenport = 2014
    sendport = 2015
    bindhost = '0.0.0.0'
    states = {'idle':0, 'scheduling':1, 'communicating':2}

    def __init__(self, name):
        # name is the identifier
        self.name = name
        self.state = self.states['idle']
        
        sndsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sndsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        recsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.sndsock = sndsock
        self.recsock = recsock

    def receive(self):
        (bytes_info, cli_addr) = self.recsock.recvfrom(self.MSGLEN)
        print ('receiving from', cli_addr)
        return bytes_info
    
    def json_decode(self, msgreceived):
        decoded_msg = json.loads(msgreceived.decode('utf-8').strip())
        # a dict of subgraph info
        return decoded_msg
    
    # reconstruct local taskgraph motif
    def restore_motif(self, wfdict):
        wf = bases.wfgraph('local_taskgraph')
        for k,v in wfdict.items():
            tmpmod = bases.mod(k, v['res'])
            if v['host_id']!=None:
                tmpmod.host_id = v['host_id']
            wf.add(tmpmod)

        for k,v in wfdict.items():
            if len(v['suc'])>0:
                for l,c in v['suc'].items():
                    if l in wfdict.keys():
                        bases.mod_join(wf.get(k), wf.get(l), c)
        return wf

    # msgtosend: a updated dict of subgraph info
    def json_encode(self, msgtosend):
        encoded_msg = bytes( json.dumps(msgtosend), encoding='utf-8' )
        # a ready-to-send bytestring
        return encoded_msg
   
    def send(self, msg, desthost, port):
        self.sndsock.sendto(msg, (desthost, port))


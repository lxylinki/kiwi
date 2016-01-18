from kiwi_sched import agent
from bases import *
import global_info

class scheduler(agent):
    # scheduler running on each server
    # listening for incoming workflow motifs
    # respond with its schedule decision

    def __init__(self, name, hostaddr):
        agent.__init__(self, name)
        self.role = 'scheduler'
        self.host = hostaddr
    
    def start(self):
        self.recsock.bind((self.bindhost, self.listenport))
        self.sndsock.bind((self.bindhost, self.sendport))
        print ('listening at %s:%s' % (self.bindhost, self.listenport))
        while True:
            encoded_info = self.receive()
            print (type(encoded_info))
            print (encoded_info)
         
            decoded_info = self.json_decode(encoded_info)
            print (type(decoded_info))
            print (decoded_info)
            motif = self.restore_motif(decoded_info)
            print (type(motif))
            for k,v in motif.mods.items():
                print (k, type(v), v.__dict__)

            self.schedule( motif, self.localnet )
            for k,v in motif.mods.items():
                print (k, type(v), v.__dict__)
        
        self.recsock.close()
    

    # coordinator is (host, port) tuple
    def set_coordinator(self, host, port=None):
        if port==None:
            self.coordinator = (host, self.listenport)
        else:
            self.coordinator = (host, port)
    
    # get local star graph
    def collect_localnet(self):
        globalnet = global_info.network('local_netgraph')
        self.localnet = globalnet.star_extract(self.host)
    
    # we are scheduling on the restored objects
    def schedule(self, wfmotif, netgraph):
        for mod in wfmotif.mods.values():
            if mod.host_id != None:
                hubmod = mod
                break
        
        for mod in wfmotif.mods.values():
            if mod.host_id == None:
                self.single_schedule( hubmod, self.localnet, mod)
 
    # this function operates on objects
    def single_schedule( self, hubmod, netgraph, sucmod ):
        hubnode = netgraph.get( hubmod.host_id )
        mindelay = maxsize
        for cand_id, bw in hubnode.neighbors.items():
            print (cand_id, bw)
            if netgraph.get(cand_id).res < sucmod.res:
                continue
            ds = hubmod.suc[sucmod.mod_id]
            if (ds/bw) < mindelay:
                mindelay = (ds/bw)
                print (mindelay)
                sucmod.decision_pool[hubmod.mod_id]=cand_id

if __name__=='__main__':
    s = scheduler('scheduler_0', 'c0')
    print ('I am running at host %s' % s.host)
    s.set_coordinator('192.168.2.51')
    print ('my coordinator is running at %s:%s' % s.coordinator)
    s.collect_localnet()
    print ('my local network view:', s.localnet)
    s.start()

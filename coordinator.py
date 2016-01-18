import global_info
from scheduler import *
from kiwi_sched import agent

# coordinator has full task graph
# fill in its entire graph with pieces from schedulers
class coordinator(agent):
    def __init__(self, name):
        agent.__init__(self, name)
        self.role = 'coordinator'
        # all schedulers, entry as name:address
        self.schedulers = {}

    # global view of task graph
    def set_taskgraph(self, tgname):
        self.workflow = global_info.taskgraph(tgname)

    def new_scheduler(self, name, address):
        self.schedulers[name] = address

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
            print (motif.mods.items())
        
        self.recsock.close()
    

if __name__=='__main__':
    c = coordinator('coordinator_0')
    c.new_scheduler('scheduler_0', '192.168.2.13')
    c.set_taskgraph('wf')
    c.start()

import json
import random
import global_info
from sys import maxsize

# a simulated version of program in task graph
class mod:
    # pending : waiting/collecting placement decisions
    # readytoplace : received all placement decisions
    # readytostart : all pres finished and incoming data ready
    
    states = {'pending':0, 'readytoplace':1, 'placed':2,
            'readytostart':3, 'inexecution':4, 'finished':5}
   
    # resource requirement is an abstract value
    def __init__( self, mod_id, res_require ):
        self.mod_id = mod_id
        self.pre = {}
        self.suc = {}
        self.endtime = 0
        self.starttime = 0
        self.host_id = None
        self.res = res_require
        self.decision_pool = {}
        self.state = self.states['pending']

    def in_deg(self):
        return len(self.pre)

    def out_deg(self):
        return len(self.suc)

    def set_state(self):
        # if received schedules from all its pres
        if len(self.decision_pool) == len(self.pre):
            self.state = self.states['readytoplace']

        if self.host_id != None:
            self.state = self.states['placed']

    # random select a schedule
    def decide(self):
        preid = random.choice( list(self.decision_pool.keys()) )
        self.host_id = self.decision_pool[preid]

    def __repr__(self):
        if self.host_id is None:
            return '< prog %s, res %s, state %s >' % (self.mod_id, self.res, self.state)
        else:
            return '< prog %s, res %s, state %s, host %s >' % (self.mod_id, self.res, self.state, self.host_id)

# workflow graph, just a list of customized mods
# this is intended to present motifs
class wfgraph:
    # entry in mods is mod.id:mod
    def __init__(self, name):
        self.name = name
        self.mods = {}

    def add(self, mod):
        self.mods[mod.mod_id]=mod

    def get(self, mod_id):
        return self.mods[mod_id]

    # return a mod and its successors in a dictionary
    def suc_extract(self, mod_id):
        hubmod = self.mods[mod_id]
        subgraph = {suc_id: self.mods[suc_id] for suc_id in hubmod.suc.keys()}
        subgraph.update({mod_id:hubmod})
        return subgraph 

    def order(self):
        return len(self.mods)

    def size(self):
        edges = 0
        for k,v in self.mods.items():
            edges = edges + v.in_deg() + v.out_deg() 
        return (edges/2)

# input a dictionary of mods of interest
# for json encoding use
def infodict(mods):
    return { k:v.__dict__ for k,v in mods.items()}
    
# a simulated version of a node in network
class node:
     states = {'up':1, 'down':0}

     # neighbor entry is node:bandwidth
     def __init__( self, node_id, avail_res):
         self.node_id = node_id
         self.res = avail_res
         self.neighbors = {}
         self.state = self.states['up']

     def deg(self):
         return len(self.neighbors)

     def __repr__(self):
         return '< node %s, res %s, state %s >' % (self.node_id, self.res, self.state)

# a graph consists of nodes
class netgraph:
    # entry in nodes is node.id:node
    def __init__(self, name):
        self.name = name
        self.nodes = {}

    def add(self, node):
        self.nodes[node.node_id]=node

    def get(self, node_id):
        return self.nodes[node_id]
    
    # return a dictionary of node and its neighbors
    def star_extract(self, node_id):
        hubnode = self.nodes[node_id]
        star = {neighbor_id:self.nodes[neighbor_id] for neighbor_id in hubnode.neighbors.keys()}
        star.update({node_id:hubnode})
        return star

    def order(self):
        return len(self.nodes)
    
    def size(self):
        edges = 0
        for k,v in self.nodes.items():
            edges = edges + v.deg() 
        return (edges/2)

# join in the order of prog1->prog2 with datasize
def mod_join( mod1, mod2, datasize):
    mod1.suc[mod2.mod_id] = datasize
    mod2.pre[mod1.mod_id] = datasize

# join nodes with bandwidth
def node_join( node1, node2, bandwidth ):
    node1.neighbors[node2.node_id] = bandwidth
    node2.neighbors[node1.node_id] = bandwidth

if __name__=='__main__':
    wf = wfgraph('wf')
    w2motif = wfgraph('w2motif')
    net = netgraph('net')

    # scheduler on c0 and scheduler on c1 
    w0 = mod('w0', 25)
    w1 = mod('w1', 12)
    w2 = mod('w2', 24)
    w0.host_id = 'c0'
    w1.host_id = 'c1'
    w3 = mod('w3', 20)
    w4 = mod('w4', 64)

    # composition: this is global information for central manager
    mod_join(w0, w2, 100)
    mod_join(w1, w2, 200)
    mod_join(w2, w3, 180)
    mod_join(w2, w4, 400)

    wf.add(w0)
    wf.add(w1)
    wf.add(w2)
    wf.add(w3)
    wf.add(w4)

    w2motif.add(w2)
    w2motif.add(w3)
    w2motif.add(w4)

    c0 = node('c0', 10)
    c1 = node('c1', 12)
    c2 = node('c2', 25)
    c3 = node('c3', 26)
    
    node_join(c0, c1, 16)
    node_join(c0, c3, 50)
    node_join(c0, c2, 10)
    node_join(c1, c3, 20)
    node_join(c1, c2, 40)

    net.add(c0)
    net.add(c1)
    net.add(c2)
    net.add(c3)

    # motif extracted as a dictionary
    w0motif = wf.suc_extract('w0')
    w0info = infodict(w0motif)

    c2star = net.star_extract('c2')
    print (c2star)

    print ('workflow size:%d, network size:%d' % (wf.size(), net.size()))
    scheduler.single_schedule(w0, net, w2)
    scheduler.single_schedule(w1, net, w2)
    print (w2.decision_pool)

    w2info = infodict(w2motif.mods)
    print (w2info)

    with open('w2.json', mode='w', encoding='utf-8') as f:
        json.dump( w2.__dict__, f, indent=2 )
    
    with open('w0motif.json', mode='w', encoding='utf-8') as f:
        json.dump( w0info, f, indent=2 )
    
    with open('w2motif.json', mode='w', encoding='utf-8') as f:
        json.dump( w2info, f, indent=2 )
    


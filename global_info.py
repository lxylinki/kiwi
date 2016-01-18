# test files
import socket
import json
import bases

# this is a small test wf
def taskgraph(name):
    wf = bases.wfgraph(name)
    
    w0 = bases.mod('w0', 25)
    w1 = bases.mod('w1', 12)
    w2 = bases.mod('w2', 24)
    w0.host_id = 'c0'
    w1.host_id = 'c1'

    w3 = bases.mod('w3', 20)
    w4 = bases.mod('w4', 64)
    
    bases.mod_join(w0, w2, 100)
    bases.mod_join(w1, w2, 200)
    bases.mod_join(w2, w3, 180)
    bases.mod_join(w2, w4, 400)

    wf.add(w0)
    wf.add(w1)
    wf.add(w2)
    wf.add(w3)
    wf.add(w4)

    return wf

# test network
def network(name):
    net = bases.netgraph(name)
    
    c0 = bases.node('c0', 10)
    c1 = bases.node('c1', 12)
    c2 = bases.node('c2', 25)
    c3 = bases.node('c3', 26)
    
    bases.node_join(c0, c1, 16)
    bases.node_join(c0, c3, 50)
    bases.node_join(c0, c2, 10)
    bases.node_join(c1, c3, 20)
    bases.node_join(c1, c2, 40)

    net.add(c0)
    net.add(c1)
    net.add(c2)
    net.add(c3)

    return net

if __name__=='__main__':
    myworkflow = taskgraph('wf')
    mynetwork = network('net')

    w0motif = myworkflow.suc_extract('w0')
    print (w0motif)

    w0info = bases.infodict(w0motif)
    print (w0info)    

    print ('workflow size:%d, network size:%d' % (myworkflow.size(), mynetwork.size()))

    # with open('w0motif.json', mode='w', encoding='utf-8') as f:
    #    json.dump( motifinfo, f, indent=2 )
    

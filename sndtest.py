import bases
import time
import global_info
import scheduler

if __name__=='__main__':
    wf = global_info.taskgraph('wf')
    c = scheduler.scheduler('c','localhost')
    
    # 1st subgraph
    w0 = wf.suc_extract('w0')
    w0info = bases.infodict(w0)
    w0bytesinfo = c.json_encode(w0info)

    c.send(w0bytesinfo, 'localhost', 2014)
    c.sndsock.close()

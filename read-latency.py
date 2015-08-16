import sys
from collections import Counter
import babeltrace
import Gnuplot

class Read():
    def __init__(self, filename):
        self.fd = 0
        self.filename = filename
        self.last_open = 0
        self.begin_timestamp = -2
        self.end_timestamp = -1
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "\t"+str(self.fd)+ "\n\t" + self.filename + "\n\tdur: " + str(self.end_timestamp - self.begin_timestamp) + "\n"

class Process():

    def __init__(self, vtid, name, argv):
        self.vtid = vtid
        self.name = name
        self.argv = argv
        self.last_read_fd = 0
        self.reads = []
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "<" + str(self.vtid) + " ," + self.name + " ," + str(self.argv) + "\n" + str(self.reads) + ">"

def generate_gnuplot_graph(begin, end, processes):
    g = Gnuplot.Gnuplot(debug=1, persist=1)
    g.title('A simple example') # (optional)
    g('set style data linespoints') # give gnuplot an arbitrary command
    g('set yrange [0:100]')
    g('set xrange [{}:{}]'.format( begin/1000, (end/1000)))
    
    i = 0
    for tid,process in processes.items():
        for read in process.reads:
            if read.begin_timestamp < 0 or read.end_timestamp < 0:
                continue
            g("set object rectangle from {},{} to {},{} fs {} fc rgb \"{}\" behind ".format(read.begin_timestamp/1000, i, read.end_timestamp/1000,i+1, "solid", "red"))
        i +=1
    g.plot([1,2])

def read_latency():
    if len(sys.argv) != 2:
        msg = 'Usage: python {} TRACEPATH'.format(sys.argv[0])
        raise ValueError(msg)

    # a trace collection holds one to many traces
    col = babeltrace.TraceCollection()

    # add the trace provided by the user
    # (LTTng traces always have the 'ctf' format)
    if col.add_trace(sys.argv[1], 'ctf') is None:
        raise RuntimeError('Cannot add trace')
    
    # we trace only processes that were exec() during the trace.
    processes = {}
    begin_ts = -1
    end_ts = -1 
    current_ts = -1
    for event in col.events:
        if begin_ts < 0:
            begin_ts = event.timestamp
        else:
            current_ts = event.timestamp
        # keep only `sched_switch` events
        if event.name == 'syscall_entry_execve':
            processes[event['vtid']] = Process(event['vtid'], event['filename'], event['argv'])

        if event['vtid'] in processes:
            process = processes[event['vtid']]
            if 'fd' in event:
                # forget about stdin, stdout and stderr
                if event['fd'] in [0,1,2]:
                    continue
            if event.name == 'syscall_entry_open':
                process.last_open = Read(event['filename'])
            elif event.name == 'syscall_exit_open':
                process.last_open.fd = event['ret']
                process.reads.append(process.last_open)
                process.last_open = None
            elif event.name == 'syscall_entry_read':
                for i, read in enumerate(process.reads):
                    # fd can be reused
                    if read.fd == event['fd'] and read.begin_timestamp < 0:
                        process.reads[i].begin_timestamp = event.timestamp-begin_ts
                        process.last_read_fd = event['fd']
                        break
            elif event.name == 'syscall_exit_read':
                for i, read in enumerate(process.reads):
                    if read.fd == process.last_read_fd and read.end_timestamp < 0:
                        process.reads[i].end_timestamp = event.timestamp-begin_ts

    end_ts = current_ts
    print(processes)
    generate_gnuplot_graph(begin_ts, end_ts, processes)
if __name__ == '__main__':
    ##top5proc()
    read_latency()

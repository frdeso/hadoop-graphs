import operator
import sys
import csv 

class bar:
    def __init__(self, id):
        self.currentstart = -1
        self.currentend = -1
        self.id = id
    def is_empty(self, start):
        if self.currentend <= float(start):
            return True
        else:
            return False

    def set_task(self, start, end):
        self.currentstart = float(start)
        self.currentend = float(end)
        return self.id
class task:
        def __init__(self, name, start, end, type,status, run):
                self.name = name 
                self.start= start
                self.end= end
                self.type= type
                self.status= status
                self.run= run
        def __str__(self):
                return "start: {} \nend: {}\nType:{}\n".format(self.start, self.end, self.type )

rectheight = 0
rowcount= 0
c = open(sys.argv[1], 'r')
rowcount = sum(1 for row in c)
rowcount -= 1
csvFile1 = open(sys.argv[1]) 
#rectheight = 120000/rowcount
rectheight = 20000
rectindex = 0
color= "blue"
reader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')
tasks = []
for row in reader1:
    if len(row)>2:
        if row[1]=="start":
            continue
        tasks.append(task(row[0],row[1], row[2], row[3], row[4], 1))
if len(sys.argv )>2:
    csvFile2 = open(sys.argv[2]) 
    reader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')
    for row in reader2:
        if len(row)>2:
            if row[1]=="start":
                continue
            tasks.append(task(row[0],row[1], row[2], row[3], row[4], 2))

sortedtasks = sorted(tasks, key=lambda x: float(x.start))

bars=[bar(0)]
for t in sortedtasks:
    currbar = None
    for b in bars:
        if b.is_empty(t.start):
            currbar = b.set_task(t.start,t.end)
            break
    if currbar is None:
        bars.append(bar(len(bars)))
        currbar = bars[len(bars)-1].set_task(t.start, t.end)

rectheight=10.0/len(bars)
nbbars=len(bars)
bars = []
for i in range(0,nbbars):
    bars.append(bar(i))

for t in sortedtasks:
    if t.run == 1:
        if t.type == 'r':
            color="red"
        else:
            color="orange"
    else:
        if t.type == 'r':
            color="blue"
        else:
            color="purple"
    currbar = None
    for b in bars:
        if b.is_empty(t.start):
            currbar = b.set_task(t.start, t.end)
            break
    fillstyle=0
    if(t.status == "0"): 
        fillstyle = "pattern 1"
    else: #Succeed
        fillstyle = "solid" 
    print("set object rectangle from {},{} to {},{}  fs {} fc rgb \"{}\" behind".format(t.start, currbar*rectheight, t.end, currbar*rectheight + rectheight,fillstyle, color))


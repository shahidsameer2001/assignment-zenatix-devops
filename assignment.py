import datetime
import time
import subprocess
from datetime import datetime, time, date
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time
es = Elasticsearch('localhost:9200')

cmd = "ps -eo pid,%mem,%cpu"
indexname = "os-stat-data"
indexname2 = "os-stat-system-data"

pid = int(input("enter the processID: "))


def warn(pid, memory, cpu, now):
    return {
        "timestamp": now,
        "cpu": float(cpu),
        "mem": float(memory),
        "pid": pid
    }


def monitor(line):
    sp = line.split()
    now = datetime.now()
    return warn(sp[0], sp[1], sp[2], now)


while True:

    out = subprocess.getoutput(cmd)
    lines = out.splitlines()
    cpu = 0
    memory = 0
    for x in map(monitor, out.splitlines()[1:]):
        es.index(index=indexname, body=x)
        cpu += x["cpu"]
        memory += x["mem"]
    es.index(index=indexname2, body={"memory": memory,
                                     "cpu": cpu, "timestamp": datetime.now()})

    time.sleep(1)

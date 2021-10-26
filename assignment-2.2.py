import psutil
import datetime
import time
import schedule
pid = int(input("enter the processID: "))


def warn():
    cpuusage = psutil.cpu_percent(interval=1)
    if cpuusage > 50:
        print("Cpu usage is 40%", cpuusage)
    memusage = psutil.virtual_memory().percent
    if memusage > 50:
        print("memory utilization is above 40%", memusage)


def monitor():
    time = datetime.datetime.now().strftime("%Y%m%d - %H:%M:%S")
    p = psutil.Process(pid)
    cpu = p.cpu_percent(interval=1)/psutil.cpu_count()
    memory_mb = p.memory_full_info().rss / (1024*1024)
    memory = p.memory_percent()


schedule.every(1).second.do(warn)
schedule.every(5).seconds.do(monitor)
while True:
    schedule.run_pending()
    time.sleep(1)

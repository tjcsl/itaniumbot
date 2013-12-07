import os
def run():
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    return "%d processes" % len(pids)

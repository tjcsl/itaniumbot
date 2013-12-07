import os

def run():
    return "Load averages: %s, %s, %s" % os.getloadavg()

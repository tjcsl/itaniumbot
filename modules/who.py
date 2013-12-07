import subprocess
def run():
    	who = subprocess.check_output("who").split('\n')
	return "%d logged in users" % len(who)

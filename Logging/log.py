#####################################################
# Created by: nlickey
# 10/28/2015
# Created to make a log file for other scripts
#####################################################

import time

def startlog():
    with open("c:\system_monitoring.log","a") as log:
        # Get current time and log script start
        now = time.strftime("%c")
        print ("Script started: %s" % now)
        log.write ("Script started: %s" % now + "\n")
def endlog():
    with open("c:\system_monitoring.log","a") as log:
        # Get current time and log script start
        now = time.strftime("%c")
        print ("Script completed: %s" % now)
        log.write ("Script completed: %s" % now + "\n")

startlog()
endlog()

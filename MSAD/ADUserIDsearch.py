#!/bin/env python -tt
#######################################################################
# Search AD to see if UID matches any others in Microsoft AD
#
# Helpful video:  https://www.youtube.com/watch?v=fhQE342ZTrk
#
# Created by: J.Lickey
# 20220317
#######################################################################

# How to connect to AD from a machine that is not a member of the domain
from ldap3 import Connection,Server
import ADenv,ADip
import subprocess,argparse,sys,os

def uidsearch(uid2search):
    # Variables
    entry_lst = []
    uid_lst = []

    # Sets up SSL connection to AD Server
    server = Server(ADip.ip, use_ssl=True)

    # Sets up actual connection to AD Server, passing in user and credentials
    con = Connection(server, ADenv.admin_user + "@" + ADenv.domain, ADenv.passwd, auto_bind=True)

    # Search AD and pull out user ID if it exists
    con.search("DC=ad,DC=example,DC=com","(uid={})".format(uid2search), attributes=['uid','gecos'])
    uid_list = con.entries
    con.unbind()
    
    for entry in uid_list:
        entry_lst.append(str(entry).split())
    
    # Check to see if entry_lst is empty
    if len(entry_lst) == 0:
        return False
    else:
        for uid in entry_lst:
            if uid[-1] == uid2search:
                gecos = ' '.join(uid[11:13])
                userid = uid[-1]
                return True, gecos, userid


if __name__ == "__main__":
    uid2search = ''
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user_id", help="Enter user ID to search on", type=str)
    args = parser.parse_args()
    try:
        uid2search = str(sys.argv[2])
        print(uidsearch(uid2search))
    except Exception as Err:
        cmd = 'python ADUserIDsearch.py -h'
        output = subprocess.getoutput(cmd)
        print(output)

#!/bin/env python -tt
#################################################################
#
# Created to search for a single user from Active Directory
#
# Created by: Jon Lickey
# 20220318
#
#################################################################
from ldap3 import Connection,Server,ALL_ATTRIBUTES,ALL_OPERATIONAL_ATTRIBUTES,ALL
import ADenv,ADip
import argparse,subprocess,sys,os

def usersearch(userid):
    # Sets up SSL connection to AD Server
    server = Server(ADip.ip, use_ssl=True)

    # Sets up actual connection to AD Server, passing in user and credentials
    con = Connection(server, ADenv.admin_user + "@" + ADenv.domain, ADenv.admin_passwd, auto_bind=True)

    # Search AD and pull out all users with uidNumber set
    con.search("DC=ad,DC=example,DC=com","(&(objectcategory=person)(cn={}))".format(str(userid)), attributes=[ALL_ATTRIBUTES,ALL_OPERATIONAL_ATTRIBUTES])

    # Prints AD Entries found by search
    print(con.entries)
    con.unbind()

if __name__ == "__main__":
    try:
        userid = ''
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--userid", help="Enter the users login ID or username", type=str)
        args = parser.parse_args()
        userid = str(sys.argv[2])
        usersearch(userid)
    except Exception as Err:
        cmd = 'python ADpasswdReset.py -h'
        output = subprocess.getoutput(cmd)
        print(output)


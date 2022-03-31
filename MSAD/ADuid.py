#!/bin/env python -tt
#######################################################################
# Find next available uidNumber in MS AD
#
# Helpful video:  https://www.youtube.com/watch?v=fhQE342ZTrk
#
# Created by: J.Lickey
# 20220315
#######################################################################

# How to connect to AD from a machine that is not a member of the domain
from ldap3 import Connection,Server
import ADenv
import ADip

# Variables
entry_lst = []
uid_lst = []

# Sets up SSL connection to AD Server
server = Server(ADip.ip, use_ssl=True)

# Sets up actual connection to AD Server, passing in user and credentials
con = Connection(server, ADenv.admin_user + "@" + ADenv.domain, ADenv.passwd, auto_bind=True)

# Search AD and pull out all users with uidNumber set
#con.search("DC=ad,DC=cll,DC=cloud","(&(uid=jlickey)(uidNumber=*))", attributes=['sn', 'uidNumber', 'objectclass'])
con.search("DC=ad,DC=cll,DC=cloud","(uidNumber=*)", attributes=['uidNumber'])
uid_list = con.entries

for entry in uid_list:
    entry_lst.append(str(entry).split())

for item in entry_lst:
    uid_lst.append(item[-1])

current_uid = sorted(uid_lst)[-1]
next_available_uid = int(sorted(uid_lst)[-1]) + 1
#print(f"The current uid: {current_uid}\nNext available uid: {next_available_uid}")
# Prints AD Entries found by search
#print(con.entries)
con.unbind()

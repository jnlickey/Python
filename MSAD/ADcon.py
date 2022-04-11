#!/bin/env python -tt
#######################################################################
# Connect LDAP Server (Microsoft AD)
#
# Helpful video:  https://www.youtube.com/watch?v=fhQE342ZTrk
#
# Created by: J.Lickey
# 20220315
#######################################################################

# How to connect to AD from a machine that is not a member of the domain
from ldap3 import Connection,Server
import ADip
import ADenv

# Sets up SSL connection to AD Server
server = Server(ADip.ip,use_ssl=True)

# Sets up actual connection to AD Server, passing in user and credentials
con = Connection(server, ADenv.admin_user + "@" + ADenv.domain, ADenv.admin_passwd, auto_bind=True)

# See who we are connected as
#print(con.extend.standard.who_am_i())
# Prints AD Entries found by search
#print(con.entries)

# Search AD and see all AD users
#  con.search("AD Distinguished Name","(Search criteria)") 
#con.search("DC=ad,DC=example,DC=com","(cn=*)")

# Search AD and pull out all users with uidNumber set
#con.search("DC=ad,DC=example,DC=com","(&(uid=myuserid)(uidNumber=*))", attributes=['sn', 'uidNumber', 'objectclass'])
#con.search("DC=ad,DC=example,DC=com","(uidNumber=*)", attributes=['uidNumber'])




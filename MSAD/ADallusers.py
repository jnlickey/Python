#!/bin/env python -tt
#################################################################
#
# Created to list all users from Active Directory
#
# Created by: Jon Lickey
# 20220316
#
#################################################################
from ldap3 import Connection,Server,ALL_ATTRIBUTES,ALL_OPERATIONAL_ATTRIBUTES,ALL
import ADenv
import ADip

# Sets up SSL connection to AD Server
server = Server(ADip.ip, use_ssl=True)

# Sets up actual connection to AD Server, passing in user and credentials
con = Connection(server, ADenv.admin_user + "@" + ADenv.domain, ADenv.admin_passwd, auto_bind=True)

# Search AD and pull out all users with uidNumber set
#con.search("DC=ad,DC=example,DC=com","(&(uid=<myloginid>)(uidNumber=*))", attributes=['sn', 'uidNumber', 'objectclass'])
con.search("DC=ad,DC=example,DC=com","(objectcategory=person)", attributes=[ALL_ATTRIBUTES,ALL_OPERATIONAL_ATTRIBUTES])

# Prints AD Entries found by search
print(con.entries)
con.unbind()

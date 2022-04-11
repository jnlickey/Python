#!/bin/env python -tt
#############################################################################################
#
# This script was created in order to reset users passwords in MS Active Directory, while
# randomly generating a password, and setting the "User MUST change password at next logon" 
# field.
#
# Created by: J.Lickey
# 20220331 
#
#############################################################################################
import ADenv,ADip,ADgenpasswd
import subprocess,argparse,sys,os
from ldap3 import Connection,Server,ALL_ATTRIBUTES,ALL_OPERATIONAL_ATTRIBUTES,ALL,MODIFY_REPLACE,ASYNC_STREAM

def resetpwd(userid):
    info_lst = []
    msg_lst = []
    
    if userid == "":
        userid = input("Username to reset password for: ")

    # Generate new random password
    new_passwd = ADgenpasswd.genpwd(10)

    # Sets up SSL connection to AD Server
    # ADip.ip - Grabs MS AD Server ip
    # use_ssl - Forces use of SSL
    server = Server(ADip.ip, use_ssl=True)

    # Open a connection to the MS AD server
    admin_user = str(ADenv.admin_user) + "@" + str(ADenv.domain)
    admin_passwd = ADenv.admin_passwd
    con = Connection(server, user='{}'.format(admin_user), password='{}'.format(admin_passwd), auto_bind=True)

    # Search for user in AD
    con.search("{}".format(ADenv.base_dn), "(&(objectcategory=person)(cn={}))".format(str(userid)), attributes=['distinguishedName'])

    # Get users DN from search
    for entry in con.entries:
        user_info = str(entry).strip('\n')
        info_lst.append(user_info.split(" "))
    user_dn = info_lst[0][-1]

    # Modify users password
    con.extend.microsoft.modify_password(user_dn, new_password='{}'.format(new_passwd), old_password=None)
    password_expire = {"pwdLastSet": (MODIFY_REPLACE, [0])}
    con.modify(user_dn, changes=password_expire)
    for item in list(con.result.values()):
        msg_lst.append(str(item))
    print(f"{msg_lst[1]}")
    print("User:  {}\nNew password:  {}".format(user_dn,new_passwd))
    con.unbind()

if __name__ == "__main__":
    try:
        userid = ''
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--userid", help="Enter the users login ID or username", type=str)
        args = parser.parse_args()
        userid = str(sys.argv[2])
        resetpwd(userid)
    except Exception as Err:
        cmd = 'python ADpasswdReset.py -h'
        output = subprocess.getoutput(cmd)
        print(output)

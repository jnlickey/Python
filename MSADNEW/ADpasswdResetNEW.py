#!/bin/env python -tt
#############################################################################################
#
# This script was created in order to reset users passwords in MS Active Directory, while
# randomly generating a password, and setting the "User MUST change password at next logon" 
# field.
#
# Created by: J.Lickey
# 20220331 
# Modified: 20220407
#
#############################################################################################
import ADenv
import subprocess,argparse,sys,os,random
from ldap3 import Connection,Server,ALL_ATTRIBUTES,ALL_OPERATIONAL_ATTRIBUTES,ALL,MODIFY_REPLACE,ASYNC_STREAM

def ADgenpasswd(length):
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    num = ['1','2','3','4','5','6','7','8','9','0']
    spc = ['`','`','!','@','#','$','%','^','&','*','(',')','_','+','-','=','{','}','|','[',']','\\',';','\'',':','"',',','.','/','<','>','?']
    L = 0
    p = []
    passwd = []

    while L <= length:
        randnum = random.randrange(1, 5)
        if ( randnum == 1):
            p = str(random.choice(alpha)) 
        elif ( randnum == 2):
            p = str(random.choice(num))
        elif ( randnum == 3):
            p = str(random.choice(spc))
        else:
            p = str(random.choice(alpha)).lower()
            #p = p.lower()
        passwd.append(p)
        L = L + 1
    return ''.join(passwd)

def ADip():
    ip_lst = []

    for ips in ADenv.ip.split(','):
        ip_lst.append(ips)

    ip = random.choice(ip_lst)
    return ip
    
def resetpwd(userid):
    info_lst = []
    msg_lst = []
    
    if userid == "":
        userid = input("Username to reset password for: ")

    # Generate new random password
    new_passwd = ADgenpasswd(10)

    # Sets up SSL connection to AD Server
    # ADip.ip - Grabs MS AD Server ip
    # use_ssl - Forces use of SSL
    server = Server(ADip(), use_ssl=True)

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

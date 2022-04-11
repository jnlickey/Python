#!/bin/env python -tt
################################################################
#
# Created to add a user to Microsoft AD
#
# Created by: Jon Lickey
# 20220316
#
################################################################
import ADcon,ADenv,ADip,ADuid,ADgenpasswd,ADUserIDsearch
import datetime,subprocess,sys

def create_user(username,display_name,uid_Number,disabled,gecos,uHomeDir,passwd):
    '''
    Create New User in Microsoft AD
    :param username
    :param gecos (First and Last Name)
    :param display_name (same as gecos)
    :param uHomeDir (Linux Home Directory)
    :param passwd (Randomly generated password)
    :param uid_Number (for Linux)
    :param active
    '''

    description = "User added via AD Python BOT".format(datetime.datetime.now())
    dn = '"CN={},OU=NEW_OU_FOR_USERS,DC=ad,DC=example,DC=com"'.format(username,users_ou)
    groups = 'cn=vpn-users,{}'.format(groups_ou)

    command = 'dsadd user'\
                '{} '\
                '-samid "{}" '\
                '-upn "{}" '\
                '-display "{}" '\
                '-desc "{}" '\
                '-disabled "{}" '\
                '-pwd "{}" '\
                '-pwdneverexpires yes '\
                '-mustchpwd yes '\
                '-memberof "{}" '\
                '-acctexpires never '\
                '-uidNumber "{}" '\
                '-loginShell /bin/bash '\
                '-gecos "{}" '\
                '-unixHomeDirectory "{}" '\
                ''.format(dn, username, username, display_name, description, disabled, passwd, groups, uid_Number, gecos, uHomeDir)
    print(command)
    ans = input("Do you want to commit this account to M$ AD (Y|N): ")
    if ans == "Y" or ans == "y" or ans == "YES" or ans == "yes" or ans == "Yes":
        send_command(command)
    else:
        exit()

def send_command(command):
    try:
        connection = ADcon.con
        connection.run_command(command)
    except Exception as Err:
        print('Error in send command',str(Err))

def UserIDSearch(userid,Fname,Lname):
    UIDSearch = []
    IDSearch = []
   
    count = 2
    for info in userid,Fname,Lname: 
        IDSearch.append(str(info))
   
    if ADUserIDsearch.uidsearch(userid) != False: 
        for entry in ADUserIDsearch.uidsearch(userid):
            UIDSearch.append(str(entry))
    
        if UIDSearch != False:
            print(f"{UIDSearch[2]} currently exists for {UIDSearch[1]}.")
            ans = input("Do you want to create a new username (Y|N): ")
            if ans == "Y" or ans == "y" or ans == "YES" or ans == "yes" or ans == "Yes":
                Lname = IDSearch[2]
                Fname = IDSearch[1]
                last = int(len(Lname) - 1)
                userid = str(Fname[:count]) + str(Lname[:last])
                UserIDSearch(userid,Fname,Lname)
                count += 1
    
    Fname = Fname.replace(Fname[0],Fname[0].upper())
    Lname = Lname.replace(Lname[0],Lname[0].upper())
    
    name = str(Fname) + " " + str(Lname)
    return userid,name

if __name__ == "__main__":
    domain_controller = 'DC=ad,DC=example,DC=com'
    users_ou = 'OU=NEW_OU_FOR_USERS,{}'.format(domain_controller)
    groups_ou = 'OU=Groups,OU=NEW_OU_FOR_USERS,{}'.format(domain_controller)
    pwd_length = 10
    name = []

    passwd = ADgenpasswd.genpwd(pwd_length)
    gecos = input("Enter new First and Last name (seperated by space): ")
    displayed_name = gecos
    name = gecos.lower().split(" ")
    Fname = name[0]
    Lname = name[1]
    userid = Fname[0] + Lname
    userinfo = UserIDSearch(userid,Fname,Lname)
    username = userinfo[0]
    display_name = userinfo[1]
    uHomeDir = "/home/" + userid
    active = input("Disable new user account (Y|N): ")
    if active == "Y" or active == "YES" or active == "yes" or active == "Yes":
        disabled = "yes"
    else:
        disabled = "no"
    uid_Number = ADuid.next_available_uid

    create_user(username,display_name,uid_Number,disabled,gecos,uHomeDir,passwd)

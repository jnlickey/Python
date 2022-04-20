#!/bin/env python -tt
################################################################
#
# Created to add a user to Microsoft AD
#
# Created by: Jon Lickey
# 20220316
#
################################################################
import ADenv,ADUserIDsearch,ADip
import datetime,subprocess,sys,random,argparse
from ldap3 import Connection,Server,MODIFY_REPLACE,SUBTREE,ALL_ATTRIBUTES

def ADCON():
    # Sets up SSL connection to AD Server
    server = Server(ADip.ip, use_ssl=True)

    # Sets up actual connection to AD Server, passing in user and credentials
    con = Connection(server, ADenv.admin_user + "@" + ADenv.domain, ADenv.admin_passwd, auto_bind=True)
    return con

def ADuid(con):
    # Variables
    entry_lst = []
    uid_lst = []

    # Search AD and pull out all users with uidNumber set
    #con.search(ADenv.base_dn, "(&(uid=<myuserid>)(uidNumber=*))", attributes=['sn', 'uidNumber', 'objectclass'])
    con.search(ADenv.base_dn, "(uidNumber=*)", attributes=['uidNumber'])
    uid_list = con.entries

    for entry in uid_list:
        entry_lst.append(str(entry).split())

    for item in entry_lst:
        uid_lst.append(item[-1])

    #current_uid = sorted(uid_lst)[-1]
    next_available_uid = int(sorted(uid_lst)[-1]) + 1
    return next_available_uid

def ADgenpasswd(pwd_length):
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    num = ['1','2','3','4','5','6','7','8','9','0']
    spc = ['`','`','!','@','#','$','%','^','&','*','(',')','_','+','-','=','{','}','|','[',']','\\',';','\'',':','"',',','.','/','<','>','?']
    L = 0
    p = []
    passwd = []

    while L <= pwd_length:
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

def create_user(con,username,display_name,uid_Number,disabled,gecos,uHomeDir,passwd):
    gidNumber = ADenv.default_gidNumber
    loginShell = ADenv.loginShell
    givenname = display_name.split()[0]
    surname = display_name.split()[1]
    email = '{}@{}'.format(username,ADenv.email_domain)
    upn = '{}@{}'.format(username,ADenv.domain)
    users_ou = '{}'.format(ADenv.users_ou)
    description = 'User added via AD Python Script'.format(datetime.datetime.now())
    dn = 'CN={},{}'.format(username,ADenv.users_ou)
    groups = '{}'.format(ADenv.groups_ou)
    OBJECT_CLASS = ['top', 'person', 'organizationalPerson', 'user']
    attributes = {
    'Name': username,\
    'description': description,\
    'userPrincipalName': upn,\
    'sAMAccountName': username,\
    'sn': surname,\
    'givenName': givenname,\
    'displayName': display_name,\
    'mail': email,\
    'uid': username,\
    'uidNumber': '{}'.format(uid_Number),\
    'loginShell': loginShell,\
    'gecos': display_name,\
    'gidNumber': gidNumber,\
    'unixHomeDirectory': uHomeDir
    }
   
    try:
        con.add(dn, OBJECT_CLASS, attributes)
        # Unlock and set password
        con.extend.microsoft.unlock_account(user=dn)
        con.extend.microsoft.modify_password(user=dn, new_password="{}".format(passwd), old_password=None)

        # Enable account - must happen after password has been set
        enable_account = {"userAccountControl": (MODIFY_REPLACE, [512])}
        con.modify(dn, changes=enable_account)

        # Add to vpn group
        con.extend.microsoft.add_members_to_groups([dn], groups)

        # Force Password reset
        force_passwd_reset = {"pwdLastSet": (MODIFY_REPLACE, [0])}
        con.modify(dn, changes=force_passwd_reset)
        
        # Prints Success if user was added 
        results = con.result
        print(results.get('description'))

    except Exception as Err:
        print('Adding user {} failed.'.format(username))
        print(Err) 


def UserIDSearch(con,userid,Fname,Lname):
    UIDSearch = []
    IDSearch = []
   
    count = 2
    for info in userid,Fname,Lname: 
        IDSearch.append(str(info))
   
    if ADUserIDsearch.uidsearch(userid) != False: 
        for entry in ADUserIDsearch(con,userid):
            UIDSearch.append(str(entry))
    
        if UIDSearch != False:
            print(f"{UIDSearch[2]} currently exists for {UIDSearch[1]}.")
            print("Creating new userid...")
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

#================  MAIN SCRIPT  ================
if __name__ == "__main__":
    name = []
    pwd_length = ADenv.passwd_length
    passwd = ADgenpasswd(pwd_length)
    domain_controller = ADenv.base_dn
    users_ou = ADenv.users_ou
    groups_ou = ADenv.groups_ou
    gecos = ''
    disabled = ADenv.disabled
    try: 
        if gecos == '':
            parser = argparse.ArgumentParser()
            parser.add_argument("-g", "--gecos", nargs='+', help="Enter the users First and Last Name (e.g. John Doe)", type=str)
            args = parser.parse_args()
            gecos_name = str(' '.join(args.gecos))
            gecos = f'{gecos_name}'
        else:
            gecos = input("Enter new First and Last name (seperated by space): ")
# For troubleshooting name (gecos)
#        print(gecos)
        con = ADCON()
        displayed_name = gecos
        name = gecos.lower().split(" ")
        Fname = name[0]
        Lname = name[1]
        userid = Fname[0] + Lname
        userinfo = UserIDSearch(con,userid,Fname,Lname)
        username = userinfo[0]
        display_name = userinfo[1]
        uHomeDir = "/home/" + userid
        uid_Number = ADuid(con)
        create_user(con,username,display_name,uid_Number,disabled,gecos,uHomeDir,passwd)
        con.unbind()
        print(f'New user account for: {userid}\nTemporary password: {passwd}')
    except Exception as Err:
        cmd = 'python ADadduser.py -h'
        output = subprocess.getoutput(cmd)
        print(output)
        print('\n')
        # For troubleshooting errors
        #print(Err)

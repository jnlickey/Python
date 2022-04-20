############################################################
#
# This file holds variables to be used in other Python
# scripts.
#
# Created by: J.Lickey
# 20220410
#
############################################################
# Multiple AD Server IP addresses must be comma seperated
ip = "192.168.50.53,192,168.40.53"
domain = "ad.example.com"
base_dn = "DC=ad,DC=example,DC=com" 
admin_user = "admin_4_adding_accts"
admin_passwd = "SomeR34lly$tr@n63P@55w0rd"
loginShell = "/bin/bash"
email_domain = "example.com"
users_ou = 'OU=My_Users,DC=ad,DC=example,DC=com'
groups_ou = 'CN=myusergroup,OU=Groups,OU=My_Users,DC=ad,DC=example,DC=com'
default_gidNumber = '5001'
disabled = "no"
passwd_length = 12

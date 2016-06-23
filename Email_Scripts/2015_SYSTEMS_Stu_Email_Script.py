#!/usr/bin/python -tt
# Creates email list of System's Students that can
# be imported into ldap as an ldif file.
# Original file format:
# "LastName, FirstName",@00123456,Junior,Systems Engineering,email@example.com,"City, State",,
#
# LDIF file format:
# rfc822MailMember: "Lname, Fname (Systems)" <Fname_Lname@example.com>
#
# nlickey 20150925

import csv, sys, os
import operator

# Opens a file for reading
inFile = open("201590 Systems.csv",'r+')
outFile = open("SYSTEM_STUDENTS.CSV",'w')

outFile.write('dn: cn=all_sys, ou=Aliases, dc=cse,dc=example,dc=com\n')
print('dn: cn=all_sys, ou=Aliases, dc=cse,dc=example,dc=com')

# Loops through individual lines within the CSV file
for row in inFile:
    if row.startswith("@"):
        row = row.replace(" ","").replace("\"","") 
        row = row.strip()
        row = row.split(",")
        Lname = row[1]
        Fname = row[2]
        email = row[14]+"@example.com"

        ## Writes output to console and to a file in
        ## the format that an LDIF file will need
        ## for importing email addresses into ldap.
        outFile.write('rfc822MailMember: \"'+Lname+', '+Fname+' (Systems)" '+'<' + email + '>\n')
        print('rfc822MailMember: \"'+ Lname +', '+ Fname + ' (Systems)" '+'<' + email + '>')

outFile.write('objectClass: nisMailAlias\nobjectClass: top\ncn: all_sys')
print('objectClass: nisMailAlias\nobjectClass: top\ncn: all_sys')

inFile.close()
outFile.close()

# Renames the output file so that it is ready to import to LDAP
os.rename("SYSTEM_STUDENTS.CSV","SYSTEM_STUDENTS.ldif")

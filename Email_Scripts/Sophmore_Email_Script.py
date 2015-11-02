#!/usr/bin/python -tt
# Creates email list of Sophmore's that can
# be imported into ldap as an ldif file.
# Original file format:
# email_address@somewhere.com
#
# LDIF file format:
# rfc822MailMember: "Lname, Fname (Systems)" <Fname_Lname@example.com>
#
# nlickey 20141106

import csv, sys
import operator

# Opens a file for reading
inFile = open("sophmore.CSV",'r+')
outFile = open("SOPHMORE_STUDENTS.csv",'r+')

#listIDs = []

outFile.write('dn: cn=so_cos, ou=Aliases, dc=cse,dc=example,dc=com\n')
# Loops through individual lines within the CSV file, finding all email
# addresses and splits them into first and last name. Then creates the
# sends the output to a CSV file in ldif format. To upload the file to
# ldap, just rename the SOPHMORE_STUDENTS.csv to SOPHMORE_STUDENTS.ldif
for row in inFile:
    row = row.strip()
    email = row
    row = row.split('@')
    row = row[0].split("_")
    Lname = row[1]
    Fname = row[0]
    # print (Lname + ", " + Fname + " " + email)
    # Writes output to console and to a file in
    # the format that an LDIF file will need
    # for importing email addresses into a group.
    print('rfc822MailMember: \"'+Lname+', '+Fname+' (Computer Science)" '+ email)
    outFile.write('rfc822MailMember: \"'+Lname+', '+Fname+' (Computer Science)" '+ email +'\n')
outFile.write('objectClass: nisMailAlias\nobjectClass: top\ncn: so_cos')
inFile.close()
outFile.close()

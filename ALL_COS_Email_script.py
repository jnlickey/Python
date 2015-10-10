#!/usr/bin/python -tt
# Creates email list of ALL COS students that can
# be imported into ldap as an ldif file.
# Original file format:
# email_address@somewhere.com
#
# LDIF file format:
# rfc822MailMember: "Lname, Fname (Systems)" <Fname_Lname@example.com>
#
# nlickey 20141106

import csv, sys, os
import operator, shutil

# Opens a file for reading
inFile = open("ALL_COS.CSV",'r+')
outFile = open("ALL_COS_STUDENTS.csv",'w')

outFile.write('dn: cn=all_cos_major, ou=Aliases, dc=example,dc=com\n')
print('dn: cn=all_cos_major, ou=Aliases, dc=example, dc=com\n')
# Loops through individual lines within the CSV file, finding all email
# addresses and splits them into first and last name. Then creates the
# sends the output to a CSV file in ldif format. To upload the file to
# ldap, just rename the .csv to .ldif
for row in inFile:
    row = row.strip()
    email = row
    row = row.split('@')
    row = row[0].split("_")
    Lname = row[1]
    Fname = row[0]
    #print (Lname + ", " + Fname + " " + email)
    # Writes output to console and to a file in
    # the format that an LDIF file will need
    # for importing email addresses into a group.
    print('rfc822MailMember: \"'+Lname+', '+Fname+' (Computer Science)" '+ '<'+email+'>')
    outFile.write('rfc822MailMember: \"'+Lname+', '+Fname+' (Computer Science)' + '<' + email + '>\n')
outFile.write('objectClass: nisMailAlias\nobjectClass: top\ncn: all_cos_major')
print('objectClass: nisMailAlias\nobjectClass: top\ncn: all_cos_major')

inFile.close()
outFile.close()

os.rename("ALL_COS_STUDENTS.csv","ALL_COS_STUDENTS.ldif")

#!/usr/bin/python -tt
# Creates email list of ALUMNI Students that can be imported to ldap as an
# ldif file.
# Original file format:
# Last_Name,stu_id,Maiden_Name,First,Spouse,Internships_jobs,employer_seeking,Major_Degree,Class_of,Master_or_Phd,Grad_School,Company,Occupation,Address,City,State,Zip,Email1,Phone,HOME_Address,City,State,Zip,Email2,Phone,Last_Updated,Career_Fair,Speak_in_Class,Poster_Judge,NOTE,,,,,,,,,,,,
#
# LDIF file format:
# rfc822MailMember: "Lname, Fname (Maiden_Name)" <email_address>
#
# nlickey 20150318

import csv, sys
import operator

# Opens a file for reading
inFile = open("Alumni_spreadsheet.csv",'r+')
outFile = open("Pre_ALMUNI_STUDENTS.CSV",'r+')
ldifFile = open("ALMUNI_STUDENTS.ldif",'w+')

listEmails = []

# Loops through individual lines within the CSV file, parsing through them to
# create an email list in LDIF format.
for row in inFile:
    if '@' in row:
        row = row.strip()
        row = row.replace('",','')
        row = row.replace(',"','')
        row = row.replace('","','')
        alumni = row.split(',')
        if '@' in (alumni[17] or alumni[24]): 
            Last_Name = alumni[0]
            Maiden_Name = alumni[2]
            First_Name = alumni[3]
            Email1 = alumni[17]
            Email2 = alumni[24]

            if Maiden_Name is '':
                if '@' in Email1:
                    listEmails.append(Email1)
                    print('rfc822MailMember: \"'+Last_Name+', '+First_Name+'" '+'<'+Email1+'>')
                    outFile.write('rfc822MailMember: \"'+Last_Name+', '+First_Name+'" '+'<'+Email1+'>\n')
                if '@' in Email2:
                    listEmails.append(Email2)
                    print('rfc822MailMember: \"'+Last_Name+', '+First_Name+'" '+'<'+Email2+'>')
                    outFile.write('rfc822MailMember: \"'+Last_Name+', '+First_Name+'" '+'<'+Email2+'>\n')
            
            else:
                if '@' in Email1:
                    listEmails.append(Email1)
                    print('rfc822MailMember: \"'+Last_Name+', '+First_Name+' ('+Maiden_Name+')" '+'<'+Email1+'>')
                    outFile.write('rfc822MailMember: \"'+Last_Name+', '+First_Name+' ('+Maiden_Name+')" '+'<'+Email1+'>\n')
                if '@' in Email2:
                    listEmails.append(Email2)
                    print('rfc822MailMember: \"'+Last_Name+', '+First_Name+' ('+Maiden_Name+')" '+'<'+Email2+'>')
                    outFile.write('rfc822MailMember: \"'+Last_Name+', '+First_Name+' ('+Maiden_Name+')" '+'<'+Email2+'>\n')

print("dn: cn=all_cos_alumni, ou=Aliases, dc=example,dc=com")
print("rfc822MailMember: dept")
ldifFile.write("dn: cn=all_cos_alumni, ou=Aliases,dc=example,dc=com\n")
ldifFile.write("rfc822MailMember: dept\n")
for line in outFile:
    line = line.replace('""','"')
    print(line)
    ldifFile.write(line)
ldifFile.write("objectClass: nisMailAlias\n")
ldifFile.write("objectClass: top\n")
ldifFile.write("cn: all_cos_alumni\n")
print("objectClass: nisMailAlias")
print("objectClass: top")
print("cn: all_cos_alumni")  

    

inFile.close()
outFile.close()

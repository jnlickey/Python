<H3>MS AD Password Reset Scripts</H3>
---
Modify the BASH script to point to the location where you have saved the python virtual environment.
<br>



<H4>Notes for Python Scripts</H4>
---
Install LDAP3 - pip3 install ldap3

Per StackOverflow - https://stackoverflow.com/questions/38164544/unable-to-change-users-password-via-ldap3-python3
Use the following for password reset instead of con.modify()
con.extend.microsoft.modify_password(user, new_password)

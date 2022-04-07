<H3>MS AD Password Reset Scripts</H3>

---

Download the entire repo named MSADNEW and save this under your home directory (/home/\<your account\>) on a Linux host.
If it is not saved to this location you will need to modify the BASH script to point to that location where you have saved the python virtual environment.
<br>
To reset a users password in Microsoft AD just run the following:

./ADPasswdReset.sh \<userid\>
<br>
<br>
<br>


<H4>Notes for Python Scripts</H4>

---

Install LDAP3 - pip3 install ldap3

Per StackOverflow - https://stackoverflow.com/questions/38164544/unable-to-change-users-password-via-ldap3-python3
Use the following for password reset instead of con.modify()
con.extend.microsoft.modify_password(user, new_password)

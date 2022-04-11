#!/usr/bin/python3 -tt
import subprocess
import pexpect

child = pexpect.spawn ('realm join -U Administrator ad.example.com --computer-name="SERVER01" --os-name="Ubuntu" --os-version="Ubuntu 20.04.3 LTS" --computer-ou="CN=Computers,DC=ad,DC=example,DC=com" --automatic-id-mapping=no')
child.expect ('Password for Administrator:')
child.sendline ("<passwd_removed>")
child.expect(pexpect.EOF)
print('Joining ad.example.com domain')

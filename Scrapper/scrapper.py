#!/bin/env python -tt
import config
import urllib.request

user = config.user
passwd = config.passwd

url = 'http://someURL'

with urllib.request.urlopen(url) as response:
    html = response.read()

#headers = urllib3.make_headers(basic_auth='{user}:{passwd}')
#r = urllib3.request('GET', url, headers=headers)
#page = urlopen(r)
#print(page)



#url = "http://someURL"
#http = urllib3.PoolManager()
#headers = urllib3.make_headers(basic_auth='{user}:{passwd}')
#r = http.request('GET', url, headers=headers)
#page = urlopen(r)

#html_bytes = page.read()
#html = html_bytes.decode("utf-8")
#print(html)

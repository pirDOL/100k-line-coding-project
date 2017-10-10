import getpass  
import requests
import json
import re

if __name__ == '__main__':
    email = raw_input('Enter e-mail: ')
    password = getpass.getpass('Enter password: ')  
    print email, password
    
    s = requests.Session()
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
    loginURL = 'http://www.renren.com/ajaxLogin/login'
    loginParams = {'email' : email, 'password' : password}
    r = s.post(loginURL, loginParams, headers=headers)
#     print(r.text)
    j = json.loads(r.text)
    if not j['code']:
        print(j['failDescription'])
        exit(-1)
    
    homeURL = 'http://www.renren.com/home'
    r = s.get(homeURL)
#     print(r.text)
    m = re.search("requestToken : '(\d+)'[^_]*_rtk : '([^']*)'", r.text)
    try:
#     	print(m.group(1), m.group(2))
        collectrpURL = 'http://renpin.renren.com/action/collectrp'
        collectrpParams = {'requestToken' : m.group(1), '_rtk' : m.group(2)}
        r = s.post(collectrpURL, collectrpParams, headers=headers)
#         print(r.text)
        j = json.loads(r.text)
        print('collectrp response: %s' % j['msg'])
        if (j['code'] == 0):
        	print('current rp: %d' % j['rp'])
    except Exception as e:
        print(e)
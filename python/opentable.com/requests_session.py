# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime, timedelta
import re
import argparse
import getpass
import time

def isValidCovers(s):
    try:
        n = int(s)
        return True if n >= 1 and n <= 20 else False
    except:
        return False
    
def isValidDate(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except:
        return False

def isValidTime(s):
    try:
        datetime.strptime(s, "%H:%M")
        return True
    except:
        return False

restaurant_profile = {'The French Laundry': '1180', 'Ad Hoc': '17617', 'Brix': '763'}

def isValidRestaurant(s):
    return s in restaurant_profile

if __name__ == '__main__':
    now = datetime.now()
    if now.minute < 30:
        dt = now + timedelta(days=30, minutes=30-now.minute)
    else:
        dt = now + timedelta(days=30, minutes=60-now.minute)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--covers", default=2, type=int, help="people(1-20)")
    parser.add_argument("-d", "--date", default=dt.strftime('%Y-%m-%d'), help="date(YYYY-MM-DD)")
    parser.add_argument("-t", "--time", default=dt.strftime('%H:%M'), help="time(HH:MM)")   
    parser.add_argument("-r", "--restaurant", default='Ad Hoc', help="restaurant name") 
    parser.add_argument("-e", "--email", default='ld_12315@sina.com', help="email address(opentable login usrname)") 
    parser.add_argument("-p", "--phone", default='222-333-4444', help="mobile phone number")
    parser.add_argument("-n", "--timeout", type=int, default=600, help="retry for [timeout]*0.1s if unavailable")
                
#     password = getpass.getpass('Enter password: ')
    password = '010791'   

    args = parser.parse_args()
#     print(args.covers, args.date, args.time, args.restaurant)
    if isValidCovers(args.covers) and isValidDate(args.date) and isValidTime(args.time) and isValidRestaurant(args.restaurant):
        s = requests.Session()
        s.headers.update({'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'})
        #必须先GET一下首页，直接GET登录页面会导致重定向到/loginpopup.aspx，但是后面登陆是POST到/loginpopup2.aspx，这是两个不同的登陆页面
        s.get('http://www.opentable.com/start/home')
        url = 'https://secure.opentable.com/loginpopup2.aspx?rp=http%3a%2f%2fwww.opentable.com%2fstart%2fhome'
        r = s.get(url, verify=False, headers={'Referer' : 'http://www.opentable.com/start/home'})
        mvs = re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]*)" />', r.text)
        mvsg = re.search(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="([^"]*)" />', r.text)
        mev = re.search(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]*)" />', r.text) 
        #没有值的参数也可以不用写到POST报文的实体中
        params = {'__VIEWSTATE' : mvs.group(1), 
                  '__VIEWSTATEGENERATOR' : mvsg.group(1), 
                  '__EVENTVALIDATION' : mev.group(1),
                  'btnMember' : 'Sign In',
                  'txtUserEmail' : args.email, 
                  'txtUserPassword' : password,
                  'txtUserPasswordPlaceholder' : '',
                  '__EVENTTARGET' : '',
                  '__EVENTARGUMENT' : '',
                  'ucSocialUserLogin$ucLoginPopupFBConnect$hfPostMessageUrl' : 'http://www.opentable.com/start/home',
                  'ucSocialUserLogin$ucLoginPopupFBConnect$hfSignInAction' : "__doPostBack('ucSocialUserLogin$ucLoginPopupFBConnect','[OtUserId],[IsCaller],1')",
                  'ucSocialUserLogin$ucLoginPopupGooglePlusSignIn$hGPlusSignInAction' : "__doPostBack('ucSocialUserLogin$ucLoginPopupGooglePlusSignIn','[OtUserId],[IsCaller],3')"}
        r = s.post(url, data=params, verify=False)
        if r.status_code != 200:
            print('Login error!')
            exit(-1)
        s.get('http://www.opentable.com/start/home', verify=False)
        
        nTimes = 0
        rid = restaurant_profile[args.restaurant]
        url = 'http://www.opentable.com/restaurant/profile/%s/search' % rid
        params = {'covers': '%d' % args.covers, 'dateTime': '%s %s' % (args.date, args.time)}
        while True:
            r = s.post(url, data=json.dumps(params), headers={'Content-Type' : 'application/json'}, verify=False)
#             print(r.text)
            m = re.search("data-datetime=\"([^\"]*)\"[^h]*hash='(\d+)'[^>]*>([^<]*)</a>", r.text)
            if not m:
                nTimes += 1
                if nTimes == 50:
                    print('auto-booking failed: 5s timeout!')
                    break
                time.sleep(0.1)
                continue
            
            try:
                dataHash = m.group(2)
                dataDatetime = m.group(1)
    #             print(dataHash, dataDatetime)
                print('auto-booking: tables found @ %s' % dataDatetime)
                
                params = {'rid' : rid, 
                          'd' : dataDatetime, 
                          'sd' : dataDatetime, 
                          'hash' : dataHash,
                          'p' : '2', 
                          'pt' : '100',
                          'pofids' : '', 
                          'ss' : '', 
                          'ra' : '', 
                          'iid' : ''}
                r = s.get('https://www.opentable.com/httphandlers/ValidateReservationRequest.ashx', params=params, verify=False)
    #             print(r.url)
    #             print(r.text)
                mvs = re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]*)" />', r.text)
                mvsg = re.search(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="([^"]*)" />', r.text)
                mev = re.search(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]*)" />', r.text) 
    #             print(mvs.group(1), mvsg.group(1), mev.group(1))
                params = {'phoneNumber' : args.phone, 
                          'countryCode$SelectDropDown' : 'US',
                          'email' : args.email, 
                          'phoneNumberKind$SelectDropDown' : '4', 
                          'completeReservation' : 'Complete Reservation',
                          '__VIEWSTATE' : mvs.group(1),
                          '__VIEWSTATEGENERATOR' : mvsg.group(1),
                          '__EVENTVALIDATION' : mev.group(1),
                          'BTQueryString' : '',
                          'BTClientErrors' : '', 
                          'phoneNumberExt' : '',
                          'specialRequests' : '',
                          'ctl13' : ''}
                r = s.post(r.url.replace('details', 'details2'), data=params, verify=False)
    #             print(r.text)
                m = re.search('<h1 id="ctl04_ReservationPageHeaderTitle" class="page-header-title">([^<]*)</h1>[^<]*<h5 id="ctl04_ReservationConfirmationNumber" class="color-light reservation-confirmation-number">([^<]*)</h5>', r.text)
                print('auto-booking succeeded: %s %s' % (m.group(1), m.group(2)))
            except Exception as e:
                print('auto-booking failed:', e)
                exit(-1)
    else:
        print('auto-booking failed:unvalid parameters!')
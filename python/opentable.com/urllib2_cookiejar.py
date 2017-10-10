# -*- coding: utf-8 -*-
import cookielib
import urllib, urllib2
import json
from datetime import datetime, timedelta
import re
import argparse
import os

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

def printCookie(cookie):
    for item in cookie:
        print('Name = %s, Value = %s' % (item.name, item.value))

def json2txt():
    try:
        with open('f:/Python/cookies.json', 'r') as jsonfile:
            cookie = json.load(jsonfile)
            with open('f:/Python/cookies.txt', 'w') as txtfile:
                for e in cookie:
                    txtfile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\r\n' % 
                            (e['domain'], 
                             'TRUE' if e['hostOnly'] else 'FALSE', 
                             e['path'], 
                             'TRUE' if e['secure'] else 'FALSE', 
                             e['expirationDate'] if 'expirationDate' in e else ' ',  
                             e['name'],
                             e['value']
                            ))
    except IOError as e:
        print('Please export cookies.json')
        exit(-1)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    if not os.path.exists('f:/Python/cookies.txt'):
        json2txt()
    
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

    args = parser.parse_args()
#     print(args.covers, args.date, args.time, args.restaurant)
    if isValidCovers(args.covers) and isValidDate(args.date) and isValidTime(args.time) and isValidRestaurant(args.restaurant):
#         cookie = cookielib.CookieJar()
#         cookie = cookielib.MozillaCookieJar('f:\Python\cookies.txt')
        cookie = cookielib.FileCookieJar('f:/Python/cookies.txt')
        
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')]
        
        rid = restaurant_profile[args.restaurant]
        url = 'http://www.opentable.com/restaurant/profile/%s/search' % rid
        params = {'covers': '%d' % args.covers, 'dateTime': '%s %s' % (args.date, args.time)}
        request = urllib2.Request(url, json.dumps(params))
        request.add_header('Content-Type', 'application/json')
        response = opener.open(request)
        html = response.read().decode('utf-8')
#         print(html)
        m = re.search("data-datetime=\"([^\"]*)\"[^h]*hash='(\d+)'[^>]*>([^<]*)</a>", html)
        try:
            dataHash = m.group(2)
            dataDatetime = m.group(1)
#             print(dataHash, dataDatetime)
            
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
            url = 'https://www.opentable.com/httphandlers/ValidateReservationRequest.ashx?%s' % urllib.urlencode(params)
#             print(url)
            response = opener.open(url.replace('+', r'%20'))
            html = response.read().decode('utf-8')
#             print(html)
            mvs = re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]*)" />', html)
            mvsg = re.search(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="([^"]*)" />', html)
            mev = re.search(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]*)" />', html) 
#             print(mvs.group(1), mvsg.group(1), mev.group(1))           
#             print(response.geturl())
            phoneNumber = '3474464578'
            countryCode = 'US'
            email = 'ld_12315@sina.com'
            params = {'phoneNumber' : phoneNumber, 
                      'countryCode$SelectDropDown' : countryCode, 
                      'email' : email, 
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
            response = opener.open(response.geturl(), urllib.urlencode(params))
            print(response.read().decode('utf-8'))
        except Exception as e:
            print(e)
    else:
        print('unvalid parameters!')
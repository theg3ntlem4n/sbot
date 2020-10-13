import requests
import time
import random
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
from termcolor import colored, cprint
import playsound
import concurrent.futures
import threading
import time
from discord_webhooks import DiscordWebhooks
from datetime import datetime, date, timedelta, timezone
import sys
import os
import json
from appdirs import *
import uuid
import ctypes
import questionary
from prompt_toolkit.styles import Style
from fake_useragent import UserAgent
import logFormats as logging


#create a fake UserAgent with a header that updates from a real life database (ie: ua.random)
ua = UserAgent()

#aesthetic
custom_style_fancy = Style([
    ('qmark', 'fg:#63fffd bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#63fffd bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#63fffd bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#63fffd bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#63fffd'),         # style for a selected item of a checkbox
    ('separator', 'fg:#63fffd'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#63fffd italic')   # disabled choices for select and checkbox prompts
])

#clear screen
def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

#global variables
global cartNumber
global paymentFraud
global possibleCheckout
cartNumber = 0
paymentFraud = 0
possibleCheckout = 0

#software information
version = '0.0.3'
ctypes.windll.kernel32.SetConsoleTitleW(f"Shoop Palace Version {version} | Carts: {cartNumber} | Payment Frauds: {paymentFraud} | Verified Checkouts: {possibleCheckout}")

state_codes = {"AL":1,"AK":2,"AZ":4,"AR":5,"CA":12,"CO":13,"CT":14,"DE":15,"DC":16,"FL":18,"GA":19,"HI":21,"ID":22,"IL":23,"IN":24,"IA":25,"KS":26,"KY":27,"LA":28,"ME":29,"MD":31,"MA":32,"MI":33,"MN":34,"MS":35,"MO":36,"MT":37,"NE":38,"NV":39,"NH":40,"NJ":41,"NM":42,"NY":43,"NC":44,"ND":45,"OH":47,"OK":48,"OR":49,"PA":51,"RI":53,"SC":54,"SD":55,"TN":56,"TX":57,"UT":58,"VT":59,"VA":61,"WA":62,"WV":63,"WI":64,"WY":65}

thread_local = threading.local()
init(convert=True)

#get settings from settings.json
def getsetting(dname):
    os.chdir(dname)
    with open('settings.json') as f:
        setting = json.load(f)
    return setting

#Eastern Standard Time return
def est():
    d2 = datetime.now(timezone.utc).strftime("%H:%M:%S")
    d3 = datetime.strptime(d2, "%H:%M:%S")
    start = d3 - timedelta(hours=4)
    hour = (start.hour)
    minute = (start.minute)
    sec = (start.second)
    if sec < 10:
        sec = '0' + str(start.second) 
    if minute < 10:
        minute = '0' + str(minute)
    if hour < 10:
        hour = '0' + str(hour)
    return (f'{hour}:{minute}:{sec}')

#more formatting with datetime
def logFormat():
    now = str(datetime.now())
    now = now.split(' ')[1]
    printFormat = '[' + str(now) + ']' + ' ' + '[Shoop Palace] '
    return printFormat

#send success message
def success(frontend, product, size, successwebhook):
    time = est()
    successwebhook.set_footer(text='Danyul#0001')
    successwebhook.set_content(title='Shoop Palace Cart',
            description=("\n" + "**Product:**" + "\n" + "> " + str(product) + "\n" + "\n"
            "**Size:**" + "\n" + "> " + str(size) + "\n" + "\n"
            "**Cookie:**" + "\n" + "> " + str(frontend) + "\n" + "\n"
            "**Timestamp:**" + "\n" + "> " + time + ' EST' "\n" + "\n"
            ),
            color=0x00FA9A)
    try:
        successwebhook.send()
    except:
        pass

#use initial request to grab HTML data from URL and find sizes
def grabURL(num, count, productLink, new_sizes, task, rotate, cookieList, dname, successwebhook, profileInput, proxy_group, sizes, proxy_type):
    s = requests.Session()
    status = 'Loading Website'
    buttonid = 'None'  
    instance = 0
    if int(task) > 60:
        randomStart = 60
    else:
        randomStart = int(task)
    time.sleep(random.randint(0, randomStart))
    setting = getsetting(dname)
    while True:
        retrydelay = 60
        rotatedelay = int(retrydelay/rotate) 
        if instance >= rotate:
            instance = 0
        proxy = count[(num + int(task)*instance)]

        if cookieList:
            cookieArray = cookieList[num].split(',')
            cfuid = (cookieArray[0])
            cfbm = (cookieArray[1])
        else: 
            pass

        #create proxy
        p = {
        'https' : proxy
        }
        s.payload = {}
        s.headers = {
        'authority': "www.shoepalace.com",
        'pragma': "no-cache",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/84.0.4147.122 Mobile/15E148 Safari/604.1",
        'accept-language': "en-US,en;q=0.9",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document"
        }
        
        try:
            response = s.get(productLink, allow_redirects = False, proxies = p)
        except:
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Proxy Error... Rotating", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            continue

        cookies = s.cookies.get_dict()

        if cookieList:
            cookies['__cfduid'] = cfuid
            cookies['__cf_bm'] = cfbm

        #print(f'First Cookies: {cookies}')
        html = (response.text)
        soup = BeautifulSoup(html, 'html.parser')
        buttons = soup.findAll('button', attrs={"data-id": True})
        checkoutDict = {}

        for button in buttons:
            checkoutDict[button.text] = button['data-id']

        #print(str(x) + ": " + soup.title.text)
        #check for errors
        if (response.status_code) == 501:
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Error 501 Backend Timeout | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif (response.status_code == 502):
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Error 502 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif (response.status_code == 403):
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Error 403 ASN Banned | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif (response.status_code == 522):
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Error 522 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif (response.status_code == 503):
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Error 522 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif (response.status_code == 429):
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Error 429 Rate Limited | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 420:
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Error 420 Calm Down | Retrying", "red"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2)))) 
        elif not buttons: 
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + "Not Released | Refreshing", "red"))
            instance +=1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        else:
            product = soup.title.text
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + f'{product} Loaded', "magenta"))
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + f'Found Sizes: {checkoutDict}', "cyan"))
            for size in new_sizes:
                #print(size)
                if size.upper() == 'RANDOM':
                    dicLength = len(checkoutDict)-1
                    x = random.randint(0, dicLength)
                    size = list(checkoutDict.keys())[x] 
                    buttonid = (checkoutDict[size])
                    break
                else:
                    if size in checkoutDict:
                        buttonid = checkoutDict[size]
                        break
                    else:
                        pass
            print(colored(logging.logFormat(profileInput, proxy_group, sizes, proxy, status) + f'Using Size: {size}', "cyan"))
            return s, buttonid, product, instance, size
        
def addToCart(num, count, productLink, new_sizes, task, rotate, cookieList, dname, successwebhook, profileInput, proxy_group, sizes, proxy_type):
    global time
    global cartNumber
    cartID = ''
    s, buttonid, product, instance, size = grabURL(num, count, productLink, new_sizes, task, rotate, cookieList, dname, successwebhook, profileInput, proxy_group, sizes, proxy_type)
    if buttonid == 'None':
        print(colored(logFormat() + "Size Not Found... Stopping", "red"))
        return 'stopped', 'stopped', 'stopped', 'stopped', 'stopped'
    status = 'ATC'
    setting = getsetting(dname)
    while True:
        retrydelay = 60
        rotatedelay = int(retrydelay/rotate)
        if instance >= rotate:
            instance = 0
        
        if cookieList:
            cookieArray = cookieList[num].split(',')
            cfuid = (cookieArray[0])
            cfbm = (cookieArray[1])
        else: 
            pass

        proxy = count[(num + int(task)*instance)]
        p = {
        'https' : proxy
        }
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        url = f"https://www.shoepalace.com/checkout/cart/add/product/{buttonid}?iCartSubmit.x={x}&iCartSubmit.y={y}"
        #print(url)
        s.payload = {}
        s.headers = {
        'authority': "www.shoepalace.com",
        'pragma': "no-cache",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/84.0.4147.122 Mobile/15E148 Safari/604.1",
        'accept-language': "en-US,en;q=0.9",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'sec-fetch-site': "same-origin" ,
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'referer': productLink
        }
        cookies = s.cookies.get_dict()
        cookies['languages'] = 'en-US,en;'
        if cookieList:
            cookies['__cfduid'] = cfuid
            cookies['__cf_bm'] = cfbm
        #print(f'Second Cookie: {cookies}')
        try:
            response = s.get(url, allow_redirects = True, proxies = p, cookies = cookies)
        except:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Proxy Error | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            continue
        
        '''
        with open('cookies.txt', 'a') as file:
                file.write(f'{response.headers}')
                file.write("\n")
        '''

        html = (response.text)
        x = (response.status_code)
        soup = BeautifulSoup(html, 'html.parser')

        if soup.title.text == '504 All Carts Busy at Shoe Palace':
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "All Carts Busy | Retrying", "magenta"))
            instance +=1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 502:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 502 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 501:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 501 Backend Timeout | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 403:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 403 ASN Banned | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 404:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 404 | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 429:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 429 Rate Limited | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 503:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 503 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))    
        elif response.status_code == 522:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 522 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2)))) 
        elif response.status_code == 303:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + f'Size {size} OOS | Stopping', "red"))
            return 'stopped', 'stopped', 'stopped', 'stopped', 'stopped'
        elif response.status_code == 420:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + f'420 Error Calm Down | Retrying', "red"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2)))) 
        else:
            try:
                cookies = s.cookies.get_dict()
                frontend = (cookies['frontend'])
                cf_id = (cookies['__cfduid'])
                try:
                    cf_bm = (cookies['__cf_bm'])
                    filename = os.path.join(dname, f'available_cookies.txt')
                    with open(filename, 'a') as file:
                        file.write(f'{frontend};{cf_id};{cf_bm}')
                        file.write("\n")
                except:
                    filename = os.path.join(dname, f'available_cookies.txt')
                    with open(filename, 'a') as file:
                        file.write(f'{frontend};{cf_id};')
                        file.write("\n")
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + f"ADDED TO CART: {frontend}", "green"))
                
                '''
                with open('logs.txt', 'a') as file:
                    file.write(frontend)
                    file.write("\n")
                '''

                try:
                    success(frontend, product, size, successwebhook)
                except:
                    pass

                inputs = soup.findAll('input', {"class": "middle rwd"})
                for middle in inputs:
                    try:
                        cartID = middle['name']
                    except:
                        continue
                
                try:
                    playsound.playsound('success.mp3')
                except:
                    pass
                #cartID = cartID[5:12]
                cartNumber += 1
                ctypes.windll.kernel32.SetConsoleTitleW(f"Shoop Palace Version {version} | Carts: {cartNumber} | Payment Frauds: {paymentFraud} | Verified Checkouts:  {possibleCheckout}")
                return s, product, instance, cartID, frontend, size
            except:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + f'Unknown Error {response.status_code} | Retrying', "yellow"))
                instance += 1
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2)))) 

'''
def updateCart(num, count, productLink, new_sizes, task, rotate, quantity, instance, cartID, frontend, s, dname):
    while True:
        setting = getsetting(dname)
        if instance >= rotate:
            instance = 0
        proxy = count[(num + int(task)*instance)]
        p = {
        'https' : proxy
        }
        url = "https://www.shoepalace.com/checkout/cart/updatePost"

        cookie = s.cookies.get_dict()
        #cookie['frontend'] = frontend
        payload = f'cart%5B{cartID}%5D%5Bqty%5D={quantity}'
        headers = {
        'authority': 'www.shoepalace.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.shoepalace.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/84.0.4147.122 Mobile/15E148 Safari/604.1",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.shoepalace.com/checkout/cart/',
        'accept-language': 'en-US,en;q=0.9',
        }

        response = requests.request("POST", url, data=payload, headers=headers, proxies = p, cookies = cookie)
        html = (response.text)
        x = (response.status_code)
        soup = BeautifulSoup(html, 'html.parser')
        if response.status_code == 502:
            if setting['displayProxy'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + "502 While ATC Site Down... Retrying", "yellow"))
            else:
                print(colored(logFormat() + "502 While ATC Site Down... Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 501:
            if setting['displayProxy'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + "501 While ATC... Rotating", "yellow"))
            else:
                print(colored(logFormat() + "501 While ATC... Rotating", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 403:
            if setting['displayProxy'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + "Error 403 ASN Banned... Rotating", "yellow"))
            else:
                print(colored(logFormat() + "Error 403 ASN Banned... Rotating", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 404:
            if setting['displayProxy'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + "404 While ATC... Rotating", "yellow"))
            else:
                print(colored(logFormat() + "404 While ATC... Rotating", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 429:
            if setting['displayProxy'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + "429 While ATC Rate Limited... Rotating", "yellow"))
            else:
                print(colored(logFormat() + "429 While ATC Rate Limited... Rotating", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 503:
            if setting['displayProxy'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + "Error 503 Site Down While ATC... Retrying", "yellow"))
            else:
                print(colored(logFormat() + "Error 503 Site Down While ATC... Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))    
        elif response.status_code == 522:
            if setting['displayProxy'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + "Error 522 Site Down While ATC... Retrying", "yellow"))
            else:
                print(colored(logFormat() + "Error 522 Site Down While ATC... Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        else:
            cookies = s.cookies.get_dict()
            frontend = cookies['frontend']
            #print(response.text)
            if setting['discord'] == 'TRUE':
                print(colored(logFormat() + f'[{proxy}] ' + f"SUCCESSFULLY CHANGED CART QUANTITY: {frontend}", "green"))
            else:
                print(colored(logFormat() + f"SUCCESSFULLY CHANGED CART QUANTITY: {frontend}", "green"))
            return 
'''

#checkout with the paymet info
def checkout(num, count, productLink, new_sizes, task, rotate, quantity, profile, cookieList, dname, successwebhook, profileInput, proxy_group, sizes, proxy_type):
    global possibleCheckout
    global paymentFraud
    status = 'Checkout'
    s, product, instance, cartID, frontend, size = addToCart(num, count, productLink, new_sizes, task, rotate, cookieList, dname, successwebhook, profileInput, proxy_group, sizes, proxy_type)
    if s == 'stopped':
        return
    #if int(quantity) > 1:
    #    updateCart(num, count, productLink, new_sizes, task, rotate, quantity, instance, cartID, frontend, s, dname)
    finalCookie = s.cookies.get_dict()
    
    if cookieList:
        cookieArray = cookieList[num].split(',')
        cfuid = (cookieArray[0])
        cfb = (cookieArray[1])
        finalCookie['__cfduid'] = cfuid
        finalCookie['__cf_bm'] = cfb
    else: 
        pass
        
    setting = getsetting(dname)
    while True:
        
        retrydelay = 60
        timeoutDelay = 30
        rotatedelay = int(retrydelay/rotate)
        if instance >= rotate:
            instance = 0
        proxy = count[(num + int(task)*instance)]
        p = {
        'https' : proxy
        }
        url = "https://www.shoepalace.com/onestepcheckout/"

        state = profile['state']
        region_id = state_codes[state]
        payload = {
        "billing[country_id]": "US",
        "billing[firstname]": profile['firstName'],
        "billing[lastname]": profile['lastName'],
        "billing[street][]": profile['addy'],
        "billing[city]": profile['city'],
        "billing[region_id]": region_id,
        "billing[region]": "",
        "billing[postcode]": profile['zipCode'],
        "billing[telephone]": profile['phoneNumber'],
        "billing[email]": profile['email'],
        "billing[confirmemail]": profile['email'],
        "billing[customer_password]": "",
        "billing[confirm_password]": "",
        "billing[save_in_address_book]": "1",
        "shipping[country_id]": "US",
        "billing[use_for_shipping]": "1",
        "shipping[country_id]": "US",
        "shipping[firstname]": profile['firstName'],
        "shipping[lastname]": profile['lastName'],
        "shipping[street][]": profile['addy'],
        "shipping[city]": profile['city'],
        "shipping[region_id]": region_id,
        "shipping[region]": "",
        "shipping[postcode]": profile['zipCode'],
        "shipping[telephone]": profile['phoneNumber'],
        "shipping[save_in_address_book]": "1",
        "shipping[address_id]": "",
        "shipping_method": "flatrate_flatrate",
        "payment[method]": "firstdataglobalgateway",
        "payment[cc_type]": profile['ccType'],
        "payment[cc_number]": profile['cardNumber'],
        "payment[cc_exp_month]": profile['expMonth'],
        "payment[cc_exp_year]": profile['expYear'],
        "payment[cc_cid]": profile['cvv'],
        "onestepcheckout-couponcode": "",
        "gift-wrapping-current": "0",
        "onestepcheckout_comments": "",
        "onestepcheckout-feedback": "",
        "onestepcheckout-feedback-freetext": "",
        "agreement[1]": "1"
        }    
        #print(payload)
        headers = {
        'authority': 'www.shoepalace.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.shoepalace.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/84.0.4147.122 Mobile/15E148 Safari/604.1",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.shoepalace.com/onestepcheckout/',
        'accept-language': 'en-US,en;q=0.9',
        }
        #print(f'Final Cookie: {finalCookie}')
        try:
            response = requests.request("POST", url, cookies = finalCookie, headers=headers, data = payload, allow_redirects = True, proxies = p, timeout=timeoutDelay)
        except:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "503 PayPal Load Error | Retrying", "yellow"))             
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            continue
        cookies = response.cookies.get_dict()
        #print(f'Last Cookie: {cookies}')

        html = (response.text)
        #x = (response.status_code)
        
        soup = BeautifulSoup(html, 'html.parser')
        try:
            title = soup.title.text
        except:
            title = ''
        #print(str(x) + ": " + soup.title.text)
        #print(response.text)
        if (response.text == ''):
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Empty Charge Error | Retrying", "blue"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 502:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 502 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 501:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 501 Backend Timeout | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 403:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 403 ASN Banned | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 404:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 404 Not Found | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 429:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 429 Rate Limited | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 503:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 503 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))    
        elif response.status_code == 522:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 522 Site Down | Retrying", "yellow"))
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif response.status_code == 402:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 402 Payment Fraud | Retrying", "magenta"))
            #print(response.elapsed.total_seconds())
            paymentFraud += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Shoop Palace Version {version} | Carts: {cartNumber} | Payment Frauds: {paymentFraud} | Verified Checkouts: {possibleCheckout}")
            if proxy_type == 'Residential':
                pass
            else:
                instance +=1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif title == 'Shopping Cart at Shoe Palace':
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Kicked Back to Cart | Retrying", "yellow"))
            if 'Shopping Cart Empty' in html:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Shopping Cart Empty | Stopping", "red"))
                return
            instance += 1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        elif 'Log in to your PayPal account' in html:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error PayPal Load Redirect | Retrying", "magenta"))
            if proxy_type == 'Residential':
                pass
            else:
                instance +=1
        elif 'Your credit card has been declined' in html:
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Credit Card Declined | Retrying", "magenta"))
            if proxy_type == 'Residential':
                pass
            else:
                instance +=1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
        else: 
            cookies = s.cookies.get_dict()
            frontend = cookies['frontend']
            #print(response.elapsed.total_seconds()) 
            print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + f"POSSIBLY CHECKED OUT: {frontend}", "green"))
            possibleCheckout += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Shoop Palace Version {version} | Carts: {cartNumber} | Payment Frauds: {paymentFraud} | Verified Checkouts: {possibleCheckout}")
            if proxy_type == 'Residential':
                pass
            else:
                instance +=1
            time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2)))) 

#exactly what the method name says
def initiateTask(dname):
    setting = getsetting(dname)
    SUCCESS_WEBHOOK = setting['Discord']
    successwebhook = DiscordWebhooks(SUCCESS_WEBHOOK)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=800)
    count = []
    arr = os.listdir('proxies')
    arr.append('Return to Main Menu')

    proxy_group = questionary.select(
            "Select Proxy Group:", style = custom_style_fancy, 
            choices=arr).ask()
    
    if proxy_group == 'Return to Main Menu':
        return False
    filename = os.path.join(dname, f'proxies\{proxy_group}')

    try:
        with open(filename) as f:
            content = f.readlines()
    except:
        print(colored("Invalid Proxy Group", "red")) 
        return False
    
    for proxy in content:
            prox = proxy.split(':')
            if len(prox) > 2:
                x = (prox[3])
                y = x.strip("\n").strip()
                p = f'https://{prox[2]}:{y}@{prox[0]}:{prox[1]}'
                count.append(p)
            else:
                z = prox[1].strip("\n").strip()
                a = prox[1].strip()
                p = f'https://{prox[0]}:{a}'
                count.append(p)
    numProxies = len(count)

    if numProxies == 0:
        print(colored("No Proxies Loaded", "red")) 
        return False

    profiles = os.listdir('profiles')
    profiles.append('Return to Main Menu')
    
    profileInput = questionary.select(
            "Select Profile:", style = custom_style_fancy, 
            choices=profiles).ask()

    if profileInput == 'Return to Main Menu':
        return False
    try:
        with open(f'profiles/{profileInput}') as f:
            profile = json.load(f)
            profile['city']
    except:
        print(colored("Invalid or Incorrect Profile", "red"))
        return False
    
    try:
        linksText = os.path.join(dname, f'links.txt')
        with open(linksText) as f:
            links = f.readlines()

        strip_list = [item.strip() for item in links]
    except:
        print(colored("Error Loading Links", "red"))
        strip_list = ['?']
    
    productLink = questionary.autocomplete(
    'Enter Product Link:', style = custom_style_fancy,
    choices=
         strip_list
    ).ask()


    if 'shoepalace' not in productLink:
        print(colored("Invalid Product Link", "red"))
        return False


    task = questionary.autocomplete(
    'Enter Task Amount:', style = custom_style_fancy,
    choices=[
         '10',
         '50',
         '100',
         '150'
    ]).ask()

    cookieList = []
    '''
    
    cookieText = os.path.join(dirname, f'cfcookies.txt')
    with open(cookieText) as f:
        cookies = f.readlines()
    if (len(cookies)) < int(task):
        print(colored("Less CF Cookies than tasks, will run without cookies", "yellow"))
    else:
        for num in range(int(task)):
            cfcookie = (cookies[num].strip("\n"))
            cookieList.append(cfcookie)
            with open(cookieText, 'r') as fin:
                data = fin.read().splitlines(True)
            with open(cookieText, 'w') as fout:
                fout.writelines(data[1:])
        #print(cookieList)
    '''

    rotate = int(int(numProxies/int(task)))
    
    if int(task) > numProxies:
        print(colored("More Tasks than Proxies:", "red"))
        return False

    while True:
        sizes = questionary.checkbox(
        'Select Sizes', style = custom_style_fancy,
        choices=[
            "Random",
            "4.5",
            "5",
            "5.5",
            "6",
            "6.5",
            "7",
            "7.5",
            "8",
            "8.5",
            "9",
            "9.5",
            "10",
            "10.5",
            "11",
            "11.5",
            "12",
            "13",
            "14",
            "15",
            "Custom"
        ]).ask()
        
        if 'Custom' in sizes:
            sizes.pop()
            sizes.append(questionary.text("Enter Custom Size:", style = custom_style_fancy).ask())

        sizes = sizes[::-1]
        new_sizes = [x.strip() for x in sizes]

        if not new_sizes:
            print(colored("No Size Selected", "red"))
        else:
            break
    
    '''
    quantity = questionary.select(
    'Select Quantity', style = custom_style_fancy,
    choices=[
        "1",
        "2",
        "3",
        "4",
    ]).ask()
    '''
    quantity = 1

    proxy_type = questionary.select(
    'Select Proxy Type', style = custom_style_fancy,
    choices=[
        "Residential",
        "Datacenter",
    ]).ask()

    disposable = questionary.text(f"Press ENTER to Start Tasks", style = custom_style_fancy).ask()

    clear() 
    print(colored("Starting Shoe Palace Tasks", "cyan"))
    for num in range(int(task)):
        executor.submit(checkout, num, count, productLink, new_sizes, task, rotate, quantity, profile, cookieList, dname, successwebhook, profileInput, proxy_group, sizes, proxy_type)
    return True
        


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
import logFormats as logging

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

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

thread_local = threading.local()

state_codes = {"AL":1,"AK":2,"AZ":4,"AR":5,"CA":12,"CO":13,"CT":14,"DE":15,"DC":16,"FL":18,"GA":19,"HI":21,"ID":22,"IL":23,"IN":24,"IA":25,"KS":26,"KY":27,"LA":28,"ME":29,"MD":31,"MA":32,"MI":33,"MN":34,"MS":35,"MO":36,"MT":37,"NE":38,"NV":39,"NH":40,"NJ":41,"NM":42,"NY":43,"NC":44,"ND":45,"OH":47,"OK":48,"OR":49,"PA":51,"RI":53,"SC":54,"SD":55,"TN":56,"TX":57,"UT":58,"VT":59,"VA":61,"WA":62,"WV":63,"WI":64,"WY":65}

def getsetting(dname):
    os.chdir(dname)
    with open('settings.json') as f:
        setting = json.load(f)
    return setting

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

def logFormat():
    now = str(datetime.now())
    now = now.split(' ')[1]
    printFormat = '[' + str(now) + ']' + ' ' + '[Shoop Palace] '
    return printFormat

def checkout(frontend, cf_id, cf_bm, count, rotatedelay, dname, profile, profileInput, proxy_group):
    size = 'Unknown'
    status = 'Cookie'

    if cf_id == None:
        finalCookie = {'frontend': frontend}
    elif cf_bm == None:
        finalCookie = {'__cfduid': cf_id, 'frontend': frontend}
    else:
        finalCookie = {'__cf_bm': cf_bm, '__cfduid': cf_id, 'frontend': frontend}
    while True:
        for proxy in count:
            setting = getsetting(dname)
            timeoutDelay = 30
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
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/84.0.4147.122 Mobile/15E148 Safari/604.1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.shoepalace.com/onestepcheckout/',
            'accept-language': 'en-US,en;q=0.9',
            }
            #print(finalCookie)
            try:
                response = requests.request("POST", url, cookies = finalCookie, headers= headers, data = payload, allow_redirects = True, proxies = p, timeout=timeoutDelay)
            except:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "503 PayPal Load Error | Retrying", "yellow"))                     
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
            if (response.text == ''):
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Empty Charge Error | Retrying", "blue"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif response.status_code == 502:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 502 Site Down | Retrying", "yellow"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif response.status_code == 501:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 501 Backend Timeout | Retrying", "yellow"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif response.status_code == 403:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 403 ASN Banned | Retrying", "yellow"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif response.status_code == 404:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 404 Not Found | Retrying", "yellow"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif response.status_code == 429:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 429 Rate Limited | Retrying", "yellow"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif response.status_code == 503:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 503 Site Down | Retrying", "yellow"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))    
            elif response.status_code == 522:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 522 Site Down | Retrying", "yellow"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif response.status_code == 402:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error 402 Payment Fraud | Retrying", "magenta"))
                paymentFraud += 1
                ctypes.windll.kernel32.SetConsoleTitleW(f"Shoop Palace Version {version} | Carts: {cartNumber} | Payment Frauds: {paymentFraud} | Verified Checkouts: {possibleCheckout}")
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif title == 'Shopping Cart at Shoe Palace':
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Kicked Back to Cart | Retrying", "yellow"))
                if 'Shopping Cart Empty' in html:
                    print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Shopping Cart Empty | Stopping", "red"))
                    return
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif 'Log in to your PayPal account' in html:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Error PayPal Load Redirect | Retrying", "magenta"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            elif 'Your credit card has been declined' in html:
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + "Credit Card Declined | Retrying", "magenta"))
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2))))
            else:
                cookies = s.cookies.get_dict()
                frontend = cookies['frontend']
                print(colored(logging.logFormat(profileInput, proxy_group, size, proxy, status) + f"POSSIBLY CHECKED OUT: {frontend}", "green"))
                possibleCheckout += 1
                ctypes.windll.kernel32.SetConsoleTitleW(f"Shoop Palace Version {version} | Carts: {cartNumber} | Payment Frauds: {paymentFraud} | Verified Checkouts: {possibleCheckout}")                
                time.sleep(rotatedelay + (random.randint(0, int(rotatedelay/2)))) 


def startCookieTask(dname):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=800)
    count = []
    arr = os.listdir('proxies')
    arr.append('Return to Main Menu')

    proxy_group = questionary.select(
            "Select Proxy Group:", style = custom_style_fancy, 
            choices=arr).ask()
    
    if proxy_group == 'Return to Main Menu':
        return False
    
    proxy_filename = os.path.join(dname, f'proxies\{proxy_group}')

    profiles = os.listdir('profiles')

    try:
        with open(proxy_filename) as f:
            proxies = f.readlines()
    except:
        print(colored("Invalid Proxy Group", "red")) 
        return False
    
    for proxy in proxies:
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
    
    first = 0
    iteration = 0
    while True:
        setting = getsetting(dname)
        number_proxies = int(setting['Cookie Proxy Amount'])
        filename = os.path.join(dname, f'cookies.txt')
        with open(filename) as f:
            content = f.readlines() 
        if (len(content)) <= iteration:
            time.sleep(5)
            print(colored('! ' + 'All Cookies Used... Checking for New Cookies', "red"))
            continue
        else:
            cookie = (content[iteration-1].strip("\n"))
            arr = cookie.split(';')
            frontend = arr[0]
            try:
                cf_id = arr[1]
            except:
                cf_id = None
            try:
                cf_bm = arr[2]
            except:
                cf_bm = None

            count = []
            with open(proxy_filename) as f:
                proxies = f.readlines()
            for num in range(iteration*number_proxies, (iteration * number_proxies + number_proxies)):
                try:
                    proxy = proxies[num].strip("\n")
                    prox = proxy.split(':')
                    x = (prox[3])
                    y = x.strip("\n")
                    p = f'https://{prox[2]}:{y}@{prox[0]}:{prox[1]}'
                    count.append(p)
                except:
                   print(colored('! ' + 'Not Enough Proxies Error ', "red")) 
                   time.sleep(10)
                   continue
            iteration += 1
            time.sleep(1)
            rotatedelay = int(60/10)
            if first == 0:
                clear()
                print(colored("Starting Shoe Palace Cookie Mode", "cyan"))
            first = 1
            executor.submit(checkout, frontend, cf_id, cf_bm, count, rotatedelay, dname, profile, profileInput, proxy_group)
            
    

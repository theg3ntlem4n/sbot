from colorama import init, Fore, Back, Style
from termcolor import colored, cprint
from pyfiglet import figlet_format
from datetime import datetime, date, timedelta, timezone
from appdirs import *
import json

appname = "data"
appauthor = "Shoop Palace"
appdata = user_data_dir(appname, appauthor)
logSettings = (appdata + '\logSettings.json')



def time():
    now = str(datetime.now())
    now = now.split(' ')[1]
    return (str(now[:-4]))

def bracket_format(element):
    return '[' + element + '] '


def logFormat(profileInput, proxy_group, sizes, proxy, status):
    with open(logSettings) as f:
        content = json.load(f)
    print_array = []
    if content['one'] == 'time':
        print_array.append(time())
    elif content['one'] == 'title':
        print_array.append('Shoop Palace')
    elif content['one'] == 'proxy_group':
        print_array.append(proxy_group)
    elif content['one'] == 'profile':
        print_array.append(profileInput)
    elif content['one'] == 'proxy':
        print_array.append(proxy)
    elif content['one'] == 'size':
        print_array.append(sizes)
    elif content['one'] == 'status':
        print_array.append(status)
    else: 
        print_array.append(None)

    if content['two'] == 'time':
        print_array.append(time())
    elif content['two'] == 'title':
        print_array.append('Shoop Palace')
    elif content['two'] == 'proxy_group':
        print_array.append(proxy_group)
    elif content['two'] == 'profile':
        print_array.append(profileInput)
    elif content['two'] == 'proxy':
        print_array.append(proxy)
    elif content['two'] == 'size':
        print_array.append(sizes)
    elif content['two'] == 'status':
        print_array.append(status)
    else: 
        print_array.append(None)
    
    if content['three'] == 'time':
        print_array.append(time())
    elif content['three'] == 'title':
        print_array.append('Shoop Palace')
    elif content['three'] == 'proxy_group':
        print_array.append(proxy_group)
    elif content['three'] == 'profile':
        print_array.append(profileInput)
    elif content['three'] == 'proxy':
        print_array.append(proxy)
    elif content['three'] == 'size':
        print_array.append(sizes)
    elif content['three'] == 'status':
        print_array.append(status)
    else: 
        print_array.append(None)
    
    if content['four'] == 'time':
        print_array.append(time())
    elif content['four'] == 'title':
        print_array.append('Shoop Palace')
    elif content['four'] == 'proxy_group':
        print_array.append(proxy_group)
    elif content['four'] == 'profile':
        print_array.append(profileInput)
    elif content['four'] == 'proxy':
        print_array.append(proxy)
    elif content['four'] == 'size':
        print_array.append(sizes)
    elif content['four'] == 'status':
        print_array.append(status)
    else: 
        print_array.append(None)

    if content['five'] == 'time':
        print_array.append(time())
    elif content['five'] == 'title':
        print_array.append('Shoop Palace')
    elif content['five'] == 'proxy_group':
        print_array.append(proxy_group)
    elif content['five'] == 'profile':
        print_array.append(profileInput)
    elif content['five'] == 'proxy':
        print_array.append(proxy)
    elif content['five'] == 'size':
        print_array.append(sizes)
    elif content['five'] == 'status':
        print_array.append(status)
    else: 
        print_array.append(None)
    
    if content['six'] == 'time':
        print_array.append(time())
    elif content['six'] == 'title':
        print_array.append('Shoop Palace')
    elif content['six'] == 'proxy_group':
        print_array.append(proxy_group)
    elif content['six'] == 'profile':
        print_array.append(profileInput)
    elif content['six'] == 'proxy':
        print_array.append(proxy)
    elif content['six'] == 'size':
        print_array.append(sizes)
    elif content['six'] == 'status':
        print_array.append(status)
    else: 
        print_array.append(None)

    print_return = ''
    for element in print_array:
        if not element:
            continue
        else:
            if isinstance(element, list):
                temp_element = ''
                for count, item in enumerate(element):
                    if count == (len(element) - 1):
                        temp_element = temp_element + item
                    else:
                        temp_element = temp_element + item + ', '
                    el = bracket_format(temp_element)

                print_return = print_return + el
            else: 
                el = bracket_format(element)
                print_return = print_return + el

    return print_return
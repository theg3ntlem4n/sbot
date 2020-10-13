from colorama import init, Fore, Back, Style
from termcolor import colored, cprint
import os
import uuid
from pyfiglet import figlet_format
import requests
from datetime import datetime, date, timedelta, timezone
import json
import ctypes
from appdirs import *
import time
import logFormats as logs
import sh as ShoePalace
import checkout as ShoePalaceCookie
import questionary

from prompt_toolkit.styles import Style

custom_style_fancy = Style([
    ('qmark', 'fg:#e770ff bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#e770ff bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#e770ff bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#e770ff bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#e770ff'),         # style for a selected item of a checkbox
    ('separator', 'fg:#e770ff'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#e770ff italic')   # disabled choices for select and checkbox prompts
])  

finish = False
version = '0.0.2'
init()

ctypes.windll.kernel32.SetConsoleTitleW(f"Shoop Palace Version {version}")

appname = "data"
appauthor = "Shoop Palace"
appdata = user_data_dir(appname, appauthor)
keyPath = (appdata + '\keys.json')
logSettings = (appdata + '\logSettings.json')

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

if not os.path.exists(appdata):
    os.makedirs(appdata)

if not os.path.exists(keyPath):
    data = {'key': ''}
    with open(keyPath, 'w') as f:
        json.dump(data, f, indent=2)

if not os.path.exists(logSettings):
    data = {
        'one': 'time',
        'two': 'title',
        'three': 'status',
        'four': 'size',
        'five': 'None',
        'six': 'None',
    }
    with open(logSettings, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__": 
    instance = uuid.getnode()
    count = []
    
    cprint(figlet_format('Shoop Palace', font='slant'), 'magenta', attrs=['bold'])

    url = "https://api.suduapps.com/shoopVersion"

    response = requests.request("GET", url, allow_redirects = False)
    if (response.status_code) == 200 and (response.text == version):
        pass
    else:
        print(colored('! ' + "Version Mismatch", "red"))
        sys.exit()
    
    while True:
        if finish == True:
            break
        with open(keyPath) as f:
            keyData = json.load(f)
            key = (keyData['key'])
        
        if key == '':
            print(colored("Enter Key:", "magenta"))
            key = input()
            
            url = "https://api.suduapps.com/shoopKey"
            data = {
            "key": key,
            "instance": instance
            }
            payload = json.dumps(data, ensure_ascii=False)
            headers = {'content-type': 'application/json'}

            keyResponse = requests.request("GET", url, data = payload, headers = headers, allow_redirects = False)
            if keyResponse.text == 'None':
                print(colored('! ' + "Incorrect Key", "red"))
                continue
            elif (keyResponse.text == 'Mismatch'):
                print(colored('! ' + "Mismatched Device", "red"))
                continue
            elif (keyResponse.text == 'Good'):    
                data = {'key': key}
                with open(keyPath, 'w') as f:
                    json.dump(data, f, indent=2)
                pass
            else:
                print(colored('! ' + "Unknown Error", "red"))
        else:
            url = "https://api.suduapps.com/shoopKey"
            data = {
            "key": key,
            "instance": instance
            }
            
            payload = json.dumps(data, ensure_ascii=False)
            headers = {'content-type': 'application/json'}
            
            keyResponse = requests.request("GET", url, data = payload, headers = headers, allow_redirects = False)
            
            if keyResponse.text == 'None':
                print(colored('! ' + "Incorrect Key", "red"))
                data = {'key': ''}
                with open(keyPath, 'w') as f:
                    json.dump(data, f, indent=2)
                continue
            elif (keyResponse.text == 'Mismatch'):
                print(colored('! ' + "Mismatched Device", "red"))
                data = {'key': ''}
                with open(keyPath, 'w') as f:
                    json.dump(data, f, indent=2)
                continue
            elif (keyResponse.text == 'Good'):    
                pass
            else:
                print(colored('! ' + "Unknown Error", "red"))

        url = "https://api.suduapps.com/userInfo"
        data = {
                "key": key,
                }
                    
        payload = json.dumps(data, ensure_ascii=False)

        headers = {'content-type': 'application/json'}

        response = requests.request("GET", url, data=payload, headers=headers)

        disc_object = json.loads(response.text)
        disc_id = disc_object['discord']

        url = f"https://discord.com/api/users/{disc_id}"

        payload = ""
        headers = {
            'content-type': "application/json",
            'authorization': "Bot NTg0NTgxODQxMTYwNTAzMzA3.XPNAQw.6CkUomNXwAtpW1OjObDx3lgCL08",
            'user-agent': "DiscordBot ($url, $versionNumber)"
            }

        response = requests.request("GET", url, data=payload, headers=headers)
        discord = json.loads(response.text)
        discord_user = (discord['username'] + '#' + discord['discriminator'])
        print(colored('! ' + f"Verification Successful: Welcome {discord_user}!", "green"))

        while True:
            menu = questionary.select(
            "Main Menu", style = custom_style_fancy,
            choices=[
                'Quickstart Shoe Palace Tasks',
                'Run Cookie Tasks',
                'Create/Edit Profile',
                'Change Task Printing',
                'Edit Settings',
                'Manage Key',
                'Exit Shoop Palace'
            ]).ask()

            if menu == 'Quickstart Shoe Palace Tasks':
                init = ShoePalace.initiateTask(dname)
                if init:    
                    finish = True
                    break
            
            if menu == 'Run Cookie Tasks':
                init = ShoePalaceCookie.startCookieTask(dname)
            
            
            if menu == 'Create/Edit Profile':
                profiles = os.listdir('profiles')
                profiles.append('Create New Profile')
                profiles.append('Return to Main Menu')
                profileInput = questionary.select(
                "Select/Create Profile:", style = custom_style_fancy, 
                choices=profiles).ask()
                if profileInput == 'Return to Main Menu':
                    continue
                elif profileInput == 'Create New Profile':
                    profile_name = questionary.text("Profile Name:", style = custom_style_fancy).ask()
                    if (profile_name.lower() == 'c') or (profile_name.lower() == 'cancel'):
                        continue
                    email = questionary.text("Email Address:", style = custom_style_fancy).ask()
                    if (email.lower() == 'c') or (email.lower() == 'cancel'):
                        continue
                    name = questionary.text("Full Name:", style = custom_style_fancy).ask()
                    name_array = name.split(' ')
                    first_name = name_array[0]
                    last_name = name_array[1]
                    if (name.lower() == 'c') or (name.lower() == 'cancel'):
                        continue
                    addy = questionary.text("Address Line:", style = custom_style_fancy).ask()
                    if (addy.lower() == 'c') or (addy.lower() == 'cancel'):
                        continue
                        
                    address2 = questionary.text("Address Line 2:", style = custom_style_fancy).ask()
                    if (address2.lower() == 'c') or (address2.lower() == 'cancel'):
                        continue
                    state = questionary.select("State:", style = custom_style_fancy, choices = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD", "TN","TX","UT","VT","VA","WA","WV","WI","WY","Return to Main Menu"]).ask()
                    if state == 'Return to Main Menu':
                        continue
                    city = questionary.text("City:", style = custom_style_fancy).ask()
                    if (city.lower() == 'c') or (city.lower() == 'cancel'):
                        continue
                    zipCode = questionary.text("Zip Code:", style = custom_style_fancy).ask()
                    if (zipCode.lower() == 'c') or (zipCode.lower() == 'cancel'):
                        continue
                    phoneNumber = questionary.text("Phone Number:", style = custom_style_fancy).ask()
                    if (phoneNumber.lower() == 'c') or (phoneNumber.lower() == 'cancel'):
                        continue
                    ccType = questionary.select("Credit Card Type:", style = custom_style_fancy, choices = ["VI", "AE", "MC", "DI", "Return to Main Menu"]).ask()
                    if ccType == 'Return to Main Menu':
                        continue
                    cardNumber = questionary.text("Card Number:", style = custom_style_fancy).ask()
                    if (cardNumber.lower() == 'c') or (cardNumber.lower() == 'cancel'):
                        continue
                    expMonth = questionary.select("Credit Card Expiration Month", style = custom_style_fancy, choices = ["1","2","3","4","5","6","7","8","9","10","11","12", "Return to Main Menu"]).ask()
                    if expMonth == 'Return to Main Menu':
                        continue
                    expYear = questionary.select("Credit Card Expiration Year", style = custom_style_fancy, choices = ["2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030", "Return to Main Menu"]).ask()
                    if expYear == 'Return to Main Menu':
                        continue
                    cvv = questionary.text("CVV (Digits on Back of Card):", style = custom_style_fancy).ask()
                    if (cvv.lower() == 'c') or (cvv.lower() == 'cancel'):
                        continue
                    data = {
                            "email": email,
                            "firstName": first_name,
                            "lastName": last_name,
                            "addy": addy,
                            "apartmentNumber": address2,
                            "state": state,
                            "country": "US",
                            "city": city,
                            "zipCode": zipCode,
                            "phoneNumber": phoneNumber,
                            "ccType": ccType,
                            "cardNumber": cardNumber,
                            "expMonth": expMonth,
                            "expYear": expYear,
                            "cvv": cvv
                            }
                    with open(f'profiles/{profile_name}.json', 'w') as f:
                        json.dump(data, f)
                else:
                    try:
                        while True:
                            with open(f'profiles/{profileInput}') as f:
                                profile = json.load(f)
                            prof = []
                            for element in profile:
                                output = profile[element]
                                prof.append(f'{element}: {output}')
                            prof.append('Return to Main Menu')
                            edit_profile = questionary.select("Edit Profile Element", style = custom_style_fancy, choices = prof).ask()
                            edit_profile_split = edit_profile.split(':')
                            profile_element = (edit_profile_split[0])
                            if profile_element == 'Return to Main Menu':
                                break
                            if profile_element in ['firstName', 'email', 'lastName', 'addy', 'apartmentNumber', 'zipCode', 'phoneNumber', 'cardNumber', 'cvv', 'city']:
                                user_input = questionary.text(f"New Value for {profile_element}", style = custom_style_fancy).ask()
                            elif profile_element == "state":
                                user_input = questionary.select("State:", style = custom_style_fancy, choices = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD", "TN","TX","UT","VT","VA","WA","WV","WI","WY","Cancel"]).ask()
                            elif profile_element == 'ccType':
                                user_input = ccType = questionary.select("Credit Card Type:", style = custom_style_fancy, choices = ["VI", "AE", "MC", "DI", "Cancel"]).ask()
                            elif profile_element == 'expMonth':
                                user_input = questionary.select("Credit Card Expiration Month", style = custom_style_fancy, choices = ["1","2","3","4","5","6","7","8","9","10","11","12", "Cancel"]).ask()
                            else:
                                user_input = questionary.select("Credit Card Expiration Year", style = custom_style_fancy, choices = ["2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030", "Cancel"]).ask()

                            if user_input in ['C', 'c', 'CANCEL', 'Cancel']:
                                continue
                            else:
                                profile[profile_element] = user_input
                                with open(f'profiles/{profileInput}', 'w') as f:
                                    json.dump(profile, f, indent=2)
                    except:
                        print(colored('! ' + 'Corrupted Profile Selected', "red"))

            if menu == 'Change Task Printing':
                while True:
                    with open(logSettings) as f:
                        loggingData = json.load(f)
                        one = loggingData['one']
                        two = loggingData['two']
                        three = loggingData['three']
                        four = loggingData['four']
                        five = loggingData['five']
                        six = loggingData['six']

                    print(colored('! ' + f'[1. {one}] ' + f'[2. {two}] ' + f'[3. {three}] ' + f'[4. {four}] ', "cyan"))
                    print_input = questionary.select(
                        "Select Task Box:", style = custom_style_fancy,
                        choices=[
                            f'[1. {one}] ',
                            f'[2. {two}] ',
                            f'[3. {three}] ',
                            f'[4. {four}] ',
                            f'[5. {five}] ',
                            f'[6. {six}] ',
                            'Return to Main Menu',
                        ]).ask()
                    
                    if print_input == 'Return to Main Menu':
                        break

                    if print_input == f'[1. {one}] ':
                        output = questionary.select(
                        "Change Output:", style = custom_style_fancy,
                        choices=[
                            'time',
                            'title',
                            'proxy_group',
                            'profile',
                            'proxy',
                            'size',
                            'status',
                            'None',
                            'Return to Select Screen',
                        ]).ask()
                        if output == 'Return to Select Screen':
                            continue
                        loggingData['one'] = output
                        with open(logSettings, 'w') as f:
                            json.dump(loggingData, f, indent=2)
                    if print_input == f'[2. {two}] ':
                        output = questionary.select(
                        "Change Output:", style = custom_style_fancy,
                        choices=[
                            'time',
                            'title',
                            'proxy_group',
                            'profile',
                            'proxy',
                            'size',
                            'status',
                            'None',
                            'Return to Select Screen',
                        ]).ask()
                        if output == 'Return to Select Screen':
                            continue
                        loggingData['two'] = output
                        with open(logSettings, 'w') as f:
                            json.dump(loggingData, f, indent=2)
                    if print_input == f'[3. {three}] ':
                        output = questionary.select(
                        "Change Output:", style = custom_style_fancy,
                        choices=[
                            'time',
                            'title',
                            'proxy_group',
                            'profile',
                            'proxy',
                            'size',
                            'status',
                            'None',
                            'Return to Select Screen',
                        ]).ask()
                        if output == 'Return to Select Screen':
                            continue
                        loggingData['three'] = output
                        with open(logSettings, 'w') as f:
                            json.dump(loggingData, f, indent=2)
                    if print_input == f'[4. {four}] ':
                        output = questionary.select(
                        "Change Output:", style = custom_style_fancy,
                        choices=[
                            'time',
                            'title',
                            'proxy_group',
                            'profile',
                            'proxy',
                            'size',
                            'status',
                            'None',
                            'Return to Select Screen',
                        ]).ask()
                        if output == 'Return to Select Screen':
                            continue
                        loggingData['four'] = output
                        with open(logSettings, 'w') as f:
                            json.dump(loggingData, f, indent=2)
                    if print_input == f'[5. {five}] ':
                        output = questionary.select(
                        "Change Output:", style = custom_style_fancy,
                        choices=[
                            'time',
                            'title',
                            'proxy_group',
                            'profile',
                            'proxy',
                            'size',
                            'status',
                            'None',
                            'Return to Select Screen',
                        ]).ask()
                        if output == 'Return to Select Screen':
                            continue
                        loggingData['five'] = output
                        with open(logSettings, 'w') as f:
                            json.dump(loggingData, f, indent=2)
                    if print_input == f'[6. {six}] ':
                        output = questionary.select(
                        "Change Output:", style = custom_style_fancy,
                        choices=[
                            'time',
                            'title',
                            'proxy_group',
                            'profile',
                            'proxy',
                            'size',
                            'status',
                            'None',
                            'Return to Select Screen',
                        ]).ask()
                        if output == 'Return to Select Screen':
                            continue
                        loggingData['six'] = output
                        with open(logSettings, 'w') as f:
                            json.dump(loggingData, f, indent=2)
                
            if menu == 'Edit Settings':
                while True:
                    with open(f'settings.json') as f:
                        setting = json.load(f)
                    setting_array = []
                    for element in setting:
                        output = setting[element]
                        setting_array.append(f'{element}: {output}')
                    setting_array.append('Return to Main Menu')
                    edit_setting = questionary.select("Edit Settings", style = custom_style_fancy, choices = setting_array).ask()
                    edit_setting_split = edit_setting.split(':')
                    edit_element = (edit_setting_split[0])
                    if edit_element == 'Return to Main Menu':
                        break
                    setting_input = questionary.text(f"New Value for {edit_element}", style = custom_style_fancy).ask()
                    if setting_input in ['C', 'c', 'CANCEL', 'Cancel']:
                        continue
                    else:
                        setting[edit_element] = setting_input
                        with open(f'settings.json', 'w') as f:
                            json.dump(setting, f, indent=2)

            if menu == 'Manage Key':
                print(colored('! ' + 'Key: ' + key, "cyan"))
                print(colored('! ' + 'Hardware ID: ' + str(instance), "cyan"))
                print(colored('! ' + 'Discord: ' + discord_user, "cyan"))
                key_input = questionary.select(
                            "Select Key Action:", style = custom_style_fancy,
                            choices=[
                                'Deactivate Key',
                                'Return to Main Menu',
                            ]).ask()
                if key_input == 'Deactivate Key':
                    url = "https://api.suduapps.com/deactivateShoop"
                    data = {
                            "id": disc_id,
                            }
                    payload = json.dumps(data, ensure_ascii=False)
                    headers = {'content-type': 'application/json'}
                    response = requests.request("GET", url, data=payload, headers=headers)
                    sys.exit()
                else:
                    continue
            
            if menu == 'Exit Shoop Palace':
                sys.exit()


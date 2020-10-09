import os
import requests
import sys

from selenium import webdriver

driver = webdriver.Chrome('/Users/alexkim/chromedriver')

'''

Information Needed: Username, Password, Credit Card Info, Shoe Make, Shoe Size

To Do List:

    -Add a hex editor for the chromedriver file
    -Find a way to bypass Akamai bot detection (method above)
        -Create "human-like features" using wait()
    -Find the xpath keys in html coding (for information needed fields)
    -Determine if there is a way to automate key evaluation (for different sites)
    -Make script scalable

'''



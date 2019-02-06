'''
This module contains functionality to authenticate chrome driver
as well as "authenticate" with TRACE by logging in/opening it
'''

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def initialize_chrome():
    options = Options()
    if os.getenv('HEADLESS', 'headless') == 'True':
        options.add_argument("--headless")
    prefs = {
        "download.default_directory": os.getenv('DOWNLOAD', 'download'),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        'safebrowsing.enabled': False,
        'safebrowsing.disable_download_protection': True
    }
    options.add_experimental_option('prefs', prefs)
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "normal"
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe",options=options, desired_capabilities=capa)

    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': os.getenv('DOWNLOAD', 'download')}}
    driver.execute("send_command", params)
    return driver


def CAS_authentification(driver):
    driver.get("https://neuidmsso.neu.edu/cas-server/login")
    usern = driver.find_element_by_id("username")
    usern.send_keys(os.getenv('USERNAME', 'username'))
    passw = driver.find_element_by_id("password")
    passw.send_keys(os.getenv('PASSWORD', 'password'))
    passw.submit()
    return driver


def confirm_login(driver):
    if ('Log In Successful' in driver.page_source):
        print('Log In Successful')
    else:
        print('Log In Failed')

def open_TRACE(driver):
    # This step is necessary to use the exposed API's
    # (some kind of authentication step for the TRACE site)
    driver.get("https://www.applyweb.com/eval/shibboleth/neu/36892")
    return driver

def auth():
    driver = initialize_chrome()
    driver = CAS_authentification(driver)
    confirm_login(driver)
    driver = open_TRACE(driver)

    return driver

if __name__ == "__main__":
    driver = auth()

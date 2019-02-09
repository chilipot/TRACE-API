'''
Creates a webdriver that is authenticated for Trace access
'''

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TraceDriver(webdriver.Chrome):
    def __init__(self, path):
        options, capabilities = TraceDriver.chrome_settings()
        super(TraceDriver, self).__init__(executable_path=path, options=options, desired_capabilities=capabilities)
        self.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {
            'behavior': 'allow', 'downloadPath': os.getenv('DOWNLOAD', 'download')}}
        self.execute("send_command", params)

    @staticmethod
    def chrome_settings():
        options = Options()
        if os.getenv('HEADLESS', 'headless') == 'True':
            options.add_argument("--headless")

        preferences = {
            "download.default_directory": os.getenv('DOWNLOAD', 'download'),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            'safebrowsing.enabled': False,
            'safebrowsing.disable_download_protection': True
        }
        options.add_experimental_option('prefs', preferences)
        capabilities = DesiredCapabilities.CHROME
        capabilities["pageLoadStrategy"] = "normal"

        return options, capabilities

    def confirm_login(driver):
        if ('Log In Successful' in driver.page_source):
            print('Log In Successful')
        else:
            print('Log In Failed')
            raise ValueError('Invalid credentials')

    def authenticate(self, username=os.getenv('USERNAME'), password=os.getenv('PASSWORD')):
        self.get("https://neuidmsso.neu.edu/cas-server/login")
        user_input, password_input = self.find_element_by_id("username"), self.find_element_by_id("password")
        user_input.send_keys(username)
        password_input.send_keys(password)
        password_input.submit()
        self.confirm_login()

    def open_TRACE(self):
        self.get("https://www.applyweb.com/eval/shibboleth/neu/36892")


if __name__ == "__main__":
    driver = TraceDriver(r'chromedriver.exe')
    driver.authenticate()
    print(type(driver))

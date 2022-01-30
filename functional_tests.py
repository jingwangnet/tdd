from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)

try:
    browser.get('http://127.0.0.1:8000')
except WebDriverException:
    pass

assert 'success' in browser.title, browser.title



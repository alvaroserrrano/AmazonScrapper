from selenium import webdriver

DIRECTORY = 'reports'
NAME = 'iphone'
CURRENCY = '€'
MIN_PRICE = '300'
MAX_PRICE = '800'
FILTERS = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}
BASE_URL = "http://www.amazon.es/"

def get_chrome_web_driver(opts):
    return webdriver.Chrome('./chromedriver', chrome_options=opts)

def get_driver_opts():
    return webdriver.ChromeOptions()

#ignore certificate errors
def set_ignore_cert_errors(opts):
    opts.add_argument('--ignore-certificate-errors')

#incognito
def set_incognito(opts):
    opts.add_argument('--incognito ')


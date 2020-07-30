#get dictionary of products
from amazon_config import (
    DIRECTORY,
    PRODUCT_NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    get_chrome_web_driver,
    get_driver_opts,
    set_ignore_cert_errors,
    set_incognito
)
import json
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class GenerateReport:
    def __init__(self, filename, filters, base_url, currency, data):
        self.filename = filename
        self.filters = filters
        self.base_url = base_url
        self.currency = currency
        self.data = data
        report = {
            'title': self.filename,
            'date': self.get_current_time(),
            #best product according to price
            'best_product': self.get_best_product(),
            'filters': self.filters,
            'base_url': self.base_url,
            'currency': self.currency,
            'product_list': self.data
        }

        print('Generating report...')
        with open(f'{DIRECTORY}/{filename}.json', 'w') as file:
            json.dump(report, file)
        print('Done!')

    @staticmethod
    def get_current_time():
        now = datetime.now()
        return now.strftime('%d/%m/%Y %H:%M:%S')

    def get_best_product(self):
        try:
            return sorted(self.data, key=lambda x: x['price'])[0]
        except Exception as e:
            print('An error occurred categorizing the products')
            print(e)
            return None

class AmazonAPI:
    def __init__(self, product_name, filters, base_url, currency):
        self.product_name = product_name
        self.base_url = base_url
        self.currency = currency
        opts = get_driver_opts()
        set_ignore_cert_errors(opts)
        set_incognito(opts)
        self.driver = get_chrome_web_driver(opts)
        #might be different depending on country (specfied on URL)
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print('Opening Amazon on Google Chrome...')
        time.sleep(2)
        print(f'Searching for {self.product_name}...')
        links = self.get_product_links()
        if not links:
            print('Script stopped running')
            return
        print(f'Got {len(links)} links')
        print('Retrieving information about products...')
        products = self.get_products_info(links)
        print(f'Fetched data from {len(products)} products')
        self.driver.quit()
        return products

    def get_product_links(self):
        self.driver.get(self.base_url)
        #Focus on search box
        search_box = self.driver.find_element_by_id('twotabsearchtextbox')
        #Enter name of product on search box
        search_box.send_keys(self.product_name)
        time.sleep(2)
        #Press ENTER
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)   #wait to see how word is entered on the search box
        print('Filtering out price preferences...')
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)   #wait for page load
        result_list = self.driver.find_elements_by_class_name('s-result-list')
        links = []
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print('No products matching search terms...')
            print(e)
            return links

    def get_products_info(self, links):
        #Get ASIN Amazon Standard Identification Number
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_product(asin)
            if product:
                products.append(product)
        return products

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    #clear the links
    @staticmethod
    def get_asin(link):
        return link[link.find('/dp/') + 4:link.find('/ref')]

    def get_product(self, asin):
        print(f"Product ID: {asin} - getting data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)    #Wait for page load
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product = {
                'asin': asin,
                'url': product_short_url,
                'title' : title,
                'seller': seller,
                'price': price
            }
            return product
        return None

    def shorten_url(self, asin):
        return self.base_url + '/dp/' + asin

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f'Cannot get title from url: {self.driver.current_url}')
            return None

    def get_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print (e)
            print(f'Cannot get seller from url: {self.driver.current_url}')
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element_by_id('availability').text
                if 'Available' in availability:
                    price = self.driver.find_element_by_class_name('olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price

    #this depends on the Amazon store (country)
    def convert_price(self, price):
        #638,99 €
        #1.159,00 €
        price = price.split(self.currency)[0]
        try:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        except:
            Exception()
        try:
            price = price.split(",")[0] + price.split(",")[1]
        except:
            Exception()
        return float(price)
    #29000 €&nbsp€

if __name__ == "__main__":
    amazon_scrapper = AmazonAPI(PRODUCT_NAME, FILTERS, BASE_URL, CURRENCY)
    data = amazon_scrapper.run()
    GenerateReport(PRODUCT_NAME, FILTERS, BASE_URL, CURRENCY, data)

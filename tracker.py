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

class ReportGenerator():
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, product_name, filters, base_url, currency):
        self.product_name = product_name
        self.base_url = base_url
        self.currency = currency
        opts = get_driver_opts()
        set_ignore_cert_errors(opts)
        set_incognito(opts)
        self.driver = get_driver_opts()
        #might be different depending on country (specfied on URL)
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"
        pass


if __name__ == "__main__":
    amazon_scrapper = AmazonAPI(PRODUCT_NAME, FILTERS, BASE_URL, CURRENCY)
    print(amazon_scrapper.price_filter)

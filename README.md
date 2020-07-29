# Amazon Web Scrapper

## Generate report of products in JSON format
*A JSON report is generated after running the API.
*It is recommended to copy and paste the report into an online JSON formatter
to obtain a more readable format
*Amazon site, price ranges, and products are specified in config file
*Tracker is the main API that generates a dictionary of results
*The results returned by the tracker are passed for further filtering
*Make sure to download WebDriver based on your browser version

##Project Breakdown
*Run Chrome Browser
*Go to Amazon
*Enter product name into the search bar
*Get links from multiple pages
*Scrape each link and get product data
*Generate report from products dictionary

##Selenium  framework
Visit the docs for Selenium WebDriver ![Selenium Docs](https://www.selenium.dev/documentation/en/webdriver/)

##Use cases
*Customize the config file to meet your needs : product, price range...
*Run as a chron job on a remote server in the cloud


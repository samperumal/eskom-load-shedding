import wget
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timezone
import pytz

tz = pytz.timezone('Africa/Johannesburg')
time_string = datetime.now(tz).strftime("%H:%M")

def parseGeneric(url, site, parser):
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)
    browser.set_page_load_timeout(30)
    print("Retrieving Url")
    browser.get(url)

    print("Parsing page")
    match = parser(browser)

    browser.quit()

    if match != None:
        print(match)
        return {
            "stage": match.group(1),
            "site" : site,
            "url"  : url,
            "text" : match.group(0),
            "time" : time_string
        }
    else: return None

def parseCpt():
    url = "https://www.capetown.gov.za/Family%20and%20home/Residential-utility-services/Residential-electricity-services/Load-shedding-and-outages"
    
    def parser(browser):
        element = browser.find_element_by_class_name("ExternalClass898DBDD1A6E04104B2A22756904464A5")
        text = element.get_attribute('innerHTML')
        match = re.search("stage (\d) active", text, re.IGNORECASE)
        return match

    return parseGeneric(url, "City of Cape Town", parser)

def parseJhb():
    url = "https://www.citypower.co.za/customers/Pages/Load_Shedding_Downloads.aspx"
    
    options = Options()
    options.add_argument('--headless')

    def parser(browser):
        element1 = browser.find_element_by_id("MSOZoneCell_WebPartWPQ3")
        element2 = element1.find_element_by_class_name("ms-rtestate-field")
        text = element2.get_attribute('innerText')
        match = re.search("stage\W(\d)\W+\(in-progress\)", text, re.IGNORECASE)
        return match
        
    return parseGeneric(url, "City Power", parser)

def parsePta():
    url = "http://www.tshwane.gov.za/sites/Departments/Public-works-and-infrastructure/Pages/Load-Shedding.aspx"
    
    def parser(browser):
        element = browser.find_element_by_id("status")
        text = element.get_attribute('innerHTML')
        match = re.search("Load Shedding Stage (\d) is in progress", text, re.IGNORECASE)
        return match
    
    return parseGeneric(url, "City of Tshwane", parser)

if __name__ == "__main__":
    parseCpt() 
    parseJhb()
    parsePta()

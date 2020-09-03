import wget
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timezone
import pytz

tz = pytz.timezone('Africa/Johannesburg')
time_string = datetime.now(tz).strftime("%H:%M, %d %b")

def parseGeneric(url, site, parser):
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)
    try:
        browser.set_page_load_timeout(120)
        print("Retrieving Url")
        browser.get(url)

        print("Parsing page")
        (stage, text) = parser(browser)
    except:
        print(sys.exc_info())
        return None
    finally:
        browser.quit()

    return {
        "stage": None if stage is None else str(stage * 1),
        "site" : site,
        "url"  : url,
        "text" : text,
        "time" : time_string
    }

def parseCpt():
    url = "https://www.capetown.gov.za/Family%20and%20home/Residential-utility-services/Residential-electricity-services/Load-shedding-and-outages"
    
    def parser(browser):
        print("Sleeping")
        time.sleep(90) # Wait for onLoad scripts to complete
        print("Processing CPT site")
        try:
            element = browser.find_element_by_class_name("page-content")
        except: 
            return (None, None)
        
        text = element.get_attribute('innerText')
        match = re.search(r"stage\W+(\d+)(\W+load-shedding)?\W+active(\W+from\W+\d+:\d+\W+(\d+:\d+))?", text, re.IGNORECASE)
        
        if match != None: return (match.group(1), match.group(0))
        else: return (None, None)

    for i in range(3):
        result = parseGeneric(url, "City of Cape Town", parser)
        if result != None: return result
        else: print("Retrying")

    return None

def parseJhb():
    url = "https://www.citypower.co.za/customers/Pages/Load_Shedding_Downloads.aspx"
    
    options = Options()
    options.add_argument('--headless')

    def parser(browser):
        print("Processing JHB site")
        element1 = browser.find_element_by_id("MSOZoneCell_WebPartWPQ3")
        element2 = element1.find_element_by_class_name("ms-rtestate-field")
        text = element2.get_attribute('innerText')
        match = re.search(r"stage\W+(\d+)\W+-?\W*(in-?\W*progress|is\W+in\W+progress|will\W+be\W+implemented|.*will\W+resume)", text, re.IGNORECASE)
        
        if match != None: return (match.group(1), match.group(0))
        else: return (None, None)
        
    return parseGeneric(url, "City Power", parser)

def parsePta():
    url = "http://www.tshwane.gov.za/sites/Departments/Public-works-and-infrastructure/Pages/Load-Shedding.aspx"
    
    def parser(browser):
        print("Processing PTA site")
        element = browser.find_element_by_id("status")
        text = element.get_attribute('innerHTML')
        match = re.search(r"Load\W+Shedding\W+Stage\W+(\d+)\W+is\W+in\W+progress", text, re.IGNORECASE)
        
        if match != None: return (match.group(1), match.group(0))
        else: return (None, None)
    
    return parseGeneric(url, "City of Tshwane", parser)

if __name__ == "__main__":
    print(parseCpt())
    print(parseJhb())
    print(parsePta())

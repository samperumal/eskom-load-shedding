import wget
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = "https://www.capetown.gov.za/Family%20and%20home/Residential-utility-services/Residential-electricity-services/Load-shedding-and-outages"
    
def parseSite():
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)
    browser.set_page_load_timeout(30)
    print("Retrieving Url")
    browser.get(url)

    print("Parsing page")
    element = browser.find_element_by_class_name("ExternalClass898DBDD1A6E04104B2A22756904464A5")
    text = element.get_attribute('innerHTML')
    print(text)

    match = re.search("stage (\d) active", text)

    browser.quit()

    if match != None:
        print(match)
        return {
            "stage": match.groups()[0],
            "site" : "City of Cape Town",
            "url"  : url,
            "text" : text
        }
    else: return None

if __name__ == "__main__":
    parseSite() 
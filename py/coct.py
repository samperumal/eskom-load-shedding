import wget
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def parseSiteOld():
    url = "https://www.capetown.gov.za/Family%20and%20home/Residential-utility-services/Residential-electricity-services/Load-shedding-and-outages"
    html = wget.download(url, "./cape-town.html")
    print(html)
    with open('./cape-town.html') as htmlfile:
        content = htmlfile.read()
        result = re.search("stage 2 active", content)
        print(result)

    return None

url = "https://www.capetown.gov.za/Family%20and%20home/Residential-utility-services/Residential-electricity-services/Load-shedding-and-outages"
    
def parseSite():
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)
    print("Retrieving Url")
    browser.get(url)

    html = browser.page_source
    f = open("myhtml", "wt")
    f.write(html)
    f.close()

    print("Parsing page")
    element = browser.find_element_by_class_name("ExternalClass898DBDD1A6E04104B2A22756904464A5")
    print(element.get_attribute('innerHTML'))

    browser.quit()



if __name__ == "__main__":
    parseSite() 
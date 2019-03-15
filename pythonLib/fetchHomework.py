from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import sys

print("Starting to fetch homeworks")
sys.stdout.flush()

url = "https://entauvergne.fr/"
urlPronote = "https://0630018c.index-education.net/pronote"

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)


driver.find_element_by_id("input_1").send_keys("liam.latour")
driver.find_element_by_id ("input_2").send_keys("pikmine##2")
driver.find_element_by_id("SubmitCreds").click()

driver.get(urlPronote)

while 1:
    try:
        driver.find_element_by_id("id_84id_7").click()
        break
    except:
        continue



time.sleep(1)
html = driver.find_elements_by_css_selector("tr[valign=top]")

jsonObj = {}
currentSubject = "bug"
for elem in html:
    tempText = elem.get_attribute("innerText").splitlines()[2:]
    if tempText[0] == '\t':
        tempText = tempText[1:]

    if len(tempText) == 2:
        currentSubject = tempText[1]
        jsonObj[tempText[1]] = {"moyenne" : tempText[0]}
    else:
        jsonObj[currentSubject]["DS" + str(len(jsonObj[currentSubject]))] = {
            "note" : tempText[0],
            "date" : tempText[1],
            "moyenne": tempText[2][14:]
        }

print(json.dumps(jsonObj))
sys.stdout.flush()
quit(0)
driver.close()
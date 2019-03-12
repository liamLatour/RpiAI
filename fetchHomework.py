# Ce code dépend de selenium 'pip install selenium'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

url = "https://entauvergne.fr/"
urlPronote = "https://0630018c.index-education.net/pronote"

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Envoie les identifiants
driver.find_element_by_id("input_1").send_keys("NOM UTILISATEUR")
driver.find_element_by_id ("input_2").send_keys("MOT DE PASSE")
driver.find_element_by_id("SubmitCreds").click()

driver.get(urlPronote)

# Tente de clicker jusqu'à que cela soit possible
while 1:
    try:
        driver.find_element_by_id("id_84id_7").click()
        break
    except:
        continue

# Attends que tous se charge
time.sleep(1)
html = driver.find_elements_by_css_selector("tr[valign=top]")

# Met tout dans un objet JSON
jsonObj = {}
currentSubject = "bug"
for elem in html:
    tempText = elem.get_attribute("innerText").splitlines()[2:]
    if tempText[0] == '\t':
        tempText = tempText[1:]

    if len(tempText) == 2:
        currentSubject = tempText[1]
        jsonObj[tempText[1]] = {'moyenne' : tempText[0]}
    else:
        jsonObj[currentSubject]['DS' + str(len(jsonObj[currentSubject]))] = {
            'note' : tempText[0],
            'date' : tempText[1],
            'moyenne': tempText[2][14:]
        }

print(jsonObj)
driver.close()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import copy
import time
import json
import sys
import os

print("Starting to look for current version")
sys.stdout.flush()

url = "https://github.com/liamLatour/RpiAI/blob/master/version"

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

version = driver.find_element_by_class_name("data")
text = version.get_attribute("innerText")
currentVersion = -1

for ver in text.splitlines():
    if "CurrentVersion" in ver:
        currentVersion = ver.split("=")[1]

if currentVersion != -1:
    myVersion = -1
    try:
        f = open("..//version", "r")
        for ver in f.read().splitlines():
            if "CurrentVersion" in ver:
                myVersion = ver.split("=")[1]
        f.close()
    except:
        pass

    if myVersion == -1 or myVersion != currentVersion:
        print("Updating to version: " + currentVersion)
        copy("update.py", "..//..//")
        os.system("python ..//..//update.py")
        exit()
    else:
        print("Up to date")
else:
    print("No version found")

driver.close()
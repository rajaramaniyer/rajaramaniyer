#!/opt/homebrew/opt/python@3.9/libexec/bin/python

import glob
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_lines(filename):
  file = open(filename, 'r', encoding="UTF-8")
  Lines = file.readlines()
  file.close()
  return Lines

def scrub():
    files=sorted(glob.glob("/Users/rajaramaniyer/books/narayaneeyam/narayaneeyam-???-tamil.txt"))

    found = False
    for file in files:
        lines = get_lines(file)
        with open(file, "w", encoding="UTF-8") as f:
            for line in lines:
                if re.search(r'^<p>', line):
                    found = True
                if found and re.search(r'^<hr />', line):
                    break
                if found:
                    f.write(line)

def visit(url, file_number):
    try:
        driver = webdriver.Chrome()
    except BaseException as err:
        print("Error",err)
        print("Download correct version of chromedriver\n\tFrom: https://chromedriver.chromium.org/downloads\n\tand save into C:\\Users\\rajar\\AppData\\Local\\Microsoft\\WindowsApps\\")
        input("Press enter to exit")
        sys.exit(1)

    driver.get(url)
    driver.implicitly_wait(30)

    p_tags = driver.find_elements(by=By.TAG_NAME, value="P")

    with open('/Users/rajaramaniyer/books/narayaneeyam/narayaneeyam-' + str(file_number).zfill(3) + '-tamil.txt', 'w', encoding='UTF-8') as f:
        for p_tag in p_tags:
            if not re.search(r'[A-Za-z]', p_tag.text):
                f.write(p_tag.text)
                f.write('\n')

visit("https://stotranidhi.com/ta/narayaneeyam-dasakam-"+str(100)+"-in-tamil/",100)

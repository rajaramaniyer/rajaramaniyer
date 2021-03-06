#!/opt/homebrew/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import os.path;
import glob
import wave, struct, contextlib
import uuid
import datetime, time, math
import re

#
# Main Code Starts
#
if len(sys.argv) < 4:
  adyayam_number = input ("Adhyayam Number: ")
  from_image = int(input ("From Image Number: "))
  to_image = int(input ("To Image Number: "))
else:
  adyayam_number=sys.argv[1]
  from_image = int(sys.argv[2])
  to_image = int(sys.argv[3])
root_folder="D:/Books/Bhagavatham/"
working_folder="jpg_with_hindi_anuvad/"
if len(sys.argv) == 5:
  working_folder = sys.argv[4] + "/"
archive_folder="archive/"

driver = webdriver.Chrome()
driver.get("https://ocr.sanskritdictionary.com/")
driver.implicitly_wait(30)

outputFile=open("C:/Users/rajar/srimad_bhaghavatham/sanskrit/canto10/chapter" + adyayam_number + ".txt", 'w', encoding='UTF-8')

while from_image <= to_image:
    imageFileName="page-%04d.jpg" %(from_image)
    fullArchiveFileName=root_folder + archive_folder + imageFileName
    fullImageFileName=root_folder + working_folder + imageFileName
    if not os.path.exists(fullImageFileName):
        print(fullImageFileName + " file does not exists")
        break
    pictureFile = driver.find_element(By.ID,"pictureFile")
    pictureFile.send_keys(fullImageFileName)
    print("Waiting for modal to show")
    WebDriverWait(driver, 30).until_not(EC.invisibility_of_element((By.ID, "loadingModal")))
    print("Waiting for modal to disappear")
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, "loadingModal")))
    print("Switching to iFrame")
    frameName=driver.find_element(By.ID, "tinymcetext_ifr")
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it(frameName))
    sanskritText = driver.find_element(By.ID, "tinymce")
    print ("sanskritText = %s" %(sanskritText.text))
    outputFile.write(sanskritText.text)
    outputFile.write("\n")
    ## Switch back to the "default content" (that is, out of the iframes) ##
    driver.switch_to.default_content()
    clearImageButton = driver.find_element(By.XPATH, '//a[text()="Clear Image"]')
    clearImageButton.click()
    if fullImageFileName != fullArchiveFileName:
      os.rename(fullImageFileName, fullArchiveFileName)
    from_image += 1

outputFile.close()
driver.close()
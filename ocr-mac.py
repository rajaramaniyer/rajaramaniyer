#!/opt/homebrew/opt/python@3.9/libexec/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import os.path;

#
# Main Code Starts
#
if len(sys.argv)< 4:
  adyayam_number = input ("Adhyayam Number: ")
  from_image = int(input ("From Image Number: "))
  to_image = int(input ("To Image Number: "))
else:
  adyayam_number=sys.argv[1]
  from_image = int(sys.argv[2])
  to_image = int(sys.argv[3])
root_folder="/Users/rajaramaniyer/Downloads/"
working_folder="RangaShathakam/"
if len(sys.argv) == 5:
  working_folder = sys.argv[4] + "/"
archive_folder="archive/"
image_file_template="Image-%02d.jpg"

try:
  driver = webdriver.Chrome()
except BaseException as err:
  print("Error",err)
  print("Download correct version of chromedriver\n\tFrom: https://chromedriver.chromium.org/downloads\n\tand save into C:\\Users\\rajar\\AppData\\Local\\Microsoft\\WindowsApps\\")
  input("Press enter to exit")
  sys.exit(1)

driver.get("https://ocr.sanskritdictionary.com/")
driver.implicitly_wait(30)

outputFile=open("/Users/rajaramaniyer/Downloads/ranga-shathakam-" + adyayam_number + ".txt", 'w', encoding='UTF-8')

while from_image<= to_image:
    imageFileName=image_file_template %(from_image)
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

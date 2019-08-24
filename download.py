from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import requests
import urllib
import os


delay = 100
brws_name = 'chrome'
filedir = ""
username = ""
password = ""


def get_accountinfo():
  account_file = open('./accountinfo.txt', 'r')
  account_info = account_file.readlines()
  return account_info[0], account_info[1]


def login(driver):
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    elem = driver.find_element_by_id('identifierId')
    elem.clear()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)
    time.sleep(3)
  except TimeoutException:
    print("Loading took too much time!")

  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    elem = driver.find_element_by_class_name('whsOnd')
    elem.clear()
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
  except TimeoutException:
    print("Loading took too much time!")


def scroll_infi(driver):  
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))

    while True:
      try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 's5e-file-row')))
        elems = driver.find_elements_by_class_name('s5e-file-row')   
        l = len(elems)
        elems[l-1].click()
        if l == 520:
          break
      except TimeoutException:
        print("Loading took too much time!")
  except TimeoutException:
    print("Loading took too much time!")


def get_hrefs(driver):
  try:
    tm_elem = driver.find_element_by_xpath('//div/fb-appbar')
    driver.execute_script('arguments[0].style.display="none"', tm_elem)
    
  except TimeoutException:
    print("Loading took too much time!")
  
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//ng-transclude/span/md-icon')))
    elems = driver.find_elements_by_xpath('//ng-transclude/span/md-icon')
    print(len(elems))
    
  except TimeoutException:
    print("Loading took too much time!")

  for i in range(520):
    elems[519-i].find_element_by_xpath('..').find_element_by_xpath('..').click()
    print("clicked {}".format(i))

    link_elem = driver.find_element_by_xpath('//storage-side-panel/div/div/div/a')

    filename = driver.find_element_by_xpath('//fb-card-drawer-header/h4').text.strip().split()[1]

    if not os.path.exists(filedir):
      os.makedirs(filedir)

    link = link_elem.get_attribute('href')
    f = urllib.request.urlopen(link)
    myfile = f.read()

    writeFileObj = open(filedir+'/'+filename, 'wb')
    writeFileObj.write(myfile)
    writeFileObj.close()
    time.sleep(1)


txt_file = open('./urls.txt', 'r')
list_urls = txt_file.readlines()
if brws_name == 'firefox': driver = webdriver.Firefox(executable_path='./drivers/geckodriver') 
else: driver = webdriver.Chrome(executable_path='./drivers/chromedriver') 

loggedin = False

username, password = get_accountinfo()

for url in list_urls: 
  spl = url.split()
  filedir = "wavs/"+spl[0]
  urll = spl[1]
  driver.get(urll)
  if not loggedin:
    login(driver)
    loggedin = True
  scroll_infi(driver)
  get_hrefs(driver)


driver.close()
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep
import pandas as pd

driver_path = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(options=chrome_options, service=service)
driver.implicitly_wait(20)

def userLogin(driver, username, passwd):
    driver.get("https://www.linkedin.com")
    # Login with supplied user account
    driver.find_element(By.ID, "session_key").send_keys(username)
    driver.find_element(By.ID, "session_password").send_keys(passwd)
    driver.find_element(By.ID, "session_password").submit()

def sendMessage(driver, messagingThreadID, msg):
    # Browse to messaging - This will load the latest focused conversation
    driver.get(f'https://www.linkedin.com/messaging/thread/{messagingThreadID}/')
    form = driver.find_element(By.XPATH, '//*[@id="msg-form-ember67"]/div[3]/div/div[1]/div[1]')
    form.send_keys(msg)
    form.submit()

def readLastMessage(driver, messagingThreadID):
    source = driver.page_source
    soup = bs(source)
    lis = soup.findAll('li')
    msgs = []
    for li in lis:
        if 'class' in li.attrs.keys():
            if 'msg-s-message-list__event' in li['class']:
                msgs.append(li)
    lastMsg = msgs[len(msgs)-1]
    return lastMsg.findAll('p')[0].text


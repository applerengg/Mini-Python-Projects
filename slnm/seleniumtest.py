from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


browser = webdriver.Chrome(r"C:\Users\Administrator\Desktop\chromedriver.exe")
browser.get("https://google.com")
time.sleep(3)

searchbox = browser.find_element_by_name("q")
searchbox.send_keys("appleren-the-original")
time.sleep(1)

searchbox.send_keys(Keys.RETURN)


browser.close()


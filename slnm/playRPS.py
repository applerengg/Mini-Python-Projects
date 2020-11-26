from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from random import choice

driver = webdriver.Chrome(r"C:\Users\Administrator\Desktop\chromedriver.exe")
driver.set_window_size(400, 600)
driver.set_window_position(780, 324)
driver.get("https://www.afiniti.com/corporate/rock-paper-scissors")
# time.sleep(30)
time.sleep(5)

buttons = driver.find_elements_by_class_name("rock-paper-scissors__svgButton--38SiM")

while 1:
	choice(buttons).click()
	time.sleep(1)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


# https://thispersondoesnotexist.com/
driver = webdriver.Chrome(r"C:\Users\Administrator\Desktop\chromedriver.exe")
driver.set_window_size(400, 600)
driver.set_window_position(780, 324)
driver.get("https://thispersondoesnotexist.com/")
time.sleep(3)

while 1:
	try:
		driver.refresh()
		time.sleep(3)
	except WebDriverException:
		break
	
# driver.close()



from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService 
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")
print(driver.title)
driver.close()

from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses



## create a web driver instance (must be in the same directory as the script)
driver = webdriver.Chrome()     ## opens a Chrome browser window

## load a website
driver.get("https://www.python.org")    ## waits for the page to load completely

## check page title
print(driver.title) 


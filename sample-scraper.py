
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document



## create a web driver instance (only few browsers are supported)
driver = webdriver.Chrome()     ## opens a Chrome browser window

## load a website
driver.get("https://www.python.org")    ## waits for the page to load completely

## check page title
print(f'page title: {driver.title}') 
assert "Python" in driver.title

## interact with the search bar
search_bar = driver.find_element(By.NAME, 'q')  ## finds search bar element
search_bar.clear()                              ## clears any existing text
search_bar.send_keys('pycon')                   ## types query into the search bar
search_bar.send_keys(Keys.RETURN)               ## simulates pressing return key

## check the updated url
print(f'new url: {driver.current_url}')
assert "No results found." not in driver.page_source    ## check that some results were found

## close the tab
driver.close()

## close the window
# driver.quit()



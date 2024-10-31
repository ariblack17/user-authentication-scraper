## a basic program that takes in a webpage, scrapes its content, and checks if cookies
## are used as a user authentication method

## ---------------------------------------------------------------- ##

## imports 
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document

## ---------------------------------------------------------------- ##

## helper function
def parse_cookies():
    ''' returns an array of cookies/tokens likely used for authentication '''

    auth_cookies = []                       ## array of authentication cookies/tokens
    cookie_words = {'xsrf', 'token', 'sso'} ## words commonly used in auth cookies/tokens
    
    for cookie in cookies:
        if any(word in cookie['name'].lower() for word in cookie_words):
            auth_cookies.append(cookie)

    print(f'found {len(auth_cookies)} authentication cookies')
    return auth_cookies


## helper function
def write_file():
    ''' writes website and cookies to a txt file '''

    with open('./cookies/check-cookies.txt', 'w') as f: ## if running from root
        f.write(f'{website}\n')         ## website url header
        for cookie in auth_cookies:
            f.write(f'{cookie}\n')      ## cookies

## ---------------------------------------------------------------- ##

## create a web driver instance (only few browsers are supported)
driver = webdriver.Chrome()     ## opens a Chrome browser window

## other variables
# website = 'https://profile.callofduty.com/cdl/login'    ## site that has cookies/tokens
website = 'https://www.activision.com/'                 ## site that has cookies/tokens
website2 = "https://www.python.org"

## load a website
driver.get(website)

## get cookies
cookies = driver.get_cookies()
print(f'\nfound {len(cookies)} cookies for {website}')

## parse cookies (not all cookies are for authentication)
auth_cookies = parse_cookies()

## write to txt file
write_file()


## -- program exit -- ##


## close the tab
driver.close()

## close the window
# driver.quit()


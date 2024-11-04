
## a temporary program to run all user authentication scraping programs
## in sub-directories
## ---------------------------------------------------------------- ##

## imports 
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document

from captcha import check_captcha as cap
from cookies import check_cookies as coo
from oauth import check_oauth as oau
from passwords import check_passwords as pas

## ---------------------------------------------------------------- ##

## helper function
def write_file():
    ''' writes website and results to a txt file '''

    with open('./tmp_results.txt', 'w') as f:
        f.write(f'{website}\n')         ## website url header

        ## cookies
        if len(auth_cookies) > 0:
            f.write('COOKIE/TOKEN BASED AUTHENTICATION\n')

        ## passwords
        if len(login_links) > 0:
            f.write('PASSWORD BASED AUTHENTICATION\n')

        ## general oauth
        if len(oauth_providers) > 0:
            f.write('SSO/OAUTH BASED AUTHENTICATION\n')

        ## FIDO2 oauth
        if fido2:
            f.write('FIDO2/PASSWORDLESS AUTHENTICATION\n')
        


## ---------------------------------------------------------------- ##

website1 = 'https://www.activision.com/'                 
website2 = 'https://www.formula1.com/'      ## broken, since its html structure is weird
website3 = 'https://www.python.org'
website4 = 'https://www.ebay.com/'  ## doesn't always work, and only finds facebook
                                    ## (^ broken when blocked by bot-detection)
website5 = 'https://soundcloud.com/'
website6 = 'https://bestbuy.com/'   ## has fido2
website7 = 'https://twitter.com/i/flow/login'   ## nav to login from home page is weird,
                                                ## naming conventions are unconventional
website8 = 'https://en.wikipedia.org/'

## ---------------------------------------------------------------- ##

## create a web driver instance (only few browsers are supported)
driver = webdriver.Safari()     ## opens a browser window
options = webdriver.SafariOptions()
options.add_argument('--enable-javascript')

## choose a site for testing
website = website3

## load a website
driver.get(website)
print(f'url: {driver.current_url}')

## ---------------------------------------------------------------- ##

## get cookies
cookies = driver.get_cookies()
print(f'\nfound {len(cookies)} cookies for {website}')

## parse cookies
auth_cookies = coo.parse_cookies(cookies)

## ---------------------------------------------------------------- ##

## get all login links (by tag name)
login_links = pas.get_login_links(driver, By.TAG_NAME, 'a')

## get all links (by class name, if tag name did not work)
if len(login_links) == 0: login_links = pas.get_login_links(driver, By.CLASS_NAME, 'a')
print(f'{len(login_links)} login links found')

## click on the first login link
if login_links: 
    login_link = login_links[0]
    driver.get(login_link)
    print(f'new url: {driver.current_url}')

## check if there's a uname/pswd field 
username_id = pas.find_login_field(driver, By.ID)   ## by id
if not username_id: username_name = pas.find_login_field(driver, By.NAME) ## by name (if id didn't work)
if not username_id and not username_name: username_class = pas.find_login_field(driver, By.CLASS_NAME)  ## by class name

## ---------------------------------------------------------------- ##

## check if there's a captcha (by id)
captcha_id = cap.find_captcha(driver)

## ---------------------------------------------------------------- ##

## check if there are any general oauth/sso options
providers = []
oauth_providers = oau.find_oauth(driver, providers, 'href') 
if len(oauth_providers) == 0: 
    oauth_providers = oau.find_oauth(driver, 'onclick') 
    oauth_providers = oau.find_oauth(driver, 'id')  

## check if there is any fido2 option
fido2 = oau.find_fido2(driver)

## ---------------------------------------------------------------- ##

write_file()

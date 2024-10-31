## a basic program that takes in a webpage, scrapes its content, navigates to the
## login page, then checks if the user can sign in via OAuth

## ---------------------------------------------------------------- ##

## imports 
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document

## ---------------------------------------------------------------- ##

## helper function
def write_file(website):
    ''' writes website and login links to a txt file '''

    with open('./captcha/check-captcha.txt', 'w') as f: ## if running from root
        f.write(f'{website}\n')         ## website url header
        for link in login_links:
            f.write(f'{link}\n')        ## links

## helper function
def get_login_links(by, value):
    ''' finds and returns matching login-related links on the web page (where a captcha may be)'''

    login_links = []
    login_terms = {'login', 'log in', 'signin', 'sign in'}

    ## get all links
    links = driver.find_elements(by, value)              
    if len(links) > 0: print(f'{len(links)} links found')
    for link in links:
        url = link.get_attribute('href')                        ## isolate the url
        if url and any(term in url for term in login_terms):    ## append only login links
            login_links.append(url)

    return login_links

## helper function
def find_login_field(by):
    ''' finds matching login-related fields on the web page, returns True if found '''

    username_words = {'username', 'accountName', 'loginform', 'userid', 
                  'user', 'acctName', 'login'}
    
    ## look for username- and login-related words on the web page
    for word in username_words:
        username = driver.find_elements(by, word)
        if len(username) > 0:
            print(f'found login field -- password based authentication detected')
            return True
    
    return False


## helper function
def find_oauth():
    ''' finds matching  '''
    pass


## ---------------------------------------------------------------- ##

## create a web driver instance (only few browsers are supported)
driver = webdriver.Safari()     ## opens a browser window
options = webdriver.SafariOptions()
options.add_argument('--enable-javascript')

## other variables
website1 = 'https://www.activision.com/'                 
website2 = 'https://www.formula1.com/'      ## broken, since its html structure is weird
website3 = 'https://www.python.org'
website4 = 'https://www.ebay.com/'

## choose a site for testing
website = website4

## load a website
driver.get(website)
print(f'url: {driver.current_url}')


## -- finding links to a login page -- ##


## get all links (by tag name)
login_links = get_login_links(By.TAG_NAME, 'a')

## get all links (by class name, if tag name did not work)
if len(login_links) == 0: login_links = get_login_links(By.CLASS_NAME, 'a')
print(f'{len(login_links)} login links found')


## -- navigating to the login page -- ##


## click on the first login link
if login_links: 
    login_link = login_links[0]
    driver.get(login_link)
    print(f'new url: {driver.current_url}')


## -- finding oauth -- ##

## check if there are any oauth options (by id)
oauth_id = find_oauth() ## TODO: output all found oauth methods to text file?

## output negative results
if not oauth_id:
    print(f'no oauth options detected')


## -- program exit -- ##


## close the tab
driver.close()

## close the window
# driver.quit()


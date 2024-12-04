## a basic program that takes in a webpage, scrapes its content, navigates to the
## login page, then checks if the user can sign in via OAuth

## ---------------------------------------------------------------- ##

## imports 
import requests
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document
from selenium.webdriver.chrome.service import Service
import time
# from webdriver_manager.chrome import ChromeDriverManager

## ---------------------------------------------------------------- ##

## helper function
def write_file(fido2):
    ''' writes website and login links to a txt file '''

    with open('check_oauth.txt', 'w') as f: ## if running from root
        f.write(f'{website}\n')         ## website url header
        if fido2:
            f.write(f'FIDO2')
        for provider in providers:
            f.write(f'{provider}\n')    ## providers


## helper function
def get_login_links(by, value):
    ''' finds and returns matching login-related links on the web page (where sso may be)'''

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
def find_oauth(driver, by):
    ''' finds matching  '''
    return find_providers(driver, [], by)

## helper function
def find_providers(driver, providers, by):
    ''' searches for common OAuth provider names, returns an array of all matching names '''
    oauth_signs = {'client_id', 'redirect_uri', 'response_type=code', 'scope'}

    ## look for username- and login-related words on the web page
    for sign in oauth_signs:
        
        ## check if href link includes provider name anywhere within the string
        found_providers = driver.find_elements(By.XPATH, f"//script[contains(text(), {sign})]")
        if found_providers: providers.append(sign)

    if len(providers) > 0:
        print(f'oauth found -- {providers} sso authentication detected')
        
    return providers

def find_fido2(driver):
    ''' searches the page and returns True if FIDO2 is likely used for authentication '''
    fido_signs = {'navigator.credentials.create', 'navigator.credentials.get'}
    # fido_signs = {'attestation', 'userVerification', 'pubKeyCredParams', 'allowCredentials'}
    # look for fido-related words on the web page      

    # if (driver.find_elements(By.XPATH, f"//script[contains(text(), 'navigator.credentials.create')]") and driver.find_elements(By.XPATH, f"//script[contains(text(), 'navigator.credentials.get')]")):
    #     print(f'found fido-related word -- fido authentication detected')
    #     return True
    fido2_signs = {"'X-FIDO2-Request': 'true'", }
    for sign in fido_signs:
        if driver.find_elements(By.XPATH, f"//script[contains(text(), {sign})]"):
            print(f'found fido-related word -- fido authentication detected')
            print(f'word: {sign}')
            return True
    print("fido2 not found")
    return False





## ---------------------------------------------------------------- ##

if __name__ == '__main__':
    ## create a web driver instance (only few browsers are supported)
    driver = webdriver.Chrome()     ## opens a browser window
    options = webdriver.ChromeOptions()
    options.add_argument('--enable-javascript')

    ## other variables
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

    providers = []

    ## choose a site for testing
    website = website2

    ## load a website
    driver.get(website)
    print(f'url: {driver.current_url}')

    html = driver.page_source

    # resp = requests.get(website)
    # print(resp.request.body)
    # headers = resp.headers.get('Content-Type')
    # print(headers)

    ## -- finding links to a login page -- ##


    ## get all links (by tag name)
    login_links = get_login_links(By.TAG_NAME, 'a')

    ## get all links (by class name, if tag name did not work)
    if len(login_links) == 0: login_links = get_login_links(By.CLASS_NAME, 'a')
    print(f'{len(login_links)} login links found')


    ## -- navigating to the login page -- ##

    # try all login links
    if login_links: 
        for login_link in login_links:
            try:
                driver.get(login_link)
                print(f'new url: {driver.current_url}')

                # resp = requests.get(login_link)
                # print("I AM HERE")
                # print(resp.request.body)
                # # j = resp.json()
                # # print(j, "jerere")
                # print(resp.text)
                # print("I AM HERE")
                # headers = resp.headers.get('Content-Type')
                # print(headers)

                # -- finding oauth -- ##
                oauth_providers = find_oauth(driver, 'href') 
                if len(oauth_providers) == 0: 
                    oauth_providers = find_oauth(driver, 'onclick')  ## try searching by id otherwise
                    oauth_providers = find_oauth(driver, 'id')  ## try searching by id otherwise

                if len(oauth_providers) == 0:
                    print(f'no general sso options detected')

                fido2 = find_fido2(driver)
                ## write to txt file
                write_file(fido2)
            except:
                continue
    else:
        # -- finding oauth -- ##
        oauth_providers = find_oauth(driver, 'href') 
        if len(oauth_providers) == 0: 
            oauth_providers = find_oauth(driver, 'onclick')  ## try searching by id otherwise
            oauth_providers = find_oauth(driver, 'id')  ## try searching by id otherwise
        
        if len(oauth_providers) == 0:
            print(f'no general sso options detected')

        fido2 = find_fido2(driver)
        ## write to txt file
        write_file(fido2)

    ## -- program exit -- ##


    ## close the tab
    driver.close()

    ## close the window
    # driver.quit()

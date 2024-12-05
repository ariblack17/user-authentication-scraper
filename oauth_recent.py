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
# def find_oauth(driver, url):
#     ''' searches for common OAuth provider names, returns an array of all matching names '''
#     header = {'Authorization': 'invalid_token'}
#     resp = requests.get(url)
#     auth = resp.headers.get("Authorization")
#     www_auth = resp.headers.get('WWW-Authenticate')
#     ## look for username- and login-related words on the web page
#     if ((resp.status_code == 301) or (resp.status_code == 302)):
#         print("here, OAuth likely")
#     if ((resp.status_code == 401) and ('Bearer' in www_auth)):
#         print("OAuth definitely detected. SUCCESS.")
#         return True
#     print("HERE\n\n")
#     # if ('Bearer' in www_auth):
#     #     print("OAuth definitely detected. SUCCESS.")
#     #     return True
#     # if ('Bearer' in auth):
#     #     print("OAuth definitely detected. SUCCESS.")
#     #     return True
#     if (www_auth):
#         print("OAuth probably detected. Less success.")
#         return True
#     print("OAuth not detected. FAILURE.")
#     print(f"Resp Stat: {resp.status_code}, WWW-Auth: {www_auth}")
#     return False

def find_oauth(driver, url):
    ''' searches for common OAuth provider names, returns an array of all matching names '''
    ## look for username- and login-related words on the web page
    links = driver.find_elements(By.TAG_NAME, 'a')
    new_links = list()
    for link in links:
        try:
            url = link.get_attribute('href')  
            driver.get(url)
            new_links.extend(driver.find_elements(By.TAG_NAME, 'a'))
        except:
            continue
    for link in new_links:
        try:
            url = link.get_attribute('href')  
            driver.get(url)
            new_links.extend(driver.find_elements(By.TAG_NAME, 'a'))
        except:
            continue
    print(links)
    perf_log = driver.get_logs("performance")

    for log in perf_log:
        msg = log.get("message")
        if (msg):
            if ("oauth" in msg.lower()):
                print(f"OAuth likely: {msg}")
                return True
    print("OAuth not detected. FAILURE.")
    return False

# def find_fido2(driver, response):
#     ''' searches the page and returns True if FIDO2 is likely used for authentication '''
#     fido_signs = {'navigator.credentials.create', 'navigator.credentials.get'}
#     fido_signs = {'attestation', 'userVerification', 'pubKeyCredParams', 'allowCredentials'}
#     # look for fido-related words on the web page      

#     # if (driver.find_elements(By.XPATH, f"//script[contains(text(), 'navigator.credentials.create')]") and driver.find_elements(By.XPATH, f"//script[contains(text(), 'navigator.credentials.get')]")):
#     #     print(f'found fido-related word -- fido authentication detected')
#     #     return True
#     fido2_signs = {"'X-FIDO2-Request': 'true'", }
#     for sign in fido_signs:
#         if driver.find_elements(By.XPATH, f"//script[contains(text(), {sign})]"):
#             print(f'found fido-related word -- fido authentication detected')
#             print(f'word: {sign}')
#             return True
#     print("fido2 not found")
#     return False

def find_fido2(driver, url):
    ''' searches for common OAuth provider names, returns an array of all matching names '''
    ## look for username- and login-related words on the web page
    links = driver.find_elements(By.TAG_NAME, 'a')
    new_links = list()
    for link in links:
        try:
            url = link.get_attribute('href')  
            driver.get(url)
            new_links.extend(driver.find_elements(By.TAG_NAME, 'a'))
        except:
            continue
    for link in new_links:
        try:
            url = link.get_attribute('href')  
            driver.get(url)
            new_links.extend(driver.find_elements(By.TAG_NAME, 'a'))
        except:
            continue
    perf_log = driver.get_logs("performance")

    for log in perf_log:
        msg = log.get("message")
        if (msg):
            if ("webauthn" in msg.lower()):
                print(f"Fido2 likely: {msg}")
                return True
    print("Fido2 not detected. FAILURE.")
    return False

def find_captcha(driver, url):
    ''' finds matching login-related fields on the web page, returns True if found '''

    resp = requests.get(url)
    x_cap = resp.headers.get("X-Captcha")
    cookie = resp.headers.get('Set-Cookie')
    ## look for username- and login-related words on the web page
    if (x_cap):
        print("Captcha definitely detected. SUCCESS.")
        return True
    elif (cookie):
        if ('captcha_verified' in cookie):
            print("Captcha definitely detected. SUCCESS.")
            return True
    print(f"Captcha not detected. FAILURE. Cookie:{cookie}, Cap:{x_cap}")
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
    website9 = 'https://en.wikipedia.org/w/index.php?title=Special:UserLogin&returnto=Main+Page'

    providers = []

    ## choose a site for testing
    website = website8

    ## load a website
    driver.get(website)
    print(f'url: {driver.current_url}')

    driver.execute_cdp_cmd("Network.enable", {})

    html = driver.page_source

    resp = requests.get(website)
    print(resp.request.body)
    headers = resp.headers.get('Content-Type')
    print(headers)

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

                resp = requests.get(login_link)
                # print("I AM HERE")
                # print(resp.request.body)
                # print(resp.text)
                # print("I AM HERE")
                # headers = resp.headers.get('Content-Type')
                # print(headers)

                # -- finding oauth -- ##
                oauth_providers = find_oauth(driver, login_link) 

                fido2 = find_fido2(driver, resp)
                ## write to txt file
                write_file(fido2)

                captcha_id = find_captcha(driver, login_link)
            except:
                continue
    else:
        # -- finding oauth -- ##
        oauth_providers = find_oauth(driver, website) 
        
        fido2 = find_fido2(driver, resp)
        ## write to txt file
        write_file(fido2)

        captcha_id = find_captcha(driver, website)
    ## -- program exit -- ##

    ## close the tab
    driver.close()

    ## close the window
    # driver.quit()

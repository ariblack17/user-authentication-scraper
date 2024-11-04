## a basic program that takes in a webpage, scrapes its content, 
## and checks if a password box is present in the html
## ---------------------------------------------------------------- ##

## imports 
from selenium import webdriver                  ## to control the browser
from selenium.webdriver.common.keys import Keys ## to simulate key presses
from selenium.webdriver.common.by import By     ## to locate elements within a document

## ---------------------------------------------------------------- ##

## helper function
def write_file(website):
    ''' writes website and login links to a txt file '''

    with open('./passwords/check_passwords.txt', 'w') as f: ## if running from root
        f.write(f'{website}\n')         ## website url header
        for link in login_links:
            f.write(f'{link}\n')        ## links


## helper function
def get_write_html():
    ''' stores html source file locally '''

    html = driver.page_source
    with open('./passwords/page.html', 'w') as f: ## if running from root
        f.write(html)


## helper function
def get_login_links(driver, by, value):
    ''' finds and returns matching login-related links on the web page '''

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
def find_login_field(driver, by):
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


## ---------------------------------------------------------------- ##

if __name__ == '__main__':
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
    website = website1

    ## load a website
    driver.get(website)
    print(f'url: {driver.current_url}')


    ## -- finding links to a login page -- ##


    ## get all links (by tag name)
    login_links = get_login_links(driver, By.TAG_NAME, 'a')

    ## get all links (by class name, if tag name did not work)
    if len(login_links) == 0: login_links = get_login_links(driver, By.CLASS_NAME, 'a')
    print(f'{len(login_links)} login links found')

    ## write links to file
    # write_file(website)


    ## -- navigating to the login page -- ##


    ## click on the first login link
    if login_links: 
        login_link = login_links[0]
        driver.get(login_link)
        print(f'new url: {driver.current_url}')


    ## -- finding a username/password field -- ##


    ## check if there's a uname/pswd field (indicates password based authentication)
    ## looking for an object/element with a matching id/class/name
    username_id = find_login_field(driver, By.ID)   ## by id
    if not username_id: username_name = find_login_field(driver, By.NAME) ## by name (if id didn't work)
    if not username_id and not username_name: username_class = find_login_field(driver, By.CLASS_NAME)  ## by class name

    ## output negative results
    if not username_id and not username_name and not username_class:
        print(f'no login field detected')


    ## -- program exit -- ##


    ## close the tab
    driver.close()

    ## close the window
    # driver.quit()


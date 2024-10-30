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

    with open('./passwords/check-passwords.txt', 'w') as f: ## if running from root
        f.write(f'{website}\n')         ## website url header
        for link in login_links:
            f.write(f'{link}\n')      ## links

## helper function
def get_write_html():
    ''' stores html source file locally '''

    html = driver.page_source

    with open('./passwords/page.html', 'w') as f: ## if running from root
        f.write(html)
    


## ---------------------------------------------------------------- ##

## create a web driver instance (only few browsers are supported)
driver = webdriver.Safari()     ## opens a browser window
options = webdriver.SafariOptions()
options.add_argument('--enable-javascript')

## other variables
website1 = 'https://www.activision.com/'                 
website2 = 'https://www.formula1.com/'      ## broken, not sure why
website3 = "https://www.python.org"
website4 = 'https://www.ebay.com/'

## choose a site for testing
website = website4

## load a website
driver.get(website)
print(f'url: {driver.current_url}')

login_links = []
login_terms = {'login', 'log in', 'signin', 'sign in'}


## get all links (by tag name)
links = driver.find_elements(By.TAG_NAME, "a")              ## <a> tag for links
print(f'{len(links)} links found')
for link in links:
    url = link.get_attribute('href')                        ## isolate the url
    if url and any(term in url for term in login_terms):    ## append only login links
        login_links.append(url)


## get all links (by class name, if tag name did not work)
if len(login_links) == 0:
    links = driver.find_elements(By.CLASS_NAME, "a")              ## <a> tag for links
    print(f'{len(links)} links found')
    for link in links:
        url = link.get_attribute('href')                        ## isolate the url
        if url and any(term in url for term in login_terms):    ## append only login links
            login_links.append(url)
    print(f'{len(login_links)} login links found')
else:
    print(f'{len(login_links)} login links found')

## write to file
write_file(website)


## click on the first login link
login_link = login_links[0]
driver.get(login_link)
print(f'new url: {driver.current_url}')


## check if there's a uname/pswd field (indicates password based authentication)






## locate and click on login link
# driver.find_element(By.PARTIAL_LINK_TEXT, 'Login').click()

# driver.find_element(By.LINK_TEXT, 'Login').click()

# login_link = driver.find_element(By.LINK_TEXT, "Login")
# login_link = driver.find_element(By.PARTIAL_LINK_TEXT, "e")
# print()
# print(login_link)
# login_link.click()

# print(f'new url: {driver.current_url}')




## close the tab
driver.close()

## close the window
# driver.quit()


## Imports
from selenium import webdriver                  ## Control browser
from selenium.webdriver.common.by import By     ## Locate elements
from selenium.webdriver.common.keys import Keys ## Simulate key presses

## ---------------------------------------------------------------- ##

## Helper Function: Write Results to File
def write_file(fido2, website):
    ''' Writes FIDO2 detection results to a text file '''
    with open('./fido2_check_results.txt', 'a') as f:  # Append results
        f.write(f'Website: {website}\n')
        if fido2:
            f.write('FIDO2 Detected: Yes\n\n')
        else:
            f.write('FIDO2 Detected: No\n\n')

## Helper Function: Get Login Links
def get_login_links(driver):
    ''' Finds and returns matching login-related links on the web page '''
    login_links = []
    login_terms = {'login', 'log in', 'signin', 'sign in'}
    
    links = driver.find_elements(By.TAG_NAME, 'a')  # Get all links
    if len(links) > 0:
        print(f'{len(links)} links found.')
        for link in links:
            url = link.get_attribute('href')  # Extract the URL
            if url and any(term in url.lower() for term in login_terms):  # Check for login terms
                login_links.append(url)
    return login_links

## Helper Function: Find FIDO2 Keywords
def find_fido2(driver):
    ''' Searches for FIDO2/WebAuthn-related keywords '''
    fido_words = {'passkey', 'passwordless', 'webauthn'}
    for word in fido_words:
        # Check for keywords in IDs, classes, or links
        if driver.find_elements(By.XPATH, f'//*[contains(@id, "{word}") or contains(@class, "{word}") or contains(text(), "{word}")]'):
            print(f'Found FIDO2-related word: {word}')
            return True
    return False

## ---------------------------------------------------------------- ##

if __name__ == '__main__':
    # Create WebDriver instance (use a supported browser)
    driver = webdriver.Chrome()  # Replace with the path to your WebDriver, if needed

    # Websites for testing
    websites = [
    'https://www.khanacademy.org/',
    'https://www.edx.org/',
    'https://www.coursera.org/',
    'https://www.udemy.com/',
    'https://www.futurelearn.com/',
    'https://www.open.edu/',
    'https://www.classcentral.com/',
    'https://ocw.mit.edu/',
    'https://www.saylor.org/',
    'https://www.w3schools.com/',
    'https://www.codecademy.com/',
    'https://www.duolingo.com/',
    'https://www.hackerrank.com/',
    'https://www.brainpop.com/',
    'https://www.memrise.com/',
    'https://www.nationalgeographic.com/',
    'https://www.discoveryeducation.com/',
    'https://www.unicef.org/',
    'https://www.scientificamerican.com/',
    'https://www.ted.com/',
    'https://www.amazon.com/',
    'https://www.ebay.com/',
    'https://www.etsy.com/',
    'https://www.walmart.com/',
    'https://www.bestbuy.com/',
    'https://www.target.com/',
    'https://www.aliexpress.com/',
    'https://www.homedepot.com/',
    'https://www.wayfair.com/',
    'https://www.macys.com/',
    'https://www.nordstrom.com/',
    'https://www.costco.com/',
    'https://www.newegg.com/',
    'https://www.zappos.com/',
    'https://www.asos.com/',
    'https://www.overstock.com/',
    'https://www.gap.com/',
    'https://www.shein.com/',
    'https://www.lululemon.com/',
    'https://www.shopify.com/',
    'https://www.wikipedia.org/',
    'https://www.britannica.com/',
    'https://www.howstuffworks.com/',
    'https://www.healthline.com/',
    'https://www.mayoclinic.org/',
    'https://www.webmd.com/',
    'https://www.imdb.com/',
    'https://www.weather.com/',
    'https://www.quora.com/',
    'https://www.stackoverflow.com/',
    'https://www.snopes.com/',
    'https://www.dictionary.com/',
    'https://www.thesaurus.com/',
    'https://www.space.com/',
    'https://www.nasa.gov/',
    'https://www.timeanddate.com/',
    'https://www.usgs.gov/',
    'https://www.npr.org/',
    'https://www.cia.gov/the-world-factbook/',
    'https://www.history.com/',
    'https://www.nytimes.com/',
    'https://www.washingtonpost.com/',
    'https://www.theguardian.com/',
    'https://www.bbc.com/news',
    'https://www.cnn.com/',
    'https://www.reuters.com/',
    'https://www.aljazeera.com/',
    'https://www.nbcnews.com/',
    'https://www.abcnews.go.com/',
    'https://www.forbes.com/',
    'https://www.economist.com/',
    'https://www.bloomberg.com/',
    'https://www.nationalgeographic.com/',
    'https://www.wsj.com/',
    'https://www.huffpost.com/',
    'https://www.politico.com/',
    'https://www.propublica.org/',
    'https://www.apnews.com/',
    'https://www.axios.com/',
    'https://www.vox.com/',
    'https://www.chase.com/',
    'https://www.bankofamerica.com/',
    'https://www.wellsfargo.com/',
    'https://www.citi.com/',
    'https://www.usbank.com/',
    'https://www.capitalone.com/',
    'https://www.americanexpress.com/',
    'https://www.discover.com/',
    'https://www.barclays.com/',
    'https://www.hsbc.com/',
    'https://www.goldmansachs.com/',
    'https://www.tdbank.com/',
    'https://www.pnc.com/',
    'https://www.schwab.com/',
    'https://www.fidelity.com/',
    'https://www.paypal.com/',
    'https://www.sofi.com/',
    'https://www.robinhood.com/',
    'https://www.venmo.com/',
    'https://www.zellepay.com/',
    'https://www.facebook.com/',
    'https://www.instagram.com/',
    'https://www.twitter.com/',
    'https://www.linkedin.com/',
    'https://www.tiktok.com/',
    'https://www.snapchat.com/',
    'https://www.pinterest.com/',
    'https://www.reddit.com/',
    'https://www.tumblr.com/',
    'https://www.twitch.tv/',
    'https://www.youtube.com/',
    'https://www.discord.com/',
    'https://www.whatsapp.com/',
    'https://www.telegram.org/',
    'https://www.wechat.com/',
    'https://www.vk.com/',
    'https://www.quora.com/',
    'https://www.flickr.com/',
    'https://www.meetup.com/',
    'https://www.nextdoor.com/'
]

    for website in websites:
        print(f'\nChecking website: {website}')
        try:
            # Load the website
            driver.get(website)
            print(f'Current URL: {driver.current_url}')

            # Find login links
            login_links = get_login_links(driver)
            print(f'{len(login_links)} login links found.')

            # Navigate to the first login page, if any
            if login_links:
                login_link = login_links[0]
                driver.get(login_link)
                print(f'Navigated to login page: {driver.current_url}')

            # Check for FIDO2 support
            fido2 = find_fido2(driver)
            if fido2:
                print('FIDO2/WebAuthn detected!')
            else:
                print('No FIDO2/WebAuthn detected.')

            # Write results to file
            write_file(fido2, website)

        except Exception as e:
            print(f'Error checking website {website}: {e}')
        
    # Close the browser
    driver.quit()
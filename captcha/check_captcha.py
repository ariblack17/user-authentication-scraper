from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import random

def write_file(website, login_links, captcha_status):
    ''' writes website, login links, and captcha status to a txt file '''
    file_path = os.path.join(os.getcwd(), 'check_captcha_http_only_selenium.txt')  
    with open(file_path, 'a') as f:  ## append to file
        f.write(f'Website: {website}\n')  ## website url header
        for link in login_links:
            f.write(f'Login Link: {link}\n')  ## links
        f.write(f'Captcha Status: {captcha_status}\n')  ## Captcha found or not
        f.write('\n')

def get_login_links(driver):
    ''' Extract login-related links '''
    login_links = []
    login_terms = {'login', 'log in', 'signin', 'sign in'}
    links = driver.find_elements(By.TAG_NAME, 'a')  
    for link in links:
        url = link.get_attribute('href')
        if url and any(term in url.lower() for term in login_terms):  
            login_links.append(url)
    return login_links

def check_http_like_content(driver):
    ''' Checks for CAPTCHA-related HTTP-like content '''
    captcha_keywords = ['recaptcha', 'captcha', 'hcaptcha']
    captcha_detected = False

    # 1   Inspect <script>  tags for URLs or content
    scripts = driver.find_elements(By.TAG_NAME, 'script')
    for script in scripts:
        script_content = script.get_attribute('outerHTML') or ''
        if any(keyword in script_content.lower() for keyword in captcha_keywords):
            print(f"CAPTCHA-related content found in script: {script_content[:100]}...")
            captcha_detected = True
            break

    # 2 Inspect window object for CAPTCHA-related variables/functions
    try:
        window_content = driver.execute_script("return Object.keys(window);")
        for keyword in captcha_keywords:
            if any(keyword in key.lower() for key in window_content):
                print(f"CAPTCHA-related variable found in `window`: {key}")
                captcha_detected = True
                break
    except Exception as e:
        print(f"Error inspecting `window` object: {e}")

    return captcha_detected

if __name__ == '__main__':

    driver = webdriver.Chrome()

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

    # Clear file content before running
    file_path = os.path.join(os.getcwd(), 'check_captcha_http_only_selenium.txt')
    with open(file_path, 'w') as f:
        f.write('')  # Clear file

    for website in websites:
        try:
            driver.get(website)
            time.sleep(random.uniform(2, 5))  #delay to mimic human behavior

            login_links = get_login_links(driver)
            if login_links:
                driver.get(login_links[0])  # Navigate to the first login link
                time.sleep(random.uniform(2, 5))  # Delay for page load

            # Check HTTP-like content
            captcha_detected = check_http_like_content(driver)
            captcha_status = "Captcha Found" if captcha_detected else "No Captcha Found"
            print(f"{captcha_status} on {website}")

            write_file(website, login_links, captcha_status)
        
        except Exception as e:
            print(f"Error processing {website}: {e}")
    
    driver.quit()
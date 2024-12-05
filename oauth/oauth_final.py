from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Helper function to write results to a file
def write_file(website, oauth_detected, details=None, error=None, result_file='oauth_detected_sites.txt'):
    """Writes OAuth detection results to a single file."""
    with open(result_file, 'a') as f:
        f.write(f'Website: {website}\n')
        if error:
            f.write(f'Error: {error}\n\n')
        elif oauth_detected:
            f.write('OAuth Detected\n')
            if details:
                f.write('Details:\n')
                for detail in details:
                    f.write(f'  - {detail}\n')
            f.write('\n')
        else:
            f.write('OAuth Not Detected\n\n')

# Helper function to detect OAuth
def find_oauth(driver):
    """Detects if the page uses OAuth-based authentication logic."""
    oauth_detected = False
    detection_details = []

    try:
        # Check for OAuth-related redirect URLs in links
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href and any(param in href.lower() for param in ['response_type', 'client_id', 'redirect_uri', 'scope']):
                oauth_detected = True
                detection_details.append(f"OAuth-related redirect URL: {href}")
                print(f"OAuth-related redirect URL detected: {href}")

        # Check for forms containing OAuth logic
        forms = driver.find_elements(By.TAG_NAME, 'form')
        for form in forms:
            form_action = form.get_attribute('action')
            if form_action and any(param in form_action.lower() for param in ['authorize', 'token', 'oauth']):
                oauth_detected = True
                detection_details.append(f"Form action with OAuth logic: {form_action}")
                print(f"Form action with OAuth logic detected: {form_action}")

        # Check for JavaScript containing OAuth flow logic
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        for script in scripts:
            script_content = script.get_attribute('innerHTML')
            if script_content and any(token in script_content.lower() for token in ['access_token', 'refresh_token', 'authorization']):
                oauth_detected = True
                detection_details.append("JavaScript contains OAuth-related variables or logic.")
                print("OAuth detected via JavaScript script content.")

        # Check for query parameters in the current URL
        url = driver.current_url
        if any(param in url.lower() for param in ['code', 'state', 'scope', 'response_type']):
            oauth_detected = True
            detection_details.append(f"Current URL contains OAuth parameters: {url}")
            print(f"OAuth parameters detected in URL: {url}")

    except Exception as e:
        print(f"Error during OAuth detection: {e}")
        detection_details.append(f"Error: {e}")

    return oauth_detected, detection_details

# Helper function to handle pop-ups
def handle_popups(driver):
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert detected: {alert.text}")
        alert.dismiss()  # Dismiss the alert
    except:
        pass  # No alert present

    try:
        # Check for new pop-up windows
        main_window = driver.current_window_handle
        all_windows = driver.window_handles
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                print(f"Switched to pop-up window: {driver.title}")
                driver.close()  # Close the pop-up
                driver.switch_to.window(main_window)
    except Exception as e:
        print(f"Error handling pop-up: {e}")

# Main function
def main():
    result_file = 'oauth_detected_sites.txt'

    # Clear previous results
    with open(result_file, 'w') as f:
        f.write("OAuth Detection Results\n")
        f.write("=======================\n")

    # Set up Safari WebDriver
    driver = webdriver.Safari()
    driver.set_window_size(1024, 768)

    # List of websites to test
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
        print(f'\nTesting website: {website}')

        # Load the website with retries
        try:
            for attempt in range(2):  # Retry twice
                try:
                    driver.get(website)
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    handle_popups(driver)  # Handle any pop-ups
                    break
                except Exception as e:
                    if attempt == 1:
                        raise e
                    print(f"Retrying {website}...")

            print(f'Page Title: {driver.title}')
            print(f'Page URL: {driver.current_url}')

            # Simulate clicking "Login" or similar buttons
            try:
                login_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Log in') or contains(text(), 'Login') or contains(text(), 'Sign in')]")
                if login_buttons:
                    print(f"Login button detected: {len(login_buttons)}")
                    login_buttons[0].click()  # Click the first login button
                    time.sleep(3)  # Wait for login page to load
                    handle_popups(driver)  # Handle pop-ups again
            except Exception as e:
                print(f"Error clicking login: {e}")

            # Detect OAuth support
            oauth_detected, details = find_oauth(driver)

            # Write results to a single file
            write_file(website, oauth_detected, details=details, result_file=result_file)

        except Exception as e:
            print(f"Error loading website {website}: {e}")
            write_file(website, False, error=str(e), result_file=result_file)

    # Close the browser
    driver.quit()


if __name__ == '__main__':
    main()
from selenium import webdriver

# Helper function to write cookie results to a file
def write_file(website, cookies_detected, cookie_details=None, error=None, result_file='cookie_detected_sites.txt'):
    """Writes cookie detection results to a single file."""
    with open(result_file, 'a') as f:
        f.write(f'Website: {website}\n')
        if error:
            f.write(f'Error: {error}\n\n')
        elif cookies_detected:
            f.write('Cookies Detected\n')
            if cookie_details:
                f.write('Details:\n')
                for detail in cookie_details:
                    f.write(f'  - {detail}\n')
            f.write('\n')
        else:
            f.write('No Cookies Detected\n\n')

# Helper function to detect cookies
def find_cookies(driver):
    """Retrieves cookies and identifies those related to authentication."""
    cookie_details = []
    cookies_detected = False

    try:
        # Get all cookies for the current session
        cookies = driver.get_cookies()
        if cookies:
            cookies_detected = True
            for cookie in cookies:
                cookie_name = cookie.get("name", "N/A")
                cookie_value = cookie.get("value", "N/A")
                cookie_http_only = cookie.get("httpOnly", False)
                cookie_secure = cookie.get("secure", False)
                cookie_domain = cookie.get("domain", "N/A")

                detail = f'Cookie: {cookie_name}, Domain: {cookie_domain}, Secure: {cookie_secure}, HttpOnly: {cookie_http_only}, Value: {cookie_value[:50]}...'
                cookie_details.append(detail)

                # Log if the cookie appears to be related to authentication
                if "auth" in cookie_name.lower() or "session" in cookie_name.lower() or cookie_http_only:
                    cookie_details.append(f'  * Potential authentication cookie: {cookie_name}')

    except Exception as e:
        cookie_details.append(f"Error retrieving cookies: {e}")

    return cookies_detected, cookie_details

# Main function
def main():
    result_file = 'cookie_detected_sites.txt'

    # Clear previous results
    with open(result_file, 'w') as f:
        f.write("Cookie Detection Results\n")
        f.write("========================\n")

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
        try:
            # Start a new browser instance for each website
            driver = webdriver.Safari()  # Use Safari WebDriver
            print(f'\nTesting website: {website}')

            # Load the website
            driver.get(website)

            # Detect cookies
            cookies_detected, cookie_details = find_cookies(driver)

            # Write results to a single file
            write_file(website, cookies_detected, cookie_details=cookie_details, result_file=result_file)

        except Exception as e:
            print(f"Error loading website {website}: {e}")
            write_file(website, False, error=str(e), result_file=result_file)

        finally:
            # Clear cookies before moving to the next website
            try:
                driver.delete_all_cookies()
            except Exception as e:
                print(f"Error clearing cookies for {website}: {e}")

            # Close the browser
            driver.quit()


if __name__ == '__main__':
    main()
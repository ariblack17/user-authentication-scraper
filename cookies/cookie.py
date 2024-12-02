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
        'https://www.google.com/',
        'https://www.dropbox.com/login',
        'https://login.microsoftonline.com/',
        'https://www.ebay.com/',
        'https://soundcloud.com/',
        'https://twitter.com/i/flow/login',
        'https://example.com/',
        'https://www.gnu.org/',
        'https://textfiles.com/'
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
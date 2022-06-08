import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from credentials import *


def Chrome(headless=False):
    # add fake user agent
    chrome_options = Options()

    # return webdriver
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}

    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("user-agent={}".format(
    #     fake_useragent.UserAgent().random))
    # chrome_options.add_experimental_option(
    #     'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(
        executable_path=r'i://clients/chromedriver.exe', options=chrome_options, desired_capabilities=d)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def login():

    # get the element by for

    try:
        if driver.title == "Login | COINPAYU":
            print("info: Login page")
            try:
                driver.find_element_by_xpath(
                    '//html/body/div[1]/div/main/div/button').click()
            except Exception as e:
                print(e)
            try:
                email_input = driver.find_elements_by_xpath(
                    '//html/body/div[1]/div/main/div/div[1]/input')[0]
                # click email using js
                driver.execute_script("arguments[0].click();", email_input)

                email_input.send_keys(email)
            except Exception as e:
                print(e)
            # enter password
            try:

                password_input = driver.find_element_by_xpath(
                    "//html/body/div[1]/div/main/div/div[2]/input")
                password_input.send_keys(password)
            except Exception as e:
                print(e)
            while(True):
                if(input("Please solve the captcha then press 'y' to continue: ") == 'y'):
                    break
                time.sleep(5)
            try:

                driver.find_element_by_xpath(
                    '//html/body/div[1]/div/main/div/button').click()
            except Exception as e:
                print(e)
            time.sleep(5)
        else:
            print("info: Already logged in")
    except Exception as e:
        print(e)


def main():
    # get all the column values from the google sheet 'ticker'

    url = 'https://www.coinpayu.com/login'

    # get the driver to the url
    driver.get(url)
    driver.implicitly_wait(15)
    time.sleep(15)

    login()
    c = 1
    while(True):

        driver.get("https://www.coinpayu.com/dashboard/faucet")
        while(True):
            if(c == 0):
                time.sleep(3600)
                print("info: waiting for next hour")
            time.sleep(5)
            # scoll to the bottom of the page
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # find all the buttons with text 'Claim'

            claim_buttons = driver.find_elements_by_xpath(
                '//*[contains(text(), "Claim")]')
            # iterate over the buttons
            print(len(claim_buttons))
            if len(claim_buttons) <= 1:
                print("info: cant find any claim buttons")
                c += 1
                if c > 3:
                    driver.refresh()
                    c = 0
                continue
            else:
                break
        claim = claim_buttons[1]
        style = claim.get_attribute('style')
        # got to top of the page
        driver.execute_script("window.scrollTo(0, 0);")
        if style != "" or style != None:
            try:

                claim.click()
            except Exception as e:
                print("info: cant click the claim button", e)
            try:
                # find button with text 'Claim now'
                claim_now = driver.find_element_by_xpath(
                    '//*[contains(text(), "Claim now")]')
                claim_now.click()
            except Exception as e:
                print("info: Cant click the claim now button", e)
            while(True):

                time.sleep(5)
                if('claim' in driver.current_url):

                    try:
                        claim_now = driver.find_element_by_xpath(
                            '//*[contains(text(), "Claim now")]')
                        claim_now.click()
                    except Exception as e:
                        print("info: Cant click the claim now button", e)
                    break
                else:
                    print("info: still on the same page")
                    continue


if __name__ == '__main__':

    driver = Chrome()
    main()
    # driver.quit()

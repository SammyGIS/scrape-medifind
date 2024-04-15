import os
from dotenv import load_dotenv
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time

def get_driver(URL: str) -> webdriver.Chrome:
    """
    Launches a Selenium WebDriver with Chrome and navigates to the given URL.
    
    Parameters:
        URL (str): The URL of the website to navigate to.
    
    Returns:
        webdriver.Chrome: The initialized Selenium WebDriver with Chrome.
    
    Raises:
        TimeoutException: If the cookie banner element is not found within 30 seconds.
    """
    # Launch Selenium WebDriver with Chrome
    driver = webdriver.Chrome()
    time.sleep(2)
    # Navigate to the given URL
    driver.get(URL)
    time.sleep(10)
    
    # Wait until the "cookie-banner" element is present on the page
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "cookie-banner"))
    )
    
    return driver

def accept_cookies(driver: webdriver.Chrome, the_xpath: str):
    """
    Closes the accept cookies bottom bar if necessary.
    
    This function attempts to locate and click the "Close" button of the cookies acceptance bar 
    on a webpage using the provided XPath. If the button is found and clicked successfully, 
    it will close the cookies bar. If not found, it will pass silently without raising an exception.

    Parameters:
        driver (webdriver.Chrome): The initialized Selenium WebDriver with Chrome.
        the_xpath (str): The XPath expression to locate the "Close" button of the cookies acceptance bar.
    
    Raises:
        NoSuchElementException: If the "Close" button element is not found on the page.
    """
    try:
        # Locate the "Close" button element using the provided XPath
        close_cookies_button = driver.find_element("xpath", the_xpath)
        
        # Click the "Close" button to accept cookies
        close_cookies_button.click()
        
        # Wait for a few seconds to allow the page to update (optional)
        time.sleep(3)
    
    except Exception:
        # If the "Close" button is not found or any other exception occurs, just pass silently
        pass



def profile_button(driver, xpath):
    """
    Click the profile button identified by the given XPath on the web page.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        xpath (str): The XPath expression used to locate the profile button element on the web page.

    Returns:
        None

    Raises:
        Exception: If an error occurs while locating or clicking the profile button.

    """
    try:
        profile_button = driver.find_element("xpath", xpath)
        profile_button.click()
        time.sleep(2)
    except Exception as e:
        print(e)

    

def send_login_details(driver, username_xpath, password_xpath, username, password):
    """
    Enter the provided login details (username and password) into the respective fields on the web page.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        username_xpath (str): The XPath expression used to locate the username input field on the login page.
        password_xpath (str): The XPath expression used to locate the password input field on the login page.
        username (str): The username to be entered into the login form.
        password (str): The password to be entered into the login form.

    Returns:
        None
    """
    try:
        driver.find_elements('xpath', username_xpath)[0].send_keys(username)
        time.sleep(2)
        driver.find_elements('xpath', password_xpath)[0].send_keys(password)
        time.sleep(2)
    except Exception as e:
        print(e)


def login_button(driver, the_xpath):
    """
    Click the login button on the web page after entering the username and password.

    Parameters:
        driver (str): An instance of WebDriver, which is used to interact with the web browser.
        the_xpath (str): The XPath expression used to locate the login button element on the web page.

    Returns:
        None
    """
    try:
        log_in_button = driver.find_element('xpath', the_xpath)
        # now we are logged in, so now we can navigate search results without limitation
        log_in_button.click()
        time.sleep(5)
    except Exception as e:
        print(e)


def clear_location_input(driver, the_xpath):
    """
    Clear the location input box in case there is any information already entered.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        the_xpath (str): The XPath expression used to locate the location input box on the web page.

    Returns:
        None
    """
    try:
        location_buttons = driver.find_elements('xpath', the_xpath)
        # Check if we have 2 buttons in the location form input (location button and 'X' button)
        # If so, click the first button to clear the location information.
        if len(location_buttons) == 2:
            location_buttons[0].click()
            time.sleep(2)
    except Exception as e:
        print(e)

def search_input(driver, location, the_xpath):
    """
    Enter the provided location into the search input box on the web page.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        location (str): The location to be entered into the search input box.
        the_xpath (str): The XPath expression used to locate the search input box on the web page.

     Returns:
        None

    """
    try:
        location_inputs = driver.find_element('xpath', the_xpath)
        location_inputs.send_keys(location)
        time.sleep(2)
    except Exception as e:
        print(e)


def search_output(driver, location, the_xpath):
    """
    Choose the specified location from the search results on the web page.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        location (str): The location to be chosen from the search results.
        the_xpath (str): The XPath expression used to locate the search results on the web page.
    
     Returns:
        None
    """
    try:
        location_search_results = driver.find_elements("xpath", the_xpath)
        for i, location_search_result in enumerate(location_search_results):
            location_search_result_text = BeautifulSoup(location_search_result.get_attribute("innerHTML"), 'html.parser').text
            if location_search_result_text == location:
                chosen_index = i
                break
        location_search_results[chosen_index].click()
        time.sleep(2)
    except Exception as e:
        print(e)


def scroll_pages(driver):
    """
    Scroll down the web page to load additional content (lazy loading).

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.

    """
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e:
        print(e)
   

def extract_doctors_profile_url(driver, the_xpath):
    """
    Extract the URLs of doctor profile pages from the web page.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        the_xpath (str): The XPath expression used to locate the doctor profile URLs on the web page.

    Returns:
        set: A set containing the extracted URLs of doctor profile pages.

    """
    try:
        doctor_urls = driver.find_elements("xpath", the_xpath)

        doctor_urls_set = set()
        for url in doctor_urls:
            doctor_urls_set.add(url.get_attribute("href"))
        
        time.sleep(5)
        return doctor_urls_set
    except Exception as e:
        print(e)
        return set()


def append_to_url_df(doctors_url: set, condition: str) -> pd.DataFrame:
    """
    Append doctor URLs along with their corresponding condition and date to a DataFrame.

    Parameters:
        doctors_url (set): A set containing URLs of doctor profiles.
        condition (str): The condition or criteria associated with the doctor URLs.

    Returns:
        pd.DataFrame: The updated DataFrame after appending the doctor URLs.

    """
    try:
        # Use today's date to mark when data was scraped
        tmp = pd.DataFrame({"url": list(doctors_url), "condition": [condition]*len(doctors_url), "date": [date.today()]*len(doctors_url)})
        # create and empty DataFrame with heading
        df = pd.DataFrame({"url": [], "condition": [], "date":[]})
        # add all the data genrated to the empty DataFrame
        links_urls_df = pd.concat([df, tmp], ignore_index=True)
        # drop all duplicates
        provider_urls_df = links_urls_df.drop_duplicates(subset='url')
        
        print(f"Shape of df: {provider_urls_df.shape}")
        return provider_urls_df
    except Exception as e:
        print(e)
                      
def click_nextpage(driver, the_xpath):
    """
    Click the next page button to navigate to the next page.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        the_xpath (str): The XPath expression used to locate the next page button on the web page.

    Returns:
        None
    """

    # Find the next page button element
    next_button = driver.find_element("xpath", the_xpath)
    print(next_button)
        
    # Click the next page button to navigate to the subsequent page
    next_button.click()
        
    # Wait for 5 seconds to allow the new page to load
    time.sleep(5)



def save_data(data: pd.DataFrame, condition: str) -> pd.DataFrame:
    """
    Saves the given DataFrame to an Excel file in the "data" directory.

    This function takes a pandas DataFrame and a condition string as input. It checks if the "data" directory 
    exists, and if not, creates it. Then, it saves the DataFrame to an Excel file in the "data" directory 
    with a filename format of "medifind_providers_{condition}_{today's date}.xlsx".

    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to be saved.
        condition (str): A string representing the condition or data category, used in the filename.

    Returns:
        pd.DataFrame: The original DataFrame that was saved.

    """
    path = "data"

    # Check if the "data" directory exists, if not, create it
    if not os.path.exists(path):
        os.mkdir(path)

    # Generate the filename using the provided condition and today's date
    filename = f"{path}/medifind_providers_{condition}_{date.today()}.xlsx"

    # Save the DataFrame to an Excel file with the generated filename
    data.to_excel(filename)

    return data



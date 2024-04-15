import os
import sys 
import inspect
#ref - https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# In this file, we get the urls of the provider pages in medifind
# import undetected_chromedriver as uc
from config import LoginDetials
from config import WebAddress
from config import XPATH_DETAILS
from config import SEARCH_DETAILS
import numpy as np
from utils.url_utils import get_driver
from utils.url_utils import accept_cookies
from utils.url_utils import save_data
from utils.url_utils import profile_button
from utils.url_utils import send_login_details
from utils.url_utils import login_button
from utils.url_utils import clear_location_input
from utils.url_utils import search_input
from utils.url_utils import search_output
from utils.url_utils import scroll_pages
from utils.url_utils import extract_doctors_profile_url
from utils.url_utils import append_to_url_df
from utils.url_utils import click_nextpage
from selenium.common.exceptions import WebDriverException


def generate_search(driver, condition):
    """
    Generate a search on the web page for the specified condition and location.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.
        condition (str): The medical condition to search for on the web page.

    Returns:
        None

    """
    try:
        # After logging in successfully, clear the location search input form
        clear_location_input(driver, XPATH_DETAILS.LOCATION_BUTTON.value)
        
        # Set the location search input
        search_input(driver, SEARCH_DETAILS.LOCATION.value, XPATH_DETAILS.LOCATION_INPUT.value)
        
        # Select the top location from the list of searched locations
        search_output(driver, SEARCH_DETAILS.LOCATION.value, XPATH_DETAILS.SEARCH_RESULT.value)

        # Set the condition search input
        search_input(driver, condition, XPATH_DETAILS.CONDITION_INPUT.value)

        # Select the top condition from the list of searched conditions
        search_output(driver, condition, XPATH_DETAILS.SEARCH_RESULT.value)
    except Exception as e:
        print(e)
               
def get_data(driver):
    """
    Scrapes all the doctor profile URLs from multiple pages.

    Parameters:
        driver (WebDriver): An instance of WebDriver, which is used to interact with the web browser.

    Returns:
        list: A list containing all the scraped doctor profile URLs.

    """
    page_num = 0
    all_urls = []  # Initialize an empty list to store all the URLs

    while True:
        try:
            
            # Scroll through the page 
            scroll_pages(driver)

            # Get each doctor's unique URL from the page
            get_url = extract_doctors_profile_url(driver, XPATH_DETAILS.URL_CONTAINER.value)
    
            # Add the URLs to the list
            all_urls.extend(get_url)
                    
            # Increment the page number
            page_num += 1
            print(f"Scraped page #{page_num}!...")

            # Click to go to the next page
            click_nextpage(driver, XPATH_DETAILS.NEXT_PAGE.value)
                
        except WebDriverException as e:
            print(e)
            print("Either we have no more pages or something else went wrong")
            # Close Selenium browser  
            driver.quit()  
            break

    return all_urls

if __name__=="__main__":

    all_data = []

    for k, condition in SEARCH_DETAILS.get_condition_dict().items():
        # use driver to get the website
        driver = get_driver(WebAddress.URL.value)
        
        # close the accept cookies button on the website
        cookies = accept_cookies(driver, XPATH_DETAILS.COOKIES.value)
        
        # click on the profile button on the website
        click_profile = profile_button(driver, XPATH_DETAILS.PROFILE.value)
        
        # send login details into the login form
        login_details = send_login_details(driver,XPATH_DETAILS.EMAIL.value,
                                            XPATH_DETAILS.PASSWORD.value,
                                            LoginDetials.MEDIFIND_USERNAME.value,
                                            LoginDetials.MEDIFIND_PASSWORD.value)
        
        # click the login button
        login = login_button(driver, XPATH_DETAILS.LOGIN_BUTTON.value)

        #scrapped the url from all the pages
        generate_search(driver,condition)

        # get data
        geturl_data = get_data(driver)

        all_data.extend(geturl_data)

     # Create a DataFrame with the URLs and associated data
    compiled_data = append_to_url_df(all_data, SEARCH_DETAILS.CONDITION.value)
    
    # Save data to Excel
    save_data(compiled_data, SEARCH_DETAILS.CONDITION.value)
    
    
    
    










   


# In this file, we get the urls of the provider pages in medifind
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import os
import time
from dotenv import load_dotenv
from datetime import date

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.medifind.com/"

def append_to_url_df(df: pd.DataFrame, doctors_set: set, condition: str)-> pd.DataFrame:
    """
    Args:
        df(pd.DataFrame) :
        doctors_set (set):
        condtion(str):

    Returns:
    datafrme():

    
    """
    # use today's date to mark when data was scraped
    tmp = pd.DataFrame({"url": list(doctors_set), "condition": [condition]*len(doctors_set), "date":[date.today()]*len(doctors_set)})
    df = pd.concat([df, tmp], ignore_index=True)
    return df

def load_params(location: str="United States", condition: str= "Neurofibromatosis"):
    load_dotenv()
    MEDIFIND_USERNAME = os.getenv("MEDIFIND_USERNAME")
    MEDIFIND_PASSWORD = os.getenv("MEDIFIND_PASSWORD")
    return {
        "MEDIFIND_USERNAME": MEDIFIND_USERNAME,
        "MEDIFIND_PASSWORD": MEDIFIND_PASSWORD,
        "location": location,
        "condition": condition
    }
    

def scrape_medifind_urls(
        time_between_scraping_pages: int=15,
        location: str="United States", 
        condition: str= "Neurofibromatosis"):
    params = load_params(location = location, condition = condition)

    # launch selenium, driver
    driver = webdriver.Chrome()
    time.sleep(2)
    driver.get(URL)
    time.sleep(10)

    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "cookie-banner")) # "ac-condition-filter" # cookie-banner
    )

    # close accept cookies bottom bar if necessary
    try:
        the_xpath = '//button[contains(@id, "modal-close")]'
        close_cookies_button = driver.find_element("xpath", the_xpath)
        close_cookies_button.click()
        time.sleep(10)
    except Exception as e:
        print(e)

    # click the profile button
    the_xpath = "//button[contains(@id, 'toggle-profile')]"
    profile_button = driver.find_element("xpath", the_xpath)
    profile_button.click()
    time.sleep(10)

    # send username and password
    driver.find_elements('xpath', '//input[@type="email"]')[0].send_keys(params["MEDIFIND_USERNAME"])
    time.sleep(2)
    driver.find_elements('xpath', '//input[@type="password"]')[0].send_keys(params["MEDIFIND_PASSWORD"])
    time.sleep(2)


    # click login
    try:
        the_xpath = "/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div/form/button/span[1]/span"
        log_in_button = driver.find_element('xpath', the_xpath)
        # now we logged on, so now we can navigate search results without limitation
        log_in_button.click()
        time.sleep(5)
    except Exception as e:
        print(e)
    

    # clear location if we need to do it
    the_xpath='//div[contains(@class,"Landing_form-input__5H2Lm")]//button'
    location_buttons = driver.find_elements('xpath', the_xpath)
    # bc we have 2 buttons in location form input but sometimes we have just 1 
    # (just the location button and not the x button)
    if len(location_buttons) == 2:
        location_buttons[0].click()
        time.sleep(2)
    
    # send location param
    location_inputs = driver.find_element('xpath', '//input[@id="ac-location-filter"]')
    location_inputs.send_keys(location)
    time.sleep(2)

    # choose location out of search results
    # this works and gets past the search button not working, 
    the_xpath = '//ul[contains(@class,"Autocomplete-Select_menu-list__mETH4 Autocomplete-Select_open__ZUDjv")]//li'
    location_search_results = driver.find_elements("xpath", the_xpath)
    for i, location_search_result in enumerate(location_search_results):
        location_search_result_text = BeautifulSoup(location_search_result.get_attribute("innerHTML"), 'html.parser').text
        if location_search_result_text == location:
            chosen_index = i
            break
    location_search_results[i].click()
    time.sleep(2)

    # Send search param
    search_param = driver.find_element('xpath', '//input[@id="find-a-doctor-form-magic-filter"]')
    # other conditions show up when we input Neurofibromatosis
    search_param.send_keys("Neurofibromatosis")
    time.sleep(2)

    # choose search condition out of search results
    # this works and gets past the search button not working
    the_xpath = '//ul[contains(@class,"Autocomplete-Select_menu-list__mETH4 Autocomplete-Select_open__ZUDjv")]//li'
    search_results = driver.find_elements("xpath", the_xpath)
    for i, search_result in enumerate(search_results):
        search_result_text = BeautifulSoup(search_result.get_attribute("innerHTML"), 'html.parser').text
        print(search_result_text)
        if search_result_text == condition:
            chosen_index = i
            break
    search_results[i].click()
    time.sleep(5)

    # close accept cookies bottom bar if necessary
    try:
        the_xpath = '//button[contains(@id, "modal-close")]'
        close_cookies_button = driver.find_element("xpath", the_xpath)
        close_cookies_button.click()
        time.sleep(10)
    except Exception:
        pass

    # instantiate empty dataframe
    provider_urls_df = pd.DataFrame({"url": [], "condition": [], "date":[]})

    page_num = 0

    seeing_first_page = True

    while True:
        # scroll all the way down to get past lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if seeing_first_page:
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            seeing_first_page = not seeing_first_page


        # now get the urls of the doctor pages for every page
        the_xpath = '//div[contains(@class,"DoctorCard_header__row__XFqB2")]//a'
        doctor_urls = driver.find_elements("xpath", the_xpath)

        doctor_urls_set = set()
        for url in doctor_urls:
            doctor_urls_set.add(url.get_attribute("href"))
        
        provider_urls_df = append_to_url_df(df = provider_urls_df, doctors_set = doctor_urls_set, condition = condition)

        page_num+=1
        print(f"Shape of df: {provider_urls_df.shape}")
        print(f"Scraped page # {page_num}!...")

        # try navigating to next page
        try:
            # waiting for next button to be clickable
            time.sleep(3)
            the_xpath = '//span[text()="Next"]/ancestor::button'
            next_button = driver.find_element("xpath", the_xpath)
            print(next_button)
            next_button.click()
            time.sleep(time_between_scraping_pages)
        except Exception as e:
            print(e)
            print("Either we have no more pages or something else went wrong")
            # close selenium browser
            driver.quit()  
            break  
                       

    return provider_urls_df

if __name__=="__main__":
    # TODO: add "nf": "Neurofibromatosis" , "nf2":"Neurofibromatosis Type 2 (NF2)" to conditions list
    file_name_to_condition_dict = {
        "nf": "Neurofibromatosis",
        "nf1": "Neurofibromatosis Type 1 (NF1)",
        "nf2": "Neurofibromatosis Type 2 (NF2)",
        "nf3": "Neurofibromatosis Type 3 also known as Schwannomatosis",
        "nf6": "Neurofibromatosis Type 6 also known as Cafe-Au-Lait_Spots",
        "legius": "Neurofibromatosis 1-Like Syndrome also known as Legius Syndrome",
        "sheath": "Malignant Neurofibroma also known as Malignant Peripheral Nerve Sheath Tumor"
    }

    
    for k,condition in file_name_to_condition_dict.items():
        provider_urls_df = scrape_medifind_urls(
            time_between_scraping_pages = 2,
            location = "United States", 
            condition = condition
        )
        print(f"{condition}: {provider_urls_df.shape[0]} urls")
        
        path = "data"
        if not os.path.exists(path):
            os.mkdir(path)
            provider_urls_df.to_excel(f"{path}/medifind_providers_{k}.xlsx")
            time.sleep(60*2)
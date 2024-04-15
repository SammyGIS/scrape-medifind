import os
import sys 
import inspect
#ref - https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from utils.profile_utils import get_official_name
from utils.profile_utils import get_affiliation
from utils.profile_utils import get_affiliation_links
from utils.profile_utils import get_specialties
from utils.profile_utils import get_experience
from utils.profile_utils import get_acceptances
from utils.profile_utils import get_bio
from utils.profile_utils import get_insurance
from utils.profile_utils import get_additional_insurance
from utils.profile_utils import get_education
from utils.profile_utils import get_specialties
from utils.profile_utils import get_licenses
from utils.profile_utils import get_hospitals
from utils.profile_utils import get_languages
from utils.profile_utils import get_gender
from utils.profile_utils import get_num_clinical_trials
from utils.profile_utils import get_num_publications
from utils.profile_utils import get_locations
from utils.profile_utils import get_other_locations
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import undetected_chromedriver as uc
import time
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import concurrent.futures


def scrape_information_from_url(url_subset_df: pd.DataFrame) -> dict:
    """
    Scrapes information from a subset of URLs using a WebDriver.
    
    Args:
        url_subset_df (pd.DataFrame): A DataFrame containing at least a 'url' column
                                      specifying the URLs to be scraped.    
    Returns:
        dict: A dictionary containing the scraped HTML content for each URL.
              The keys are the URLs, and the values are the corresponding HTML content
              in string format. If scraping fails for a URL, the corresponding value
              will be "Issue with doctor".
    """
    try:
        # Initialize a WebDriver instance
        driver = webdriver.Chrome()
        
        # Dictionary to store scraped content
        soup_dict = dict()
        
        # Iterate through each row in the DataFrame
        for index, row in url_subset_df.iterrows():
            print(row.url)
            # Load the URL in the WebDriver
            driver.get(row.url)
            
            try:
                st = time.time()
                # Wait for a specific element to be present on the page
                element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "cookie-banner")) # "ac-condition-filter" # cookie-banner
                )
                et = time.time()
                print(f"Time to load: {et-st}")
                
                # Get the page source (HTML content)
                html = driver.page_source
                
                # Parse the HTML content using BeautifulSoup
                doc_doctor = BeautifulSoup(html, "html.parser")
                
                # Convert the soup object to string and store in the dictionary
                soup_dict[row.url] = str(doc_doctor)
                
            except Exception as e:
                print("Scraping individual page failed...")
                print(e)
                # Store a placeholder value for failed scraping
                soup_dict[row.url] = "Issue with doctor"
        
        # Close the WebDriver
        driver.quit()
        
        return soup_dict
    
    except Exception as e2:
        # If a higher-level exception occurs, return an empty dictionary
        # This is assuming the entire sub chunk will fail and the connection
        # to the website might be suspected as an autonomous browser.
        return dict()


def scrape_medifind_doctor_info(doc_doctor: str) -> dict:
    """
    Extracts various details about a doctor from their HTML content.
    Args:
        doc_doctor (str): The HTML content of the doctor's profile page.
        
    Returns:
        dict: A dictionary containing various details about the doctor. 
    """
    # create empty dict to store key information
    doctor_details_dict = dict()
    
    # Extract doctor's information using helper functions
    doctor_details_dict["name"] = get_official_name(doc_doctor)
    doctor_details_dict["affiliation"] = get_affiliation(doc_doctor)
    doctor_details_dict["affiliation_links"] = get_affiliation_links(doc_doctor)
    doctor_details_dict["specialties"] = get_specialties(doc_doctor)
    doctor_details_dict["experience"] = get_experience(doc_doctor)
    doctor_details_dict["acceptances"] = get_acceptances(doc_doctor)
    doctor_details_dict["biography"] = get_bio(doc_doctor)
    doctor_details_dict["insurance"] = get_insurance(doc_doctor)
    doctor_details_dict["additional_insurance"] = get_additional_insurance(doc_doctor)
    doctor_details_dict["education"] = get_education(doc_doctor)
    doctor_details_dict["licenses"] = get_licenses(doc_doctor)
    doctor_details_dict["hospitals"] = get_hospitals(doc_doctor)
    doctor_details_dict["languages"] = get_languages(doc_doctor)
    doctor_details_dict["gender"] = get_gender(doc_doctor)
    doctor_details_dict["num_clinical_trials"] = get_num_clinical_trials(doc_doctor)
    doctor_details_dict["num_publications"] = get_num_publications(doc_doctor)
    doctor_details_dict["locations"] = get_locations(doc_doctor)
    doctor_details_dict["other_locations"] = get_other_locations(doc_doctor)
    
    return doctor_details_dict


if __name__ == "__main__": 
    # load the url_excel file into the scripts
    url_df = pd.read_csv("Data-Collection-Phase-1\samuel\medfind\data\differences.csv")

    # query it to select only the link to contains medfind
    url_df = url_df.query("url.str.contains('medifind.com')")

    # split url df into chunks of 500 so that web scraping works
    n = 500
    url_df_parts_top_level = [url_df.iloc[i:i + n] for i in range(0, len(url_df), n)]
    
    all_urls = []
    num_chunks = 6
    for df in url_df_parts_top_level:
        url_df_parts = np.array_split(df, num_chunks)
        all_urls.append(url_df_parts)

    print(len(all_urls))
    for elem in all_urls:
        for x in elem:
            print(x.shape[0])
    print([x.shape for x in url_df_parts_top_level])

    generator_results = []
    all_final_dfs = []
    for i, url_chunks in enumerate(all_urls):
        print(f"Parallel scraping session: {i+1}")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            generator_results = executor.map(scrape_information_from_url, url_chunks)
            print("time for next top level chunk and next parallel scraping session...")
        
        # flatten 2d results into 1 list of dictionaries
        final_dict = {k: v for d in generator_results for k, v in d.items()}

        # scrape the html and save it to list
        df_more_details = []
        for url, doc_doctor in final_dict.items():
            doc_doctor = BeautifulSoup(doc_doctor, 'html.parser')
            tmp = scrape_medifind_doctor_info(doc_doctor)
            tmp["url"] = url
            df_more_details.append(tmp)
        
        # turn list into pandas df
        final_df = pd.DataFrame(df_more_details)
        # write patitioned data to file
        # final_df.to_excel(f"medifind_providers_nf_partition_{str(i+1).zfill(3)}.xlsx", index = False)
        all_final_dfs.append(final_df)

        # wait 2 minutes between scraping sessions
        # don't wait after finished all sessions
        if i < len(all_urls)-1:
            print("sleeping...")
            
            time.sleep(60*2)

    combined_df = pd.concat(all_final_dfs)
    combined_df.to_excel("medifind_providers_nf_all.xlsx", index = False)
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re
import time
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This decorator helps us run a function and catch and proceed with an error
# This helps when scraping website as formats might be different when scraping
# different pages
def return_on_failure(value):
  def decorate(f):
    def applicator(*args, **kwargs):
      try:
         return f(*args,**kwargs)
      except:
         print('Error')
         return value

    return applicator

  return decorate

@return_on_failure(np.NaN)
def get_official_name(doc_doctor):
    name = doc_doctor.find(class_="doctors-single_text__qTgfv").text
    return name

@return_on_failure(np.NaN)
def get_affiliation(doc_doctor):
    affiliation = "; ".join([elem.text.strip() for elem in doc_doctor.find_all(class_="doctors-single_sub-name__Qb8nw")])
    return affiliation

@return_on_failure(np.NaN)
def get_affiliation_links(doc_doctor):
  affiliation_links = []
  for elem in doc_doctor.find_all(class_="doctors-single_sub-name__Qb8nw"):
      if elem.find("a"):
          affiliation_links.append(elem.a["href"])

  affiliation_links_str = "; ".join(affiliation_links)
  return affiliation_links_str

@return_on_failure(np.NaN)
def get_specialties(doc_doctor):
  specialties = "; ".join(doc_doctor.find(class_="TopDataContainer_top-data__value__r4YAL TopDataContainer_specialties__OYNwO").text.replace(" ", "").split("|"))
  return specialties

@return_on_failure(np.NaN)
def get_experience(doc_doctor):
  experience = doc_doctor.find("a", class_="TopDataContainer_top-data__value__r4YAL").text
  return experience

@return_on_failure(np.NaN)
def get_acceptances(doc_doctor):
  acceptances = "; ".join([elem.text.strip() for elem in doc_doctor.find_all("span", class_="TopDataContainer_accepted__ygrlH")])
  return acceptances

@return_on_failure(np.NaN)
def get_bio(doc_doctor):
  biography = doc_doctor.find(class_="doctors-single_biography__ztJuk").p.text
  return biography

@return_on_failure(np.NaN)
def get_insurance(doc_doctor):
  insurance = "; ".join([elem.text.strip() for elem in doc_doctor.find_all("div", class_="DoctorInsurance_accepted__orxVP")])
  return insurance

@return_on_failure(np.NaN)
def get_additional_insurance(doc_doctor):
  additional_insurance = "; ".join([elem.text.strip() for elem in doc_doctor.find("ul", class_="DoctorInsurance_insurances__list__Gp+4P").find_all("li")])
  return additional_insurance

@return_on_failure(np.NaN)
def get_education(doc_doctor):
  education = "; ".join([elem.text.strip() for elem in doc_doctor.find("div", class_="doctors-single_credentials__header__Lstc8", text = "Graduate Institution").next_siblings])
  return education

@return_on_failure(np.NaN)
def get_specialties(doc_doctor):
  specialties = "; ".join([elem.text.strip() for elem in doc_doctor.find("div", class_="doctors-single_credentials__header__Lstc8", text = "Specialties").next_siblings])
  return specialties

@return_on_failure(np.NaN)
def get_licenses(doc_doctor):
  licenses = "; ".join([elem.text.strip() for elem in doc_doctor.find("div", class_="doctors-single_credentials__header__Lstc8", text = "Licenses").next_siblings])
  return licenses

@return_on_failure(np.NaN)
def get_hospitals(doc_doctor):
  hospitals = "; ".join([elem.text.strip() for elem in doc_doctor.find("div", class_="doctors-single_credentials__header__Lstc8", text = "Hospital Affiliations").next_siblings])
  return hospitals

@return_on_failure(np.NaN)
def get_languages(doc_doctor):
  languages = "; ".join([elem.text.strip() for elem in doc_doctor.find("div", class_="doctors-single_credentials__header__Lstc8", text = "Languages Spoken").next_siblings])
  return languages

@return_on_failure(np.NaN)
def get_gender(doc_doctor):
  gender = "; ".join([elem.text.strip() for elem in doc_doctor.find("div", class_="doctors-single_credentials__header__Lstc8", text = "Gender").next_siblings])
  return gender

@return_on_failure(np.NaN)
def get_num_clinical_trials(doc_doctor):
  num_clinical_trials = doc_doctor.find(class_="doctors-single_trials__ao-+L").find("span").text.split(" ")[0]
  return num_clinical_trials

@return_on_failure(np.NaN)
def get_num_publications(doc_doctor):
  num_publications = doc_doctor.find(class_="doctors-single_articles__gk1N0").find("span").text.split(" ")[0]
  return num_publications

@return_on_failure(np.NaN)
def get_num_publications(doc_doctor):
  doctor_video = doc_doctor.find(class_="YoutubeVideo_thumbnail__5I-Um")["style"]
  doctor_video_id = re.search(r"\/vi\/(\w+)\/", url).group(1)
  doctor_video_url = f"https://www.youtube.com/watch?v={doctor_video_id}"
  return doctor_video_url

def get_location_and_or_phone_number(elem):
    final = ""
    # try getting location
    try:
        final += elem.find(class_="LocationAccordion_locations__values__U3hjw").text
    except:
        pass

    try: 
        final += elem.find_all(class_="LocationAccordion_locations__values__U3hjw")[1].find("a")["href"]
    except:
        pass

    return final


@return_on_failure(np.NaN)
def get_locations(doc_doctor):
  locations = "; ".join([get_location_and_or_phone_number(elem) for elem in doc_doctor.find("div", text="Locations").find_next_siblings(class_="BlockContainer_block-container__body__JL3jm LocationAccordion_locations__BvMYW")])
  return locations

@return_on_failure(np.NaN)
def get_other_locations(doc_doctor):
  other_locations = "; ".join([get_location_and_or_phone_number(elem) for elem in doc_doctor.find("div", text="Other Locations").find_next_siblings(class_="BlockContainer_block-container__body__JL3jm LocationAccordion_locations__BvMYW LocationAccordion_other-locations__qwwbx")])
  return other_locations

def sample2(df):
    return {"nrows": df.shape[0]}

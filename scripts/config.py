import os
from enum import Enum
from dotenv import load_dotenv

class WebAddress(Enum):
    URL= "https://www.medifind.com/"


class LoginDetials(Enum):
    load_dotenv()
    MEDIFIND_USERNAME = os.getenv("MEDIFIND_USERNAME")
    MEDIFIND_PASSWORD = os.getenv("MEDIFIND_PASSWORD")

class XPATH_DETAILS(Enum):
    COOKIES = '//button[contains(@id, "modal-close")]'
    PROFILE  = "//button[contains(@id, 'toggle-profile')]"
    EMAIL = '//input[@type="email"]'
    PASSWORD = '//input[@type="password"]'
    LOGIN_BUTTON = "/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div/form/button/span[1]/span"
    LOCATION_BUTTON = '//div[contains(@class,"Landing_form-input__5H2Lm")]//button'
    LOCATION_INPUT = '//input[@id="ac-location-filter"]'
    SEARCH_RESULT = '//ul[contains(@class,"Autocomplete-Select_menu-list__mETH4 Autocomplete-Select_open__ZUDjv")]//li'
    CONDITION_INPUT = '//input[@id="find-a-doctor-form-magic-filter"]'
    URL_CONTAINER ='//div[contains(@class,"DoctorCard_header__row__XFqB2")]//a'
    NEXT_PAGE = '//span[text()="Next"]/ancestor::button'

class SEARCH_DETAILS(Enum):
    LOCATION = 'United States'
    CONDITION = 'Neurofibromatosis'

    @classmethod
    def get_condition_dict(cls):
        return {
            "nf": "Neurofibromatosis",
            "nf1": "Neurofibromatosis Type 1 (NF1)",
            "nf2": "Neurofibromatosis Type 2 (NF2)",
            "nf3": "Neurofibromatosis Type 3 also known as Schwannomatosis",
            "nf6": "Neurofibromatosis Type 6 also known as Cafe-Au-Lait_Spots",
            "legius": "Neurofibromatosis 1-Like Syndrome also known as Legius Syndrome",
            "sheath": "Malignant Neurofibroma also known as Malignant Peripheral Nerve Sheath Tumor"
        }

class DOCTOR_PROFILE_PATH():
    pass


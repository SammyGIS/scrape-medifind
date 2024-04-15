# Web Scraping Script for Doctors' Profiles
This repository contains a two layer data scrapping scripts where the first scripts gets the link to the doctors profile and the second scripts extract all the doctors profile based on different medical conditions from a healthcare website.

## Prerequisites
- Python 3.x
- Selenium WebDriver
- pandas
- BeautifulSoup


## How to Use

1. Clone this repository to your local machine.
    ```
    git clone https://github.com/onehealthconnectapp/Data-Collection-Phase-1/samuel
    ```

2. Install the required libraries by running:
    ```
    pip install -r requirements.txt 
    ```
3. If you don't have chrome driver install on ur PC, follow this tutorial - https://codetryout.com/selenium-chrome-driver-guide/

4. Update the required login credentials and XPATH details in the `config.py` file.

5. Run the main script `scrape_url.py` to start the web scraping process.

```
python scripts.scrape_url.py
```
6. After step 5 runs successfully, use the output data as nput into the `scrape_prfoile.py` to scrape the doctors profile info from the input url
```
python scripts.scrape_profile.py
```

7. The script will log in to the healthcare website, perform searches for different medical conditions, and extract doctors' profile URLs.

8. The scraped data will be saved in an Excel file.

## Project Structure
- `scrape_url.py`: The scripts is used to scrap the url link to each doctors profile
- `scrape_profile.py`: This script responsible for extracting doctors' information from profile URLs
- `config.py`: Contains configuration details such as URLs, XPATHs, and login credentials.
- `utils.py`: Contains utility functions for various actions like clicking buttons, sending login details, and scrolling through pages.
- `data`: A folder to store the scraped data (Excel files).


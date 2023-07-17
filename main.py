from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Create a new instance of the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Define the base URL
base_url = 'https://www.slideshare.net/search?searchfrom=header&q=simple+ppts'

# Create a list to store all the ppt links
all_urls = []

# Create a new Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Visit the base URL
driver.get(base_url)

# Scrape ppt links from each page
while True:
    # Wait for the presentation cards to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Card_card__RRXnY")))

    # Find all the presentation cards
    cards = driver.find_elements(By.CLASS_NAME, "Card_card__RRXnY")

    # Extract the URLs from the current page
    urls = [card.find_element(By.CLASS_NAME, "Card_cardAnchor__Eq5Vp").get_attribute("href") for card in cards]

    # Add the URLs to the list
    all_urls.extend(urls)

    # Check if there is a next page
    next_button = driver.find_element(By.CSS_SELECTOR, ".Pagination_navigationButton__JZWV8[title='Next']")
    is_disabled = next_button.get_attribute("aria-disabled")

    if is_disabled == 'true':
        break

    # Click on the ">" icon to go to the next page
    driver.execute_script("arguments[0].click();", next_button)

# Quit the browser
driver.quit()

# Divide the ppt links into batches of 18
batches = [all_urls[i:i+18] for i in range(0, len(all_urls), 18)]

# Print the count of links in each batch
for i, batch in enumerate(batches, start=1):
    print(f"Batch {i}: {len(batch)} links")

import os
import requests
import uuid
from bs4 import BeautifulSoup

# Directory path to save the downloaded images
base_directory = r'C:\Users\ADITYA PC\Downloads\automated downloads'
download_directory = os.path.join(base_directory, "25 batch")

# Create the download directory if it doesn't exist
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Scrape images from each URL batch
for i, batch in enumerate(batches, start=1):
    # Create a new folder for the batch
    batch_directory = os.path.join(base_directory, f"{i}th batch")
    os.makedirs(batch_directory)

    # Iterate over the URLs in the batch
    for url in batch:
        # Send a GET request
        response = requests.get(url)

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all source tags
        source_tags = soup.find_all('source')

        for source_tag in source_tags:
            # Get the srcset attribute
            srcset = source_tag.get('srcset')

            # If the srcset attribute is not None
            if srcset is not None:
                # Split the srcset attribute into a list of strings
                images = srcset.split(', ')

                # Iterate over the images
                for image in images:
                    # If '2048w' is in the string
                    if '2048w' in image:
                        # Split the string to get the image URL
                        img_url = image.split(' ')[0]

                        # Get the image
                        img_data = requests.get(img_url).content

                        # Generate a unique image name
                        unique_name = str(uuid.uuid4())
                        image_name = f"{unique_name}.jpg"

                        # Save the image with the unique name in the batch directory
                        file_path = os.path.join(batch_directory, image_name)
                        with open(file_path, 'wb') as img_file:
                            img_file.write(img_data)
                        print(f"Downloaded image: {file_path}")
                        break  # Stop searching for other resolutions for this source tag



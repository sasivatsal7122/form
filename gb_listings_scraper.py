from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import re

def getDriver():
    print("\nInitializing the driver")
    userAgent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={userAgent}")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options); driver.maximize_window()
    print("Driver initialized")
    
    return driver

def main():
    target_url = str(input("Enter the Business Listing URL: "))
    driver = getDriver()
    print("Getting the target URL")
    driver.get(target_url)
    
    print("Target URL opened, waiting for the business details to load")
    try:
        business_title_element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-attrid='title']")))
        business_title = business_title_element.text
    except Exception as e:
        business_title = "Not found"
        print(f"An exception occurred while fetching title: {e}")

    try:
        business_rating_element = driver.find_element(By.CSS_SELECTOR, "[data-attrid='subtitle']").find_element(By.TAG_NAME, "span")
        business_rating = business_rating_element.text
    except Exception as e:
        business_rating = "Not found"
        print(f"An exception occurred while fetching rating: {e}")

    try:
        business_reviews_element = driver.find_element(By.CSS_SELECTOR, "[data-async-trigger='reviewDialog']")
        business_reviews = business_reviews_element.text
    except Exception as e:
        business_reviews = "Not found"
        print(f"An exception occurred while fetching reviews: {e}")

    try:
        business_type_element = driver.find_element(By.CSS_SELECTOR, "[data-attrid='subtitle']").find_elements(By.TAG_NAME, "span")[-1]
        business_type = business_type_element.text
    except Exception as e:
        business_type = "Not found"
        print(f"An exception occurred while fetching business type: {e}")
    
    other_elements = driver.find_elements(By.CSS_SELECTOR,"div.TzHB6b.Hwkikb.WY0eLb.yqK6Z")[1]
    info_string = other_elements.find_element(By.TAG_NAME,"div").text
    service_options_match = re.search(r'Service options: (.+)', info_string)
    address_match = re.search(r'Address: (.+)', info_string)
    hours_match = re.search(r'Hours:\n(.+)', info_string)
    phone_match = re.search(r'Phone: (.+)', info_string)

    service_options = service_options_match.group(1) if service_options_match else 'Not found'
    address = address_match.group(1) if address_match else 'Not found'
    hours = str(hours_match.group(1)) if hours_match else 'Not found'
    phone = phone_match.group(1) if phone_match else 'Not found'
    
    data_dict = {
        "Business Title": business_title,
        "Business Rating": business_rating+"/5",
        "Business Reviews": business_reviews,
        "Business Type": business_type,
        "Service Options": service_options,
        "Address": address,
        "Business Hours": hours,
        "Busines Phone no": phone
        
    }
    formatted_data_dict = json.dumps(data_dict, indent=4)
    print(formatted_data_dict)
    driver.quit()
    
    return

if __name__=="__main__":
    main()
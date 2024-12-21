from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def setup_driver():
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment this if you don't want to see the browser
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_hospitals():
    driver = setup_driver()
    try:
        # Navigate to the page
        driver.get("https://www.fhpl.net/WhatsappNetworkhospitals/")
        
        # Wait for the insurance dropdown to be present
        insurance_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddinsurance"))
        )
        
        # Select Magma HDI
        Select(insurance_dropdown).select_by_visible_text("Magma HDI General Insurance Company Ltd")
        time.sleep(2)  # Give it time to process
        
        # Select State (Telangana)
        state_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlState"))
        state_dropdown.select_by_visible_text("Telangana")
        time.sleep(2)  # Give it time for city dropdown to populate
        
        # Select City (Hyderabad)
        city_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlCity"))
        city_dropdown.select_by_visible_text("Hyderabad")
        time.sleep(2)
        
        # Click Search button
        search_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnGo")
        search_button.click()
        time.sleep(3)  # Wait for results
        
        # Find and extract data from the table
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_grdProviderDetails"))
        )
        
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Skip header row and process data rows
        for row in rows[1:]:  # Skip header row
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:  # Ensure we have all columns
                hospital_data = {
                    'Serial No': cols[0].text.strip(),
                    'Hospital Name': cols[1].text.strip(),
                    'Address': cols[2].text.strip(),
                    'Contact': cols[3].text.strip()
                }
                print(hospital_data)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_hospitals()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    return driver

def get_all_insurance_companies(driver):
    insurance_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddinsurance"))
    )
    select = Select(insurance_dropdown)
    # Get all options except the first one which is usually "--Select Insurername--"
    return [option.text for option in select.options if option.text != "--Select Insurername--"]

def scrape_hospitals():
    driver = setup_driver()
    all_hospital_data = []
    
    try:
        # Navigate to the page
        driver.get("https://www.fhpl.net/WhatsappNetworkhospitals/")
        
        # Get list of all insurance companies
        insurance_companies = get_all_insurance_companies(driver)
        print(f"Found {len(insurance_companies)} insurance companies to process")
        
        # Process each insurance company
        for insurance_name in insurance_companies:
            print(f"\nProcessing insurance company: {insurance_name}")
            try:
                # Select Insurance
                insurance_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddinsurance"))
                insurance_dropdown.select_by_visible_text(insurance_name)
                time.sleep(2)
                
                # Select State (Telangana)
                state_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlState"))
                state_dropdown.select_by_visible_text("Telangana")
                time.sleep(2)
                
                # Select City (Hyderabad)
                city_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlCity"))
                city_dropdown.select_by_visible_text("Hyderabad")
                time.sleep(2)
                
                # Click Search button
                search_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnGo")
                search_button.click()
                time.sleep(3)
                
                try:
                    # Find and extract data from the table
                    table = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_grdProviderDetails"))
                    )
                    
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    
                    # Skip header row and process data rows
                    for row in rows[1:]:  # Skip header row
                        cols = row.find_elements(By.TAG_NAME, "td")
                        if len(cols) >= 4:
                            hospital_data = {
                                'Insurance Company': insurance_name,
                                'Serial No': cols[0].text.strip(),
                                'Hospital Name': cols[1].text.strip(),
                                'Address': cols[2].text.strip(),
                                'Contact': cols[3].text.strip()
                            }
                            all_hospital_data.append(hospital_data)
                            print(f"Found hospital: {hospital_data['Hospital Name']}")
                    
                    print(f"Processed {len(rows)-1} hospitals for {insurance_name}")
                    
                except NoSuchElementException:
                    print(f"No hospitals found for {insurance_name}")
                    continue
                    
            except Exception as e:
                print(f"Error processing {insurance_name}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        
    # Print summary of all collected data
    print("\nSummary:")
    print(f"Total hospitals found: {len(all_hospital_data)}")
    print("\nDetailed Data:")
    for hospital in all_hospital_data:
        print("\n-------------------")
        for key, value in hospital.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    scrape_hospitals()
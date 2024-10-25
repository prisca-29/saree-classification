!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
# Install required packages
!pip install selenium webdriver_manager pandas

# Import required libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

class SareeRetailerTest:
    def __init__(self):
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the webdriver with updated syntax
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
        # Load the dataset
        self.df = pd.read_csv('saree_retailer_data.csv')
        
    def setup(self):
        """Setup method to initialize the test environment"""
        self.driver.implicitly_wait(10)
        
    def test_retailer_websites(self):
        """Test method to check retailer websites"""
        for index, row in self.df.iterrows():
            if pd.notna(row['website']):
                try:
                    self.driver.get(row['website'])
                    time.sleep(2)
                    
                    assert self.driver.current_url != "about:blank"
                    print(f"Successfully accessed website for {row['Saree_Retailer_name']}")
                    
                except Exception as e:
                    print(f"Error accessing website for {row['Saree_Retailer_name']}: {str(e)}")

    def test_contact_information(self):
        """Test method to validate contact information format"""
        for index, row in self.df.iterrows():
            # Validate mobile number format
            if pd.notna(row['Mobile_1']):
                assert str(row['Mobile_1']).isdigit(), f"Invalid mobile number for {row['Saree_Retailer_name']}"
                assert len(str(row['Mobile_1'])) == 10, f"Invalid mobile number length for {row['Saree_Retailer_name']}"
            
            # Validate email format
            if pd.notna(row['Email_1']):
                assert '@' in row['Email_1'], f"Invalid email format for {row['Saree_Retailer_name']}"

    def test_address_validation(self):
        """Test method to validate address information"""
        for index, row in self.df.iterrows():
            if pd.notna(row['city']) and pd.notna(row['state']):
                print(f"Address validation passed for {row['Saree_Retailer_name']}")
            else:
                print(f"Missing address information for {row['Saree_Retailer_name']}")

    def test_search_functionality(self):
        """Test method to simulate search functionality"""
        search_terms = ['Silk Sarees', 'Wedding Sarees', 'Designer Sarees']
        
        for term in search_terms:
            try:
                print(f"Testing search for: {term}")
                matches = self.df[self.df['Saree_Retailer_name'].str.contains(term, na=False)].shape[0]
                print(f"Found {matches} retailers matching '{term}'")
                
            except Exception as e:
                print(f"Error during search test for {term}: {str(e)}")

    def teardown(self):
        """Cleanup method to close the browser and clean up resources"""
        self.driver.quit()

def run_tests():
    test = SareeRetailerTest()
    try:
        test.setup()
        print("Running website tests...")
        test.test_retailer_websites()
        print("\nRunning contact information tests...")
        test.test_contact_information()
        print("\nRunning address validation tests...")
        test.test_address_validation()
        print("\nRunning search functionality tests...")
        test.test_search_functionality()
    finally:
        test.teardown()

if __name__ == "__main__":
    run_tests()
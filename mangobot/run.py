from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setup Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
print("Initializing Chrome Driver")
driver = webdriver.Chrome(options=chrome_options)
print("Chrome Driver Initialized")

# URL to scrape
url = "https://www.blogger.com/"

# Get the URL
driver.get(url)

# Extract the page title
print(driver.title)

# Close the driver
driver.quit()
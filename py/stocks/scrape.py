from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Investing.com NASDAQ Stocks URL
url = "https://www.investing.com/indices/nasdaq-composite-components"

# Setup WebDriver (Headless mode)
options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions()
# _options.add_argument("--headless=new")  # or "--headless=old"
options.add_argument("--disable-gpu")  # Helps avoid rendering overhead
driver = webdriver.Chrome(options=options)
options.add_argument("--log-level=3")  # Reduce logging
options.add_argument("--disable-logging")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # Prevents RAM overload
# options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(options=options)

# Open the page
driver.get(url)
time.sleep(5)  # Allow page to load

# Extract stock table rows
stocks = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# Store stock data
stock_data = []

for stock in stocks:
    try:
        name = stock.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        price = stock.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        change = stock.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
        volume = stock.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text

        stock_data.append({
            "Stock": name,
            "Price": price,
            "Change %": change,
            "Volume": volume
        })
    except:
        continue  # Skip rows that fail to load

# Close the browser
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(stock_data)

# Save data to CSV
df.to_csv("nasdaq_stocks.csv", index=False)

# Print extracted data
print(df.head())

# If you want to visualize, install pandas and use:
# pip install pandas

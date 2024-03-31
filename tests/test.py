import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
options = ChromeOptions()
options.set_capability('sessionName', 'Flipkart')
driver = webdriver.Chrome(options=options)

driver.get("https://www.flipkart.com/")

search_box = driver.find_element(By.CLASS_NAME,"Pke_EE")
search_box.send_keys("Samsung Galaxy S10")
search_box.submit()

# mobiles_category = browser.find_element(By.LINK_TEXT,"Mobiles")

mobiles_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1jJQdf')))
print(mobiles_link.text)
mobiles_link.click()


brand_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_3879cV')))
brand_link.click()
print(brand_link.text)

assured_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Dqv36E')))
assured_link.click()
print("assured")

hightoLow_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div[4]')))
hightoLow_link.click()
print(hightoLow_link.text)

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._1AtVbE.col-12-12")))

# Find all the product divs
product_divs = driver.find_elements(By.CSS_SELECTOR, "div._1AtVbE.col-12-12")
count = 1
for product_div in product_divs:
    try:
        if count >= 24:
                break
        else:          
            # Extract product name
            product_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._4rR01T"))).text
            # product_name = product_div.find_element(By.CSS_SELECTOR, "div._4rR01T").text
                
            # Extract display price
            display_price = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._30jeq3._1_WHN1"))).text
            # display_price = product_div.find_element(By.CSS_SELECTOR, "div._30jeq3._1_WHN1").text

            # Extract link to product details page
            product_link_a = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a._1fQZEK")))
            product_link = product_link_a.get_attribute("href")
            # product_link = product_div.find_element(By.CSS_SELECTOR, "a._1fQZEK").get_attribute("href")
            # Print product information
            if("SAMSUNG" in product_name):
                print(count)
                print("Product Name:", product_name)
                print("Display Price:", display_price)
                print("Link to Product Details Page:", product_link)
                print("=" * 50)
                count +=1
    except NoSuchElementException as err:
        message = 'Exception: ' + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    except Exception as err:
        message = 'Exception: ' + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
driver.quit()
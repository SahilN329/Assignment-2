import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import json

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
options = ChromeOptions()
options.set_capability('sessionName', 'Flipkart')
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.flipkart.com/")

    WebDriverWait(driver, 10).until(EC.title_contains('Online Shopping Site for Mobiles, Electronics, Furniture, Grocery, Lifestyle, Books & More. Best Offers!'))
    search_box = driver.find_element(By.CLASS_NAME,"Pke_EE")
    search_box.send_keys("Samsung Galaxy S10")
    search_box.submit()

    mobiles_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1jJQdf')))
    print(mobiles_link.text)
    if mobiles_link.text =='Mobiles':
        mobiles_link.click()

    brand_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_3879cV')))
    print(brand_link.text)
    if brand_link.text =='SAMSUNG':
        brand_link.click()
    
    assured_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Dqv36E')))
    print("assured")
    assured_link.click()

    hightoLow_link = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div[4]')))
    print(hightoLow_link.text)
    if hightoLow_link.text == 'Price -- High to Low':
        hightoLow_link.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._1AtVbE.col-12-12")))

    product_divs = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._1AtVbE.col-12-12")))
    product_divs = driver.find_elements(By.CSS_SELECTOR, "div._2kHMtA")
    count = 0
    product_list = []
    var = 2

    for product_div in product_divs:
        try:    
            if count >= 24:
                break
            else:          
                parentXPath = f'//*[@id="container"]/div/div[3]/div/div[2]/div[{var}]'
                nameXPath = parentXPath + '/div/div/div/a/div[2]/div[1]/div[1]'
                priceXPath = parentXPath + '/div/div/div/a/div[2]/div[2]/div[1]/div[1]/div[1]'
                linkXPath = parentXPath + '/div/div/div/a'
                var += 1
                product_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, nameXPath))).text
                
                display_price = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, priceXPath))).text
                
                product_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, linkXPath))).get_attribute('href')

                print(count)
                print("Product Name:", product_name)
                product_list.append(product_name)
                print("Display Price:", display_price)
                print("Link to Product Details Page:", product_link)
                print("=" * 50)
                count +=1
            
            
        except Exception as err:
            message = 'Exception: ' + str(err.__class__) + str(err.msg)
            print(json.dumps(message))
    if(len(product_list)==24):
        executor_object = {
            'action': 'setSessionStatus',
            'arguments': {
                'status': "passed",
                'reason': "List of mobiles visible"
            }
        }
        browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
        driver.execute_script(browserstack_executor)
    time.sleep(10)
except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    print(json.dumps(message))
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    print(json.dumps(message))
finally:
    driver.quit()
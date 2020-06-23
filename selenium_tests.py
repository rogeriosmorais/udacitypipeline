import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
sys.path.insert(0,'/home/vsts/work/node_modules/chromedriver/lib/chromedriver/chromedriver')
sys.path.insert(0,'/home/vsts/work/node_modules/chromedriver/lib/chromedriver/')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

import time

def login (user, password):
    print ('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless") 
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[class='btn_action']").click()
    time.sleep(2)
    #driver.save_screenshot("screenshot.png")
    our_search = driver.find_element_by_css_selector("div[class=product_label]").text
    assert "Products" in our_search
    print("User {} logged in successfuly".format(user))
    return driver

def addProductsToCart(driver):
    for inventory_item in driver.find_elements_by_css_selector("div[class='inventory_item']"):    
      product = inventory_item.find_element_by_css_selector("div[class='inventory_item_label']").text.splitlines()[0]      
      button = inventory_item.find_element_by_css_selector("div[class='pricebar'] > button[class='btn_primary btn_inventory']")
      if button.text == 'ADD TO CART':
        button.click()
      button = inventory_item.find_element_by_css_selector("div[class='pricebar'] > button[class='btn_secondary btn_inventory']")
      assert button.text == 'REMOVE'
      print("Added {} to cart".format(product))    

def removeProductsFromCart(driver):
    for inventory_item in driver.find_elements_by_css_selector("div[class='inventory_item']"):    
      product = inventory_item.find_element_by_css_selector("div[class='inventory_item_label']").text.splitlines()[0]      
      button = inventory_item.find_element_by_css_selector("div[class='pricebar'] > button[class='btn_secondary btn_inventory']")
      if button.text == 'REMOVE':
        button.click()
      button = inventory_item.find_element_by_css_selector("div[class='pricebar'] > button[class='btn_primary btn_inventory']")
      assert button.text == 'ADD TO CART'
      print("Removed {} from cart".format(product))


driver = login('standard_user', 'secret_sauce')
addProductsToCart(driver)
removeProductsFromCart(driver)

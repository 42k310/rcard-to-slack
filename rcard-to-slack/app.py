from dotenv import load_dotenv
import os
from selenium import webdriver


def lambda_handler(event, context):

    load_dotenv()  # pjt_roo/.env にID, PASSを定義
    ID = os.environ['RCARD_ID']
    PASS = os.environ['RCARD_PASS']

    driver = webdriver.Chrome(
        executable_path="/Users/kentasato/Documents/chromedriver")
    driver.get("https://www.rakuten-card.co.jp/e-navi/")

    id_form = driver.find_element_by_id("u")
    pass_form = driver.find_element_by_id("p")

    id_form.send_keys(ID)
    pass_form.send_keys(PASS)

    login_button = driver.find_element_by_id("loginButton")
    login_button.click()

    amount = driver.find_element_by_id("rf-tera")
    print(1111111111111111)
    print(amount)

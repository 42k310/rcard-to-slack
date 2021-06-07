from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def lambda_handler(event, context):

    load_dotenv()  # pjt_roo/.env にID, PASSを定義
    ID = os.environ['RCARD_ID']
    PASS = os.environ['RCARD_PASS']

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path="/Users/kentasato/Documents/chromedriver",  # TODO: デプロイ後のパスに修正
        options=options)

    # ログイン
    driver.get("https://www.rakuten-card.co.jp/e-navi/")

    id_form = driver.find_element_by_id("u")
    pass_form = driver.find_element_by_id("p")

    id_form.send_keys(ID)
    pass_form.send_keys(PASS)

    login_button = driver.find_element_by_id("loginButton")
    login_button.click()

    # データ取得
    amount = driver.find_elements_by_class_name("rf-tera")[0].text
    left_point = driver.find_elements_by_class_name("rf-red")[7].text
    expected_point = driver.find_elements_by_class_name("rf-red")[9].text

    # TODO: Slackへ連携
    text = '支払い予定金額：' + amount + '¥n'
    + 'ポイント残高：' + left_point + '¥n'
    + '獲得予定ポイント：' + expected_point

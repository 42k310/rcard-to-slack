from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import slackweb


def lambda_handler(event, context):

    # FIX_ME: pjt_root/.env に以下を定義
    # RCARD_URL: e-naviのURL
    # RCARD_ID, RCARD_PASS
    # SLACK_WEBHOOK: webhookのURL
    load_dotenv()
    ID = os.environ['RCARD_ID']
    PASS = os.environ['RCARD_PASS']

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path="/Users/kentasato/Documents/chromedriver",  # TODO: デプロイ後のパスに修正
        options=options)

    # ログイン
    driver.get(os.environ['RCARD_URL'])

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

    # Slack通知
    text = '支払い予定金額：' + amount + '\n'\
        'ポイント残高：' + left_point + 'pt\n'\
        '獲得予定ポイント：' + expected_point + 'pt'
    attachments = []
    attachment = {"title": "楽天カード通知",
                  "title_link": os.environ['RCARD_URL'],
                  'mrkdwn_in': ['text'],
                  "color": "#2eb886",
                  "text": text,
                  "mrkdwn_in": ["text", "pretext"]}
    attachments.append(attachment)

    slack = slackweb.Slack(url=os.environ['SLACK_WEBHOOK'])
    slack.notify(attachments=attachments,
                 username="カードマン",
                 icon_emoji=":card_man")

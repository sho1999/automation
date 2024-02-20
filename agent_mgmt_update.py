import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


# 初期設定
login_link = "https://mds-fund.herokuapp.com/affiliaters/login"
base_target_link = "https://mds-fund.herokuapp.com/affiliaters?utf8=%E2%9C%93&affiliater_info=&rank%5B%5D=S&rank%5B%5D=A&rank%5B%5D=B&company=&year=&month=&commit=%E6%A4%9C%E7%B4%A2&sale_id=21&meeting_month=&bank=&work="
login_id = "mds"
login_pass = "YEMS4QECADMIN"

# データの一時保存用リスト
collected_data = []

# スプレッドシートの設定
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('mds-agent-management-5b04d726f3b8.json', scope)
client = gspread.authorize(creds)
sheet = client.open('MDS AGENT MGMT').get_worksheet(2)


# WebDriverの初期化
driver = webdriver.Chrome()

# ログインページにアクセス
driver.get(login_link)
driver.find_element(By.NAME, 'login_id').send_keys(login_id)
driver.find_element(By.NAME, 'login_pass').send_keys(login_pass)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'commit'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sidenav')))

page_number = 1
while True:
    # 対象ページに移動
    target_link = f"{base_target_link}&page={page_number}" if page_number > 1 else base_target_link
    driver.get(target_link)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody/tr")))
    except TimeoutException:
        print(f"ページ {page_number} に要素が見つかりません。")
        break

    table_rows = driver.find_elements(By.XPATH, "//tbody/tr")
    if not table_rows:
        print("ページに行がありません。")
        break

    for index, _ in enumerate(table_rows):
        row = driver.find_elements(By.XPATH, "//tbody/tr")[index]
        name = row.find_element(By.XPATH, ".//div/a[contains(@href, '/affiliaters/')]").text
        agent_id = row.find_element(By.XPATH, ".//div/a[contains(@href, '/affiliaters/search?')]").text
        try:
            email_text = row.find_element(By.XPATH, ".//td[contains(., '@')]").text
            email = email_text.split('\n')[-1]
        except NoSuchElementException:
            print(f"メールアドレスが見つかりませんでした。行: {index + 1}")
            email = 'aaa@gmail.com'
            continue

        link = row.find_element(By.CSS_SELECTOR, 'td div:nth-of-type(2) a')
        link_url = link.get_attribute('href')
        driver.get(link_url)

        mycard_elements = driver.find_elements(By.CSS_SELECTOR, '.mycard div[style*="padding: 8px 10px; white-space:nowrap;"]')
        latest_date = "NO CONTRACT"
        for element in mycard_elements:
            text = element.text
            prev_element = element.find_element(By.XPATH, './preceding-sibling::div[1]')
            if '5,000円' in prev_element.text or '6,000円' in prev_element.text or '7,000円' in prev_element.text:
                latest_date = text
                break
                

        if latest_date:
            latest_date_cleaned = latest_date.strip("'")
            formatted_date = latest_date_cleaned.replace('-', '/')
        
        try:
             # 報酬リンクを見つける
            reword_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/affiliaters/customers_list"]'))
            )
            reword_link_url = reword_link.get_attribute('href')
            driver.get(reword_link_url)

            ig_count = 0
            meo_count = 0
            single_count = 0
            multi_count = 0
            while True:
                mycard_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mycard")))
                mycard_text = mycard_element.text

                # カウントを取得
                ig_count += mycard_text.count('IG BASIC')
                meo_count += mycard_text.count('MEO BASIC')
                single_count += mycard_text.count('SINGLE')
                multi_count += mycard_text.count('MULTI')

                # 次のページに移動するためのリンクを探す
                next_page_links = driver.find_elements(By.CSS_SELECTOR, 'a[rel="next"]')
                if len(next_page_links) > 1:
                    next_page_url = next_page_links[0].get_attribute('href')
                    driver.get(next_page_url)
                else:
                    break
        except TimeoutException:
            break

        collected_data.append([
            name,
            agent_id,
            email,
            ig_count + meo_count + single_count + multi_count,
            formatted_date
        ])

        driver.get(target_link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody/tr")))

    page_number += 1

    # if page_number == 2:
    #     break

driver.quit()

# スプレッドシートにデータをバッチで更新するためのリストを作成
values = []
for data in collected_data:
    values.append([
        data[0],  # name
        data[1],  # agentId
        data[2],  # email
        data[3],  # contract
        data[4]   # lastContractDate
    ])

# 更新範囲の指定
row_index = 5  # 5行目から開始
range_name = f'B{row_index}:F{row_index + len(values) - 1}'

# バッチで更新
sheet.batch_update([{
    'range': range_name,
    'values': values
}])

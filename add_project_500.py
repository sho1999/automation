import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# スプレッドシートのデータを取得
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('mds-agent-management-bcc43f1a58ee.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1R5_3hbo0pvgSytMcdSqUlaOKgbX89qRJulItVt0_HFw").get_worksheet(0)

# スプレッドシートの全データを取得
data = sheet.get('B3:E')

add_project_form_link = "https://mds-fund.herokuapp.com/affiliaters/edit_business_case"
login_link = "https://mds-fund.herokuapp.com/affiliaters/login"

driver = webdriver.Chrome()

# ログインページにアクセス
driver.get(login_link)

# ログイン情報の入力
driver.find_element(By.NAME, 'login_id').send_keys('mds')
driver.find_element(By.NAME, 'login_pass').send_keys('YEMS4QECADMIN')

# ログインボタンをクリック
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, 'commit'))
).click()

# ログイン後のページがロードされるのを待つ
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'sidenav'))
)

for row in data:
    # 代理店IDを入力
    driver.get(add_project_form_link)

    driver.find_element(By.ID, 'business_case_original_id').send_keys(row[0])

    # ページ上の最初のドロップダウン(案件担当)を開き、ドロップダウンメニューの選択肢を取得し、「代理店案件」にする
    first_dropdown_trigger = driver.find_elements(By.CSS_SELECTOR, 'input.select-dropdown.dropdown-trigger')[0]
    first_dropdown_trigger.click()
    time.sleep(1)
    first_dropdown_menu = driver.find_elements(By.CSS_SELECTOR, 'ul.dropdown-content.select-dropdown')[0]
    manager_options = first_dropdown_menu.find_elements(By.TAG_NAME, 'span')
    for option in manager_options:
        if option.text == "代理店案件":
            option.click()
            break
    
    # ページ上の2番目のドロップダウン(ステータス)を開き、ドロップダウンメニューの選択肢を取得し、「成約済み」にする
    second_dropdown_trigger = driver.find_elements(By.CSS_SELECTOR, 'input.select-dropdown.dropdown-trigger')[1]
    second_dropdown_trigger.click()
    time.sleep(0.3) 
    second_dropdown_menu = driver.find_elements(By.CSS_SELECTOR, 'ul.dropdown-content.select-dropdown')[1]
    manager_options = second_dropdown_menu.find_elements(By.TAG_NAME, 'span')
    for option in manager_options:
        if option.text == "成約済み":
            option.click()
            break

    # クライアント名を入力
    driver.find_element(By.ID, 'business_case_company').send_keys(row[1])

    # ページ上の3番目のドロップダウン(営業担当者)を開き、ドロップダウンメニューの選択肢を取得し、「成約済み」にする
    third_dropdown_trigger = driver.find_elements(By.CSS_SELECTOR, 'input.select-dropdown.dropdown-trigger')[2]
    third_dropdown_trigger.click()
    time.sleep(0.3) 
    third_dropdown_menu = driver.find_elements(By.CSS_SELECTOR, 'ul.dropdown-content.select-dropdown')[2]
    manager_options = third_dropdown_menu.find_elements(By.TAG_NAME, 'span')
    for option in manager_options:
        if option.text == row[2]:
            option.click()
            break
    # JavaScriptを使用してドロップダウンを閉じる
    driver.execute_script('arguments[0].style.display = "none";', third_dropdown_menu)

    # 電話番号を入力
    driver.find_element(By.ID, 'business_case_tel').send_keys('08012345678')

    # メールアドレスを入力
    driver.find_element(By.ID, 'business_case_email').send_keys('1@1')

    driver.execute_script("window.scrollBy(0, 250);")

    # 見込みサービスを入力
    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][value="appointment"]')
    driver.execute_script("arguments[0].click();", checkbox)

    # 日付を入力
    date_string = row[3]
    year, month, day = map(str, date_string.split('/'))

    date_dropdown_trigger = driver.find_elements(By.CSS_SELECTOR, 'input.select-dropdown.dropdown-trigger')[3]
    date_dropdown_trigger.click()
    time.sleep(0.3) 
    date_dropdown_menu = driver.find_elements(By.CSS_SELECTOR, 'ul.dropdown-content.select-dropdown')[3]
    manager_options = date_dropdown_menu.find_elements(By.TAG_NAME, 'span')
    for option in manager_options:
        if option.text == year:
            option.click()
            break

    # 月を入力
    date_dropdown_trigger = driver.find_elements(By.CSS_SELECTOR, 'input.select-dropdown.dropdown-trigger')[4]
    date_dropdown_trigger.click()
    time.sleep(0.3) 
    date_dropdown_menu = driver.find_elements(By.CSS_SELECTOR, 'ul.dropdown-content.select-dropdown')[4]
    manager_options = date_dropdown_menu.find_elements(By.TAG_NAME, 'span')
    for option in manager_options:
        if option.text == month:
            option.click()
            break
    
    # 日を入力
    date_dropdown_trigger = driver.find_elements(By.CSS_SELECTOR, 'input.select-dropdown.dropdown-trigger')[5]
    date_dropdown_trigger.click()
    time.sleep(0.3) 
    date_dropdown_menu = driver.find_elements(By.CSS_SELECTOR, 'ul.dropdown-content.select-dropdown')[5]
    manager_options = date_dropdown_menu.find_elements(By.TAG_NAME, 'span')
    for option in manager_options:
        if option.text == day:
            option.click()
            break

    # 報酬金を入力
    driver.find_element(By.ID, 'business_case_reward').send_keys('500')

    # 情報を更新
    submit_button = driver.find_element(By.ID, 'check')
    submit_button.click()

driver.quit()
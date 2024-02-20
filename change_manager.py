from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time

login_link = "https://mds-fund.herokuapp.com/affiliaters/login"
argent_index_link = "https://mds-fund.herokuapp.com/affiliaters"
basic_password = "YEms4QeC"
login_id = "mds"
login_pass = "YEMS4QECADMIN"
manager_name = "霜鳥 涼"

driver = webdriver.Chrome()

# ログインページにアクセス
driver.get(login_link)

# ログイン情報の入力
driver.find_element(By.NAME, 'login_id').send_keys(login_id)
driver.find_element(By.NAME, 'login_pass').send_keys(login_pass)

# ログインボタンをクリック
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, 'commit'))
).click()

# ログイン後のページがロードされるのを待つ
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'sidenav'))
)

agent_info = {}
with open('agent_info.txt', 'r') as file:
    lines = file.readlines()
    for i in range(0, len(lines), 2):  # 2行ごとの処理
        # 名前行を読み込んで不要な空白を削除
        agent_name = lines[i].strip()  
        # ID行を読み込んで不要な空白とダブルクオートを削除
        agent_id = lines[i+1].strip().replace('"', '')
        # 辞書にIDをキーとして名前を値として保存する
        agent_info[agent_id] = agent_name


for agent_id, desired_date in agent_info.items():
    try:
        driver.get(argent_index_link)

        # 検索バーに名前を入力し、検索
        search_box = driver.find_element(By.ID, 'affiliater_info')
        search_box.clear()
        search_box.send_keys(agent_id)
        search_button = driver.find_element(By.NAME, 'commit')
        search_button.click()

        # 最初のリンクをクリック
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr:nth-child(1) td div a'))
        ).click()

        # "重要情報" ボタンをクリック
        important_info_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.tab')
        important_info_button.click()

        # ベーシック認証のポップアップが表示されたときの処理
        alert = Alert(driver)
        alert.send_keys(basic_password)
        alert.accept()

        # ドロップダウンメニューを開く
        dropdown_trigger = driver.find_element(By.CSS_SELECTOR, 'input.select-dropdown.dropdown-trigger')
        dropdown_trigger.click()

        # "manager_name" のテキストを持つ要素をクリック
        manager_option = driver.find_element(By.XPATH, f"//span[text()='{manager_name}']")
        manager_option.click()

        # 担当開始日を入力するためのフィールドを特定、新しい日付を入力
        # date_field = driver.find_element(By.ID, 'affiliater_charge_date')
        # date_field.clear()
        # date_field.send_keys(desired_date)
        # date_field.send_keys(desired_date)  # 新しい日付を入力

        # "更新する" ボタンを特定してクリック
        update_button = driver.find_element(By.NAME, 'commit')
        update_button.click()

    except NoSuchElementException:
        print(f"Element not found for agent {agent_id}, skipping.")

driver.quit()
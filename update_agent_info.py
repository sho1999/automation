# agent_names.txtに書いてある人の情報のみ取得

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

login_link = "https://mds-fund.herokuapp.com/affiliaters/login"
argent_index_link = "https://mds-fund.herokuapp.com/affiliaters"
login_id = "mds"
login_pass = "YEMS4QECADMIN"

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

with open('agent_names.txt', 'r') as file:
    for name in file:
        name = name.strip()
        driver.get(argent_index_link)

        # 検索バーに名前を入力し、検索
        search_box = driver.find_element(By.ID, 'affiliater_info')
        search_box.clear()
        search_box.send_keys(name)
        search_button = driver.find_element(By.NAME, 'commit')
        search_button.click()

        # i番目のリンクをクリック
        link_selector = f'tbody tr:nth-child({i + 1}) td div a'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, link_selector))
        ).click()

        # 新しいページで特定の要素がロードされるのを待つ
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.show_field div.input-field'))
        )
        
        # 情報を抽出
        name_element = driver.find_element(By.XPATH, "//tr/td/div/a[contains(@href, '/affiliaters/')]")
        agent_id_element = driver.find_element(By.XPATH, "//tr/td/div/a[contains(@href, '/affiliaters/search?')]")
        email_element = driver.find_element(By.XPATH, "//tr/td[contains(., '@') and not(contains(., 'YEMS4QECADMIN'))]")
       

        # 抽出した情報を取得
        name = name_element.text
        agent_id = agent_id_element.text
        email_text = email_element.text
        email_parts = email_text.split('\n')  # 改行で分割
        email = [part for part in email_parts if '@' in part][0]  # メールアドレスを含む部分を取得

        # 結果を出力
        print(f"{email}\t{name}\t{email}\t{agent_id}")


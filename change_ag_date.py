from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()

# ログインページにアクセス
driver.get('https://mds-fund.herokuapp.com/affiliaters/login')

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

### テキストに書かれたのIDで担当者変更 ###

argent_index_link = "https://mds-fund.herokuapp.com/affiliaters"

with open('agent_info.txt', 'r') as file:
    for agent_id in file:
        driver.get(argent_index_link)

        # 検索バーに名前を入力し、検索
        search_box = driver.find_element(By.ID, 'affiliater_info')
        search_box.clear()
        search_box.send_keys(agent_id)
        search_button = driver.find_element(By.NAME, 'commit')
        search_button.click()

        # i番目のリンクをクリック
        link_selector = f'tbody tr:nth-child(1) td div a'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, link_selector))
        ).click()

        # 新しいページで特定の要素がロードされるのを待つ
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.show_field div.input-field'))
        )

        # フォーム要素を見つける
        form = driver.find_element(By.CLASS_NAME, 'edit_affiliater')

        # フォーム内の特定のinput要素を見つける
        # このinput要素は class="field datepicker" を持っています
        date_input = form.find_element(By.CSS_SELECTOR, 'input.field.datepicker')

        # 日付を変更（'2023/11/21'に変更）
        date_input.clear()
        date_input.send_keys('2024/1/31')

        # ページをスクロールダウン
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 更新ボタンをクリック
        update_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="更新する"]')
        update_button.click()



### 提供したリンクで日付を変更 ###
    
# target_link = f"https://mds-fund.herokuapp.com/affiliaters?utf8=%E2%9C%93&affiliater_info=&rank%5B%5D=S&rank%5B%5D=A&rank%5B%5D=B&company=&year=&month=&commit=%E6%A4%9C%E7%B4%A2&sale_id=29&meeting_year=2023&meeting_month=12&bank=&work="

# driver.get(target_link)

# for i in range(30):
#     # i番目のリンクをクリック
#     link_selector = f'tbody tr:nth-child({i + 1}) td div a'
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, link_selector))
#     ).click()

#     # 新しいページで特定の要素がロードされるのを待つ
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, 'div.show_field div.input-field'))
#     )

#     # フォーム要素を見つける
#     form = driver.find_element(By.CLASS_NAME, 'edit_affiliater')

#     # フォーム内の特定のinput要素を見つける
#     # このinput要素は class="field datepicker" を持っています
#     date_input = form.find_element(By.CSS_SELECTOR, 'input.field.datepicker')

#     # 日付を変更（'2023/11/21'に変更）
#     date_input.clear()
#     date_input.send_keys('2024/1/31')

#     # ページをスクロールダウン
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # 更新ボタンをクリック
#     update_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="更新する"]')
#     update_button.click()

#     # 一覧ページに戻る
#     driver.get(target_link)
    
# page_number = 2
# target_link = f"https://mds-fund.herokuapp.com/affiliaters?affiliater_info=&bank=&company=&meeting_month=12&meeting_year=2023&month=&page={page_number}&rank%5B%5D=S&rank%5B%5D=A&rank%5B%5D=B&sale_id=29&work=&year="

# for _ in range(1): 
    
#     driver.get(target_link)

#     for i in range(30):
#         # i番目のリンクをクリック
#         link_selector = f'tbody tr:nth-child({i + 1}) td div a'
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, link_selector))
#         ).click()

#         # 新しいページで特定の要素がロードされるのを待つ
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'div.show_field div.input-field'))
#         )

#         # フォーム要素を見つける
#         form = driver.find_element(By.CLASS_NAME, 'edit_affiliater')

#         # フォーム内の特定のinput要素を見つける
#         # このinput要素は class="field datepicker" を持っています
#         date_input = form.find_element(By.CSS_SELECTOR, 'input.field.datepicker')

#         # 日付を変更（'2023/11/21'に変更）
#         date_input.clear()
#         date_input.send_keys('2023/12/31')

#         # ページをスクロールダウン
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # 更新ボタンをクリック
#         update_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="更新する"]')
#         update_button.click()

#         # 一覧ページに戻る
#         driver.get(target_link)
    
#     page_number += 1

# driver.quit()


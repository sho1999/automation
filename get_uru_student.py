import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ログインページのURL
LOGIN_URL = 'https://lim-administration.herokuapp.com/affiliaters/login'

# ログイン後のページURL
TARGET_URL = 'https://lim-administration.herokuapp.com/connects'

# ログイン情報
payload = {
    'login_id': 'limconsulting',  # ユーザー名
    'login_pass': 'YEms4QeC5434',  # パスワード
}

# 期間を指定
FROM_DATE = datetime.strptime('2023-10-24', '%Y-%m-%d')
TO_DATE = datetime.strptime('2023-11-01', '%Y-%m-%d')

# セッションを作成
with requests.Session() as session:
    # ログイン
    get = session.get(LOGIN_URL, data=payload)

    # ログインが成功したか確認
    if get.status_code == 200 and "authentication failed" not in get.text.lower():
        print("Login successful")
    else:
        print("Login failed")
        exit()

    page = 1

    while True:
        if page == 1:
            r = session.get(TARGET_URL)
        else:
            r = session.get(f"{TARGET_URL}?page={page}")

        soup = BeautifulSoup(r.text, 'html.parser')
        
        tbody = soup.find('tbody')
        if tbody is None:  # tbodyタグがなければループを終了
            break

        for row in tbody.find_all('tr'):
            columns = row.find_all('td')
            
            # 名前、メールアドレス、申し込み日を取得
            name = columns[1].get_text(strip=True)  # 2番目の列
            email = columns[3].get_text(strip=True)  # 4番目の列
            application_date_str = columns[5].get_text(strip=True)  # 6番目の列
            application_date = datetime.strptime(application_date_str, '%Y-%m-%d')
            
            # 指定した期間内であれば出力
            if FROM_DATE <= application_date <= TO_DATE:
                print(f"{name}\t{email}\t{application_date_str}")

            # FROM_DATEより古いデータが来たらそこで探索をやめる
            elif application_date < FROM_DATE:
                exit()

        # 次ページのリンクがあるか確認
        next_link = soup.find('a', rel='next')
        if next_link is None:  # 次ページのリンクがなければループを終了
            break

        page += 1  # 次のページ番号へ

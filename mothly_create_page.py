import json
from tqdm import tqdm
import requests
from datetime import datetime, timedelta, timezone
import calendar

def init_settings():
    today = datetime.now()
    this_year = today.year
    this_month = today.month
    last_day = calendar.monthrange(this_year, this_month)[1]
    last_date = datetime(this_year, this_month, last_day).strftime("%Y-%m-%d")
    first_date = datetime(this_year, this_month, 1).strftime("%Y-%m-%d")

    return first_date, last_date

def set_payload(after_date, before_date):
    payload = {
        "filter": {
            "property": "날짜",
            "date": {
                "on_or_after": f"{after_date}",
                "on_or_before": f"{before_date}"
            }
        }
    }
    return payload



# 노션 API 기본 정보
key_database_id = "페이지 데이터베이스 아이디"
api_key = "내 API 키"
api_url = f"https://api.notion.com/v1/databases/{key_database_id}/query"
api_url_page = "https://api.notion.com/v1/pages/"
new_number = 0

# 페이지 타이틀 생성 회차 구하기
# 노션 API 헤더
headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 시작
dates = init_settings()
payload = set_payload(dates[0], dates[1])

response = requests.post(api_url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    new_number = len(response.json().get("results",[])) + 1
    print(new_number)
else:
    print(response.text)


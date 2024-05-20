import json
import requests
from datetime import datetime, timedelta, timezone

key_database_id = "데이터베이스id"
api_key = "내프라이빗스크릿키"
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

response = requests.post(api_url, headers=headers)
new_number = len(response.json().get("results",[])) + 1

page_title = f"{new_number}차 : 제목"
# 페이지 타이틀 생성 회차 구하기

# 날짜 및 포맷 설정
# 단식시작시간 : 전날 오후 7시 30분
# 단식종료시간 : 오늘 오전 11시 30분
# 식사시작시간 : 오늘 오전 11시 30분
# 식사종료시간 : 오늘 오후 7시 30분

today = datetime.now().date()
yesterday = today - timedelta(days=1)
gmt_plus_9 = timezone(timedelta(hours=9))

h_start = datetime.combine(yesterday, datetime.strptime("19:30", "%H:%M").time(), gmt_plus_9)
h_end = datetime.combine(today, datetime.strptime("11:30", "%H:%M").time(), gmt_plus_9)
e_start = datetime.combine(today, datetime.strptime("11:30", "%H:%M").time(), gmt_plus_9)
e_end = datetime.combine(today, datetime.strptime("19:30", "%H:%M").time(), gmt_plus_9)

format_h_start = h_start.isoformat()
format_h_end = h_end.isoformat()
format_e_start = e_start.isoformat()
format_e_end = e_end.isoformat()
# 날짜 및 포맷 설정

# 요일
weekday_number = today.weekday()
days_of_week = ["월","화","수","목","금","토","일"]
today_day = days_of_week[weekday_number]
# 요일

# 페이지 생성 객체
page = {
    "parent": {
      "database_id": key_database_id
    },
    "properties": {
        "이름": {
			"title": [
				{
					"text": {
						"content": f"{page_title}"
					}
				}
			]
		},
        "요일": {
            "select": {
                "name": f"{today_day}"
            }
        },
        "날짜": {
            "date": {
                "start": f"{today}"
            }
        },
        "단식시작시간": {
            "date": {
                "start": f"{format_h_start}"
            }
        },
        "단식종료시간": {
            "date": {
                "start": f"{format_h_end}"
            }
        },
        "식사시작시간": {
            "date": {
                "start": f"{format_e_start}"
            }
        },
        "식사종료시간": {
            "date": {
                "start": f"{format_e_end}"
            }
        }
    }
}
# 페이지 생성 객체

response = requests.post(api_url_page, headers=headers, json=page)
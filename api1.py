import requests
import json
from datetime import datetime, date, timedelta
import pymysql
import sys
import time
import schedule

weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?"

service_key = 'VLLJPpWzDYk9PlT3cSSdGnrcAqJ9lUOVoX19ePNxEDtoy1Z8ueZOBs%2F2Bi0JYXg%2BhhHC0QRuOMd13EaYR0hveg%3D%3D'


def load_data(nx, ny, base_date, base_time):
    now = datetime.now()
    today = datetime.today()
    today_date = today.strftime("%Y%m%d")
    today_time = now.hour
    date_diff = int(today_date) - int(base_date)
    base_time = base_time[:-2] + '00'
    if 60 <= int(nx) <= 61 and 120 <= int(ny) <= 124 and len(base_date) == 8 and len(base_time) == 4:
        if date_diff >= 0 or (date_diff == 0 and today_time >= int(base_time[:2])) or (
                date_diff == 1 and today_time < int(base_time[:2])):
            pageNo = '1'
            numOfRows = '1000'
            payload = "serviceKey=" + service_key + "&" + \
                      "pageNo=" + pageNo + "&" + \
                      "numOfRows=" + numOfRows + "&" + \
                      "dataType=JSON" + "&" + \
                      "base_date=" + base_date + "&" + \
                      "base_time=" + base_time + "&" + \
                      "nx=" + nx + "&" + \
                      "ny=" + ny

            res = requests.get(weather_url + payload)
            if res.json()['response']['header']['resultCode'] == '00':
                conn = pymysql.connect(host='172.28.1.2', user='root', password='alstjd', db='weather', charset='utf8', \
                                       port=3306, connect_timeout=30)
                temp = {}
                for i in res.json()['response']['body']['items']['item']:
                    temp[i['category']] = i['obsrValue']
                cursor = conn.cursor()

                sql = f"INSERT INTO weather_data (x, y, Date, Time, PTY, REH, RN1, T1H, UUU, VEC, VVV, WSD) VALUES({int(nx)}, {int(ny)}, {base_date}, {int(base_time)}, {temp['PTY']}, {temp['REH']}, {temp['RN1']}, {temp['T1H']}, {temp['UUU']}, {temp['VEC']}, {temp['VVV']}, {temp['WSD']})"
                cursor.execute(sql)

                conn.commit()
                conn.close()
            else:
                return 0
        else:
            print("현재부터 24시간 전까지 시간을 입력해 주세요.")
    else:
        print("알맞은 값을 입력해 주세요. (x: 60~61, y: 120~124, 날짜: yyyymmdd, 시간: hhmm")
    return 1


time_list = []
now = datetime.now()
today = datetime.today()
today_date = today.strftime("%Y%m%d")
today_time = now.hour
print(today)
for i in range(24):
    str_time = '0'*(2-len(str(today_time))) + str(today_time) +'00'
    time_list.append((today_date, str_time))
    if today_time == 0:
        yesterday = date.today() - timedelta(days=1)
        today_date = yesterday.strftime('%Y%m%d')
        today_time = 23
    else:
        today_time -= 1
for D, T in time_list.__reversed__():
    for i in range(60, 62):
        for j in range(120, 125):
            load_data(str(i), str(j), D, T)
    print(f"({D}, {T}) data loaded")
print("end of loading")

def batchload():
    now = datetime.now()
    today = datetime.today()
    today_date = today.strftime("%Y%m%d")
    today_time = now.hour
    base_time = '0'*(2-len(str(today_time))) + str(today_time) + '00'
    while True:
        for i in range(60, 62):
            for j in range(120, 125):
                res = load_data(str(i), str(j), today_date, base_time)
                if res == 0:
                    if today_time == 0:
                        today_date = yesterday.strftime("%Y%m%d")
                        today_time = 23
                        base_time = '0'*(2-len(str(today_time))) + str(today_time) + '00'
                    else:
                        today_time -= 1
                        base_time = '0'*(2-len(str(today_time))) + str(today_time)+ '00'
                    break
            if res == 0:
                break
        if res == 1:
            break
    print(f"{today_date} {base_time} loaded")

if len(sys.argv) >= 2:
    if sys.argv[1] == 'param':
        now = datetime.now()
        today = datetime.today()
        today_date = today.strftime("%Y%m%d")
        today_time = now.hour
        nx, ny, base_date, base_time = input('x, y, 날짜(yyyymmdd), 시간(hhmm) : ').split()
        # nx, ny, base_date, base_time = '60', '120', '20220506', '2000'
        date_diff = int(today_date) - int(base_date)
        base_time = base_time[:-2] + '00'
        load_data(nx, ny, base_date, base_time)

schedule.every(60).minutes.do(batchload)

while True:
    schedule.run_pending()
    time.sleep(1)

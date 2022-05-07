import pymysql
rain_cat = ['없음', '비', '비/눈', '눈', '빗방울', '빗방울눈날림', '눈날림']
base_date = input('날짜(yyyymmdd): ')
# base_date = '20220506'

conn = pymysql.connect(host='172.28.1.2', user='root', password='alstjd', db='weather', charset='utf8', \
                                   port=3306, connect_timeout=30)
cursor = conn.cursor()

sql = f"SELECT * FROM weather_data WHERE Date = {base_date} ORDER BY Time ASC, x ASC, y ASC"

cursor.execute(sql)
res = cursor.fetchall()
for data in res:
    print(f'Time :{data[4]}  (x, y) :({data[1]}, {data[2]})  기온 :{data[8]}ºC  1시간 강수량 :{data[7]}mm  동서바람성분 :{data[9]}m/s  남북바람성분 :{data[11]}m/s  습도 :{data[6]}%  강수형태 :{rain_cat[data[5]]}  풍향 :{data[10]}deg  풍속 :{data[12]}m/s')

conn.commit()
conn.close()

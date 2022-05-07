import pymysql
data = ['T1H', 'REH', 'WSD']
nx, ny, base_date = input('x, y, 날짜(yyyymmdd)').split()
# nx, ny, base_date = '60', '120', '20220506'

conn = pymysql.connect(host='172.28.1.2', user='root', password='alstjd', db='weather', charset='utf8', \
                                   port=3306, connect_timeout=30)
cursor = conn.cursor()

sql = f"SELECT MAX(T1H), MIN(T1H), MAX(REH), MIN(REH), MAX(WSD), MIN(WSD), SUM(RN1) FROM weather_data WHERE Date = {base_date} and x = {nx} and y = {ny}"
cursor.execute(sql)
res = cursor.fetchall()

temp_data = []
for i in range(len(data)):
    sql = "SET @rowIndex=-1"
    cursor.execute(sql)
    sql = f"SELECT ROUND(AVG({data[i]}), 2) AS Median FROM (SELECT @rowIndex:=@rowIndex+1 AS RowNumber, {data[i]} FROM weather_data WHERE Date = {base_date} and x = {nx} and y = {ny} ORDER BY {data[i]}) sub WHERE RowNumber IN (FLOOR(@rowIndex / 2), CEIL(@rowIndex / 2));"
    cursor.execute(sql)
    temp_data.append(cursor.fetchall())
for data in res:
    print(f'(x, y) :({nx}, {ny})')
    print(f'기온의 최대값, 최소값, 중간값 :{data[0]}ºC, {data[1]}ºC, {temp_data[0][0][0]}ºC')
    print(f'습도의 최대값, 최소값, 중간값 :{data[2]}%, {data[3]}%, {temp_data[1][0][0]}%')
    print(f'풍속의 최대값, 최소값, 중간값 :{data[4]}m/s, {data[5]}m/s, {temp_data[2][0][0]}m/s')
    print(f'일일 누적 강수량 :{data[6]}mm')
conn.commit()
conn.close()
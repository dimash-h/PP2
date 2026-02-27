from datetime import datetime, date, timedelta
#1
today = date.today()
print(today - timedelta(days=5))
#2
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print(yesterday)
print(today)
print(tomorrow)
#3
now = datetime.now()
print(now.replace(microsecond=0))
#4
dt1 = datetime(2026, 2, 18, 10, 0, 0)
dt2 = datetime(2026, 2, 26, 12, 30, 0)
print(int(abs((dt2 - dt1).total_seconds())))
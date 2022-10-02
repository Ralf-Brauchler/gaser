import sys, datetime
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: <filename>")
    sys.exit(1)
_, file_name  = sys.argv

file = open(file_name, "r")
data = []
order = ["datetime", "type", "text", "value"]
for line in file.readlines():
    details = line.split("|")
    details = [x.strip() for x in details]
    structure = {key: value for key, value in zip(order, details)}
    data.append(structure)

faktor=11.450*0.9187
increment=faktor/100
format = "%Y-%m-%d %H:%M:%S"
moments = []
usage = []
sum=[]

hourly=[]
hourlyMoments=[]
lastHour=0
hourCollect=0

daily=[]
dailyMoments=[]
lastDay=0
dayCollect=0

for entry in data:
    if entry["text"] == "sensor change":
        if (entry["value"] == '1'):
            moment=datetime.datetime.strptime(entry["datetime"], format)
            moments.append(moment)
            usage.append(entry["value"])

            thisHour=moment.hour
            if lastHour==thisHour:
                hourCollect+=increment
            else:
                hourly.append(hourCollect)
                lastHour=moment.hour
                hourCollect=increment
                hourlyMoments.append(moment.replace(second=0, microsecond=0, minute=30, hour=moment.hour-1))

            thisDay=moment.day
            if lastDay == thisDay:
                dayCollect += increment
            else:
                daily.append(dayCollect)
                lastDay = moment.day
                dayCollect = increment
                moment = moment + datetime.timedelta(days=-1)
                dailyMoments.append(moment.replace(second=0, microsecond=0, minute=00, hour=12))

    if entry["text"] == "sum of gas":
        sum.append((float(entry["value"])-18620)/10)


plt.bar(hourlyMoments, hourly, width=0.036, color = "#aa0000", alpha = 0.6)
plt.bar(dailyMoments, daily, width=1, color = "#ccccff", alpha = 0.6)
plt.plot(moments, sum, color = "#00aa00", alpha = 0.6)
# plt.scatter(moments, usage, color = "#0000aa", alpha = 0.6)
plt.show()

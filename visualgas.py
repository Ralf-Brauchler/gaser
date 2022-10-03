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
        sum.append(float(entry["value"]))

# plt.scatter(moments, usage, color = "#0000aa", alpha = 0.6)
# plt.show()

fig, ax1 = plt.subplots()

hourlyColor = "#0000aa"
dailyColor = "#ccccff"
m3Color = "#00aa00"

ax1.set_xlabel('time')
ax1.set_ylabel('kWh / Tag', color=dailyColor)
ax1.bar(dailyMoments, daily, color = dailyColor, alpha = 0.6)
ax1.tick_params(axis='y', labelcolor=dailyColor)

ax2 = ax1.twinx()
ax2.set_ylabel('kWh / Stunde', color=hourlyColor)
ax2.bar(hourlyMoments, hourly, width=0.036, color=hourlyColor, alpha = 0.6)
ax2.tick_params(axis='y', labelcolor=hourlyColor)

ax3 = ax1.twinx()
ax3.set_ylabel('m3', color=m3Color, labelpad=-10)
ax3.tick_params(axis='y', pad=30, labelcolor=m3Color) # labelleft = True
ax3.plot(moments, sum, color = m3Color, alpha = 0.6)

fig.tight_layout()
plt.show()
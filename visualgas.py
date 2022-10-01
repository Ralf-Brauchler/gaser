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

format = "%Y-%m-%d %H:%M:%S"
moments = []
usage = []
sum=[]
for entry in data:
    if entry["text"] == "sensor change":
        if (entry["value"] == '1'):
            moments.append(datetime.datetime.strptime(entry["datetime"][:-4], format))
            usage.append(entry["value"])
    if entry["text"] == "sum of gas":
        sum.append(float(entry["value"]))

plt.scatter(moments, usage, color = "#0000aa", alpha = 0.6)
plt.plot(moments, sum, color = "#00aa00", alpha = 0.6)
plt.show()

#coding:utf-8
import csv

def trans_date(date):
	time = date.split(":")[0]
	#print time+"-"+time_index
	return time

file_con = open("Motor_Vehicle_Collisions_-_Crashes.csv", "rb")
csv_con = csv.reader(file_con)
content = []
for row in csv_con:
	content.append(row)
class_type = content[0]
crash_type_index = class_type.index("CONTRIBUTING FACTOR VEHICLE 1") # 获取类别列
print crash_type_index  # 获取事故原因所在的键索引

#所有的事故原因
event_index_list = ['Driver Inattention/Distraction', 'Backing Unsafely', 'Unspecified', 'Following Too Closely', 'Brakes Defective', 'Passing Too Closely', 'Traffic Control Disregarded', 'Failure to Yield Right-of-Way', 'Unsafe Speed', 'Fell Asleep', 'Other Vehicular', 'Reaction to Uninvolved Vehicle', 'Alcohol Involvement', 'Oversized Vehicle', 'Driver Inexperience', 'Passing or Lane Usage Improper', 'Using On Board Navigation Device', 'Driverless/Runaway Vehicle', 'Aggressive Driving/Road Rage', 'Cell Phone (hand-Held)', 'Turning Improperly', 'Passenger Distraction', 'View Obstructed/Limited', 'Unsafe Lane Changing', 'Outside Car Distraction', 'Tire Failure/Inadequate', 'Fatigued/Drowsy', 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion', 'Pavement Defective', 'Traffic Control Device Improper/Non-Working', 'Obstruction/Debris', 'Pavement Slippery', 'Other Electronic Device', 'Lost Consciousness', 'Glare', 'Failure to Keep Right', 'Illnes', 'Animals Action', 'Steering Failure', 'Texting', 'Lane Marking Improper/Inadequate', 'Accelerator Defective', 'Physical Disability', 'Drugs (illegal)', 'Vehicle Vandalism', 'Other Lighting Defects', 'Eating or Drinking', 'Tow Hitch Defective', 'Tinted Windows', 'Prescription Medication', 'Cell Phone (hands-free)', 'Headlights Defective', 'Shoulders Defective/Improper', 'Windshield Inadequate', 'Listening/Using Headphones']

event_time_list = {}
event_time_count = {}
for i in event_index_list:  # 初始化，event_time_count实际上对于每个事故原因都对应一个 {"AM-0":0,"AM-1":0,"PM-0":0,"PM-1":0}
	event_time_list[i] = []  # event_time_list统计每个事故原因的所有发生时间
	event_time_count[i] = {"AM-0":0,"AM-1":0,"PM-0":0,"PM-1":0}

#遍历csv文件内容,把每个原因的发生时间放到event_time_list,键是事故原因，键值是所有时间的一个列表
for i in range(len(content)):
	try:
		time = content[i][1]
		event_name = content[i][18]
		if event_name in event_index_list:
			event_time_list[event_name].append(time)
	except:
		print "error content"
		continue

print event_time_list["Following Too Closely"]
trans_date("16:25")


keys = event_time_list.keys()  # 拿到所有事故原因
for i in range(len(keys)):
	temp = event_time_list[keys[i]] # 拿到该原因的时间列表
	for j in range(len(temp)):
		time_temp = temp[j]
		trans_time = trans_date(time_temp) # 根据时间来判断属于四个时段的哪一个，得到每个时间段发生的次数
		if int(trans_time.split("-")[0])<=6 :
			event_time_count[keys[i]]["AM-0"] = event_time_count[keys[i]]["AM-0"] + 1
		if int(trans_time.split("-")[0])>6 and int(trans_time.split("-")[0]) <=12:
			event_time_count[keys[i]]["AM-1"] = event_time_count[keys[i]]["AM-1"] + 1
		if int(trans_time.split("-")[0])>12 and  int(trans_time.split("-")[0])<=18:
			event_time_count[keys[i]]["AM-0"] = event_time_count[keys[i]]["AM-0"] + 1
		if int(trans_time.split("-")[0])>18 and int(trans_time.split("-")[0]) <=24:
			event_time_count[keys[i]]["AM-1"] = event_time_count[keys[i]]["AM-1"] + 1
print event_time_count

# 根据每个时间段发生的次数来进行归一化
for i in range(len(keys)):
	temp = event_time_count[keys[i]]
	all_count = 0
	for j in temp.keys():
		all_count = all_count + temp[j]
	if all_count == 0:
		print keys[i]
	index = ["AM-0","AM-1","PM-0","PM-1"]
	for k in index:
		event_time_count[keys[i]][k] = float(event_time_count[keys[i]][k])/float(all_count)
print event_time_count

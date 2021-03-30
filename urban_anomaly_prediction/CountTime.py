#coding:utf-8
import csv

# def trans_date(date):
# 	time = date.split(":")[0]
# 	#print time+"-"+time_index
# 	return time
def trans_date(date):
	time = date.split(" ")[1].split(":")[0]
	return time
def ampm(date):
	m = date.split(" ")[2]
	return m
print(trans_date("08/26/2017 10:00:00 AM"))

file_con = open("../data/Chicago/trans/crashes_crashes.csv", "r")
csv_con = csv.reader(file_con)
content = []
for row in csv_con:
	content.append(row)
class_type = content[0]
crash_type_index = class_type.index("PRIM_CONTRIBUTORY_CAUSE") # 获取类别列
print(crash_type_index)  # 获取事故原因所在的键索引

#所有的事故原因
event_index_list = ['FAILING TO YIELD RIGHT-OF-WAY', 'FOLLOWING TOO CLOSELY', 'EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST', 'WEATHER', 'FAILING TO REDUCE SPEED TO AVOID CRASH', 'DISREGARDING STOP SIGN', 'IMPROPER TURNING/NO SIGNAL', 'IMPROPER BACKING', 'DRIVING SKILLS/KNOWLEDGE/EXPERIENCE', 'IMPROPER OVERTAKING/PASSING', 'DISREGARDING ROAD MARKINGS', 'DISTRACTION - FROM OUTSIDE VEHICLE', 'ANIMAL', 'DISREGARDING TRAFFIC SIGNALS', 'EXCEEDING SAFE SPEED FOR CONDITIONS', 'OPERATING VEHICLE IN ERRATIC, RECKLESS, CARELESS, NEGLIGENT OR AGGRESSIVE MANNER', 'IMPROPER LANE USAGE', 'DISREGARDING OTHER TRAFFIC SIGNS', 'EXCEEDING AUTHORIZED SPEED LIMIT', 'DRIVING ON WRONG SIDE/WRONG WAY', 'VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)', 'ROAD ENGINEERING/SURFACE/MARKING DEFECTS', 'DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)', 'EQUIPMENT - VEHICLE CONDITION', 'PHYSICAL CONDITION OF DRIVER', 'UNDER THE INFLUENCE OF ALCOHOL/DRUGS (USE WHEN ARREST IS EFFECTED)', 'DISREGARDING YIELD SIGN', 'ROAD CONSTRUCTION/MAINTENANCE', 'DISTRACTION - FROM INSIDE VEHICLE', 'HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)', 'BICYCLE ADVANCING LEGALLY ON RED LIGHT', 'TURNING RIGHT ON RED', 'RELATED TO BUS STOP', 'CELL PHONE USE OTHER THAN TEXTING', 'TEXTING', 'MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT', 'PASSING STOPPED SCHOOL BUS', 'OBSTRUCTED CROSSWALKS']

event_time_list = {}
event_time_count = {}
for i in event_index_list:  # 初始化，event_time_count实际上对于每个事故原因都对应一个 {"AM-0":0,"AM-1":0,"PM-0":0,"PM-1":0}
	event_time_list[i] = []  # event_time_list统计每个事故原因的所有发生时间
	event_time_count[i] = {"AM-0":0,"AM-1":0,"PM-0":0,"PM-1":0}

#遍历csv文件内容,把每个原因的发生时间放到event_time_list,键是事故原因，键值是所有时间的一个列表
for i in range(len(content)):
	try:
		time = content[i][3]
		event_name = content[i][crash_type_index]
		if event_name in event_index_list:
			event_time_list[event_name].append(time)
	except:
		print("error content")
		continue

# print(event_time_list["Following Too Closely"])
# trans_date("16:25")


keys = list(event_time_list.keys())  # 拿到所有事故原因
for i in range(len(keys)):
	temp = event_time_list[keys[i]] # 拿到该原因的时间列表
	for j in range(len(temp)):
		time_temp = temp[j]
		trans_time = trans_date(time_temp) # 根据时间来判断属于四个时段的哪一个，得到每个时间段发生的次数
		trans_ampm = ampm(time_temp)
		if trans_time:
			if trans_ampm == 'AM':
				if int(trans_time)<=6 :
					event_time_count[keys[i]]["AM-0"] = event_time_count[keys[i]]["AM-0"] + 1
				# if int(trans_time)>6 and int(trans_time) <=12:
				if int(trans_time) > 6:
					event_time_count[keys[i]]["AM-1"] = event_time_count[keys[i]]["AM-1"] + 1
			elif trans_ampm == 'PM':
				# if int(trans_time)>12 and int(trans_time) <=18:
				if int(trans_time)<=6 :
					event_time_count[keys[i]]["PM-0"] = event_time_count[keys[i]]["PM-0"] + 1
				# if int(trans_time)>18 and int(trans_time) <=24:
				if int(trans_time) > 6:
					event_time_count[keys[i]]["PM-1"] = event_time_count[keys[i]]["PM-1"] + 1
		# if int(trans_time.split("-")[0])<=6 :
		# 	event_time_count[keys[i]]["AM-0"] = event_time_count[keys[i]]["AM-0"] + 1
		# if int(trans_time.split("-")[0])>6 and int(trans_time.split("-")[0]) <=12:
		# 	event_time_count[keys[i]]["AM-1"] = event_time_count[keys[i]]["AM-1"] + 1
		# if int(trans_time.split("-")[0])>12 and  int(trans_time.split("-")[0])<=18:
		# 	event_time_count[keys[i]]["PM-0"] = event_time_count[keys[i]]["PM-0"] + 1
		# if int(trans_time.split("-")[0])>18 and int(trans_time.split("-")[0]) <=24:
		# 	event_time_count[keys[i]]["PM-1"] = event_time_count[keys[i]]["PM-1"] + 1
print(event_time_count)

# 根据每个时间段发生的次数来进行归一化
for i in range(len(keys)):
	temp = event_time_count[keys[i]]
	all_count = 0
	for j in temp.keys():
		all_count = all_count + temp[j]
	if all_count == 0:
		print(keys[i])
	index = ["AM-0","AM-1","PM-0","PM-1"]
	for k in index:
		event_time_count[keys[i]][k] = float(event_time_count[keys[i]][k])/float(all_count)
print(event_time_count)

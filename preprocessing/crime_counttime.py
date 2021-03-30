#coding:utf-8
import csv


# def trans_date(date):
# 	time = date.split(" ")[1].split(":")[0]
# 	return time
# def ampm(date):
# 	m = date.split(" ")[2]
# 	return m
# print(trans_date("08/26/2017 10:00:00 AM"))
def trans_date(date):
	time = date.split(":")[0]
	return time

file_con1 = open("../data/NY/crime/crime_changed.csv", "r")
file_con2 = open("../data/Chicago/crime/Crimes_-_2001_to_present.csv", "r")
csv_con = csv.reader(file_con1)
content = []
for row in csv_con:
	content.append(row)
class_type = content[0]
crime_type_index = class_type.index("OFNS_DESC") # 获取类别列 Primary Type OFNS_DESC
print(crime_type_index)  # 获取事故原因所在的键索引

#所有的事故原因
event_index_list = ['OBSCENITY', 'BURGLARY', 'INTOXICATED/IMPAIRED DRIVING', 'THEFT', 'DECEPTIVE PRACTICE', 'ROBBERY', 'NARCOTICS', 'CRIMINAL MISCHIEF & RELATED OF', 'ASSAULT', 'OFF. AGNST PUB ORD SENSBLTY &', 'SEX OFFENSE', 'CRIMINAL TRESPASS', 'VEHICLE AND TRAFFIC LAWS', 'MISCELLANEOUS PENAL LAW', 'MOTOR VEHICLE THEFT', 'WEAPONS VIOLATION', 'PUBLIC PEACE VIOLATION', 'CRIM SEXUAL ASSAULT', 'CRIMINAL DAMAGE', 'THEFT-FRAUD', 'OTHER OFFENSE', 'ARSON', 'POSSESSION OF STOLEN PROPERTY', 'NYS LAWS-UNCLASSIFIED FELONY', 'ANTICIPATORY OFFENSES', 'KIDNAPPING', 'INTERFERENCE WITH PUBLIC OFFICER', 'GAMBLING', 'HOMICIDE', 'OFFENSE INVOLVING CHILDREN', 'OTHER STATE LAWS', 'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'NON-CRIMINAL', 'ESCAPE', 'RITUALISM', 'HOMICIDE-NEGLIGENT-VEHICLE']
# event_index_list =['DECEPTIVE PRACTICE', 'CRIM SEXUAL ASSAULT', 'BURGLARY', 'THEFT', 'OFFENSE INVOLVING CHILDREN',
# 				   'CRIMINAL DAMAGE', 'OTHER OFFENSE', 'NARCOTICS', 'SEX OFFENSE', 'BATTERY', 'MOTOR VEHICLE THEFT',
# 				   'ROBBERY', 'ASSAULT', 'CRIMINAL TRESPASS', 'WEAPONS VIOLATION', 'OBSCENITY', 'PUBLIC PEACE VIOLATION',
# 				   'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'INTIMIDATION', 'ARSON', 'INTERFERENCE WITH PUBLIC OFFICER',
# 				   'GAMBLING', 'STALKING', 'KIDNAPPING', 'OTHER NARCOTIC VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION',
# 				   'HOMICIDE', 'RITUALISM', 'HUMAN TRAFFICKING', 'PUBLIC INDECENCY', 'NON-CRIMINAL']
event_time_list = {}
event_time_count = {}
for i in event_index_list:  # 初始化，event_time_count实际上对于每个事故原因都对应一个 {"AM-0":0,"AM-1":0,"PM-0":0,"PM-1":0}
	event_time_list[i] = []  # event_time_list统计每个事故原因的所有发生时间
	event_time_count[i] = {"AM-0":0,"AM-1":0,"PM-0":0,"PM-1":0}

#遍历csv文件内容,把每个原因的发生时间放到event_time_list,键是事故原因，键值是所有时间的一个列表
for i in range(len(content)):
	try:
		time = content[i][2]
		event_name = content[i][crime_type_index]
		if event_name in event_index_list:
			event_time_list[event_name].append(time)
	except:
		print("error content")
		continue

print(event_time_list["THEFT"])

keys = list(event_time_list.keys())  # 拿到所有犯罪类型
for i in range(len(keys)):
	temp = event_time_list[keys[i]] # 拿到该类型的时间列表
	# print(temp)
	for j in range(len(temp)):
		time_temp = temp[j]
		trans_time = trans_date(time_temp) # 根据时间来判断属于四个时段的哪一个，得到每个时间段发生的次数
		# trans_ampm = ampm(time_temp)
		# print(trans_time)
		if trans_time:
			# if trans_ampm == 'AM':
				if int(trans_time)<=6 :
					event_time_count[keys[i]]["AM-0"] = event_time_count[keys[i]]["AM-0"] + 1
				if int(trans_time)>6 and int(trans_time) <=12:
				# if int(trans_time) > 6:
					event_time_count[keys[i]]["AM-1"] = event_time_count[keys[i]]["AM-1"] + 1
			# elif trans_ampm == 'PM':
				if int(trans_time)>12 and int(trans_time) <=18:
				# if int(trans_time)<=6 :
					event_time_count[keys[i]]["PM-0"] = event_time_count[keys[i]]["PM-0"] + 1
				if int(trans_time)>18 and int(trans_time) <=24:
				# if int(trans_time) > 6:
					event_time_count[keys[i]]["PM-1"] = event_time_count[keys[i]]["PM-1"] + 1
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

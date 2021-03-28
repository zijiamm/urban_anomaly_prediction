#获取交通事故类型
import csv
import pandas as pd
file_con = open("Traffic_Crashes_-_Crashes.csv","rb")
csv_con = csv.reader(file_con)
content = []
for row in csv_con:
	content.append(row)
class_type = content[0]
crash_type_index = class_type.index("PRIM_CONTRIBUTORY_CAUSE") # 获取类别列
content = content[1:] # 获取所有记录
crash_type = []
for crash_record in content:
	#print crash_record
	try:
		if crash_record[22] not in crash_type:
			crash_type.append(crash_record[22])
	except:
		print(crash_record)
		continue
print("类型数：",crash_type.__len__())
for c_type in crash_type:
	print(c_type)
    

crime_all=['DECEPTIVE PRACTICE', 'CRIM SEXUAL ASSAULT', 'BURGLARY', 'THEFT', 'OFFENSE INVOLVING CHILDREN',
           'CRIMINAL DAMAGE', 'OTHER OFFENSE', 'NARCOTICS', 'SEX OFFENSE', 'BATTERY', 'MOTOR VEHICLE THEFT',
           'ROBBERY', 'ASSAULT', 'CRIMINAL TRESPASS', 'WEAPONS VIOLATION', 'OBSCENITY', 'PUBLIC PEACE VIOLATION',
           'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'INTIMIDATION', 'ARSON', 'INTERFERENCE WITH PUBLIC OFFICER',
           'GAMBLING', 'STALKING', 'KIDNAPPING', 'OTHER NARCOTIC VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION',
           'HOMICIDE', 'RITUALISM', 'HUMAN TRAFFICKING', 'PUBLIC INDECENCY', 'OTHER OFFENSE ', 'NON-CRIMINAL',
           'ESCAPE', 'OTHER STATE LAWS', 'INTOXICATED/IMPAIRED DRIVING', 'CRIMINAL MISCHIEF & RELATED OF',
           'CRIMINAL MISCHIEF & RELATED OF', 'VEHICLE AND TRAFFIC LAWS', 'MISCELLANEOUS PENAL LAW', 'THEFT-FRAUD',
           'POSSESSION OF STOLEN PROPERTY', 'NYS LAWS-UNCLASSIFIED FELONY', 'ANTICIPATORY OFFENSES',
           'HOMICIDE-NEGLIGENT-VEHICLE', 'OFF. AGNST PUB ORD SENSBLTY &']
path = '../data/NY/crime/crime_changed.csv'
data = pd.read_csv(path,low_memory=False)
y = data['OFNS_DESC']#读取类别列
ny_ctype=y.drop_duplicates().tolist()
print(ny_ctype.__len__())
print(ny_ctype)

chicago_ctype = ['DECEPTIVE PRACTICE', 'CRIM SEXUAL ASSAULT', 'BURGLARY', 'THEFT', 'OFFENSE INVOLVING CHILDREN',
             'CRIMINAL DAMAGE', 'OTHER OFFENSE', 'NARCOTICS', 'SEX OFFENSE', 'BATTERY', 'MOTOR VEHICLE THEFT',
             'ROBBERY', 'ASSAULT', 'CRIMINAL TRESPASS', 'WEAPONS VIOLATION', 'OBSCENITY', 'PUBLIC PEACE VIOLATION',
             'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'INTIMIDATION', 'ARSON', 'INTERFERENCE WITH PUBLIC OFFICER',
             'GAMBLING', 'STALKING', 'KIDNAPPING', 'OTHER NARCOTIC VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION',
             'HOMICIDE', 'RITUALISM', 'HUMAN TRAFFICKING', 'PUBLIC INDECENCY', 'NON-CRIMINAL']
print(set(chicago_ctype).issubset(set(crime_all)))
print(set(ny_ctype).issubset(set(crime_all)))
for elem in ny_ctype:
    if elem not in crime_all:
        print(elem)


#获取犯罪事件类型
import requests
import re
url2 = "https://data.cityofchicago.org/api/id/c7ck-438e.json?$query=select *, :id limit 100"
content = []
content1 = requests.get(url2).content
all_record = content1.split("\n")[:-1]
print(all_record.__len__())


for i in [100,200,300,400]:
	temp_content = requests.get("https://data.cityofchicago.org/api/id/c7ck-438e.json?$query=select *, :id offset {0} limit 100".format(str(i)))
	temp_content = temp_content.content.split("\n")[:-1]
	all_record = all_record + temp_content

type_list = []
for i in range(all_record.__len__()):
	iucr = re.findall(".*iucr\":\"(.*)\",\"primary_description",all_record[i])[0]
	primary_description = re.findall(".*primary_description\":\"(.*)\",\"secondary_description",all_record[i])[0]
	secondary_description = re.findall(".*secondary_description\":\"(.*)\",\"index_code",all_record[i])[0]
	dic = {iucr:primary_description+"#"+secondary_description}
	print(dic)

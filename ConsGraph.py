# coding:utf-8
import networkx as nx
import math
import matplotlib.pyplot as plt
# 城市异常事件 id = 0
# 个体异常 id = 2
# 交通异常 id = 1
G = nx.Graph()
'''
交通异常的所有分类，主要为三层和四层的数据
'''
traffic_all = [
	{"EQUIPMENT - VEHICLE CONDITION#设备的车辆状况": []
	 },
	{"external factor#外界因素#new_cons":
		 ["ROAD CONSTRUCTION/MAINTENANCE",
		  "ROAD ENGINEERING/SURFACE/MARKING DEFECTS",
		  "VISION OBSCURED",
		  "WEATHER"]
	 },
	{"DISREGARDING ROAD MARKINGS#无视路标":
		 ["DISREGARDING STOP SIGN",
		  "TURNING RIGHT ON RED",
		  "DISREGARDING OTHER TRAFFIC SIGNS",
		  "DISREGARDING YIELD SIGN"
		  ]
	 },
	{"distractions#分心#new_cons":
		 ["DISTRACTION - FROM OUTSIDE VEHICLE"
			 , "DISTRACTION - FROM INSIDE VEHICLE",
          "DISTRACTION - OTHER ELECTRONIC DEVICE",
          "CELL PHONE USE OTHER THAN TEXTING",
          "TEXTING"]
	 },
	{"PHYSICAL CONDITION OF DRIVER#驾驶员身体状况": [
		"HAD BEEN DRINKING",
		"UNDER THE INFLUENCE OF ALCOHOL/DRUGS"]
	},
	{"EVASIVE ACTION DUE TO ANIMAL,OBJECT,NONMOTORIST#由于动物，物体，非驾驶者而做出的回避行为":

		 ["ANIMAL",
		  "BICYCLE ADVANCING LEGALLY ON RED LIGHT",
		  "MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT",
		  "RELATED TO BUS STOP",
		  "PASSING STOPPED SCHOOL BUS",
		  "OBSTRUCTED CROSSWALKS"
		  ]

	 }
	, {"DRIVING SKILLS/KNOWLEDGE/EXPERIENCE#驾驶技能/知识/经验": [
		"IMPROPER TURNING SIGNAL",
		"IMPROPER BACKING",
		"IMPROPER OVERTAKING/PASSING",
		"OPERATING VEHICLE IN ERRATIC,RECKLESS,CARELESS,NEGLIGENT OR AGGRESSIVE MANNER",
		"IMPROPER LANE USAGE",
		"FAILING TO YIELD RIGHT-OF-WAY",
		"DRIVING ON WRONG SIDE/WRONG WAY"

	]

	}, {"EXCEEDING SPEED#超速": []}
	, {"train#追尾#new_cons": [
		"FOLLOWING TOO CLOSELY",
		"FAILING TO REDUCE SPEED TO AVOID CRASH"
	]}
]
id_dic = {}
traffic_count  = 3 # 0,1,2已经分配，从3开始给每种细分节点分配唯一ID
for i in range(len(traffic_all)):
	temp = traffic_all[i]
	temp_key = list(temp.keys())[0]
	id_dic[traffic_count] = temp_key
	traffic_count = traffic_count + 1
	temp_values = traffic_all[i][temp_key]
	if len(temp_values) > 0: # 如果存在第四层节点
		for j in range(len(temp_values)):
			id_dic[traffic_count] = temp_values[j]
			traffic_count = traffic_count + 1
print(id_dic)

'''
构建交通异常分叉本体图
'''
G.add_node(0,name="城市异常事件",p_c=1)
G.add_node(1,name="交通异常事件",p_c=0)
G.add_node(2,name="个体异常事件",p_c=0)
for key in list(id_dic.keys()):
	'''
	添加的节点分为两类:
	三层节点：
	a.用一个#分割,表示将数据集中存在的描述作为三层节点
	b.用两个#分割,表示将新起的一个三层节点的描述，实际在数据中不存在
	四层节点:
	所有traffic_all中字典的value都是四层节点,即中间不加#
	'''
	node_des = id_dic[key]
	split_value = node_des.split("#")
	if len(split_value) > 2: # 新起的节点:
		G.add_node(key,des_type_eng = split_value[0] , des_type_chin = split_value[1],is_exist=0,p_c=0)
		continue
	if len(split_value) > 1: # 数据中存在的节点
		G.add_node(key, des_type_eng=split_value[0], des_type_chin=split_value[1], is_exist=1,p_c=0)
		continue
	if len(split_value) > 0:
		G.add_node(key, des_type_eng=split_value[0],p_c=0)
'''
添加本体图的边关系
'''
G.add_edge(0, 1) # 城市->交通
G.add_edge(0, 2) # 城市->个体
'''
从id_dic中返回某个节点值所对应的ID
'''
def get_node_id(des_type):
	new_dic = {v:k for k,v in id_dic.items()}
	return new_dic[des_type]

for i in range(len(traffic_all)):
	temp = traffic_all[i]
	temp_key = list(temp.keys())[0]
	G.add_edge(1,get_node_id(temp_key)) # 添加三层节点与二层节点的边
	temp_values = traffic_all[i][temp_key]
	if len(temp_values) > 0: # >0说明该三层节点下有四层节点
		for value in temp_values:
			G.add_edge(get_node_id(temp_key),get_node_id(value))

print(G.nodes)
print(G.nodes.__len__())
print(G.edges)
#print(nx.shortest_path(G,source=2,target=41))

for i in range(len(traffic_all)):
	temp = traffic_all[i]
	temp_key = list(temp.keys())[0]
	temp_key_id = get_node_id(temp_key)
	p_c_key = G[temp_key_id].__len__()/G.nodes.__len__() # 节点的p_c值
	G.nodes[temp_key_id]['p_c'] = p_c_key
	print(G.nodes[temp_key_id]['p_c'],"update")
	temp_values = traffic_all[i][temp_key]
	if len(temp_values) > 0: # >0说明该三层节点下有四层节点
		for value in temp_values:
			G.nodes[get_node_id(value)]['p_c'] = 1/G.nodes.__len__()

# 更新交通异常的p_c值:
neigh_key_list = list(G[1].keys())[1:]
value_all = 0
for i in neigh_key_list:
	value_all = value_all + G.nodes[i]['p_c']
value_all = value_all +  1/G.nodes.__len__()
G.nodes[1]['p_c'] = value_all
# 更新个体异常的p_c值:

# 每个点的ic
def getCsim(id_1,id_2):
	print(nx.shortest_path(G,source=id_1,target=0))
	print(nx.shortest_path(G,source=id_2,target=0))
	id1_to_root_list  = nx.shortest_path(G,source=id_1,target=0)[::-1]
	id2_to_root_list  = nx.shortest_path(G,source=id_2,target=0)[::-1]
	print(id1_to_root_list)
	print(id2_to_root_list)
	all_p = 0
	temp_len = min(len(id2_to_root_list),len(id1_to_root_list))
	temp_list = []
	for i in range(temp_len):
		if id1_to_root_list[i] != all_p:
			all_p = id1_to_root_list[i-1]
	print(all_p)
	sim = -math.log(G.nodes[all_p]["p_c"])
	print("cSim:",sim)
getCsim(38,39)






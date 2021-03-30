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
    {"EQUIPMENT - VEHICLE CONDITION#设备的车辆状况":
         ["Brakes Defective",
          "Tire Failure/Inadequate",
          "Windshield Inadequate",
          "Headlights Defective",
          "Tinted Windows",
          "Accelerator Defective",
          "Other Lighting Defects",
          "Tow Hitch Defective",
          "Steering Failure",
          "Driverless/Runaway Vehicle",
          "Vehicle Vandalism"]
     },
    {"external factor#外界因素#new_cons":
         ["ROAD CONSTRUCTION/MAINTENANCE",
          "ROAD ENGINEERING/SURFACE/MARKING DEFECTS",
          "VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)",
          "WEATHER",
          "Pavement Defective",
          "Traffic Control Device Improper/Non-Working",
          "Pavement Slippery",
          "Lane Marking Improper/Inadequate",
          "Obstruction/Debris"]
     },
    {"Traffic Control Disregarded#无视交通管制":
         ["DISREGARDING ROAD MARKINGS",
          "DISREGARDING STOP SIGN",
          "TURNING RIGHT ON RED",
          "DISREGARDING OTHER TRAFFIC SIGNS",
          "DISREGARDING YIELD SIGN",
          "DISREGARDING TRAFFIC SIGNALS"
          ]
     },
    {"Driver Inattention/Distraction#司机注意力不集中":
         ["DISTRACTION - FROM OUTSIDE VEHICLE",
          "DISTRACTION - FROM INSIDE VEHICLE",
          "DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)",
          "CELL PHONE USE OTHER THAN TEXTING",
          "TEXTING",
          "Eating or Drinking",
          "Passenger Distraction",
          "Using On Board Navigation Device",
          "Listening/Using Headphones"]
     },
    {"PHYSICAL CONDITION OF DRIVER#驾驶员身体状况": [
        "HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)",
        "UNDER THE INFLUENCE OF ALCOHOL/DRUGS (USE WHEN ARREST IS EFFECTED)",
        "Aggressive Driving/Road Rage",
        "Lost Consciousness",
        "Illnes",
        "Physical Disability",
        "Prescription Medication",
        "Fell Asleep",
        "Shoulders Defective/Improper",
        "Drugs (illegal)"]
    },
    {"EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST#由于动物，物体，非驾驶者而做出的回避行为":

         ["ANIMAL",
          "BICYCLE ADVANCING LEGALLY ON RED LIGHT",
          "MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT",
          "RELATED TO BUS STOP",
          "PASSING STOPPED SCHOOL BUS",
          "OBSTRUCTED CROSSWALKS",
          "Reaction to Uninvolved Vehicle",
          "Pedestrian/Bicyclist/Other Pedestrian Error/Confusion"
          ]
     }
    , {"DRIVING SKILLS/KNOWLEDGE/EXPERIENCE#驾驶技能/知识/经验": [
        "IMPROPER TURNING/NO SIGNAL",
        "IMPROPER BACKING",
        "IMPROPER OVERTAKING/PASSING",
        "OPERATING VEHICLE IN ERRATIC, RECKLESS, CARELESS, NEGLIGENT OR AGGRESSIVE MANNER",
        "IMPROPER LANE USAGE",
        "FAILING TO YIELD RIGHT-OF-WAY",
        "DRIVING ON WRONG SIDE/WRONG WAY",
        "Failure to Keep Right",
        "Glare",
        "Oversized Vehicle"
    ]
    }, {"EXCEEDING SPEED#超速": []}
    , {"train#追尾#new_cons": [
        "FOLLOWING TOO CLOSELY",
        "FAILING TO REDUCE SPEED TO AVOID CRASH"
    ]}
]

crime_all=['DECEPTIVE PRACTICE', 'CRIM SEXUAL ASSAULT', 'BURGLARY', 'THEFT', 'OFFENSE INVOLVING CHILDREN',
           'CRIMINAL DAMAGE', 'OTHER OFFENSE', 'NARCOTICS', 'SEX OFFENSE', 'BATTERY', 'MOTOR VEHICLE THEFT',
           'ROBBERY', 'ASSAULT', 'CRIMINAL TRESPASS', 'WEAPONS VIOLATION', 'OBSCENITY', 'PUBLIC PEACE VIOLATION',
           'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'INTIMIDATION', 'ARSON', 'INTERFERENCE WITH PUBLIC OFFICER',
           'GAMBLING', 'STALKING', 'KIDNAPPING', 'OTHER NARCOTIC VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION',
           'HOMICIDE', 'RITUALISM', 'HUMAN TRAFFICKING', 'PUBLIC INDECENCY', 'NON-CRIMINAL',
           'ESCAPE', 'OTHER STATE LAWS', 'INTOXICATED/IMPAIRED DRIVING', 'CRIMINAL MISCHIEF & RELATED OF', 'VEHICLE AND TRAFFIC LAWS', 'MISCELLANEOUS PENAL LAW', 'THEFT-FRAUD',
           'POSSESSION OF STOLEN PROPERTY', 'NYS LAWS-UNCLASSIFIED FELONY', 'ANTICIPATORY OFFENSES',
           'HOMICIDE-NEGLIGENT-VEHICLE', 'OFF. AGNST PUB ORD SENSBLTY &']

# newyork 交通事故事件发生次数
# newyork_traffic_count = {'Tire Failure/Inadequate': {'AM-1': 212, 'AM-0': 282, 'PM-0': 0, 'PM-1': 0}, 'Oversized Vehicle': {'AM-1': 1378, 'AM-0': 1093, 'PM-0': 0, 'PM-1': 0}, 'Following Too Closely': {'AM-1': 17189, 'AM-0': 19323, 'PM-0': 0, 'PM-1': 0}, 'Passenger Distraction': {'AM-1': 627, 'AM-0': 690, 'PM-0': 0, 'PM-1': 0}, 'Pavement Slippery': {'AM-1': 1304, 'AM-0': 1896, 'PM-0': 0, 'PM-1': 0}, 'Texting': {'AM-1': 5, 'AM-0': 10, 'PM-0': 0, 'PM-1': 0}, 'Unspecified': {'AM-1': 44449, 'AM-0': 45777, 'PM-0': 0, 'PM-1': 0}, 'Shoulders Defective/Improper': {'AM-1': 8, 'AM-0': 8, 'PM-0': 0, 'PM-1': 0}, 'Physical Disability': {'AM-1': 46, 'AM-0': 57, 'PM-0': 0, 'PM-1': 0}, 'Obstruction/Debris': {'AM-1': 327, 'AM-0': 405, 'PM-0': 0, 'PM-1': 0}, 'Cell Phone (hands-free)': {'AM-1': 12, 'AM-0': 6, 'PM-0': 0, 'PM-1': 0}, 'Illnes': {'AM-1': 199, 'AM-0': 213, 'PM-0': 0, 'PM-1': 0}, 'Cell Phone (hand-Held)': {'AM-1': 61, 'AM-0': 76, 'PM-0': 0, 'PM-1': 0}, 'Fatigued/Drowsy': {'AM-1': 157, 'AM-0': 246, 'PM-0': 0, 'PM-1': 0}, 'Brakes Defective': {'AM-1': 675, 'AM-0': 786, 'PM-0': 0, 'PM-1': 0}, 'Driver Inexperience': {'AM-1': 3038, 'AM-0': 3126, 'PM-0': 0, 'PM-1': 0}, 'Backing Unsafely': {'AM-1': 9149, 'AM-0': 8953, 'PM-0': 0, 'PM-1': 0}, 'Steering Failure': {'AM-1': 248, 'AM-0': 312, 'PM-0': 0, 'PM-1': 0}, 'Other Lighting Defects': {'AM-1': 18, 'AM-0': 20, 'PM-0': 0, 'PM-1': 0}, 'Prescription Medication': {'AM-1': 18, 'AM-0': 15, 'PM-0': 0, 'PM-1': 0}, 'View Obstructed/Limited': {'AM-1': 1643, 'AM-0': 1628, 'PM-0': 0, 'PM-1': 0}, 'Vehicle Vandalism': {'AM-1': 15, 'AM-0': 19, 'PM-0': 0, 'PM-1': 0}, 'Other Vehicular': {'AM-1': 5739, 'AM-0': 5917, 'PM-0': 0, 'PM-1': 0}, 'Unsafe Speed': {'AM-1': 2444, 'AM-0': 3123, 'PM-0': 0, 'PM-1': 0}, 'Unsafe Lane Changing': {'AM-1': 6391, 'AM-0': 6747, 'PM-0': 0, 'PM-1': 0}, 'Alcohol Involvement': {'AM-1': 1518, 'AM-0': 2566, 'PM-0': 0, 'PM-1': 0}, 'Lost Consciousness': {'AM-1': 181, 'AM-0': 211, 'PM-0': 0, 'PM-1': 0}, 'Passing or Lane Usage Improper': {'AM-1': 8597, 'AM-0': 8806, 'PM-0': 0, 'PM-1': 0}, 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion': {'AM-1': 1072, 'AM-0': 1231, 'PM-0': 0, 'PM-1': 0}, 'Animals Action': {'AM-1': 166, 'AM-0': 232, 'PM-0': 0, 'PM-1': 0}, 'Drugs (illegal)': {'AM-1': 102, 'AM-0': 116, 'PM-0': 0, 'PM-1': 0}, 'Traffic Control Disregarded': {'AM-1': 3058, 'AM-0': 3378, 'PM-0': 0, 'PM-1': 0}, 'Fell Asleep': {'AM-1': 334, 'AM-0': 868, 'PM-0': 0, 'PM-1': 0}, 'Failure to Yield Right-of-Way': {'AM-1': 13722, 'AM-0': 14106, 'PM-0': 0, 'PM-1': 0}, 'Tow Hitch Defective': {'AM-1': 21, 'AM-0': 27, 'PM-0': 0, 'PM-1': 0}, 'Traffic Control Device Improper/Non-Working': {'AM-1': 66, 'AM-0': 58, 'PM-0': 0, 'PM-1': 0}, 'Outside Car Distraction': {'AM-1': 386, 'AM-0': 427, 'PM-0': 0, 'PM-1': 0}, 'Glare': {'AM-1': 405, 'AM-0': 338, 'PM-0': 0, 'PM-1': 0}, 'Reaction to Uninvolved Vehicle': {'AM-1': 2965, 'AM-0': 3415, 'PM-0': 0, 'PM-1': 0}, 'Using On Board Navigation Device': {'AM-1': 20, 'AM-0': 14, 'PM-0': 0, 'PM-1': 0}, 'Lane Marking Improper/Inadequate': {'AM-1': 107, 'AM-0': 115, 'PM-0': 0, 'PM-1': 0}, 'Driverless/Runaway Vehicle': {'AM-1': 150, 'AM-0': 156, 'PM-0': 0, 'PM-1': 0}, 'Driver Inattention/Distraction': {'AM-1': 48418, 'AM-0': 52743, 'PM-0': 0, 'PM-1': 0}, 'Passing Too Closely': {'AM-1': 8473, 'AM-0': 7750, 'PM-0': 0, 'PM-1': 0}, 'Pavement Defective': {'AM-1': 185, 'AM-0': 245, 'PM-0': 0, 'PM-1': 0}, 'Headlights Defective': {'AM-1': 9, 'AM-0': 13, 'PM-0': 0, 'PM-1': 0}, 'Windshield Inadequate': {'AM-1': 6, 'AM-0': 3, 'PM-0': 0, 'PM-1': 0}, 'Turning Improperly': {'AM-1': 4430, 'AM-0': 4507, 'PM-0': 0, 'PM-1': 0}, 'Accelerator Defective': {'AM-1': 97, 'AM-0': 111, 'PM-0': 0, 'PM-1': 0}, 'Tinted Windows': {'AM-1': 15, 'AM-0': 18, 'PM-0': 0, 'PM-1': 0}, 'Failure to Keep Right': {'AM-1': 241, 'AM-0': 257, 'PM-0': 0, 'PM-1': 0}, 'Listening/Using Headphones': {'AM-1': 4, 'AM-0': 3, 'PM-0': 0, 'PM-1': 0}, 'Aggressive Driving/Road Rage': {'AM-1': 780, 'AM-0': 934, 'PM-0': 0, 'PM-1': 0}, 'Eating or Drinking': {'AM-1': 18, 'AM-0': 17, 'PM-0': 0, 'PM-1': 0}, 'Other Electronic Device': {'AM-1': 25, 'AM-0': 28, 'PM-0': 0, 'PM-1': 0}}
newyork_traffic_count = {'Driver Inattention/Distraction': {'AM-0': 11959, 'AM-1': 29714, 'PM-0': 40784, 'PM-1': 18704}, 'Backing Unsafely': {'AM-0': 1607, 'AM-1': 6361, 'PM-0': 7346, 'PM-1': 2788}, 'Following Too Closely': {'AM-0': 3379, 'AM-1': 10785, 'PM-0': 15944, 'PM-1': 6404}, 'Brakes Defective': {'AM-0': 195, 'AM-1': 445, 'PM-0': 591, 'PM-1': 230}, 'Passing Too Closely': {'AM-0': 1233, 'AM-1': 6363, 'PM-0': 6517, 'PM-1': 2110}, 'Traffic Control Disregarded': {'AM-0': 1093, 'AM-1': 1781, 'PM-0': 2285, 'PM-1': 1277}, 'Failure to Yield Right-of-Way': {'AM-0': 2320, 'AM-1': 8380, 'PM-0': 11786, 'PM-1': 5342}, 'Unsafe Speed': {'AM-0': 1594, 'AM-1': 1207, 'PM-0': 1529, 'PM-1': 1237}, 'Fell Asleep': {'AM-0': 599, 'AM-1': 241, 'PM-0': 269, 'PM-1': 93}, 'Other Vehicular': {'AM-0': 1616, 'AM-1': 3729, 'PM-0': 4301, 'PM-1': 2010}, 'Reaction to Uninvolved Vehicle': {'AM-0': 1001, 'AM-1': 1822, 'PM-0': 2414, 'PM-1': 1143}, 'Alcohol Involvement': {'AM-0': 1974, 'AM-1': 374, 'PM-0': 592, 'PM-1': 1144}, 'Oversized Vehicle': {'AM-0': 196, 'AM-1': 1124, 'PM-0': 897, 'PM-1': 254}, 'Driver Inexperience': {'AM-0': 765, 'AM-1': 1806, 'PM-0': 2361, 'PM-1': 1232}, 'Passing or Lane Usage Improper': {'AM-0': 1763, 'AM-1': 5309, 'PM-0': 7043, 'PM-1': 3288}, 'Using On Board Navigation Device': {'AM-0': 5, 'AM-1': 10, 'PM-0': 9, 'PM-1': 10}, 'Driverless/Runaway Vehicle': {'AM-0': 46, 'AM-1': 93, 'PM-0': 110, 'PM-1': 57}, 'Aggressive Driving/Road Rage': {'AM-0': 329, 'AM-1': 389, 'PM-0': 605, 'PM-1': 391}, 'Cell Phone (hand-Held)': {'AM-0': 28, 'AM-1': 30, 'PM-0': 48, 'PM-1': 31}, 'Turning Improperly': {'AM-0': 1032, 'AM-1': 2766, 'PM-0': 3475, 'PM-1': 1664}, 'Passenger Distraction': {'AM-0': 212, 'AM-1': 318, 'PM-0': 478, 'PM-1': 309}, 'View Obstructed/Limited': {'AM-0': 356, 'AM-1': 1085, 'PM-0': 1272, 'PM-1': 558}, 'Unsafe Lane Changing': {'AM-0': 1453, 'AM-1': 4035, 'PM-0': 5294, 'PM-1': 2356}, 'Outside Car Distraction': {'AM-0': 154, 'AM-1': 256, 'PM-0': 273, 'PM-1': 130}, 'Tire Failure/Inadequate': {'AM-0': 167, 'AM-1': 125, 'PM-0': 115, 'PM-1': 87}, 'Fatigued/Drowsy': {'AM-0': 153, 'AM-1': 102, 'PM-0': 93, 'PM-1': 55}, 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion': {'AM-0': 266, 'AM-1': 550, 'PM-0': 965, 'PM-1': 522}, 'Pavement Defective': {'AM-0': 103, 'AM-1': 88, 'PM-0': 142, 'PM-1': 97}, 'Traffic Control Device Improper/Non-Working': {'AM-0': 16, 'AM-1': 39, 'PM-0': 42, 'PM-1': 27}, 'Obstruction/Debris': {'AM-0': 174, 'AM-1': 217, 'PM-0': 231, 'PM-1': 110}, 'Pavement Slippery': {'AM-0': 822, 'AM-1': 691, 'PM-0': 1074, 'PM-1': 613}, 'Other Electronic Device': {'AM-0': 9, 'AM-1': 14, 'PM-0': 19, 'PM-1': 11}, 'Lost Consciousness': {'AM-0': 49, 'AM-1': 108, 'PM-0': 162, 'PM-1': 73}, 'Glare': {'AM-0': 39, 'AM-1': 360, 'PM-0': 299, 'PM-1': 45}, 'Failure to Keep Right': {'AM-0': 79, 'AM-1': 152, 'PM-0': 178, 'PM-1': 89}, 'Illnes': {'AM-0': 49, 'AM-1': 123, 'PM-0': 164, 'PM-1': 76}, 'Animals Action': {'AM-0': 160, 'AM-1': 70, 'PM-0': 72, 'PM-1': 96}, 'Steering Failure': {'AM-0': 160, 'AM-1': 130, 'PM-0': 152, 'PM-1': 118}, 'Texting': {'AM-0': 4, 'AM-1': 2, 'PM-0': 6, 'PM-1': 3}, 'Lane Marking Improper/Inadequate': {'AM-0': 35, 'AM-1': 74, 'PM-0': 80, 'PM-1': 33}, 'Accelerator Defective': {'AM-0': 20, 'AM-1': 59, 'PM-0': 91, 'PM-1': 38}, 'Physical Disability': {'AM-0': 13, 'AM-1': 32, 'PM-0': 44, 'PM-1': 14}, 'Drugs (illegal)': {'AM-0': 41, 'AM-1': 35, 'PM-0': 75, 'PM-1': 67}, 'Vehicle Vandalism': {'AM-0': 8, 'AM-1': 12, 'PM-0': 11, 'PM-1': 3}, 'Other Lighting Defects': {'AM-0': 12, 'AM-1': 3, 'PM-0': 8, 'PM-1': 15}, 'Eating or Drinking': {'AM-0': 7, 'AM-1': 11, 'PM-0': 10, 'PM-1': 7}, 'Tow Hitch Defective': {'AM-0': 10, 'AM-1': 16, 'PM-0': 17, 'PM-1': 5}, 'Tinted Windows': {'AM-0': 8, 'AM-1': 4, 'PM-0': 10, 'PM-1': 11}, 'Prescription Medication': {'AM-0': 4, 'AM-1': 12, 'PM-0': 11, 'PM-1': 6}, 'Cell Phone (hands-free)': {'AM-0': 2, 'AM-1': 6, 'PM-0': 4, 'PM-1': 6}, 'Headlights Defective': {'AM-0': 6, 'AM-1': 1, 'PM-0': 7, 'PM-1': 8}, 'Shoulders Defective/Improper': {'AM-0': 2, 'AM-1': 5, 'PM-0': 6, 'PM-1': 3}, 'Windshield Inadequate': {'AM-0': 1, 'AM-1': 3, 'PM-0': 2, 'PM-1': 3}, 'Listening/Using Headphones': {'AM-0': 2, 'AM-1': 3, 'PM-0': 1, 'PM-1': 1}}
# chicago 交通事故事件发生次数
# chicago_traffic_count = {'DISREGARDING YIELD SIGN': {'AM-1': 24, 'AM-0': 19, 'PM-0': 0, 'PM-1': 0}, 'OBSTRUCTED CROSSWALKS': {'AM-1': 5, 'AM-0': 2, 'PM-0': 0, 'PM-1': 0}, 'RELATED TO BUS STOP': {'AM-1': 15, 'AM-0': 18, 'PM-0': 0, 'PM-1': 0}, 'DISREGARDING ROAD MARKINGS': {'AM-1': 91, 'AM-0': 123, 'PM-0': 0, 'PM-1': 0}, 'DISTRACTION - FROM OUTSIDE VEHICLE': {'AM-1': 339, 'AM-0': 327, 'PM-0': 0, 'PM-1': 0}, 'TEXTING': {'AM-1': 28, 'AM-0': 37, 'PM-0': 0, 'PM-1': 0}, 'OPERATING VEHICLE IN ERRATIC,RECKLESS,CARELESS,NEGLIGENT OR AGGRESSIVE MANNER': {'AM-1': 967, 'AM-0': 829, 'PM-0': 0, 'PM-1': 0}, 'EVASIVE ACTION DUE TO ANIMAL,OBJECT,NONMOTORIST': {'AM-1': 141, 'AM-0': 140, 'PM-0': 0, 'PM-1': 0}, 'IMPROPER LANE USAGE': {'AM-1': 3114, 'AM-0': 3150, 'PM-0': 0, 'PM-1': 0}, 'IMPROPER TURNING/NO SIGNAL': {'AM-1': 2605, 'AM-0': 2612, 'PM-0': 0, 'PM-1': 0}, 'HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)': {'AM-1': 85, 'AM-0': 88, 'PM-0': 0, 'PM-1': 0}, 'ROAD CONSTRUCTION/MAINTENANCE': {'AM-1': 282, 'AM-0': 143, 'PM-0': 0, 'PM-1': 0}, 'EXCEEDING SAFE SPEED FOR CONDITIONS': {'AM-1': 380, 'AM-0': 294, 'PM-0': 0, 'PM-1': 0}, 'PASSING STOPPED SCHOOL BUS': {'AM-1': 11, 'AM-0': 10, 'PM-0': 0, 'PM-1': 0}, 'VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)': {'AM-1': 460, 'AM-0': 395, 'PM-0': 0, 'PM-1': 0}, 'ROAD ENGINEERING/SURFACE/MARKING DEFECTS': {'AM-1': 254, 'AM-0': 207, 'PM-0': 0, 'PM-1': 0}, 'IMPROPER BACKING': {'AM-1': 3460, 'AM-0': 3550, 'PM-0': 0, 'PM-1': 0}, 'MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT': {'AM-1': 2, 'AM-0': 1, 'PM-0': 0, 'PM-1': 0}, 'WEATHER': {'AM-1': 1468, 'AM-0': 1157, 'PM-0': 0, 'PM-1': 0}, 'UNDER THE INFLUENCE OF ALCOHOL/DRUGS (USE WHEN ARREST IS EFFECTED)': {'AM-1': 371, 'AM-0': 423, 'PM-0': 0, 'PM-1': 0}, 'BICYCLE ADVANCING LEGALLY ON RED LIGHT': {'AM-1': 10, 'AM-0': 17, 'PM-0': 0, 'PM-1': 0}, 'NOT APPLICABLE': {'AM-1': 3822, 'AM-0': 4554, 'PM-0': 0, 'PM-1': 0}, 'DISREGARDING TRAFFIC SIGNALS': {'AM-1': 1329, 'AM-0': 1200, 'PM-0': 0, 'PM-1': 0}, 'DISREGARDING OTHER TRAFFIC SIGNS': {'AM-1': 143, 'AM-0': 163, 'PM-0': 0, 'PM-1': 0}, 'DRIVING ON WRONG SIDE/WRONG WAY': {'AM-1': 309, 'AM-0': 345, 'PM-0': 0, 'PM-1': 0}, 'FOLLOWING TOO CLOSELY': {'AM-1': 8308, 'AM-0': 9120, 'PM-0': 0, 'PM-1': 0}, 'EXCEEDING AUTHORIZED SPEED LIMIT': {'AM-1': 374, 'AM-0': 406, 'PM-0': 0, 'PM-1': 0}, 'TURNING RIGHT ON RED': {'AM-1': 53, 'AM-0': 40, 'PM-0': 0, 'PM-1': 0}, 'FAILING TO YIELD RIGHT-OF-WAY': {'AM-1': 8396, 'AM-0': 9146, 'PM-0': 0, 'PM-1': 0}, 'CELL PHONE USE OTHER THAN TEXTING': {'AM-1': 111, 'AM-0': 101, 'PM-0': 0, 'PM-1': 0}, 'DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)': {'AM-1': 37, 'AM-0': 39, 'PM-0': 0, 'PM-1': 0}, 'FAILING TO REDUCE SPEED TO AVOID CRASH': {'AM-1': 3078, 'AM-0': 3444, 'PM-0': 0, 'PM-1': 0}, 'DISTRACTION - FROM INSIDE VEHICLE': {'AM-1': 629, 'AM-0': 507, 'PM-0': 0, 'PM-1': 0}, 'IMPROPER OVERTAKING/PASSING': {'AM-1': 3580, 'AM-0': 3988, 'PM-0': 0, 'PM-1': 0}, 'ANIMAL': {'AM-1': 64, 'AM-0': 58, 'PM-0': 0, 'PM-1': 0}, 'EQUIPMENT - VEHICLE CONDITION': {'AM-1': 467, 'AM-0': 461, 'PM-0': 0, 'PM-1': 0}, 'DRIVING SKILLS/KNOWLEDGE/EXPERIENCE': {'AM-1': 2492, 'AM-0': 2412, 'PM-0': 0, 'PM-1': 0}, 'DISREGARDING STOP SIGN': {'AM-1': 830, 'AM-0': 757, 'PM-0': 0, 'PM-1': 0}, 'PHYSICAL CONDITION OF DRIVER': {'AM-1': 409, 'AM-0': 433, 'PM-0': 0, 'PM-1': 0}}
chicago_traffic_count = {'FAILING TO YIELD RIGHT-OF-WAY': {'AM-0': 924, 'AM-1': 4935, 'PM-0': 8222, 'PM-1': 3461}, 'FOLLOWING TOO CLOSELY': {'AM-0': 1057, 'AM-1': 4743, 'PM-0': 8063, 'PM-1': 3565}, 'EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST': {'AM-0': 44, 'AM-1': 72, 'PM-0': 96, 'PM-1': 69}, 'WEATHER': {'AM-0': 355, 'AM-1': 897, 'PM-0': 802, 'PM-1': 571}, 'FAILING TO REDUCE SPEED TO AVOID CRASH': {'AM-0': 785, 'AM-1': 1553, 'PM-0': 2659, 'PM-1': 1525}, 'DISREGARDING STOP SIGN': {'AM-0': 146, 'AM-1': 424, 'PM-0': 611, 'PM-1': 406}, 'IMPROPER TURNING/NO SIGNAL': {'AM-0': 384, 'AM-1': 1381, 'PM-0': 2228, 'PM-1': 1224}, 'IMPROPER BACKING': {'AM-0': 444, 'AM-1': 1831, 'PM-0': 3106, 'PM-1': 1629}, 'DRIVING SKILLS/KNOWLEDGE/EXPERIENCE': {'AM-0': 362, 'AM-1': 1444, 'PM-0': 2050, 'PM-1': 1048}, 'IMPROPER OVERTAKING/PASSING': {'AM-0': 454, 'AM-1': 2030, 'PM-0': 3534, 'PM-1': 1550}, 'DISREGARDING ROAD MARKINGS': {'AM-0': 19, 'AM-1': 38, 'PM-0': 104, 'PM-1': 53}, 'DISTRACTION - FROM OUTSIDE VEHICLE': {'AM-0': 83, 'AM-1': 176, 'PM-0': 244, 'PM-1': 163}, 'ANIMAL': {'AM-0': 29, 'AM-1': 32, 'PM-0': 29, 'PM-1': 32}, 'DISREGARDING TRAFFIC SIGNALS': {'AM-0': 425, 'AM-1': 678, 'PM-0': 775, 'PM-1': 651}, 'EXCEEDING SAFE SPEED FOR CONDITIONS': {'AM-0': 111, 'AM-1': 213, 'PM-0': 183, 'PM-1': 167}, 'OPERATING VEHICLE IN ERRATIC, RECKLESS, CARELESS, NEGLIGENT OR AGGRESSIVE MANNER': {'AM-0': 252, 'AM-1': 415, 'PM-0': 577, 'PM-1': 552}, 'IMPROPER LANE USAGE': {'AM-0': 510, 'AM-1': 1766, 'PM-0': 2640, 'PM-1': 1348}, 'DISREGARDING OTHER TRAFFIC SIGNS': {'AM-0': 43, 'AM-1': 85, 'PM-0': 120, 'PM-1': 58}, 'EXCEEDING AUTHORIZED SPEED LIMIT': {'AM-0': 161, 'AM-1': 164, 'PM-0': 245, 'PM-1': 210}, 'DRIVING ON WRONG SIDE/WRONG WAY': {'AM-0': 134, 'AM-1': 137, 'PM-0': 211, 'PM-1': 172}, 'VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)': {'AM-0': 48, 'AM-1': 314, 'PM-0': 347, 'PM-1': 146}, 'ROAD ENGINEERING/SURFACE/MARKING DEFECTS': {'AM-0': 55, 'AM-1': 125, 'PM-0': 152, 'PM-1': 129}, 'DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)': {'AM-0': 6, 'AM-1': 17, 'PM-0': 33, 'PM-1': 20}, 'EQUIPMENT - VEHICLE CONDITION': {'AM-0': 133, 'AM-1': 251, 'PM-0': 328, 'PM-1': 216}, 'PHYSICAL CONDITION OF DRIVER': {'AM-0': 182, 'AM-1': 241, 'PM-0': 251, 'PM-1': 168}, 'UNDER THE INFLUENCE OF ALCOHOL/DRUGS (USE WHEN ARREST IS EFFECTED)': {'AM-0': 285, 'AM-1': 107, 'PM-0': 138, 'PM-1': 264}, 'DISREGARDING YIELD SIGN': {'AM-0': 2, 'AM-1': 16, 'PM-0': 17, 'PM-1': 8}, 'ROAD CONSTRUCTION/MAINTENANCE': {'AM-0': 29, 'AM-1': 172, 'PM-0': 114, 'PM-1': 110}, 'DISTRACTION - FROM INSIDE VEHICLE': {'AM-0': 113, 'AM-1': 324, 'PM-0': 394, 'PM-1': 305}, 'HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)': {'AM-0': 43, 'AM-1': 22, 'PM-0': 45, 'PM-1': 63}, 'BICYCLE ADVANCING LEGALLY ON RED LIGHT': {'AM-0': 1, 'AM-1': 4, 'PM-0': 16, 'PM-1': 6}, 'TURNING RIGHT ON RED': {'AM-0': 7, 'AM-1': 27, 'PM-0': 33, 'PM-1': 26}, 'RELATED TO BUS STOP': {'AM-0': 2, 'AM-1': 12, 'PM-0': 16, 'PM-1': 3}, 'CELL PHONE USE OTHER THAN TEXTING': {'AM-0': 22, 'AM-1': 50, 'PM-0': 79, 'PM-1': 61}, 'TEXTING': {'AM-0': 13, 'AM-1': 15, 'PM-0': 24, 'PM-1': 13}, 'MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT': {'AM-0': 0, 'AM-1': 0, 'PM-0': 1, 'PM-1': 2}, 'PASSING STOPPED SCHOOL BUS': {'AM-0': 0, 'AM-1': 10, 'PM-0': 10, 'PM-1': 1}, 'OBSTRUCTED CROSSWALKS': {'AM-0': 0, 'AM-1': 2, 'PM-0': 2, 'PM-1': 3}}
# newyork 犯罪事故事件发生次数
newyork_crime_count = {'OBSCENITY': {'AM-0': 2830, 'AM-1': 6626, 'PM-0': 9112, 'PM-1': 6307}, 'BURGLARY': {'AM-0': 1376, 'AM-1': 2893, 'PM-0': 2419, 'PM-1': 1594}, 'INTOXICATED/IMPAIRED DRIVING': {'AM-0': 2185, 'AM-1': 90, 'PM-0': 135, 'PM-1': 565}, 'THEFT': {'AM-0': 6249, 'AM-1': 13108, 'PM-0': 20089, 'PM-1': 11292}, 'DECEPTIVE PRACTICE': {'AM-0': 605, 'AM-1': 1107, 'PM-0': 1805, 'PM-1': 827}, 'ROBBERY': {'AM-0': 2223, 'AM-1': 1182, 'PM-0': 2623, 'PM-1': 2410}, 'NARCOTICS': {'AM-0': 2339, 'AM-1': 1827, 'PM-0': 5422, 'PM-1': 6068}, 'CRIMINAL MISCHIEF & RELATED OF': {'AM-0': 4693, 'AM-1': 4312, 'PM-0': 6089, 'PM-1': 6682}, 'ASSAULT': {'AM-0': 7215, 'AM-1': 5002, 'PM-0': 8308, 'PM-1': 7982}, 'OFF. AGNST PUB ORD SENSBLTY &': {'AM-0': 1666, 'AM-1': 3791, 'PM-0': 4223, 'PM-1': 2908}, 'SEX OFFENSE': {'AM-0': 477, 'AM-1': 667, 'PM-0': 746, 'PM-1': 412}, 'CRIMINAL TRESPASS': {'AM-0': 578, 'AM-1': 571, 'PM-0': 964, 'PM-1': 1093}, 'VEHICLE AND TRAFFIC LAWS': {'AM-0': 573, 'AM-1': 694, 'PM-0': 902, 'PM-1': 722}, 'MISCELLANEOUS PENAL LAW': {'AM-0': 882, 'AM-1': 919, 'PM-0': 1405, 'PM-1': 1221}, 'MOTOR VEHICLE THEFT': {'AM-0': 904, 'AM-1': 948, 'PM-0': 1298, 'PM-1': 1798}, 'WEAPONS VIOLATION': {'AM-0': 1164, 'AM-1': 587, 'PM-0': 1505, 'PM-1': 1976}, 'PUBLIC PEACE VIOLATION': {'AM-0': 784, 'AM-1': 814, 'PM-0': 1247, 'PM-1': 1111}, 'CRIM SEXUAL ASSAULT': {'AM-0': 201, 'AM-1': 121, 'PM-0': 111, 'PM-1': 114}, 'CRIMINAL DAMAGE': {'AM-0': 64, 'AM-1': 129, 'PM-0': 163, 'PM-1': 125}, 'THEFT-FRAUD': {'AM-0': 415, 'AM-1': 1161, 'PM-0': 611, 'PM-1': 176}, 'OTHER OFFENSE': {'AM-0': 114, 'AM-1': 60, 'PM-0': 73, 'PM-1': 67}, 'ARSON': {'AM-0': 246, 'AM-1': 84, 'PM-0': 133, 'PM-1': 182}, 'POSSESSION OF STOLEN PROPERTY': {'AM-0': 190, 'AM-1': 246, 'PM-0': 555, 'PM-1': 233}, 'NYS LAWS-UNCLASSIFIED FELONY': {'AM-0': 38, 'AM-1': 29, 'PM-0': 39, 'PM-1': 46}, 'ANTICIPATORY OFFENSES': {'AM-0': 0, 'AM-1': 1, 'PM-0': 3, 'PM-1': 1}, 'KIDNAPPING': {'AM-0': 17, 'AM-1': 32, 'PM-0': 33, 'PM-1': 26}, 'INTERFERENCE WITH PUBLIC OFFICER': {'AM-0': 7, 'AM-1': 4, 'PM-0': 13, 'PM-1': 8}, 'GAMBLING': {'AM-0': 9, 'AM-1': 9, 'PM-0': 29, 'PM-1': 31}, 'HOMICIDE': {'AM-0': 86, 'AM-1': 25, 'PM-0': 56, 'PM-1': 61}, 'OFFENSE INVOLVING CHILDREN': {'AM-0': 11, 'AM-1': 10, 'PM-0': 16, 'PM-1': 28}, 'OTHER STATE LAWS': {'AM-0': 14, 'AM-1': 53, 'PM-0': 140, 'PM-1': 48}, 'LIQUOR LAW VIOLATION': {'AM-0': 12, 'AM-1': 2, 'PM-0': 3, 'PM-1': 16}, 'PROSTITUTION': {'AM-0': 11, 'AM-1': 2, 'PM-0': 4, 'PM-1': 7}, 'NON-CRIMINAL': {'AM-0': 3, 'AM-1': 2, 'PM-0': 11, 'PM-1': 6}, 'ESCAPE': {'AM-0': 1, 'AM-1': 2, 'PM-0': 3, 'PM-1': 1}, 'RITUALISM': {'AM-0': 0, 'AM-1': 0, 'PM-0': 1, 'PM-1': 1}, 'HOMICIDE-NEGLIGENT-VEHICLE': {'AM-0': 1, 'AM-1': 0, 'PM-0': 1, 'PM-1': 0}}
# chicago 犯罪事故事件发生次数
chicago_crime_count = {'DECEPTIVE PRACTICE': {'AM-0': 1253, 'AM-1': 14321, 'PM-0': 7886, 'PM-1': 6636}, 'CRIM SEXUAL ASSAULT': {'AM-0': 644, 'AM-1': 1490, 'PM-0': 533, 'PM-1': 840}, 'BURGLARY': {'AM-0': 2035, 'AM-1': 3642, 'PM-0': 3619, 'PM-1': 3133}, 'THEFT': {'AM-0': 7720, 'AM-1': 23090, 'PM-0': 29190, 'PM-1': 23460}, 'OFFENSE INVOLVING CHILDREN': {'AM-0': 218, 'AM-1': 3160, 'PM-0': 1048, 'PM-1': 861}, 'CRIMINAL DAMAGE': {'AM-0': 5667, 'AM-1': 7144, 'PM-0': 8462, 'PM-1': 10316}, 'OTHER OFFENSE': {'AM-0': 1772, 'AM-1': 6263, 'PM-0': 6290, 'PM-1': 6028}, 'NARCOTICS': {'AM-0': 1435, 'AM-1': 6092, 'PM-0': 9195, 'PM-1': 10025}, 'SEX OFFENSE': {'AM-0': 245, 'AM-1': 1292, 'PM-0': 633, 'PM-1': 566}, 'BATTERY': {'AM-0': 10788, 'AM-1': 12705, 'PM-0': 17831, 'PM-1': 18666}, 'MOTOR VEHICLE THEFT': {'AM-0': 1744, 'AM-1': 2845, 'PM-0': 3281, 'PM-1': 4471}, 'ROBBERY': {'AM-0': 2188, 'AM-1': 1845, 'PM-0': 2886, 'PM-1': 3534}, 'ASSAULT': {'AM-0': 2445, 'AM-1': 5777, 'PM-0': 8657, 'PM-1': 7218}, 'CRIMINAL TRESPASS': {'AM-0': 978, 'AM-1': 1893, 'PM-0': 2602, 'PM-1': 2433}, 'WEAPONS VIOLATION': {'AM-0': 1027, 'AM-1': 1051, 'PM-0': 1464, 'PM-1': 2681}, 'OBSCENITY': {'AM-0': 4, 'AM-1': 44, 'PM-0': 22, 'PM-1': 22}, 'PUBLIC PEACE VIOLATION': {'AM-0': 193, 'AM-1': 347, 'PM-0': 715, 'PM-1': 742}, 'LIQUOR LAW VIOLATION': {'AM-0': 52, 'AM-1': 56, 'PM-0': 118, 'PM-1': 182}, 'PROSTITUTION': {'AM-0': 201, 'AM-1': 295, 'PM-0': 222, 'PM-1': 891}, 'INTIMIDATION': {'AM-0': 9, 'AM-1': 58, 'PM-0': 68, 'PM-1': 49}, 'ARSON': {'AM-0': 205, 'AM-1': 116, 'PM-0': 83, 'PM-1': 156}, 'INTERFERENCE WITH PUBLIC OFFICER': {'AM-0': 165, 'AM-1': 299, 'PM-0': 511, 'PM-1': 629}, 'GAMBLING': {'AM-0': 5, 'AM-1': 37, 'PM-0': 174, 'PM-1': 160}, 'STALKING': {'AM-0': 23, 'AM-1': 84, 'PM-0': 91, 'PM-1': 84}, 'KIDNAPPING': {'AM-0': 18, 'AM-1': 68, 'PM-0': 92, 'PM-1': 54}, 'OTHER NARCOTIC VIOLATION': {'AM-0': 1, 'AM-1': 2, 'PM-0': 3, 'PM-1': 5}, 'CONCEALED CARRY LICENSE VIOLATION': {'AM-0': 49, 'AM-1': 33, 'PM-0': 44, 'PM-1': 63}, 'HOMICIDE': {'AM-0': 153, 'AM-1': 88, 'PM-0': 146, 'PM-1': 170}, 'RITUALISM': {'AM-0': 0, 'AM-1': 0, 'PM-0': 0, 'PM-1': 1}, 'HUMAN TRAFFICKING': {'AM-0': 0, 'AM-1': 11, 'PM-0': 3, 'PM-1': 3}, 'PUBLIC INDECENCY': {'AM-0': 1, 'AM-1': 7, 'PM-0': 6, 'PM-1': 1}, 'NON-CRIMINAL': {'AM-0': 0, 'AM-1': 3, 'PM-0': 3, 'PM-1': 5}}

newyork_crime_key = list(newyork_crime_count.keys())
chicago_crime_key = list(chicago_crime_count.keys())


combine_crime_count = newyork_crime_count
for key in chicago_crime_key:
    if key not in newyork_crime_key:
        combine_crime_count[key] = chicago_crime_count[key]
    if key in newyork_crime_key:
        index = ["AM-0", "AM-1", "PM-0", "PM-1"]
        for j in index:
            combine_crime_count[key][j] = combine_crime_count[key][j] + chicago_crime_count[key][j]



id_dic = {}
traffic_count = 3  # 0,1,2已经分配，从3开始给每种细分节点分配唯一ID
for i in range(len(traffic_all)):
    temp = traffic_all[i]
    temp_key = list(temp.keys())[0]
    id_dic[traffic_count] = temp_key
    traffic_count = traffic_count + 1
    temp_values = traffic_all[i][temp_key]
    if len(temp_values) > 0:  # 如果存在第四层节点
        for j in range(len(temp_values)):
            id_dic[traffic_count] = temp_values[j]
            traffic_count = traffic_count + 1

print("traffic_count",traffic_count)
crime_count = traffic_count
for j in range(len(crime_all)):
    temp = crime_all[j]
    id_dic[crime_count] = temp
    crime_count = crime_count + 1
print("本体图中所有的三层和四层节点id及对应的类型:",id_dic)

'''
构建交通异常分叉本体图
'''
G.add_node(0, name="城市异常事件", p_c=1, is_exist=0)
G.add_node(1, name="交通异常事件", p_c=0, is_exist=0)
G.add_node(2, name="个体异常事件", p_c=0, is_exist=0)
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
    if len(split_value) > 2:  # 新起的节点:
        G.add_node(key, des_type_eng=split_value[0], des_type_chin=split_value[1], is_exist=0, p_c=0,all=[])
        continue
    if len(split_value) > 1:  # 数据中存在的节点
        G.add_node(key, des_type_eng=split_value[0], des_type_chin=split_value[1], is_exist=1, p_c=0,all=[])
        continue
    if len(split_value) > 0:
        G.add_node(key, des_type_eng=split_value[0], p_c=0, is_exist=1,city="",all=[])

'''
从id_dic中返回某个节点值所对应的ID
'''


def get_node_id(des_type):
    new_dic = {v: k for k, v in id_dic.items()}
    return new_dic[des_type]


# newyork交通
newyork_type = ['Driver Inattention/Distraction', 'Backing Unsafely', 'Following Too Closely', 'Brakes Defective', 'Passing Too Closely', 'Traffic Control Disregarded', 'Failure to Yield Right-of-Way', 'Unsafe Speed', 'Fell Asleep', 'Other Vehicular', 'Reaction to Uninvolved Vehicle', 'Alcohol Involvement', 'Oversized Vehicle', 'Driver Inexperience', 'Passing or Lane Usage Improper', 'Using On Board Navigation Device', 'Driverless/Runaway Vehicle', 'Aggressive Driving/Road Rage', 'Cell Phone (hand-Held)', 'Turning Improperly', 'Passenger Distraction', 'View Obstructed/Limited', 'Unsafe Lane Changing', 'Outside Car Distraction', 'Tire Failure/Inadequate', 'Fatigued/Drowsy', 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion', 'Pavement Defective', 'Traffic Control Device Improper/Non-Working', 'Obstruction/Debris', 'Pavement Slippery', 'Other Electronic Device', 'Lost Consciousness', 'Glare', 'Failure to Keep Right', 'Illnes', 'Animals Action', 'Steering Failure', 'Texting', 'Lane Marking Improper/Inadequate', 'Accelerator Defective', 'Physical Disability', 'Drugs (illegal)', 'Vehicle Vandalism', 'Other Lighting Defects', 'Eating or Drinking', 'Tow Hitch Defective', 'Tinted Windows', 'Prescription Medication', 'Cell Phone (hands-free)', 'Headlights Defective', 'Shoulders Defective/Improper', 'Windshield Inadequate', 'Listening/Using Headphones']
#chicago交通
chicago_type = ['FAILING TO YIELD RIGHT-OF-WAY', 'FOLLOWING TOO CLOSELY', 'EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST', 'WEATHER', 'FAILING TO REDUCE SPEED TO AVOID CRASH', 'DISREGARDING STOP SIGN', 'IMPROPER TURNING/NO SIGNAL', 'IMPROPER BACKING', 'DRIVING SKILLS/KNOWLEDGE/EXPERIENCE', 'IMPROPER OVERTAKING/PASSING', 'DISREGARDING ROAD MARKINGS', 'DISTRACTION - FROM OUTSIDE VEHICLE', 'ANIMAL', 'DISREGARDING TRAFFIC SIGNALS', 'EXCEEDING SAFE SPEED FOR CONDITIONS', 'OPERATING VEHICLE IN ERRATIC, RECKLESS, CARELESS, NEGLIGENT OR AGGRESSIVE MANNER', 'IMPROPER LANE USAGE', 'DISREGARDING OTHER TRAFFIC SIGNS', 'EXCEEDING AUTHORIZED SPEED LIMIT', 'DRIVING ON WRONG SIDE/WRONG WAY', 'VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)', 'ROAD ENGINEERING/SURFACE/MARKING DEFECTS', 'DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)', 'EQUIPMENT - VEHICLE CONDITION', 'PHYSICAL CONDITION OF DRIVER', 'UNDER THE INFLUENCE OF ALCOHOL/DRUGS (USE WHEN ARREST IS EFFECTED)', 'DISREGARDING YIELD SIGN', 'ROAD CONSTRUCTION/MAINTENANCE', 'DISTRACTION - FROM INSIDE VEHICLE', 'HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)', 'BICYCLE ADVANCING LEGALLY ON RED LIGHT', 'TURNING RIGHT ON RED', 'RELATED TO BUS STOP', 'CELL PHONE USE OTHER THAN TEXTING', 'TEXTING', 'MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT', 'PASSING STOPPED SCHOOL BUS', 'OBSTRUCTED CROSSWALKS']
# newyork犯罪
newyork_crime_type = ['OBSCENITY', 'BURGLARY', 'INTOXICATED/IMPAIRED DRIVING', 'THEFT', 'DECEPTIVE PRACTICE', 'ROBBERY', 'NARCOTICS', 'CRIMINAL MISCHIEF & RELATED OF', 'ASSAULT', 'OFF. AGNST PUB ORD SENSBLTY &', 'SEX OFFENSE', 'CRIMINAL TRESPASS', 'VEHICLE AND TRAFFIC LAWS', 'MISCELLANEOUS PENAL LAW', 'MOTOR VEHICLE THEFT', 'WEAPONS VIOLATION', 'PUBLIC PEACE VIOLATION', 'CRIM SEXUAL ASSAULT', 'CRIMINAL DAMAGE', 'THEFT-FRAUD', 'OTHER OFFENSE', 'ARSON', 'POSSESSION OF STOLEN PROPERTY', 'NYS LAWS-UNCLASSIFIED FELONY', 'ANTICIPATORY OFFENSES', 'KIDNAPPING', 'INTERFERENCE WITH PUBLIC OFFICER', 'GAMBLING', 'HOMICIDE', 'OFFENSE INVOLVING CHILDREN', 'OTHER STATE LAWS', 'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'NON-CRIMINAL', 'ESCAPE', 'RITUALISM', 'HOMICIDE-NEGLIGENT-VEHICLE']
#chicago犯罪
chicago_crime_type =['DECEPTIVE PRACTICE', 'CRIM SEXUAL ASSAULT', 'BURGLARY', 'THEFT', 'OFFENSE INVOLVING CHILDREN','CRIMINAL DAMAGE', 'OTHER OFFENSE', 'NARCOTICS', 'SEX OFFENSE', 'BATTERY', 'MOTOR VEHICLE THEFT','ROBBERY', 'ASSAULT', 'CRIMINAL TRESPASS', 'WEAPONS VIOLATION', 'OBSCENITY', 'PUBLIC PEACE VIOLATION','LIQUOR LAW VIOLATION', 'PROSTITUTION', 'INTIMIDATION', 'ARSON', 'INTERFERENCE WITH PUBLIC OFFICER','GAMBLING', 'STALKING', 'KIDNAPPING', 'OTHER NARCOTIC VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION','HOMICIDE', 'RITUALISM', 'HUMAN TRAFFICKING', 'PUBLIC INDECENCY', 'NON-CRIMINAL']

newyork_type_id_list = []
newyork_no_exist_list = []
chicago_type_id_list = []
chicago_no_exist_list = []
for i in newyork_type:
    try:
        newyork_type_id_list.append(get_node_id(i))
    except:
        new_dic = {v: k for k, v in id_dic.items()}
        find = 0
        for key in list(new_dic.keys()):
            if i == key.split("#")[0]:
                newyork_type_id_list.append(get_node_id(key))
                find = 1
                break
        if find==0:
            newyork_no_exist_list.append(i)
            #print(i, "no id in graph")
        continue
print("纽约事件类型存在的ID：",newyork_type_id_list)
print("纽约事件类型不存在的类型：",newyork_no_exist_list)

for i in chicago_type:
    try:
        chicago_type_id_list.append(get_node_id(i))
    except:
        new_dic = {v: k for k, v in id_dic.items()}
        find = 0
        for key in list(new_dic.keys()):
            if i == key.split("#")[0]:
                chicago_type_id_list.append(get_node_id(key))
                find = 1
                break
        if find==0:
            chicago_no_exist_list.append(i)
            #print(i, "no id in graph")
        continue
print("芝加哥事件类型存在的ID：",chicago_type_id_list)
print("芝加哥事件类型不存在的类型：",chicago_no_exist_list)


# 合并两个城市的部分事件类型：
# 纽约事件类型不存在的类型：['Backing Unsafely', 'Following Too Closely', 'Passing Too Closely', 'Failure to Yield Right-of-Way', 'Unsafe Speed', 'Other Vehicular', 'Alcohol Involvement', 'Driver Inexperience', 'Passing or Lane Usage Improper', 'Cell Phone (hand-Held)', 'Turning Improperly', 'View Obstructed/Limited', 'Unsafe Lane Changing', 'Outside Car Distraction', 'Fatigued/Drowsy', 'Other Electronic Device', 'Animals Action', 'Texting', 'Cell Phone (hands-free)']
# Backing Unsafely
G.nodes[get_node_id("IMPROPER BACKING")]["all"].append("ny#"+"Backing Unsafely")

# Following Too Closely
G.nodes[get_node_id("FOLLOWING TOO CLOSELY")]["all"].append("ny#" + "Following Too Closely")
# Passing Too Closely
G.nodes[get_node_id("FOLLOWING TOO CLOSELY")]["all"].append("ny#" + "Passing Too Closely")
# Failure to Yield Right-of-Way
G.nodes[get_node_id("FAILING TO YIELD RIGHT-OF-WAY")]["all"].append("ny#" + "Failure to Yield Right-of-Way")
# Unsafe Speed
G.nodes[get_node_id("EXCEEDING SPEED#超速")]["all"].append("ny#" + "Unsafe Speed")
G.nodes[get_node_id("EXCEEDING SPEED#超速")]["all"].append("zj#" + "EXCEEDING SAFE SPEED FOR CONDITIONS")
G.nodes[get_node_id("EXCEEDING SPEED#超速")]["all"].append("zj#" + "EXCEEDING AUTHORIZED SPEED LIMIT")
# Other Vehicular
G.nodes[get_node_id("DISTRACTION - FROM OUTSIDE VEHICLE")]["all"].append("ny#" + "Other Vehicular")
# Alcohol Involvement
G.nodes[get_node_id("HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)")]["all"].append("ny#" + "Alcohol Involvement")
# Driver Inexperience
G.nodes[get_node_id("DRIVING SKILLS/KNOWLEDGE/EXPERIENCE#驾驶技能/知识/经验")]["all"].append("ny#" + "Driver Inexperience")
# Passing or Lane Usage Improper
G.nodes[get_node_id("IMPROPER LANE USAGE")]["all"].append("ny#" + "Passing or Lane Usage Improper")
# Cell Phone (hand-Held)
G.nodes[get_node_id("CELL PHONE USE OTHER THAN TEXTING")]["all"].append("ny#" + "Cell Phone (hand-Held)")
# Turning Improperly
G.nodes[get_node_id("IMPROPER TURNING/NO SIGNAL")]["all"].append("ny#" + "Turning Improperly")
# View Obstructed/Limited
G.nodes[get_node_id("VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)")]["all"].append("ny#" + "View Obstructed/Limited")
# Unsafe Lane Changing
G.nodes[get_node_id("IMPROPER LANE USAGE")]["all"].append("ny#" + "Unsafe Lane Changing")
# Outside Car Distraction
G.nodes[get_node_id("DISTRACTION - FROM OUTSIDE VEHICLE")]["all"].append("ny#" + "Outside Car Distraction")
# Fatigued/Drowsy
G.nodes[get_node_id("Fell Asleep")]["all"].append("ny#" + "Fatigued/Drowsy")
# Other Electronic Device
G.nodes[get_node_id("DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)")]["all"].append("ny#" + "Other Electronic Device")
# Animals Action
G.nodes[get_node_id("ANIMAL")]["all"].append("ny#" + "Animals Action")
# Texting
G.nodes[get_node_id("TEXTING")]["all"].append("ny#" + "Texting")
# Cell Phone (hands-free)
G.nodes[get_node_id("CELL PHONE USE OTHER THAN TEXTING")]["all"].append("ny#" + "Cell Phone (hands-free)")




'''
添加本体图的边关系
'''
G.add_edge(0, 1)  # 城市->交通
G.add_edge(0, 2)  # 城市->个体



for i in range(len(traffic_all)):
    temp = traffic_all[i]
    temp_key = list(temp.keys())[0]
    G.add_edge(1, get_node_id(temp_key))  # 添加三层节点与二层节点的边
    temp_values = traffic_all[i][temp_key]
    if len(temp_values) > 0:  # >0说明该三层节点下有四层节点
        for value in temp_values:
            G.add_edge(get_node_id(temp_key), get_node_id(value))

for j in range(len(crime_all)):
    temp = crime_all[j]
    G.add_edge(2, get_node_id(temp))

print("本体图中所有的节点：",G.nodes)
print("本体图中节点的个数：",G.nodes.__len__())
print("本体图中的所有边：",G.edges)
# print(nx.shortest_path(G,source=2,target=41))

for i in range(len(traffic_all)):
    temp = traffic_all[i]
    temp_key = list(temp.keys())[0]
    temp_key_id = get_node_id(temp_key)
    p_c_key = G[temp_key_id].__len__() / G.nodes.__len__()  # 节点的p_c值
    G.nodes[temp_key_id]['p_c'] = p_c_key
    #print(G.nodes[temp_key_id]['p_c'], "update")
    temp_values = traffic_all[i][temp_key]
    if len(temp_values) > 0:  # >0说明该三层节点下有四层节点
        for value in temp_values:
            G.nodes[get_node_id(value)]['p_c'] = 1 / G.nodes.__len__()

for j in range(len(crime_all)):
    temp = crime_all[j]
    G.nodes[get_node_id(temp)]['p_c'] = 1 / G.nodes.__len__()

# 更新交通异常的p_c值:
neigh_key_list = list(G[1].keys())[1:]

value_all = 0
for i in neigh_key_list:
    value_all = value_all + G.nodes[i]['p_c']
value_all = value_all + 1 / G.nodes.__len__()
G.nodes[1]['p_c'] = value_all
# 更新个体异常的p_c值:
G.nodes[2]['p_c'] = 1 - value_all


# 分层类型感知距离
def C(id_1, id_2):
    r = 1  # 距离参数 自定
    #try:
        #print(nx.shortest_path(G, source=id_1, target=0))
        #print(nx.shortest_path(G, source=id_2, target=0))
    #except:
    #    print(id_1, id_2, "debug")
    id1_to_root_list = nx.shortest_path(G, source=id_1, target=0)[::-1]
    id2_to_root_list = nx.shortest_path(G, source=id_2, target=0)[::-1]
    #print(id1_to_root_list)
    #print(id2_to_root_list)
    all_p = 0
    temp_len = min(len(id2_to_root_list), len(id1_to_root_list))
    temp_list = []
    for i in range(temp_len):
        if id1_to_root_list[i] != id2_to_root_list[i]:
            all_p = id1_to_root_list[i - 1]
            break
    # print(all_p)
    sim = -math.log(G.nodes[all_p]["p_c"])
    # print(sim)
    cSim = r * (1 - (sim / max(-math.log(G.nodes[id_1]["p_c"]), -math.log(G.nodes[id_2]["p_c"]))))
    #print("cSim:", cSim)
    return cSim



# 语义相似性
def gethop(id_1, id_2):
    hop = nx.shortest_path(G, source=id_1, target=id_2)
    return hop.__len__() - 1


print("语义相似性",gethop(3, 36))


def S(id_1, id_2):
    sei = 0.05  # 收缩率𝜃 ∈ (0,0.1)
    max_hop = 3  # 最大拓扑距离 自定
    s = pow(1 + sei, max_hop + 1 - gethop(id_1, id_2))
    if gethop(id_1, id_2) > max_hop:
        s = 1
    return s



# 输入一个事故类型
# 输出该事故类型在不同时间段发生的分布
def get_time_feature(des):

    find = 0
    # 进来的可能有三层节点，所有有#，要去掉# 再查找
    if(des.split("#").__len__()>1):
        des = des.split("#")[0]
    # 如果是新构造的三层节点，那么就不要进行后面的判断
    if("#new_cons" in des):
        return "no_exist"
    # 如果是crime犯罪的，暂时还没有时间信息添加，所以暂时跳过不比较
    #if(des in crime_all):
    #    return "no_exist"
    node_list = list(G.nodes)[3:]
    #print(node_list)
    time_dis = {}
    for i in node_list:
        if des == id_dic[i].split("#")[0]:
            #print("main_feature相等")
            #print(des)
            #print(id_dic[i])

            other_feature = G.nodes[i]["all"]
            '''
            芝加哥交通和纽约的交通异常
            '''
            if des in list(chicago_traffic_count.keys()):
                time_dis = chicago_traffic_count[des]
                #print(time_dis)
            elif des in list(newyork_traffic_count.keys()):
                time_dis = newyork_traffic_count[des]

            elif des in list(combine_crime_count.keys()):
                time_dis = combine_crime_count[des]

                #print(time_dis)
            else:
                print(des)
                print("[*] 事故属性不存在，检查一下图中的属性")
                print("程序有问题-condition0")
            if len(other_feature)>0:
                for j in range(len(other_feature)):
                    temp_feature = other_feature[j].split("#")[1]
                    if temp_feature in list(chicago_traffic_count.keys()):
                        temp_feature_value = chicago_traffic_count[temp_feature]
                        temp_key_list = list(time_dis.keys())
                        for key in temp_key_list:
                            time_dis[key] = time_dis[key] + temp_feature_value[key]
                    elif temp_feature in list(newyork_traffic_count.keys()):
                        temp_feature_value = newyork_traffic_count[temp_feature]
                        temp_key_list = list(time_dis.keys())
                        for key in temp_key_list:
                            time_dis[key] = time_dis[key] + temp_feature_value[key]
                    else:
                        print("[*] 事故属性不存在,检查一下图中的属性")
                        print("程序有问题-condition1")
            find = 1
            break
        # 这种情况对应于该属性是合并的，在节点的all属性里存在
        if(list(G.nodes[i]["all"]).__len__()>0):
            #print("other_feature相等")
            #print(des)
            #print(id_dic[i])
            other_feature = list(G.nodes[i]["all"])
            for j in range(len(other_feature)):
                temp_feature = other_feature[j].split("#")[1]
                #
                # 如果当前的feature存在在all里面，则要把当前对比的这个i对应的先赋值给dis，再把all里的加起来
                #
                if(des == temp_feature):
                    find = 1
                    main_feature = id_dic[i]
                    print(main_feature)
                    if main_feature in list(chicago_traffic_count.keys()):
                        time_dis = chicago_traffic_count[main_feature]
                    elif main_feature in list(newyork_traffic_count.keys()):
                        time_dis = newyork_traffic_count[main_feature]
                    else:
                        print("[*] 事故属性不存在，检查一下图中的属性")
                        exit("程序有问题-condition2")
                    for j in range(len(other_feature)):
                        temp_feature = other_feature[j].split("#")[1]
                        if temp_feature in list(chicago_traffic_count.keys()):
                            temp_feature_value = chicago_traffic_count[temp_feature]
                            temp_key_list = list(time_dis.keys())
                            for key in temp_key_list:
                                time_dis[key] = time_dis[key] + temp_feature_value[key]
                        elif temp_feature in list(newyork_traffic_count.keys()):
                            temp_feature_value = newyork_traffic_count[temp_feature]
                            temp_key_list = list(time_dis.keys())
                            for key in temp_key_list:
                                time_dis[key] = time_dis[key] + temp_feature_value[key]
                        else:
                            print("[*] 事故属性不存在,检查一下图中的属性")
                            exit("程序有问题-condition3")
    if find == 1:
        index = ["AM-0", "AM-1", "PM-0", "PM-1"]
        all_count = 0
        for j in list(time_dis.keys()):
            all_count = all_count + time_dis[j]
        for k in index:
            time_dis[k] = float(time_dis[k]) / float(all_count)
        return  time_dis
    else:
        return "no_exist"

def get_oushi(time_dis1,time_dis2):
    distance = 0
    key_list = list(time_dis1.keys())
    for key in key_list:
        distance = distance + pow(time_dis1[key]-time_dis2[key],2)
    distance = math.sqrt(distance)
    return distance

def get_distance(id_1):
    des = id_dic[id_1]
    des_time_dis = get_time_feature(des)
    node_list = list(G.nodes)[3:]
    distance_list = {}
    distance_list_oushi = {}
    for i in node_list:
        if("new_cons" in id_dic[i]):
            continue
        if("EXCEEDING SPEED" == id_dic[i].split("#")[0]):
            key_list =   ["Unsafe Speed","EXCEEDING SAFE SPEED FOR CONDITIONS","EXCEEDING AUTHORIZED SPEED LIMIT"]
            distance_list["EXCEEDING SPEED#超速"] = {"AM-0":0,"AM-1":0,"PM-0":0,"PM-1":0}
            for key in key_list:
                if key in chicago_type:
                    for p_key in list(distance_list["EXCEEDING SPEED#超速"].keys()):
                        distance_list["EXCEEDING SPEED#超速"][p_key] = distance_list["EXCEEDING SPEED#超速"][p_key] + chicago_traffic_count[key][p_key]
                if key in newyork_type:
                    for p_key in list(distance_list["EXCEEDING SPEED#超速"].keys()):
                        distance_list["EXCEEDING SPEED#超速"][p_key] = distance_list["EXCEEDING SPEED#超速"][p_key] + newyork_traffic_count[key][p_key]
            continue
        temp_time_dis = get_time_feature(id_dic[i])

        if temp_time_dis != "no_exist":
            distance_list[id_dic[i]] = temp_time_dis
    print("distance_list:",distance_list)
    #print(distance_list.__len__())
    # des不跟当前自己的同节点比较
    for i in node_list:
        feature = id_dic[i]
        all_feature = G.nodes[i]["all"]
        if des == feature:
            print(des)
            print(feature)
            #if "#" in des or "#" in feature:
            #    des = des.split("#")[0]
            #    feature = feature.split("#")[0]
            #print(des)
            #print(feature)
            del distance_list[des]
            break
        if len(all_feature)>0:
            for j in all_feature:
                if des == j.split("#")[1]:
                    del distance_list[feature]
                    break
    print(distance_list)

    for key in distance_list.keys():
        des_id = get_node_id(des)
        key_id = get_node_id(key)
        distance_list_oushi[str(des_id) + "--->" + str(key_id)] = get_oushi(des_time_dis,distance_list[key])

    print("当前类型距离本体图其他所有节点的欧式距离为：",distance_list_oushi)
    return distance_list_oushi
    #distance_list_oushi = sorted(distance_list_oushi.items(), key=lambda x: x[1], reverse=True)
#get_distance("Fell Asleep")


# 相似度衡量公式
def D(id_1, id_2,node_distance):

    d = C(id_1, id_2) / (S(id_1, id_2)* node_distance)
    return d


#print(D(0, 26))


def getmore(id_1):
    node_list = list(G.nodes)
    exist_node_list = {}
    #print(node_list, "nodelist")
    distance_list = get_distance(id_1)

    for i in range(node_list.__len__()):
        if id_1 != node_list[i]:
            if G.nodes[i]['is_exist'] != 0:
                #print(G.nodes[i]['is_exist'])
                node_distance = distance_list[str(id_1)+"--->"+str(node_list[i])]
                exist_node_list[str(id_1)+"--->" + str(node_list[i])] = D(id_1, node_list[i],node_distance)
    temp = sorted(exist_node_list.items(), key=lambda x: x[1], reverse=True)
    return temp


print(getmore(62), "resu")

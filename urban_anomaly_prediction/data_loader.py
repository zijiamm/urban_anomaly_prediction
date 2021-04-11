
import os
import pandas as pd
import functools
import numpy as np
import collections
from datetime import datetime
import random
import torch
import logging
from urban_anomaly_prediction.ConsGraph import *
# from CityTransfer.utility.utility_tool import _norm

input_list = []

class DataLoader(object):
    def __init__(self, args):
        self.args = args
        self.source_youbiao = 0
        self.target_youbiao = 0
        # define data path
        data_dir = os.path.join(args.data_dir, args.city_name)
        # dianping_data_path = os.path.join(data_dir, 'dianping.csv')
        # _data_path = os.path.join(data_dir, 'dianping_bookshop_edit.csv')
        POI_data_path = "../data/NY/NYC_POI.csv"
        # anomaly_data_path = os.path.join(data_dir,args.ano_type,'anomaly.csv').replace('\\', '/')
        anomaly_data_path = "../data/NY/crime/anomaly.csv"
        # load dianping data,trans and crime data
        source_area_POI_data, target_area_POI_data, self.POI_category_dict, self.POI_category_dict_reverse, \
            = self.load_POI_data(POI_data_path)
        # print("source_area_POI_data",source_area_POI_data)
        # print("target_area_POI_data",target_area_POI_data)
        # print("self.POI_category_dict",self.POI_category_dict)
        # print("self.POI_category_dict_reverse",self.POI_category_dict_reverse)

        self.n_POI_category = len(self.POI_category_dict)
        # print("self.n_POI_category",self.n_POI_category)

        print("[1 /10]       load POI data done.")

        source_area_anomaly_data, target_area_anomaly_data, self.anomaly_category_dict, self.anomaly_category_dict_reverse,self.anomaly_id_time_dict \
            = self.load_anomaly_data(anomaly_data_path)
        # print("source_area_anomaly_data",source_area_anomaly_data)
        # print("target_area_anomaly_data",target_area_anomaly_data)
        # print("self.anomaly_category_dict",self.anomaly_category_dict)
        # print("self.anomaly_category_dict_reverse",self.anomaly_category_dict_reverse)

        self.n_anomaly_category = len(self.anomaly_category_dict)
        # print("self.n_anomaly_category",self.n_anomaly_category)

        print("[2 /10]       load anomaly data done.")

        # check enterprise and get small category set
        # valid_small_category_set, self.target_enterprise_index, self.all_enterprise_index, \
        #     self.portion_enterprise_index = self.check_enterprise(source_area_POI_data, target_area_POI_data)
        # print("[2 /10]       check enterprise and get small category set.")

        # split grid
        self.n_source_grid, self.n_target_grid, self.source_area_longitude_boundary, \
        self.source_area_latitude_boundary, self.target_area_longitude_boundary, self.target_area_latitude_boundary\
            = self.split_grid()
        # print("self.n_source_grid",self.n_source_grid)
        # print("self.n_target_grid",self.n_target_grid)
        # print("self.source_area_longitude_boundary",self.source_area_longitude_boundary)
        # print("self.source_area_latitude_boundary",self.source_area_latitude_boundary)
        # print("self.target_area_longitude_boundary",self.target_area_longitude_boundary)
        # print("self.target_area_latitude_boundary",self.target_area_latitude_boundary)


        print("[3 /10]       split grid done.")

        # distribute data into grids
        source_POI_data_dict, target_POI_data_dict, source_grid_POI_data, target_grid_POI_data, \
        source_anomaly_data_dict, target_anomaly_data_dict, source_grid_anomaly_data, target_grid_anomaly_data\
            = self.distribute_data(source_area_POI_data, target_area_POI_data,source_area_anomaly_data, target_area_anomaly_data)
        print("[4 /10]       distribute data into grids done.")
        # print("source_POI_data_dict",source_POI_data_dict)
        # print("target_POI_data_dict",target_POI_data_dict)
        # print("source_grid_POI_data",source_grid_POI_data)
        # print("target_grid_POI_data",target_grid_POI_data)
        # print("source_anomaly_data_dict",source_anomaly_data_dict)
        # print("target_anomaly_data_dict",target_anomaly_data_dict)
        # print("source_grid_anomaly_data",source_grid_anomaly_data)
        # print("target_grid_anomaly_data",target_grid_anomaly_data)

        # generate rating matrix for Transfer Rating Prediction Model
        # self.source_rating_matrix, self.target_rating_matrix = self.generate_rating_matrix(source_grid_POI_data,
        #                                                                                    target_grid_POI_data)
        # print("[5 /10]       generate rating matrix for Transfer Rating Prediction Model done.")

        # extract geographic features
        source_geographic_features, target_geographic_features = self.extract_geographic_features(source_POI_data_dict,
                                                                                                  target_POI_data_dict)
        print("[5 /10]       extract geographic features done.")
        # print("source_geographic_features",source_geographic_features)
        # print("target_geographic_features",target_geographic_features)

        # extract anomaly features
        source_anomaly_features, target_anomaly_features = \
            self.extract_anomaly_features(source_anomaly_data_dict, target_anomaly_data_dict)
        print("[6 /10]       extract anomaly features done.")
        # print("source_anomaly_features",source_anomaly_features)
        # print("target_anomaly_features",target_anomaly_features)
        # combine features
        self.source_feature, self.target_feature, self.feature_dim = \
            self.combine_features(source_geographic_features, target_geographic_features,
                                  source_anomaly_features, target_anomaly_features)
        print("[7 /10]       combine features done.")
        # print("self.source_feature",self.source_feature)
        # print("self.target_feature",self.target_feature)
        # print("self.feature_dim",self.feature_dim)

        #
        # # get PCCS and generate delta set
        self.PCCS_score, self.delta_source_grid, self.delta_target_grid = \
            self.generate_delta_set(self.source_feature, self.target_feature)
        print("[8 /10]       get PCCS and generate delta set done.")
        # print("self.PCCS_score",self.PCCS_score)
        # print("self.delta_source_grid",self.delta_source_grid)
        # print("self.delta_target_grid",self.delta_target_grid)
        # #
        # # # generate training and testing index
        self.source_grid_ids, self.target_grid_ids = self.generate_training_and_testing_index()
        print("[9/10]       generate training and testing index done.")
        # print("self.source_grid_ids",self.source_grid_ids)
        # print("self.target_grid_ids",self.target_grid_ids)
        anomaly_type = input("input a anomaly type:\n")
        #self.source_area_list,self.target_area_list = self.generate_area_list(anomaly_type,source_anomaly_data_dict)
        self.source_feature_list, self.target_feature_list = self.generate_area_list(anomaly_type, source_anomaly_data_dict,self.anomaly_category_dict_reverse,self.anomaly_id_time_dict,self.source_feature\
                                ,self.delta_target_grid,target_anomaly_data_dict,self.target_feature)
        self.split_feature(self.source_feature_list, self.target_feature_list)
        # #
        # # change data to tensor
        self.source_feature = torch.Tensor(self.source_feature)  # not sure
        self.target_feature = torch.Tensor(self.target_feature)  # not sure


    def cmp(self,time1,time2):
        format_pattern = "%m/%d/%Y %H:%M:%S"
        #print(time1)
        #print(time2)
        time1 = datetime.strptime(time1[1], format_pattern)
        time2 = datetime.strptime(time2[1], format_pattern)
        if time2>time1:
            return 1
        else:
            return -1
    def split_feature(self,source_feature_list, target_feature_list):
        #source_feature, target_feature, latest_source_feature, latest_target_feature = input[0], input[1], input[2],    input[3]
        print("split_feature")
        #print(len(source_feature_list))
        #print(len(source_feature_list[0]))
        print(len(target_feature_list))
        print(len(target_feature_list[0]))
        print(type(source_feature_list))
        #print(target_feature_list)
        source_list_1 = []
        source_list_2 = []
        for i in range(source_feature_list.__len__()):
            if(i+11)>=source_feature_list.__len__():
                source_list_1.append(source_feature_list[i:source_feature_list.__len__()-1])
                source_list_2.append(source_feature_list[source_feature_list.__len__()-1:])
                break
            temp1 = source_feature_list[i:i+10]
            temp2 = source_feature_list[i+11]
            source_list_1.append(temp1)
            source_list_2.append(temp2)
        #print(source_list_1[:-1])
        #print(source_list_2[:-1])
        #print(source_list_1.__len__())
        #print(source_list_2.__len__())
        target_list_1 = []
        target_list_2 = []
        for i in range(target_feature_list.__len__()):
            if(i+11)>=target_feature_list.__len__():
                target_list_1.append(target_feature_list[i:target_feature_list.__len__()-1])
                target_list_2.append(target_feature_list[target_feature_list.__len__()-1:])
                break
            temp1 = target_feature_list[i:i+10]
            temp2 = target_feature_list[i+11]
            target_list_1.append(temp1)
            target_list_2.append(temp2)

        print(target_list_1.__len__())
        print(target_list_2.__len__())
        global input_list
        input_list.append(source_list_1)
        input_list.append(source_list_2)
        input_list.append(target_list_1)
        input_list.append(target_list_2)

    def generate_area_list(self,anomaly_type,source_anomaly_data_dict,anomaly_category_dict_reverse,anomaly_id_time_dict,source_feature\
                           ,delta_target_grid,target_anomaly_data_dict,target_feature):
        xiangsi_list = get_xiangsi(anomaly_type)[:3]

        all_grid_id_list = list(source_anomaly_data_dict.keys())
        source_grid_id_list = []
        # [12, -74.0860273, 40.59187179, 7]
        # 12:异常事件id 7:异常事件类型
        for grid_id in all_grid_id_list:
            for one_event in source_anomaly_data_dict[grid_id]:
                event_name = anomaly_category_dict_reverse[one_event[3]]
                if anomaly_type == event_name:
                    source_grid_id_list.append(str(grid_id)+"#"+str(one_event[0]))
        for xiangsi in xiangsi_list:
            for grid_id in all_grid_id_list:
                for one_event in source_anomaly_data_dict[grid_id]:
                    event_name = anomaly_category_dict_reverse[one_event[3]]
                    if xiangsi == event_name:
                        source_grid_id_list.append(str(grid_id) + "#" + str(one_event[0]))
        grid_id_and_time = {}
        '''
        对网格根据事件id的时间进行排序
        '''

        print(anomaly_id_time_dict)
        for i in source_grid_id_list:
            grid_id = i.split("#")[0]
            event_id = int(i.split("#")[1])
            #print(i[1])
            event_time = anomaly_id_time_dict[event_id]
            grid_id_and_time[grid_id]= event_time # 网格id->时间
        #print(grid_id_and_time)
        #print(source_grid_id_list)
        #print(sorted(grid_id_and_time.items(), key=functools.cmp_to_key(self.cmp),reverse=True))
        grid_id_and_time = sorted(grid_id_and_time.items(), key=functools.cmp_to_key(self.cmp),reverse=True)
        #print(type(source_feature))

        source_feature_list = []
        for row in grid_id_and_time:
            source_feature_list.append(source_feature[int(row[0]), :])
        print("source_feature_list",source_feature_list)

        #print(delta_target_grid)
        #print(type(delta_target_grid))



        target_grid_id_list = []
        source_grid_id_list = []
        source_grid = []
        target_add_grid = []
        target_output_grid = []

        for grid_id in all_grid_id_list:
            for one_event in source_anomaly_data_dict[grid_id]:
                event_name = anomaly_category_dict_reverse[one_event[3]]
                if anomaly_type == event_name:
                    #source_grid_id_list.append(str(grid_id)+"#"+str(one_event[0]))
                    if str(grid_id) not in source_grid:
                        source_grid.append(grid_id)

        for i in source_grid:
            row = delta_target_grid[0, :][int(i), :]
            for j in row:
                if j not in target_add_grid:
                    target_add_grid.append(j)

        for i in target_add_grid:
            for one_event in target_anomaly_data_dict[i]:
                event_name = anomaly_category_dict_reverse[one_event[3]]
                if anomaly_type == event_name:
                    target_output_grid.append(str(i) + "#" + str(one_event[0]))
        '''
        根据时间排序
        '''
        grid_id_and_time = {}

        for i in target_output_grid:
            grid_id = i.split("#")[0]
            event_id = int(i.split("#")[1])
            #print(i[1])
            event_time = anomaly_id_time_dict[event_id]
            grid_id_and_time[grid_id]= event_time # 网格id->时间时间
        grid_id_and_time = sorted(grid_id_and_time.items(), key=functools.cmp_to_key(self.cmp), reverse=True)

        target_feature_list = []

        grid_id_len= len(grid_id_and_time)
        target_test_data_len = int((grid_id_len * 0.15))

        remain_grid_id_len = grid_id_len - target_test_data_len


        self.target_test_data_grid = []

        '''
        生成target_list用于生成训练数据
        '''
        for index in range(remain_grid_id_len):
            row = grid_id_and_time[index]
            target_feature_list.append(target_feature[int(row[0]), :])
        print(target_feature_list.__len__())
        '''
        生成测试集对应的网格id
        '''
        self.target_test_data = []
        self.id_list = []
        for index in range(remain_grid_id_len,grid_id_len):
            row = grid_id_and_time[index]
            self.target_test_data.append(target_feature[int(row[0]), :])
            self.id_list.append(int(row[0]))
            #self.target_test_data_grid.append(int(row[0]))

        self.target_list_1 = []
        target_list_2 = []

        for i in range(self.target_test_data.__len__()):
            if(i+11)>=self.target_test_data.__len__():
                self.target_list_1.append(self.target_test_data[i:self.target_test_data.__len__()-1])
                target_list_2.append(self.target_test_data[self.target_test_data.__len__()-1:])
                temp2_id = self.id_list[self.id_list.__len__()-1:]
                self.target_test_data_grid.append(temp2_id)
                break
            temp1 = self.target_test_data[i:i+10]
            temp2 = self.target_test_data[i+11]
            temp2_id = self.id_list[i+11]
            self.target_test_data_grid.append(temp2_id)
            self.target_list_1.append(temp1)
            target_list_2.append(temp2)

        #for row in grid_id_and_time:
        #    target_feature_list.append(target_feature[int(row[0]), :])



        # print(source_feature_list)
        #difference = (datetime.strptime(end_date, format_pattern) - datetime.strptime(start_date, format_pattern))
        return source_feature_list, target_feature_list

    def get_batch(self):
        batch_data = {}
        global input_list
        source_all  = len(input_list[0])/32 # source一共有多少批数据
        target_all = len(input_list[2])/32
        #self.target_test_data = input_list[2][len(input_list[2])-self.target_test_all:]
        source_list1 = input_list[0]
        source_list2 = input_list[1]
        target_list1 = input_list[2]
        target_list2 = input_list[3]

        self.source_score = []

        if self.source_youbiao < source_all:
            batch_data["feature_list"] = source_list1[32*self.source_youbiao:(self.source_youbiao+1)*32]
            batch_data["latest_feature"] = source_list2[32*self.source_youbiao:(self.source_youbiao+1)*32]

            for i in range(len(batch_data["feature_list"])):
                self.source_score.append(1)
            batch_data["score"] = self.source_score
        #a= [[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]....],[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]....]] 32个0-9 三维数组
        #b= [[1,1,1,1,1,1.....],[1,1,1,1,1....]] 32个10 二维数组
        #[1,1,1,...] 32个1 一维数组
        #(a,b,c)
        #[a,b,c]
        #model((a,b,c))
        #mode([a,b,c])

        if self.source_youbiao == source_all:
            batch_data["feature_list"] = source_list1[32 * self.source_youbiao:]
            batch_data["latest_feature"] = source_list2[32 * self.source_youbiao:]

            for i in range(len(batch_data["feature_list"])):
                self.source_score.append(1)

            batch_data["score"] = self.source_score

        self.source_youbiao = self.source_youbiao + 1

        if self.source_youbiao > source_all:
            self.target_score = []
            if self.target_youbiao < target_all:
                batch_data["feature_list"] = target_list1[32*self.target_youbiao:(self.target_youbiao+1)*32]
                batch_data["latest_feature"] = target_list2[32*self.target_youbiao:(self.target_youbiao+1)*32]

                for i in range(len(batch_data["feature_list"])):
                    self.target_score.append(1)

                batch_data["score"] = self.target_score

            if self.target_youbiao == target_all:
                batch_data["feature_list"] = target_list1[32 * self.target_youbiao:]
                batch_data["latest_feature"] = target_list2[32 * self.target_youbiao:]

                for i in range(len(batch_data["feature_list"])):
                    self.target_score.append(1)

                batch_data["score"] = self.target_score

            self.target_youbiao = self.target_youbiao + 1


            if self.target_youbiao > target_all:
                batch_data["feature_list"] = ""
                batch_data["latest_feature"] = ""


        #yield batch_data
        #batch_data = {}

        return batch_data

    def load_POI_data(self, POI_data_path):
        POI_data = pd.read_csv(POI_data_path, usecols=[0, 2, 3, 7, 13])
        # remap category to id
        POI_category_name = POI_data['category id 1'].unique()
        POI_category_dict = dict()
        POI_category_dict_reverse = dict()

        POI_category_id = 0
        for name in POI_category_name:
            POI_category_dict[name] = POI_category_id
            POI_category_dict_reverse[POI_category_id] = name
            POI_category_id += 1

        POI_data['category id 1'] = POI_data['category id 1'].map(lambda x: POI_category_dict[x])

        #  split into source data and target data.
        #  (shop_id, name, one_category, two_category, longitude, latitude, review_count, branchname)
        source_area_POI_data = []
        target_area_POI_data = []
        for row in POI_data.itertuples():
            if self.args.source_area_coordinate[0] <= row.longitude <= self.args.source_area_coordinate[1] \
                    and self.args.source_area_coordinate[2] <= row.latitude <= self.args.source_area_coordinate[3]:
                source_area_POI_data.append(list(row)[1:])

            elif self.args.target_area_coordinate[0] <= row.longitude <= self.args.target_area_coordinate[1] \
                    and self.args.target_area_coordinate[2] <= row.latitude <= self.args.target_area_coordinate[3]:
                target_area_POI_data.append(list(row)[1:])

        return source_area_POI_data, target_area_POI_data, POI_category_dict, POI_category_dict_reverse

    def load_anomaly_data(self, anomaly_data_path):
        anomaly_id_time_dict = {}

        anomaly_data = pd.read_csv(anomaly_data_path, usecols=[0,1,2,3,5,6])

        anomaly_data["id"] = anomaly_data["id"].astype('int')
        anomaly_data["CMPLNT_FR_DT"] = anomaly_data["CMPLNT_FR_DT"].astype('str')
        anomaly_data["CMPLNT_FR_TM"] = anomaly_data["CMPLNT_FR_TM"].astype('str')
        # remap category to id
        anomaly_category_name = anomaly_data['OFNS_DESC'].unique()
        anomaly_category_dict = dict()
        anomaly_category_dict_reverse = dict()

        anomaly_category_id = 0
        for name in anomaly_category_name:
            anomaly_category_dict[name] = anomaly_category_id
            anomaly_category_dict_reverse[anomaly_category_id] = name
            anomaly_category_id += 1

        anomaly_data['OFNS_DESC'] = anomaly_data['OFNS_DESC'].map(lambda x: anomaly_category_dict[x])

        #  split into source data and target data.
        #  (shop_id, name, one_category, two_category, longitude, latitude, review_count, branchname)
        source_area_anomaly_data = []
        target_area_anomaly_data = []
        for row in anomaly_data.itertuples():
            if self.args.source_area_coordinate[0] <= row.longitude <= self.args.source_area_coordinate[1] \
                    and self.args.source_area_coordinate[2] <= row.latitude <= self.args.source_area_coordinate[3]:
                source_area_anomaly_data.append(list(row)[1:])

            elif self.args.target_area_coordinate[0] <= row.longitude <= self.args.target_area_coordinate[1] \
                    and self.args.target_area_coordinate[2] <= row.latitude <= self.args.target_area_coordinate[3]:
                target_area_anomaly_data.append(list(row)[1:])
        for index, row in anomaly_data.iterrows():
            id = row['id']
            date = row['CMPLNT_FR_DT']
            time = row['CMPLNT_FR_TM']
            date_time = date + " " + time
            anomaly_id_time_dict[id] = date_time
        return source_area_anomaly_data, target_area_anomaly_data, anomaly_category_dict, anomaly_category_dict_reverse,anomaly_id_time_dict

    # def check_enterprise(self, source_area_data, target_area_data):
    #     #  columns = ['shop_id', 'name', 'big_category', 'small_category',
    #     #             'longitude', 'latitude', 'review_count', 'branchname']
    #
    #     source_chains = collections.defaultdict(list)
    #     target_chains = collections.defaultdict(list)
    #
    #     valid_small_category_set = set()
    #     for item in source_area_data:
    #         if item[1] in self.args.enterprise:
    #             source_chains[item[1]].append(item)
    #             valid_small_category_set.add(item[3])
    #     for item in target_area_data:
    #         if item[1] in self.args.enterprise:
    #             target_chains[item[1]].append(item)
    #             valid_small_category_set.add(item[3])
    #
    #     for name in self.args.enterprise:
    #         if len(source_chains[name]) == 0 or len(target_chains[name]) == 0:
    #             logging.error('品牌 {} 并非在原地区和目的地区都有门店'.format(name))
    #             exit(1)
    #
    #     target_enterprise_index = -1
    #     for idx, name in enumerate(self.args.enterprise):
    #         if name == self.args.target_enterprise:
    #             target_enterprise_index = idx
    #     if target_enterprise_index < 0:
    #         logging.error('目标企业{}必须在所选择的几家连锁企业中'.format(self.args.target_enterprise))
    #         exit(1)
    #
    #     all_enterprise_index = [idx for idx, _ in enumerate(self.args.enterprise)]
    #     portion_enterprise_index = [idx for idx, _ in enumerate(self.args.enterprise)
    #                                 if idx != target_enterprise_index]
    #
    #     return valid_small_category_set, target_enterprise_index, all_enterprise_index, portion_enterprise_index

    def split_grid(self):
        # source_area_longitude_boundary = np.append(np.arange(self.args.source_area_coordinate[0],
        #                                                      self.args.source_area_coordinate[1],
        #                                                      self.args.grid_size_longitude_degree),
        #                                            self.args.source_area_coordinate[1])
        source_area_longitude_boundary = np.arange(self.args.source_area_coordinate[0],
                                                   self.args.source_area_coordinate[1],
                                                   self.args.grid_size_longitude_degree)
        source_area_latitude_boundary = np.arange(self.args.source_area_coordinate[2],
                                                  self.args.source_area_coordinate[3],
                                                  self.args.grid_size_latitude_degree)
        target_area_longitude_boundary = np.arange(self.args.target_area_coordinate[0],
                                                   self.args.target_area_coordinate[1],
                                                   self.args.grid_size_longitude_degree)
        target_area_latitude_boundary = np.arange(self.args.target_area_coordinate[2],
                                                  self.args.target_area_coordinate[3],
                                                  self.args.grid_size_latitude_degree)

        n_source_grid = (len(source_area_longitude_boundary) - 1) * (len(source_area_latitude_boundary) - 1)
        n_target_grid = (len(target_area_longitude_boundary) - 1) * (len(target_area_latitude_boundary) - 1)
        logging.info('n_source_grid: {}, n_target_grid: {}'.format(n_source_grid, n_target_grid))

        return n_source_grid, n_target_grid, source_area_longitude_boundary, source_area_latitude_boundary, \
            target_area_longitude_boundary, target_area_latitude_boundary

    def distribute_data(self, source_area_POI_data, target_area_POI_data, source_area_anomaly_data, target_area_anomaly_data):
        #  columns = ['shop_id', 'longitude', 'latitude', 'checkin', 'category']
        source_POI_data_dict = collections.defaultdict(list)
        target_POI_data_dict = collections.defaultdict(list)
        source_anomaly_data_dict = collections.defaultdict(list)
        target_anomaly_data_dict = collections.defaultdict(list)
        source_grid_POI_data = collections.defaultdict(list)
        target_grid_POI_data = collections.defaultdict(list)
        source_grid_anomaly_data = collections.defaultdict(list)
        target_grid_anomaly_data = collections.defaultdict(list)
        for item in source_area_POI_data:
            lon_index = 0
            for index, _ in enumerate(self.source_area_longitude_boundary[:-1]):
                if self.source_area_longitude_boundary[index] <= item[1] <= self.source_area_longitude_boundary[index + 1]:
                    lon_index = index
                    break
            lat_index = 0
            for index, _ in enumerate(self.source_area_latitude_boundary[:-1]):
                if self.source_area_latitude_boundary[index] <= item[2] <= self.source_area_latitude_boundary[index + 1]:
                    lat_index = index
                    break
            grid_id = lon_index * (len(self.source_area_latitude_boundary) - 1) + lat_index
            source_POI_data_dict[grid_id].append(item)
            if item[1] in self.args.POI:
                source_grid_POI_data[grid_id].append(item)

        for item in target_area_POI_data:
            lon_index = 0
            for index, _ in enumerate(self.target_area_longitude_boundary[:-1]):
                if self.target_area_longitude_boundary[index] <= item[1] <= self.target_area_longitude_boundary[index + 1]:
                    lon_index = index
                    break
            lat_index = 0
            for index, _ in enumerate(self.target_area_latitude_boundary[:-1]):
                if self.target_area_latitude_boundary[index] <= item[2] <= self.target_area_latitude_boundary[index + 1]:
                    lat_index = index
                    break
            grid_id = lon_index * (len(self.target_area_latitude_boundary) - 1) + lat_index
            target_POI_data_dict[grid_id].append(item)
            if item[1] in self.args.POI:
                target_grid_POI_data[grid_id].append(item)

        for item in source_area_anomaly_data:
            lon_index = 0
            for index, _ in enumerate(self.source_area_longitude_boundary[:-1]):
                if self.source_area_longitude_boundary[index] <= item[1] <= self.source_area_longitude_boundary[index + 1]:
                    lon_index = index
                    break
            lat_index = 0
            for index, _ in enumerate(self.source_area_latitude_boundary[:-1]):
                if self.source_area_latitude_boundary[index] <= item[2] <= self.source_area_latitude_boundary[index + 1]:
                    lat_index = index
                    break
            grid_id = lon_index * (len(self.source_area_latitude_boundary) - 1) + lat_index
            source_anomaly_data_dict[grid_id].append(item)
            if item[0] in self.args.anomaly:
                source_grid_anomaly_data[grid_id].append(item)

        for item in target_area_anomaly_data:
            lon_index = 0
            for index, _ in enumerate(self.target_area_longitude_boundary[:-1]):
                if self.target_area_longitude_boundary[index] <= item[1] <= self.target_area_longitude_boundary[index + 1]:
                    lon_index = index
                    break
            lat_index = 0
            for index, _ in enumerate(self.target_area_latitude_boundary[:-1]):
                if self.target_area_latitude_boundary[index] <= item[2] <= self.target_area_latitude_boundary[index + 1]:
                    lat_index = index
                    break
            grid_id = lon_index * (len(self.target_area_latitude_boundary) - 1) + lat_index
            target_anomaly_data_dict[grid_id].append(item)
            if item[0] in self.args.anomaly:
                target_grid_anomaly_data[grid_id].append(item)

        return source_POI_data_dict, target_POI_data_dict, source_grid_POI_data, target_grid_POI_data, \
               source_anomaly_data_dict, target_anomaly_data_dict, source_grid_anomaly_data, target_grid_anomaly_data,

    def extract_geographic_features(self, source_POI_data_dict, target_POI_data_dict):
        traffic_convenience_corresponding_ids = [self.POI_category_dict[x]
                                                 for x in [ 'Highway or Road','Airport Tram','Train Station', 'Bus Line', 'Train','Taxi','Parking Garage','Subway','Bus Station' ] if x in self.POI_category_dict]

        def get_feature(grid_info):
            #  columns = ['shop_id', 'name', 'big_category', 'small_category',
            #             'longitude', 'latitude', 'review_count', 'branchname']

            n_grid_POI = len(grid_info)

            human_flow = 0
            traffic_convenience = 0
            POI_count = np.zeros(self.n_POI_category)

            for POI in grid_info:
                # Equation (3)
                if POI[4] in traffic_convenience_corresponding_ids:
                    traffic_convenience -= 1 #这里要看交通类的在哪一层
                # Equation (4)
                POI_count[POI[4]] += 1
                # Equation (2)
                human_flow -= POI[3]

            # Equation (1)
            diversity = -1 * np.sum([(v / (1.0 * n_grid_POI)) * np.log(v / (1.0 * n_grid_POI))
                                     if v != 0 else 0 for v in POI_count])

            return np.concatenate(([diversity, human_flow, traffic_convenience], POI_count))

        source_geographic_features = []
        target_geographic_features = []
        for index in range(self.n_source_grid):
            if len(source_POI_data_dict[index]) > 0:
                source_geographic_features.append(get_feature(source_POI_data_dict[index]))
            else:
                source_geographic_features.append(np.zeros(330))

        for index in range(self.n_target_grid):
            if len(target_POI_data_dict[index]) > 0:
                target_geographic_features.append(get_feature(target_POI_data_dict[index]))
            else:
                target_geographic_features.append(np.zeros(330))

        source_geographic_features, target_geographic_features = \
            np.array(source_geographic_features), np.array(target_geographic_features)

        diversity_max = max(np.max(source_geographic_features[:, 0]), np.max(target_geographic_features[:, 0]))
        diversity_min = min(np.min(source_geographic_features[:, 0]), np.min(target_geographic_features[:, 0]))
        human_flow_max = max(np.max(source_geographic_features[:, 1]), np.max(target_geographic_features[:, 1]))
        human_flow_min = min(np.min(source_geographic_features[:, 1]), np.min(target_geographic_features[:, 1]))
        traffic_conv_max = max(np.max(source_geographic_features[:, 2]), np.max(target_geographic_features[:, 2]))
        traffic_conv_min = min(np.min(source_geographic_features[:, 2]), np.min(target_geographic_features[:, 2]))
        POI_cnt_max = max(np.max(source_geographic_features[:, 3:]), np.max(target_geographic_features[:, 3:]))
        POI_cnt_min = min(np.min(source_geographic_features[:, 3:]), np.min(target_geographic_features[:, 3:]))

        def _norm(data, mmax, mmin):
            if mmax == mmin:
                return 0
            else:
                return (data - mmin) / (mmax - mmin)

        source_geographic_features[:, 0] = _norm(source_geographic_features[:, 0], diversity_max, diversity_min)
        source_geographic_features[:, 1] = _norm(source_geographic_features[:, 1], human_flow_max, human_flow_min)
        source_geographic_features[:, 2] = _norm(source_geographic_features[:, 2], traffic_conv_max, traffic_conv_min)
        source_geographic_features[:, 3:] = _norm(source_geographic_features[:, 3:], POI_cnt_max, POI_cnt_min)
        target_geographic_features[:, 0] = _norm(target_geographic_features[:, 0], diversity_max, diversity_min)
        target_geographic_features[:, 1] = _norm(target_geographic_features[:, 1], human_flow_max, human_flow_min)
        target_geographic_features[:, 2] = _norm(target_geographic_features[:, 2], traffic_conv_max, traffic_conv_min)
        target_geographic_features[:, 3:] = _norm(target_geographic_features[:, 3:], POI_cnt_max, POI_cnt_min)

        return source_geographic_features, target_geographic_features

    def extract_anomaly_features(self, source_anomaly_data_dict, target_anomaly_data_dict):

        def get_feature(grid_info):
            #  columns = ['id', 'longitude', 'latitude',  'category']
            n_grid_anomaly = len(grid_info)
            anomaly_count = np.zeros(self.n_anomaly_category)
            # Equation (异常密度)
            density = 0
            for anomaly in grid_info:
                density -= 1
                anomaly_count[anomaly[3]] += 1

            # Equation (异常复杂性)
            diversity = -1 * np.sum([(v / (1.0 * n_grid_anomaly)) * np.log(v / (1.0 * n_grid_anomaly))
                                     if v != 0 else 0 for v in anomaly_count])

            return np.concatenate(([diversity,density], anomaly_count))

        source_anomaly_features = []
        target_anomaly_features = []
        for index in range(self.n_source_grid):
            source_anomaly_features.append(get_feature(source_anomaly_data_dict[index]))
        for index in range(self.n_target_grid):
            target_anomaly_features.append(get_feature(target_anomaly_data_dict[index]))

        source_anomaly_features, target_anomaly_features = \
            np.array(source_anomaly_features), np.array(target_anomaly_features)

        diversity_max = max(np.max(source_anomaly_features[:, 0]), np.max(target_anomaly_features[:, 0]))
        diversity_min = min(np.min(source_anomaly_features[:, 0]), np.min(target_anomaly_features[:, 0]))
        density_max = max(np.max(source_anomaly_features[:, 1]), np.max(target_anomaly_features[:, 1]))
        density_min = min(np.min(source_anomaly_features[:,1]), np.min(target_anomaly_features[:, 1]))
        anomaly_cnt_max = max(np.max(source_anomaly_features[:, 2:]), np.max(target_anomaly_features[:, 2:]))
        anomaly_cnt_min = min(np.min(source_anomaly_features[:, 2:]), np.min(target_anomaly_features[:, 2:]))

        def _norm(data, mmax, mmin):
            if mmax == mmin:
                return 0
            else:
                return (data - mmin) / (mmax - mmin)

        source_anomaly_features[:, 0] = _norm(source_anomaly_features[:, 0], diversity_max, diversity_min)
        source_anomaly_features[:, 1] = _norm(source_anomaly_features[:, 1], density_max, density_min)
        source_anomaly_features[:, 2:] = _norm(source_anomaly_features[:, 2:], anomaly_cnt_max, anomaly_cnt_min)
        target_anomaly_features[:, 0] = _norm(target_anomaly_features[:, 0], diversity_max, diversity_min)
        target_anomaly_features[:, 1] = _norm(target_anomaly_features[:, 1], density_max, density_min)
        target_anomaly_features[:, 2:] = _norm(target_anomaly_features[:, 2:], anomaly_cnt_max, anomaly_cnt_min)

        return source_anomaly_features, target_anomaly_features


    def combine_features(self, source_geographic_features, target_geographic_features,
                         source_anomaly_features, target_anomaly_features):
        source_feature = np.concatenate((source_geographic_features, source_anomaly_features), axis=1)
        target_feature = np.concatenate((target_geographic_features, target_anomaly_features), axis=1)
        #print("soutrce",source_feature)

        feature_dim = source_feature.shape[1]
        print("所有网格的特征??",len(target_feature))

        # enterprise size * grid size * feature size
        return source_feature, target_feature, feature_dim

    def generate_rating_matrix(self, source_grid_enterprise_data, target_grid_enterprise_data):
        # columns = ['shop_id', 'name', 'big_category', 'small_category',
        #             'longitude', 'latitude', 'review_count', 'branchname']
        source_rating_matrix = np.zeros((len(self.args.enterprise), self.n_source_grid))
        target_rating_matrix = np.zeros((len(self.args.enterprise), self.n_target_grid))
        for grid_id in range(self.n_source_grid):
            for item in source_grid_enterprise_data[grid_id]:
                for idx, name in enumerate(self.args.enterprise):
                    if item[1] == name:
                        source_rating_matrix[idx][grid_id] += item[6]

        for grid_id in range(self.n_target_grid):
            for item in target_grid_enterprise_data[grid_id]:
                for idx, name in enumerate(self.args.enterprise):
                    if item[1] == name:
                        target_rating_matrix[idx][grid_id] += item[6]
        def _norm(data, mmax, mmin):
            if mmax == mmin:
                return 0
            else:
                return (data - mmin) / (mmax - mmin)

        source_rating_matrix = _norm(source_rating_matrix, self.args.score_norm_max, 0) * 5
        target_rating_matrix = _norm(target_rating_matrix, self.args.score_norm_max, 0) * 5

        source_rating_matrix = torch.Tensor(source_rating_matrix)
        target_rating_matrix = torch.Tensor(target_rating_matrix)
        res0 = torch.sort(target_rating_matrix[0], descending=True)
        res1 = torch.sort(target_rating_matrix[1], descending=True)

        return source_rating_matrix, target_rating_matrix

    def generate_delta_set(self, source_feature, target_feature):
        # Equation (13)
        score = []
        for idx, _ in enumerate(self.args.anomaly):
            source_info = source_feature
            target_info = target_feature
            source_mean = np.mean(source_info, axis=1)[:, None]
            target_mean = np.mean(target_info, axis=1)[:, None]
            source_std = np.std(source_info, axis=1)[:, None]
            target_std = np.std(target_info, axis=1)[:, None]
            idx_score = (np.matmul((source_info - source_mean), (target_info - target_mean).T) / self.feature_dim) / \
                        (np.matmul(source_std, target_std.T) + self.args.eps)
            score.append(idx_score)
        # score = np.array(score)
        score = torch.Tensor(score)

        delta_source_grid = [[[] for _ in range(self.n_source_grid)] for _ in self.args.anomaly]
        print("delta_source_grid",delta_source_grid)
        delta_target_grid = [[[] for _ in range(self.n_target_grid)] for _ in self.args.anomaly]

        for idx, _ in enumerate(self.args.anomaly):
            for source_grid_id in range(self.n_source_grid):
                sorted_index = np.argsort(-score[idx][source_grid_id])
                for k in range(min(self.args.gamma, self.n_target_grid)):
                    delta_source_grid[idx][source_grid_id].append(sorted_index[k])

        for idx, _ in enumerate(self.args.anomaly):
            for target_grid_id in range(self.n_target_grid):
                sorted_index = np.argsort(-score[idx][:, target_grid_id])
                for k in range(min(self.args.gamma, self.n_source_grid)):
                    delta_target_grid[idx][target_grid_id].append(sorted_index[k])
        #print("delta_target_grid",delta_target_grid)
        #print("len", len(delta_target_grid))
        #print(len(delta_target_grid[0]))
        # for idx in self.portion_enterprise_index:
        #     for target_grid_id in range(self.n_target_grid):
        #         sorted_index = np.argsort(-score[idx][:, target_grid_id])
        #         for k in range(min(self.args.gamma, self.n_source_grid)):
        #             delta_target_grid[idx][target_grid_id].append(sorted_index[k])

        delta_source_grid = np.array(delta_source_grid)
        delta_target_grid = np.array(delta_target_grid)
        #print("delta_target_grid",delta_target_grid)
        return score, delta_source_grid, delta_target_grid

    def generate_training_and_testing_index(self):
        source_grid_ids = np.arange(self.n_source_grid)
        target_grid_ids = np.arange(self.n_target_grid)
        random.shuffle(source_grid_ids)
        random.shuffle(target_grid_ids)
        return source_grid_ids, target_grid_ids

    def get_score_and_feature_for_inter_city(self, batch_index, batch_type):
        score, source_feature, target_feature = [], [], []

        if batch_type == 's':
            for idx in self.all_enterprise_index:
                source_index = []
                target_index = []
                for index in batch_index:
                    source_index.extend([index for _ in range(self.delta_source_grid[idx][index].shape[0])])
                    target_index.extend(self.delta_source_grid[idx][index])
                score.append(self.PCCS_score[idx][source_index, target_index])
                source_feature.append(self.source_feature[idx][source_index])
                target_feature.append(self.target_feature[idx][target_index])
        else:
            for idx in self.portion_enterprise_index:
                source_index = []
                target_index = []
                for index in batch_index:
                    source_index.extend(self.delta_target_grid[idx][index])
                    target_index.extend([index for _ in range(self.delta_target_grid[idx][index].shape[0])])
                score.append(self.PCCS_score[idx][source_index, target_index])
                source_feature.append(self.source_feature[idx][source_index])
                target_feature.append(self.target_feature[idx][target_index])

        score = torch.stack(score, dim=0)
        source_feature = torch.stack(source_feature, dim=0)
        target_feature = torch.stack(target_feature, dim=0)

        return score, source_feature, target_feature

    def get_feature_and_rel_score_for_prediction_model(self, grid_index, grid_type):
        if grid_type == 's':
            feature = self.source_feature[:, grid_index]
            score = self.source_rating_matrix[:, grid_index]
        elif grid_type == 't':
            feature = self.target_feature[self.portion_enterprise_index][:, grid_index]
            score = self.target_rating_matrix[self.portion_enterprise_index][:, grid_index]
        else:
            logging.error('未定义类型')
            exit(1)
        return feature, score

    def get_feature_and_rel_score_for_evaluate(self):

        # target_data_test = self.target_test_data

        feature = self.target_list_1
        ground_truth_grid = self.target_test_data_grid
        ground_truth_grid = ground_truth_grid[:-1]
        return feature, ground_truth_grid

    def get_grid_coordinate_rectangle_by_grid_id(self, grid_id, grid_type):
        if grid_type == 's':
            row_id = grid_id // (len(self.source_area_latitude_boundary) - 1)
            col_id = grid_id % (len(self.source_area_latitude_boundary) - 1)
            lon_lef = self.source_area_longitude_boundary[row_id]
            lon_rig = self.source_area_longitude_boundary[row_id + 1]
            lat_down = self.source_area_latitude_boundary[col_id]
            lat_up = self.source_area_latitude_boundary[col_id + 1]
        else:
            row_id = grid_id // (len(self.target_area_latitude_boundary) - 1)
            col_id = grid_id % (len(self.target_area_latitude_boundary) - 1)
            lon_lef = self.target_area_longitude_boundary[row_id]
            lon_rig = self.target_area_longitude_boundary[row_id+1]
            lat_down = self.target_area_latitude_boundary[col_id]
            lat_up = self.target_area_latitude_boundary[col_id+1]
        return [[lat_up, lon_lef], [lat_down, lon_rig]]
        # coordinate_lon = [lon_lef, lon_lef, lon_rig, lon_rig, lon_lef]
        # coordinate_lat = [lat_up, lat_down, lat_down, lat_up, lat_up]
        # return coordinate_lon, coordinate_lat

    def get_grid_coordinate_circle_by_grid_id(self, grid_id, grid_type):
        if grid_type == 's':
            row_id = grid_id // (len(self.source_area_latitude_boundary) - 1)
            col_id = grid_id % (len(self.source_area_latitude_boundary) - 1)
            lon = (self.source_area_longitude_boundary[row_id] + self.source_area_longitude_boundary[row_id + 1]) / 2
            lat = (self.source_area_latitude_boundary[col_id] + self.source_area_latitude_boundary[col_id + 1]) / 2
        else:
            row_id = grid_id // (len(self.target_area_latitude_boundary) - 1)
            col_id = grid_id % (len(self.target_area_latitude_boundary) - 1)
            lon = (self.target_area_longitude_boundary[row_id] + self.target_area_longitude_boundary[row_id+1]) / 2
            lat = (self.target_area_latitude_boundary[col_id] + self.target_area_latitude_boundary[col_id+1]) / 2
        return [lat, lon]

    def get_grid_coordinate(self, real_grids, pred_grids, pred_back_rank):
        real_grids_draw_info = [self.get_grid_coordinate_rectangle_by_grid_id(grid, 't') for grid in real_grids]
        pred_grids_draw_info = [self.get_grid_coordinate_circle_by_grid_id(grid, 't') for grid in pred_grids]
        pred_back_grids_draw_info = [self.get_grid_coordinate_circle_by_grid_id(grid, 't') for grid in pred_back_rank]

        return real_grids_draw_info, pred_grids_draw_info, pred_back_grids_draw_info

    def get_grid_coordinate_rhombus_by_grid_id(self, grid_id, grid_type):
        if grid_type == 's':
            row_id = grid_id // (len(self.source_area_latitude_boundary) - 1)
            col_id = grid_id % (len(self.source_area_latitude_boundary) - 1)
            lon_lef = self.source_area_longitude_boundary[row_id]
            lon_rig = self.source_area_longitude_boundary[row_id + 1]
            lat_down = self.source_area_latitude_boundary[col_id]
            lat_up = self.source_area_latitude_boundary[col_id + 1]
        else:
            row_id = grid_id // (len(self.target_area_latitude_boundary) - 1)
            col_id = grid_id % (len(self.target_area_latitude_boundary) - 1)
            lon_lef = self.target_area_longitude_boundary[row_id]
            lon_rig = self.target_area_longitude_boundary[row_id+1]
            lat_down = self.target_area_latitude_boundary[col_id]
            lat_up = self.target_area_latitude_boundary[col_id+1]
        return [[lat_up, (lon_lef+lon_rig)/2], [(lat_up+lat_down)/2, lon_lef],
                [lat_down, (lon_lef+lon_rig)/2], [(lat_up+lat_down)/2, lon_rig]]

    def get_target_other_shops_coordinate(self):
        other_shops_draw_info = []

        _, enterprises_grids = torch.sort(self.target_rating_matrix[self.portion_enterprise_index], descending=True)
        for index, enterprise_grids in enumerate(enterprises_grids):
            valid_len = len(torch.nonzero(self.target_rating_matrix[self.portion_enterprise_index][index]))
            valid_grid = enterprise_grids[:valid_len]
            for grid in valid_grid:
                other_shops_draw_info.append(self.get_grid_coordinate_rhombus_by_grid_id(grid, 't'))

        return other_shops_draw_info

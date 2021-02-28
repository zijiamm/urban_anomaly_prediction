import os
import pandas as pd
import numpy as np
import collections
import random
import torch
import logging

class DataLoader(object):
    def __init__(self, args):
        self.args = args

        # define data path
        data_dir = os.path.join(args.data_dir, args.city_name)

        # load dianping data
        source_area_data, target_area_data, self.big_category_dict, self.big_category_dict_reverse, \
            self.small_category_dict, self.small_category_dict_reverse = self.load_dianping_data(dianping_data_path)
        self.n_big_category = len(self.big_category_dict)
        self.n_small_category = len(self.small_category_dict)
        logging.info("[1 /10]       load dianping data done.")

        # check anomaly and get small category set
        valid_small_category_set, self.target_anomaly_index, self.all_anomaly_index, \
            self.portion_anomaly_index = self.check_anomaly(source_area_data, target_area_data)
        logging.info("[2 /10]       check anomaly and get small category set.")

        # split grid
        self.n_source_grid, self.n_target_grid, self.source_area_longitude_boundary, \
            self.source_area_latitude_boundary, self.target_area_longitude_boundary, self.target_area_latitude_boundary\
            = self.split_grid()
        logging.info("[3 /10]       split grid done.")

        # distribute data into grids
        source_data_dict, target_data_dict, source_grid_anomaly_data, target_grid_anomaly_data \
            = self.distribute_data(source_area_data, target_area_data)
        logging.info("[4 /10]       distribute data into grids done.")

        # generate rating matrix for Transfer Rating Prediction Model
        self.source_rating_matrix, self.target_rating_matrix = self.generate_rating_matrix(source_grid_anomaly_data,
                                                                                           target_grid_anomaly_data)
        logging.info("[5 /10]       generate rating matrix for Transfer Rating Prediction Model done.")

        # extract geographic features
        source_geographic_features, target_geographic_features = self.extract_geographic_features(source_data_dict,
                                                                                                  target_data_dict)
        logging.info("[6 /10]       extract geographic features done.")

        # extract commercial features
        source_commercial_features, target_commercial_features = \
            self.extract_commercial_features(source_data_dict, target_data_dict, valid_small_category_set)
        logging.info("[7 /10]       extract commercial features done.")

        # combine features
        self.source_feature, self.target_feature, self.feature_dim = \
            self.combine_features(source_geographic_features, target_geographic_features,
                                  source_commercial_features, target_commercial_features)
        logging.info("[8 /10]       combine features done.")
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import GRU
import argparse
import logging
import urban_anomaly_prediction.data_loader


class AutoEncoder(nn.Module):
    def __init__(self, out_dim):
        super(AutoEncoder, self).__init__()
        self.mid_dim = math.ceil(math.sqrt(370*out_dim))
        self.encoder = nn.Sequential(
            nn.Linear(370, self.mid_dim),
            nn.Tanh(),
            nn.Linear(self.mid_dim, out_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(out_dim, self.mid_dim),
            nn.Tanh(),
            nn.Linear(self.mid_dim, 370),
        )

    def forward(self, x):
        # Equation (15 & 16)
        encoded_x = self.encoder(x)
        # Equation (17 & 18)
        decoded_x = self.decoder(encoded_x)
        return encoded_x, decoded_x


class GRU(nn.Module):
    def __init__(self, feature_dim):
        super(GRU, self).__init__()
        self.gruS = nn.GRU(input_size=feature_dim, hidden_size=feature_dim)
        # self.gruT = nn.GRU(input_size=feature_dim, hidden_size=feature_dim)
        self.fc1 = nn.Sequential(
            nn.Linear(434, 2 * feature_dim),
            nn.Linear(2 * feature_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )
        # self.fc2 = nn.Sequential(
        #     nn.Linear(2*feature_dim, 32),
        #     nn.ReLU(),
        #     nn.Linear(32, 2)
        # )
        # auto encoder
        self.auto_encoder = nn.ModuleList()
        self.auto_encoder.append(AutoEncoder(feature_dim))  # source

    def forward(self,*global_input):
        source_feature_list1 = global_input[0]
        # target_feature_list1 = global_input[1]
        latest_source_feature = global_input[1]
        # print('latest_source_feature.shape',latest_source_feature.shape)
        # source_feature, target_feature, latest_source_feature, latest_target_feature= input[0], input[1], input[2], input[3]
        encode_s, decode_s = self.auto_encoder[0](source_feature_list1)
        # encode_t, decode_t = self.auto_encoder[0](target_feature_list1)

        pref1 = self.gruS(encode_s)
        # pref2 = self.gruT(encode_t)
        # print(pref1)

        pref1 = pref1[0]
        # pre1是32*10*64 latest_source_feature是32*370
        pref1 = pref1[:,-1,:]
        print(pref1.shape)
#        latest_source_feature = torch.from_numpy(latest_source_feature)
        pref1 = torch.cat([pref1, latest_source_feature], dim=-1)
        print(pref1.shape)
        # print(type(pref1))
        # pref2 = torch.cat([pref2, latest_source_feature], dim=-1)

        pref1 = self.fc1(pref1)
        # pref2 = self.fc2(pref2)
        return decode_s,  pref1



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GRU Args.")
    args = parser.parse_args()
    args.auto_encoder_dim = 9
    args.enterprise = ['a', 'b', 'c']
    c = GRU(args, 5, 1000, 1000)

    # print(res2)

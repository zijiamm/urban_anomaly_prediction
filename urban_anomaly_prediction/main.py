
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import time

from urban_anomaly_prediction.GRU import GRU
from urban_anomaly_prediction.args_parser import parse_args
import logging
import urban_anomaly_prediction.GRU
from urban_anomaly_prediction.data_loader import DataLoader
# from CityTransfer.utility.metrics import ndcf_at_k_test
# from CityTransfer.utility.visualization import VisualizationTool
# from CityTransfer.CityTransfer import CityTransfer

DEBUG = True
CUDA_AVAILABLE = False
DEVICE = None
N_GPU = 0


def system_init(system_args):
    # set seed
    random.seed(system_args.seed)
    np.random.seed(system_args.seed)
    torch.manual_seed(system_args.seed)

    # init log
    # logging_config(system_args.save_dir, no_console=False)

    # CUDA
    global CUDA_AVAILABLE, DEVICE, N_GPU
    CUDA_AVAILABLE = torch.cuda.is_available()
    DEVICE = torch.device("cuda" if CUDA_AVAILABLE else "cpu")
    N_GPU = torch.cuda.device_count()
    if N_GPU > 0:
        torch.cuda.manual_seed_all(system_args.seed)

    # other settings
    # 显示所有列
    pd.set_option('display.max_columns', None)


def softmax(X):
    """
    softmax函数实现


    返回：
    softmax计算结果
    """
    assert (len(X.shape) == 2)
    row_max = np.max(X, axis=axis).reshape(-1, 1)
    X -= row_max
    X_exp = np.exp(X)
    s = X_exp / np.sum(X_exp, axis=axis, keepdims=True)

    return s


if __name__ == '__main__':
    # get args and init
    args = parse_args()
    system_init(args)
    logging.info(args)
    logging.info("--------------parse args and init done.")

    # load data
    data = DataLoader(args)
    source_batch = [data.source_grid_ids[i: i + args.batch_size]
                    for i in range(0, len(data.source_grid_ids), args.batch_size)]
    target_batch = [data.target_grid_ids[i: i + args.batch_size]
                    for i in range(0, len(data.target_grid_ids), args.batch_size)]
    while len(source_batch) < len(target_batch):
        random_i = random.randint(0, len(data.source_grid_ids))
        source_batch.append(data.source_grid_ids[random_i: random_i + args.batch_size])
    while len(target_batch) < len(source_batch):
        random_i = random.randint(0, len(data.target_grid_ids))
        target_batch.append(data.target_grid_ids[random_i: random_i + args.batch_size])
    logging.info("--------------load data done.")

    model = GRU(64)
    model.to(DEVICE)
    logging.info(model)
    # optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, weight_decay=args.lambda_4)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.lambda_4)
    logging.info("--------------construct model and optimizer done.")

    # move to GPU
    if CUDA_AVAILABLE:
        model.to(DEVICE)
        # data.source_rating_matrix = data.source_rating_matrix.to(DEVICE)
        # data.target_rating_matrix = data.target_rating_matrix.to(DEVICE)
        data.source_feature = data.source_feature.to(DEVICE)
        data.target_feature = data.target_feature.to(DEVICE)
        # data.PCCS_score = data.PCCS_score.to(DEVICE)
        # data.score = data.score.to(DEVICE)

    # training
    logging.info("[!]-----------start training.")
    tr1ple = 0
    mzj = 0
    for epoch in range(args.n_epoch):
        model.train()
        iter_total_loss = 0
        # print("sssssssssssssssssssssssssss",len(source_batch))
        for batch_iter in range(len(source_batch)):
            batch_data = data.get_batch()
            if batch_data["feature_list"] == "":
                break

            time_iter = time.time()

            optimizer.zero_grad()
            batch_total_loss = 0

            # 二十个一等份 batch=32 (0~20,21)(1~21,22)...


            batch_data["feature_list"] = torch.tensor(batch_data["feature_list"])
            batch_data["feature_list"]  = batch_data["feature_list"].to(torch.float32)
            batch_data["feature_list"] = batch_data["feature_list"].cuda()

            #batch_data["latest_feature"] = torch.tensor(batch_data["latest_feature"])
            #batch_data["latest_feature"] = batch_data["latest_feature"].to(torch.float32)
            #batch_data["latest_feature"] = batch_data["latest_feature"].cuda()


            try:
                batch_data["latest_feature"] = torch.tensor(batch_data["latest_feature"])
                batch_data["latest_feature"] = batch_data["latest_feature"].to(torch.float32)
                batch_data["latest_feature"] = batch_data["latest_feature"].cuda()

            except:
                print("tr1ple==", tr1ple)
                print(len(batch_data["feature_list"]))
                print(type(batch_data["feature_list"][0]))
                print(len(batch_data["score"]))

                print(batch_data["feature_list"][0].shape)
                print("end")
                for i in range(len(batch_data["latest_feature"])):
                    if isinstance(batch_data["latest_feature"][i],list):
                        batch_data["latest_feature"][i] = batch_data["latest_feature"][i][0]
                        #print(type(i))

                batch_data["latest_feature"] = torch.tensor(batch_data["latest_feature"])
                batch_data["latest_feature"] = batch_data["latest_feature"].to(torch.float32)
                batch_data["latest_feature"] = batch_data["latest_feature"].cuda()

                '''
                print("tr1ple==",tr1ple)

                print(type(batch_data["latest_feature"]))
                print(len(batch_data["latest_feature"]))
                #print(type(batch_data["latest_feature"][0])) # ndarray
                for i in batch_data["latest_feature"]:
                    if isinstance(i,list):
                        print(i)
                        print(type(i))
                    else:
                        print(i.shape) # 序列长度370

                '''
                #print("这条数据不太对",batch_data["latest_feature"])

            '''
            if tr1ple == 0:
                print("tr1ple==0")
                print(type(batch_data["latest_feature"]))
                print(len(batch_data["latest_feature"]))
                print(type(batch_data["latest_feature"][0]))
                print(batch_data["latest_feature"][0]) #序列长度370
            '''
            tr1ple = tr1ple + 1
            batch_data["score"] = torch.tensor(batch_data["score"])
            batch_data["score"]  = batch_data["score"].to(torch.long)

            batch_data["score"] = batch_data["score"].cuda()
            if mzj == 0:
                print("mzj")
                print(batch_data["feature_list"].shape)
                print(batch_data["latest_feature"].shape)
            mzj = mzj+1
            # Torch.tensor(a,b,c,d, score_source, score_target);
            # a,b,c,d,s_score, t_score = a.cuda(),b.cuda()...
            # 输入source_data
            decode_s, pref1= model(batch_data["feature_list"], batch_data["latest_feature"])
            # feature_list：torch.Size([32, 10, 370]) latest_feature：torch.Size([32, 370])

            # 输入target_data
            # decode_t, pref2, = model(batch_data["feature_list"], batch_data["latest_feature"])
            Loss1 = nn.MSELoss().cuda()

            encoderLoss_source = Loss1(decode_s, batch_data["feature_list"])
            # encoderLoss_target = F.mse_loss(decode_t, batch_data["target_feature"])

            Loss2 = nn.NLLLoss().cuda()
            gruPrefLoss_source = Loss2(pref1, batch_data["score"])
            # gruPrefLoss_target = nn.NLLLoss(pref2, batch_data["target_score"])

            # def loss(encoderLoss_source,gruPrefLoss_source):
            #     loss = encoderLoss_source.item() + gruPrefLoss_source.item()
            #     return (torch.tensor(0.0, requires_grad=True) if loss == 0 else loss)
            # loss(encoderLoss_source,gruPrefLoss_source)

            loss = encoderLoss_source + gruPrefLoss_source

            loss.backward()

            optimizer.step()

            if DEBUG and (batch_iter % args.print_every) == 0:
                logging.info('Training: Epoch {:04d} / {:04d} | Iter {:04d} / {:04d} | Time {:.1f}s '
                             '| Iter Loss {:.4f} | Iter Mean Loss {:.4f}'.
                             format(epoch, args.n_epoch, batch_iter, len(source_batch) - 1, time.time() - time_iter,
                                    batch_total_loss, iter_total_loss / (batch_iter + 1)))

    # testing
    logging.info("[!]-----------start testing.")
    model.eval()
    sum = 0
    correct = 0
    tr1ple = 0
    with torch.no_grad():
        # 返回一个序列，还有ground_truth grid
        feature,ground_truth_grid_id = data.get_feature_and_rel_score_for_evaluate()
        sum += 1
        # scoreList = []
        feature_len = len(feature)
        target_feature_len = len(data.target_feature)

        for i in range(feature_len):
            temp_feature = feature[i]
            #temp_feature = np.repeat(temp_feature,target_feature_len,axis=0)
            temp_feature =  np.expand_dims(temp_feature,0).repeat(target_feature_len,axis=0)
            temp_feature = torch.tensor(temp_feature)
            temp_feature = temp_feature.to(torch.float32)
            temp_feature = temp_feature.to(DEVICE)
            o1, o2 = model(temp_feature, data.target_feature)
            o2 = F.softmax(o2,dim=1)
            baseScore = torch.LongTensor([0,1]).cuda()
            scoreList = torch.sum(o2 * baseScore, dim=1)
        # scoreList = scoreList.tensor()
        values_5, indices_5 = torch.topk(scoreList, 10000)
        indices_5 = indices_5.cpu().numpy()
        for grid_id in ground_truth_grid_id:
            if grid_id in indices_5:
                correct += 1
    print("准确率为",correct/sum)

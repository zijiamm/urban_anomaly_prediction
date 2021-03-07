import torch
from time import time
from gru import GRU
import numpy as np

CUDA_AVAILABLE = False
DEVICE = None
N_GPU = 0

if __name__ == '__main__':
    # system init and CUDA

    seed=980720
    np.random.seed(seed)
    torch.random.manual_seed(seed)

    CUDA_AVAILABLE = torch.cuda.is_available()
    if CUDA_AVAILABLE:
        torch.cuda.manual_seed_all(seed)
        N_GPU = torch.cuda.device_count()
    DEVICE = torch.device("cuda:{}".format(1) if CUDA_AVAILABLE else "cpu")
    print("|--           system init done.")

    # load data
    adj, features, y_train, y_val, y_test, train_mask, val_mask, test_mask = load_data(args.dataset)
    print('adj:', adj.shape)
    print('features:', features.shape)
    print('y:', y_train.shape, y_val.shape, y_test.shape)
    print('mask:', train_mask.shape, val_mask.shape, test_mask.shape)
    # data extract

    # model and optimizer
    print("|--           build model and optimizer.")
    model = GRU(data.n_category, data.n_city_grid, data.n_kg_relation, data.graph_entity_relation_to_ID)
    if CUDA_AVAILABLE:
        model = model.to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    # train model
    print("|--           begin training model.")
    kg_loss_list = []
    ncf_loss_list = []
    hr_list_list = [[] for k in args.K_list]
    ndcg_list_list = [[] for k in args.K_list]

    for epoch in range(args.n_epoch):
        # data.shuffle_train_data_index()
        epoch_start_time = time()
        model.train()

        # calculate attention for propagation
        for city_id, _ in enumerate(args.city_list):
            with torch.no_grad():
                attention_score = model("cal_KG_attention", city_id, data.city_graphs[city_id])
            for k, v in attention_score.items():
                data.city_graphs[city_id].edges[k[1]].data['att'] = v

      # test
        model.eval()
        with torch.no_grad():
            test_grids, target_cate_ids = data.get_test_data()

            hr_list_val, ndcg_list_val = \
                model("test", data.city_graphs[args.target_city_id], target_cate_ids, test_grids)

            for k_index, _ in enumerate(args.K_list):
                hr_list_list[k_index].append(hr_list_val[k_index])
                ndcg_list_list[k_index].append(ndcg_list_val[k_index])

            test_base_logging_info = '|--            Epoch {:03d} | Test :'.format(epoch)
            test_metrics_logging_info_list = [' | HR@{} {:.4f} - NDCG@{} {:.4f}'.format(k_val, hr_list_val[k_idx],
                                                                                        k_val, ndcg_list_val[k_idx])
                                              for k_idx, k_val in enumerate(args.K_list)]
            test_metrics_logging_info_list = ''.join(test_metrics_logging_info_list)

            print(test_base_logging_info + test_metrics_logging_info_list)

    # train model done
    print("|--           training model done.")


'''
输入：
1. 第一行为n、m、k，n为无向图节点的数量，m为边的数量，k为knn的参数；
2. 第2 - m+1行，表示边；注意，拓扑中没有孤立的点，即每个点至少都有一条边与之相连；
3. 第m+2 - m+n+1行，无向图的节点信息，依次是节点id、设备类型、槽位数量、路由数量、端口数量、关联mac数量、节点类型；未知节点标识为unknown
拓扑数量<=1000,边数量<=10000，节点id是从0开始的连续编号，每个测试用例仅包含一个unknown节点；
输出：
unknown节点的id和分类

输入样例1：
7 6 1
0 1
0 2
0 3
2 5
2 6
3 4
0 1 5 8 10 3 RSG
1 3 12 10 11 7 CSG
2 2 4 1 6 10 unknown
3 2 4 1 6 10 ASG
4 3 12 10 11 7 CSG
5 3 12 10 11 7 CSG
6 3 12 10 11 7 CSG


输出样例1：
2 ASG

1. 第一步处理每个节点特征，网元类型转变为one-hot向量；
计算欧式距离
2. 


steps:
给定一个训练集，对新的输入实例：
1. 在训练数据集中找到与该实例最近的K个实例；这K个实例的多数属于某个类，就把该输入实例分类到这个类中；实例采用欧式距离计算；
2. 临近排序时首先根据距离排序，若距离相同，根据实例id排序；如果出现多个最多数类的情况，则根据规定顺序确定新实例类别；


'''


def distance(n1, n2):
    total = 0
    for i in range(len(n1)):
        total += (n1[i] - n2[i]) ** 2
    return total / len(n1)

def knn(node_id, nodes: dict, k):
    # node_id: 需要预测类别（label）的节点编号；
    # nodes:以字典形式存储所有已知节点，结构为
    # nodes= {
    #     node_id: {
    #         'feature': [f1, f2, ..., fd],   # 特征向量
    #         'label':   'RSG'|'ASG'|'CSG'    # 已知类别
    #     },
    #     ...
    # }
    target_info=nodes[node_id]
    # 把待预测节点（node_id）的完整信息取出来，方便后续使用。
    res_list = []
    # 初始化一个空列表，用来存放“其他节点 → 与目标节点的距离”。

    for idx, value in nodes.items():
        # 遍历整个 nodes 字典，idx 是节点编号，value 是对应的字典信息（包含特征和标签）。
        if idx == node_id:
            continue
            # 如果当前节点就是待预测节点自己，则跳过，不和自己比较。
        dist = distance(target_info['feature'],value['feature'])
        # 调用前面定义的 distance 函数，计算当前节点与目标节点在特征空间中的距离。

        res_list.append([idx,dist])
        # 把 [节点编号, 距离] 作为一个子列表，追加到 res_list。


    res_list = sorted(res_list, key = lambda x: (x[1], x[0]), reverse = False)
    # 对 res_list 进行升序排序：
    # 第一排序键是距离 x[1]（越小越靠前）；
    # 第二排序键是节点编号 x[0]（保证距离相同时，编号小的排在前面，结果可复现）。
    res_list = res_list[:k]
    # 只保留距离最小的前 k 个邻居。

    labels = [nodes[item[0]]['label'] for item in res_list]
    # 把这 k 个邻居的类别标签取出来，得到一个长度为 k 的字符串列表 labels。

    stat = [labels.count('RSG'), labels.count('ASG'), labels.count('CSG')]
    # 统计每个类别出现的次数，得到一个长度为 3 的整数列表 stat，顺序固定为 [RSG 个数, ASG 个数, CSG 个数]


    for idx, label in enumerate(['RSG', 'ASG', 'CSG']):
        if stat[idx] == max(stat):
            return node_id, label
    return  node_id, -1
    # 遍历三个类别 'RSG', 'ASG', 'CSG'。
    # 如果某个类别的出现次数等于最大值（即得票最多），立即返回 (node_id, 该类别)。
    # 因为遍历顺序固定，若出现平票，排在最前面的类别（RSG）会优先胜出。

































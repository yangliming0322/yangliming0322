class Solution(object):
    def findRedundantConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        n = len(edges)  # 节点数量
        parent = list(range(n + 1))  # parent[i]=i 表示每个节点最初都是自己的“根”
        # 题目中节点编号是 1..n，所以数组长度设为 n+1（索引 0 不用）。

        # 作用：找到节点 index 所在集合的根节点
        # 路径压缩：把沿途所有节点直接挂到根节点下面，扁平化树高，后续查询更快。
        # 递归写法：简洁，但深度过大时可能爆栈（本题节点数 ≤ 1000，安全）。
        def find(index):
            if parent[index] != index:
                parent[index] = find(parent[index])
            return parent[index]

        # 合并（按根合并，无秩优化）
        # 把 index1 的根直接挂到 index2 的根下面。
        # 没有按秩合并：代码更短，但在极端数据下可能退化，本题数据规模小，可接受。
        def union(index1, index2):
            parent[find(index1)] = find(index2)

        # 主循环：依次加边

        for node1, node2 in edges:
            print("--------------$$$$$$$$$$$$$--------------")
            print(f"[{node1},{node2}]:")
            print(f"{node1} 的父亲节点为{find(node1)}")
            print(f"{node2} 的父亲节点为{find(node2)}")

            if find(node1) != find(node2):
                # 如果两端点未连通，则合并两个集合
                union(node1, node2)
            else:
                # 若两端点已连通 → 当前边就是冗余边，直接返回。
                # 关键点：题目保证有且只有一条冗余边，所以第一个遇到的成环边就是答案。
                return [node1, node2]
        return []
        # 兜底返回：根据题意，冗余边一定存在，理论上不会走到这里；写上是良好习惯。


edges=[[1,2],[1,3],[2,3]]
fine=Solution()
ret=fine.findRedundantConnection(edges)

print("最终返回结果：", ret)
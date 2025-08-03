class Solution(object):
    def findRedundantConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        n = len(edges)  # 节点数量
        parent = list(range(n + 1))  # parent[i]=i 表示每个节点最初都是自己的“根”

        # 作用：找到节点 index 所在集合的根节点
        def find(index):
            if parent[index] != index:
                parent[index] = find(parent[index])
            return parent[index]

        def union(index1, index2):
            parent[find(index1)] = find(index2)

        for node1, node2 in edges:
            print("--------------$$$$$$$$$$$$$--------------")
            print(f"[{node1},{node2}]:")
            print(f"{node1} 的父亲节点为{find(node1)}")
            print(f"{node2} 的父亲节点为{find(node2)}")

            if find(node1) != find(node2):
                union(node1, node2)
            else:
                return [node1, node2]
        return []


edges=[[1,2],[1,3],[2,3]]
fine=Solution()
ret=fine.findRedundantConnection(edges)

print("最终返回结果：", ret)
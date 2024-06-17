import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random


# 读取外部文件
def readText(fileName):
    # fileName = input("请输入文件名：")
    fileName = str(fileName + ".txt")
    txt = open(fileName, "r").read()
    txt = txt.lower()
    txt = txt.replace(",", " ").replace(".", " ")
    txt = txt.split()
    return txt


# 生成表和有向图
def geneGraph(text):
    chart = []
    for word in text:
        if word not in chart:
            chart.append(word)
    length = len(chart)
    graph = np.zeros((length, length))
    for i in range(len(text) - 1):
        row = chart.index(text[i])
        col = chart.index(text[i + 1])
        graph[row, col] = graph[row, col] + 1
    return chart, graph


# 展示有向图
def showDirectedGraph(graph, chart, path=None):
    G = nx.DiGraph()  # 创建：空的有向图
    for i in range(len(chart)):
        for j in range(len(chart)):
            if graph[i, j] > 0:
                G.add_edge(chart[i], chart[j], weight=graph[i, j])  # 添加带权边，weight表示边权
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, alpha=0.5)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    if path:
        p = []
        while path:
            p.append(path.pop())
        edgeList = []
        for i in range(len(p) - 1):
            edgeList.append((p[i], p[i + 1]))
        nx.draw_networkx_edges(G, pos, edgelist=edgeList, edge_color='m', width=4)
    plt.show()


# 查询桥接词
def queryBridgeWords(word1, word2, graph, chart):
    if word1 not in chart and word2 not in chart:
        print(f"No \"{word1}\" and \"{word2}\" in the graph!")
        return -1
    elif word1 not in chart:
        print(f"No \"{word1}\" in the graph!")
        return -1
    elif word2 not in chart:
        print(f"No \"{word2}\" in the graph!")
        return -1
    else:
        index1 = chart.index(word1)
        index2 = chart.index(word2)
        edge = []
        for i in range(len(graph[index1])):
            if graph[index1][i] != 0:
                edge.append(i)
        bridge = []
        for e in edge:
            if graph[e][index2] != 0:
                bridge.append(chart[e])
    if len(bridge) == 0:
        print(f"No bridge words from \"{word1}\" to \"{word2}\" !")
        return 0
    elif len(bridge) == 1:
        print(f"The bridge word from \"{word1}\" to \"{word2}\" is: {bridge[0]}")
    else:
        print(f"The bridge words from \"{word1}\" to \"{word2}\" are:", end="")
        for i in range(len(bridge)):
            if i == len(bridge) - 1:
                print(str(bridge[i]))
            else:
                print(str(bridge[i]) + ", ", end="")
    return bridge


# 根据 bridge word 生成新文本
def generateNewText(inputText, graph, chart):
    tempText = inputText.lower()
    tempText = tempText.replace(",", " ").replace(".", " ")
    tempText = tempText.split()
    print(tempText)
    inputText = inputText.replace(",", ", ").replace(".", ". ")
    inputText = inputText.split()
    print(inputText)
    offset = 0  # 偏移量
    tempBridge = []
    for i in range(len(tempText) - 1):
        if tempText[i] in chart and tempText[i + 1] in chart:
            index1 = chart.index(tempText[i])
            index2 = chart.index(tempText[i + 1])
            edge = []
            for j in range(len(graph[index1])):
                if graph[index1][j] != 0:
                    edge.append(j)
            for e in edge:
                if graph[e][index2] != 0:
                    tempBridge.append(chart[e])
        if len(tempBridge) > 0:
            inputText.insert(i + offset + 1, random.choice(tempBridge))
            tempBridge = []
            offset = offset + 1  # 原始文本插入单词的位置偏移量
    # 打印字符串
    for i in range(len(inputText)):
        if i == len(inputText) - 1:
            print(inputText[i], end="")
        else:
            print(inputText[i], end=" ")
    return inputText


# Dijkstra算法
def Dijkstra(graph, chart, word1):
    g = graph.copy()
    lenth = len(chart)
    path = np.array([-1 for i in range(lenth)])
    visit = np.zeros(lenth)
    dis = np.array([float('inf') for i in range(lenth)])
    g[g == 0] = float('inf')
    index1 = chart.index(word1)
    visit[index1] = 1
    for i in range(len(chart)):
        dis[i] = g[index1][i]
        if dis[i] == float('inf'):
            path[i] = -1
        else:
            path[i] = index1
    while True:
        min = float('inf')
        min_index = -1
        for i in range(lenth):
            if visit[i] == 0:
                if min > dis[i]:
                    min = dis[i]
                    min_index = i
        if min_index == -1:
            break
        visit[min_index] = 1
        temp = dis[min_index]
        for i in range(lenth):
            if visit[i] == 0:
                if g[min_index][i] + temp < dis[i]:
                    dis[i] = g[min_index][i] + temp
                    path[i] = min_index
    return path


# 计算最短路径
def calcShortestPath(graph, chart, word1, word2=None):
    path = Dijkstra(graph, chart, word1)
    if word2:
        index = chart.index(word2)
        if path[index] == -1:
            print(f"\"{word2}\" is not reachable!")
        else:
            s = [word2]
            while s[-1] != word1:
                word = s[-1]
                # index =chart.index(word)
                # index = path[index]
                # word = chart[index]
                s.append(chart[path[chart.index(s[-1])]])
                # s.append(word)
            showDirectedGraph(graph, chart, s)
    else:
        for word in chart:
            if word != word1:
                calcShortestPath(graph, chart, word1, word)
    return


# 随机游走
def randomWalk(graph, chart, start_position):
    l = len(chart)
    connect = [[] for _ in range(l)]  # 各个顶点的相邻顶点
    for i in range(l):
        for j in range(l):
            if graph[i][j] > 0:
                connect[i].append(j)
    start = 0  # 游走是否已经开始的标志
    position = -1  # 当前游走位置
    pathway = []  # 当前已走路径
    while(1):
        # command = input("直接输入回车开始/继续游走，输入E/e结束游走：")
        # if command == "E" or command == "e":
        #     print("结束游走！")
        #     break
        # elif command == "":

        if start == 0:
            print("\n开始游走！")
            # position = random.randint(0, l - 1)
            position = start_position
            print(l,position)
            pathway.append(chart[position])
            print(pathway)
            with open("Random_Walk.txt", 'a') as f:
                f.truncate(0)  # 清除 txt 文件内容
                f.write(chart[position]+' ')
            walk = chart[position]
            start = 1
        else:
            # 检验是否有出边
            if len(connect[position]) == 0:
                print("没有出边！")
                walk += "\n" + chart[position] + "没有出边，游走结束"
                break

            print("继续游走！")
            temp = random.choice(connect[position])
            if temp > 0:
                connect[position][connect[position].index(temp)] \
                    = -connect[position][connect[position].index(temp)]  # 置负数表示该边已走过
                position = temp
                pathway.append(chart[position])
                print(pathway)
                with open("Random_Walk.txt", 'a') as f:
                    f.write(chart[position] + ' ')
                walk += ' -> ' + chart[position]
            elif temp == 0:
                connect[position][connect[position].index(temp)] \
                    = -0.5  # 置负数表示该边已走过
                position = temp
                pathway.append(chart[position])
                print(pathway)
                with open("Random_Walk.txt", 'a') as f:
                    f.write(chart[position] + ' ')
                walk += ' -> ' + chart[position]
            else:
                if temp == -0.5:
                    position = 0
                else:
                    position = -temp
                pathway.append(chart[position])
                print(pathway)
                with open("Random_Walk.txt", 'a') as f:
                    f.write(chart[position] + ' ')
                walk += ' -> ' + chart[position]
                print("走到重复边！")
                walk += "\n" + "走到重复边，游走结束"
                break

        # else:
        #     print("非法输入！")
        #     continue
    return walk

if __name__ == "__main__":
    text = readText()
    chart, graph = geneGraph(text)
    # calcShortestPath(graph, chart, "to")
    # intext = input("请输入新文本：")
    # generateNewText(intext, graph, chart)
    randomWalk(graph, chart)

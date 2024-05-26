from string import punctuation
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random


# 读取外部文件
def readText(fileName):
    txt = open(fileName, "r").read()
    txt = txt.lower()
    text = ""
    for char in txt:
        if char in punctuation or char == "\n" or char == " ":
            text = text + " "
        elif 97 <= ord(char) <= 122:
            text = text + char
    text = text.split()
    return text


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
def showDirectedGraph(chart, graph, path=None):
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
        edgeList = []
        for i in range(len(path) - 1):
            edgeList.append((path[i], path[i + 1]))
        nx.draw_networkx_edges(G, pos, edgelist=edgeList, edge_color='m', width=4)
        plt.show()
    else:
        plt.savefig('directedGraph')
    return


# 查询桥接词
def queryBridgeWords(word1, word2, graph, chart):
    if word1 not in chart and word2 not in chart:
        text = 'No ' + word1 + ' and ' + word2 + ' in the graph!'
        return text
    elif word1 not in chart:
        text = 'No ' + word1 + ' in the graph!'
        return text
    elif word2 not in chart:
        text = 'No ' + word2 + ' in the graph!'
        return text
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
        text = 'No bridge words from ' + word1 + ' to ' + word2 + ' !'
        return text
    elif len(bridge) == 1:
        text = 'The bridge word from ' + word1 + ' to ' + word2 + ' is: ' + bridge[0]
        return text
    else:
        text = 'The bridge words from ' + word1 + ' to ' + word2 + ' are:'
        for i in range(len(bridge)):
            if i == len(bridge) - 1:
                text = text + bridge[i]
            else:
                text = text + bridge[i] + ', '
        return text


# 根据bridge word生成新文本
def generateNewText(inputText, graph, chart):
    text = ""
    inputText = inputText.lower()
    for char in inputText:
        if char in punctuation or char == "\n" or char == " ":
            text = text + " "
        elif 97 <= ord(char) <= 122:
            text = text + char
    text = text.split()
    txt = text.copy()
    ind = 0
    for i in range(len(text) - 1):
        if text[i] in chart and text[i + 1] in chart:
            bridge = []
            index1 = chart.index(text[i])
            index2 = chart.index(text[i + 1])
            for j in range(len(graph[index1])):
                if graph[index1][j] != 0 and graph[j][index2] != 0:
                    bridge.append(chart[j])
            if len(bridge) > 0:
                txt.insert(ind, random.choice(bridge))
                ind = ind + 1
        ind = ind + 1

    text = ""
    for i in range(len(txt)):
        if i == len(txt) - 1:
            text = text + txt[i]
        else:
            text = text + txt[i] + " "
    text = text[0].upper() + text[1:len(text)]
    print(text)
    return text


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
    text = ""
    if word2:
        index = chart.index(word2)
        if path[index] == -1:
            text = text + word2 + " is not reachable!\n"
        else:
            s = [word2]
            while s[-1] != word1:
                s.append(chart[path[chart.index(s[-1])]])
            path = []
            while s:
                temp = s.pop()
                path.append(temp)
            sum = 0
            text = text + path[0]
            for i in range(len(path) - 1):
                sum = sum + graph[chart.index(path[i])][chart.index(path[i + 1])]
                text = text + "->" + path[i + 1]
            text = text + " " + "最短长度为：" + str(sum) + "\n"
            showDirectedGraph(chart, graph, path)
    else:
        for word in chart:
            if word != word1:
                text = text + calcShortestPath(graph, chart, word1, word)
    return text


def randomWalk(chart, connect, pathway, text):
    l = len(chart)
    if len(pathway) == 0:
        position = random.randint(0, l - 1)
        pathway.append(chart[position])
        text = str(pathway[0])
    else:
        position = chart.index(pathway[-1])
        if len(connect[position]) == 0:
            text = text + "\n" + str(pathway[-1]) + "没有出边，游走结束"
        else:
            temp = random.choice(connect[position])
            index_temp = connect[position].index(temp)
            if temp > 0:
                connect[position][index_temp] = -connect[position][index_temp]
                word = chart[temp]
                pathway.append(word)
                text = text + " -> " + str(word)
            elif temp == 0:
                connect[position][index_temp] = -0.5
                word = chart[temp]
                pathway.append(word)
                text = text + " -> " + str(word)
            else:
                if temp == -0.5:
                    word = chart[0]
                else:
                    word = chart[-temp]
                pathway.append(word)
                text = text + " -> " + str(word) + "\n走到重复边，游走结束"
    with open("Random_Walk.txt", "w") as f:
        f.write(text)
    return text

import time
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog
import LAB1
from PIL import Image, ImageTk


def graphCheck():
    global graph
    if graph is None:
        messagebox.showwarning('警告', '请先生成有向图')
        return False
    return True


def geneGraphFrame():
    global frame, graph, chart, img
    frame.destroy()
    path = tkinter.filedialog.askopenfilename()
    path = path.replace("/", "\\\\")
    txt = LAB1.readText(path)
    start = time.perf_counter()
    chart, graph = LAB1.geneGraph(txt)
    end = time.perf_counter()
    print("生成有向图时间: %f 秒" % (end - start))
    LAB1.showDirectedGraph(chart, graph)
    img = Image.open('directedGraph.png')
    img = ImageTk.PhotoImage(img)
    frame = tk.Frame(window)
    frame.grid(row=1, column=0, columnspan=100)
    img_label = tk.Label(frame, image=img)
    img_label.grid(row=0, column=0)


def getWords():
    global frame, graph, chart
    word1_ = word1.get()
    word2_ = word2.get()
    if word1_ == "" and word2_ == "":
        text = "please input words!\n"
    elif word1_ not in chart or word2_ not in chart:
        if word1_ not in chart and word2_ in chart:
            text = str(word1_) + " is not in the graph!"
        elif word1_ in chart and word2_ not in chart:
            text = str(word2_) + " is not in the graph!"
        else:
            text = str(word1_) + " and " + str(word2_) + " are not in the graph!"
    else:
        start = time.perf_counter()
        text = LAB1.queryBridgeWords(word1_, word2_, graph, chart)
        end = time.perf_counter()
        print("计算桥接词时间： %f 秒" % (end - start))
    txt = tk.Label(frame, text=text)
    txt.grid(row=3, column=0, columnspan=1000)


def queryBridgeWordsFrame():
    global frame
    frame.destroy()
    if not graphCheck():
        return
    frame = tk.Frame(window)
    frame.grid(row=1, column=0, columnspan=1000)
    e_word1 = tk.Entry(frame, textvariable=word1, width=20)
    e_word2 = tk.Entry(frame, textvariable=word2, width=20)
    l_word1 = tk.Label(frame, text='word1:')
    l_word2 = tk.Label(frame, text='word2:')
    b_getWords = tk.Button(frame, text='确定', command=getWords)
    l_word1.grid(row=0, column=0)
    l_word2.grid(row=1, column=0)
    e_word1.grid(row=0, column=1)
    e_word2.grid(row=1, column=1)
    b_getWords.grid(row=2, column=0, columnspan=2)


def gene():
    global frame, graph, chart
    newTxt = newText.get()
    if len(newTxt) == 0:
        newTxt = "please input text!"
    else:
        start = time.perf_counter()
        newTxt = LAB1.generateNewText(newTxt, graph, chart)
        end = time.perf_counter()
        print("生成新文本时间： %f 秒" % (end - start))
    l_newTxt = tk.Label(frame, text=newTxt)
    l_newTxt.grid(row=2, column=0)


def geneNewTextFrame():
    global frame, graph, chart
    frame.destroy()
    if not graphCheck():
        return
    frame = tk.Frame(window)
    frame.grid(row=1, column=0, columnspan=1000)
    l_newText = tk.Label(frame, text='输入文本：')
    e_newText = tk.Entry(frame, textvariable=newText, width=30)
    b_geneNewTxt = tk.Button(frame, text='确定', command=gene)
    l_newText.grid(row=0, column=0)
    e_newText.grid(row=0, column=1)
    b_geneNewTxt.grid(row=1, column=0, columnspan=2)


def calShortestPathFrame():
    global frame, graph, chart
    word1_ = word1.get()
    word2_ = word2.get()
    if word1_ == "" and word2_ == "":
        text = "please input words!"
    elif word2_ == "" and word1_ not in chart:
        text = str(word1_) + " is not in the graph!"
    elif word1_ not in chart or word2_ not in chart:
        if word1_ == "":
            text = "please input word1!"
        elif word1_ not in chart and word2_ in chart:
            text = str(word1_) + " is not in the graph!"
        elif word1_ in chart and word2_ not in chart:
            text = str(word2_) + " is not in the graph!"
        else:
            text = str(word1_) + " and " + str(word2_) + " are not in the graph!"
    else:
        start = time.perf_counter()
        text = LAB1.calcShortestPath(graph, chart, word1_, word2_)
        end = time.perf_counter()
        print("计算最短路径时间：%f 秒" % (end - start))
    l_text = tk.Label(frame, text=text)
    l_text.grid(row=3, column=0, columnspan=1000)


def shortestPath():
    global frame, graph, chart
    frame.destroy()
    if not graphCheck():
        return
    frame = tk.Frame(window)
    frame.grid(row=1, column=0, columnspan=1000)
    e_word1 = tk.Entry(frame, textvariable=word1, width=20)
    e_word2 = tk.Entry(frame, textvariable=word2, width=20)
    l_word1 = tk.Label(frame, text='word1:')
    l_word2 = tk.Label(frame, text='word2:')
    b_getWords = tk.Button(frame, text='确定', command=calShortestPathFrame)
    l_word1.grid(row=0, column=0)
    l_word2.grid(row=1, column=0)
    e_word1.grid(row=0, column=1)
    e_word2.grid(row=1, column=1)
    b_getWords.grid(row=2, column=0, columnspan=2)


def updateWalkPath(text, connect, pathway, tim):
    global flag, chart
    start = time.perf_counter()
    if flag:
        text = LAB1.randomWalk(chart, connect, pathway, text)
        walkPath.set(text)
        if text[-1] == '束':
            flag = False
            end = time.perf_counter()
            tim = tim + end - start
            print("随机游走时间： %f 秒" % tim)
    end = time.perf_counter()
    tim = tim + end - start
    window.after(1000, updateWalkPath, text, connect, pathway, tim)


def randomWalk():
    global graph, chart, flag
    flag = True
    walkPath.set("")
    tim = 0.0
    start = time.perf_counter()
    text = ""
    pathway = []
    l = len(chart)
    connect = [[] for _ in range(l)]
    for i in range(l):
        for j in range(l):
            if graph[i][j] > 0:
                connect[i].append(j)
    end = time.perf_counter()
    tim = tim + end - start
    window.after(1000, updateWalkPath, text, connect, pathway, tim)


def stopWalk():
    global flag
    flag = False


def continueWalk():
    global flag
    flag = True


def randomWalkFrame():
    global frame
    frame.destroy()
    if not graphCheck():
        return
    frame = tk.Frame(window)
    frame.grid(row=1, column=0, columnspan=1000)
    ba = tk.Button(frame, text='开始', command=randomWalk)
    bb = tk.Button(frame, text='停止', command=stopWalk)
    bc = tk.Button(frame, text='继续', command=continueWalk)
    l_walk = tk.Label(frame, textvariable=walkPath)
    l_walk.grid(row=1, column=0, columnspan=1000)
    ba.grid(row=0, column=0)
    bb.grid(row=0, column=1)
    bc.grid(row=0, column=2)


if __name__ == "__main__":
    window = tk.Tk()
    window.title('LAB1')
    window.geometry('640x540')

    graph = None
    chart = None
    img = None
    flag = True
    frame = tk.Frame()
    word1 = tk.StringVar()
    word2 = tk.StringVar()
    newText = tk.StringVar()
    walkPath = tk.StringVar()

    b1 = tk.Button(window, text='生成有向图', command=geneGraphFrame)
    b1.grid(row=0, column=0)
    b2 = tk.Button(window, text='查询桥接词', command=queryBridgeWordsFrame)
    b2.grid(row=0, column=1)
    b3 = tk.Button(window, text='生成新文本', command=geneNewTextFrame)
    b3.grid(row=0, column=2)
    b4 = tk.Button(window, text='最短距离', command=shortestPath)
    b4.grid(row=0, column=3)
    b5 = tk.Button(window, text='随机游走', command=randomWalkFrame)
    b5.grid(row=0, column=4)
    window.mainloop()

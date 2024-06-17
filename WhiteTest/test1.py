import unittest
from LAB1 import *

class MyTestCase(unittest.TestCase):
    def test2(self):
        text = readText("test2")
        self.chart, self.graph = geneGraph(text)
        self.assertEqual(randomWalk(self.graph, self.chart, start_position=1), "test" + "\n" + "test没有出边，游走结束")

    def test3(self):
        text = readText("test3")
        self.chart, self.graph = geneGraph(text)
        self.assertEqual(randomWalk(self.graph, self.chart, start_position=1), "a -> test" + "\n" + "test没有出边，游走结束")

    def test4(self):
        text = readText("test4")
        self.chart, self.graph = geneGraph(text)
        self.assertEqual(randomWalk(self.graph, self.chart, start_position=0), "start -> test" + "\n" + "test没有出边，游走结束")

    def test5(self):
        text = readText("test5")
        self.chart, self.graph = geneGraph(text)
        self.assertEqual(randomWalk(self.graph, self.chart, start_position=0), "start -> test -> start -> test" + "\n" + "走到重复边，游走结束")

    # def test1(self):
    #     self.assertEqual(queryBridgeWords("that", "marches", self.graph, self.chart),
    #                      "The bridge word from that to marches is: time")

if __name__ == "__main__":
    unittest.main()

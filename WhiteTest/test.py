import unittest
from LAB1 import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        text = readText("test.txt")
        self.chart, self.graph = geneGraph(text)

    def test1(self):
        self.assertEqual(queryBridgeWords("that", "marches", self.graph, self.chart),
                         "The bridge word from that to marches is: time")

    def test2(self):
        self.assertEqual(queryBridgeWords("that", "", self.graph, self.chart), "No  in the graph!")

    def test3(self):
        self.assertEqual(queryBridgeWords("that", "pilot", self.graph, self.chart), "No pilot in the graph!")

    def test4(self):
        self.assertEqual(queryBridgeWords("", "marches", self.graph, self.chart), "No  in the graph!")

    def test5(self):
        self.assertEqual(queryBridgeWords("pilot", "marches", self.graph, self.chart), "No pilot in the graph!")

    def test6(self):
        self.assertEqual(queryBridgeWords("of", "moments", self.graph, self.chart),
                         "No bridge words from of to moments !")

    def test7(self):
        self.assertEqual(queryBridgeWords("", "", self.graph, self.chart), "No  and  in the graph!")

    def test8(self):
        self.assertEqual(queryBridgeWords("pilot", "plane", self.graph, self.chart), "No pilot and plane in the graph!")


if __name__ == "__main__":
    unittest.main()

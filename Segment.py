#!/usr/bin/python
#encoding:utf8
"""
@author:yizhong.wyz
@date: 2018-03-16
@desc: 基于三叉搜索树的中文分词
"""

from TernarySearchTrie import TernarySearchTrie
from TernarySearchTrie import getTreeHeight
from TernarySearchTrie import outputBalancedDict
from TernarySearchTrie import buildMatrix
from TernarySearchTrie import TSNode
from TernarySearchTrie import preOrderTraves
from TernarySearchTrie import printMatrix
from TernarySearchTrie import sortDict


class Segment(object):
    def __init__(self, root, text):
        self.tst = root
        ##当前切分位置
        self.offset = 0
        self.text = text

    def splitWordWithMaxMatch(self):
        """
        搜索三叉树并每次返回最长匹配串
        """
        word = ""
        if self.text == "" or self.tst is None:
            return word
        if self.offset >= len(self.text):
            return word
        charIndex = self.offset
        currentNode = self.tst
        while 1:
            if currentNode is None:
                if word == "":
                    word = self.text[self.offset+1]
                    self.offset += 1
                return word
            cmpRes = cmp(self.text[charIndex], currentNode.splitchar)    
            if cmpRes == 0:
                charIndex += 1
                if currentNode.nodeValue != "":
                    word = currentNode.nodeValue
                    self.offset = charIndex
                if charIndex == len(self.text):
                    return word
                currentNode = currentNode.eqNode
            elif cmpRes < 0:
                currentNode = currentNode.loNode
            else:
                currentNode = currentNode.hiNode        


def buildTrie():
    a = [u"大", u"大学", u"大学生", u"活动", u"生活", u"中", u"中心", u"心"]
    b = sortDict(a)
    outputDict = []
    outputBalancedDict(outputDict, b, 0, len(b))
    root = TSNode(outputDict[0][0])
    tst = TernarySearchTrie(root)
    for word in outputDict:
        node = tst.addWord(word)
        node.nodeValue = word
    return root
    """
    height = getTreeHeight(root)
    matrix = buildMatrix(height)
    layer = 1
    preOrderTraves(root, height, layer, -1, [0, 0], matrix)
    printMatrix(matrix)
    """
    

def testSegment():
    root = buildTrie()
    seg = Segment(root, u"大学生活动中心")
    word = ""
    while 1:
        word = seg.splitWordWithMaxMatch()
        if word == "":
            break
        print "%s/" % word,

if __name__ == "__main__":
    testSegment()
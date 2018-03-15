#!/usr/bin/python
#encoding:utf8
"""
@author: yizhong.wyz
@date: 2018-03-14
@desc: 三叉搜索树实现
"""
import sys
import json

saveStdout = sys.stdout

class TSNode(object):
    def __init__(self, splitchar):
        #左边、中间和右边节点
        self.loNode = None
        self.eqNode = None
        self.hiNode = None
        #保存的字符
        self.splitchar = splitchar
        #终止节点保存word
        self.nodeValue = ""

    def toString(self):
        return self.splitchar


class TernarySearchTrie(object):
    def __init__(self, root):
        self.root = root

    def getNode(self, key, startNode):
        """
        查找词key
        """
        if key == "" or key is None:
            return None
        length = len(key)
        if length == 0:
            return None
        currentNode = startNode
        charIndex = 0
        cmpChar = key[charIndex]
        cmpRes = -1
        while 1:
            if currentNode is None:
                return None
            cmpRes = cmp(cmpChar, currentNode.splitchar)
            if cmpRes == 0:
                ####两个字符相等
                charIndex += 1
                if charIndex == length:
                    return currentNode
                else:
                    cmpChar = key[charIndex]
                currentNode = currentNode.eqNode
            elif cmpRes < 0:
                currentNode = currentNode.loNode
            else:
                currentNode = currentNode.hiNode

    def addWord(self, key):
        currentNode = self.root
        charIndex = 0
        cmpRes = -1
        while 1:
            cmpRes = cmp(key[charIndex], currentNode.splitchar)
            if cmpRes == 0:
                charIndex += 1
                if charIndex == len(key):
                    return currentNode
                if currentNode.eqNode is None:
                    currentNode.eqNode = TSNode(key[charIndex])
                currentNode = currentNode.eqNode
            elif cmpRes < 0:
                if currentNode.loNode is None:
                    currentNode.loNode = TSNode(key[charIndex])
                currentNode = currentNode.loNode
            else:
                if currentNode.hiNode is None:
                    currentNode.hiNode = TSNode(key[charIndex])
                currentNode = currentNode.hiNode


def printMatrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == "0":
                #matrix[row][col] = ""
                print "%2s" % " ",
                continue
            print "%2s" % matrix[row][col].encode("utf8"),
        #print "".join(matrix[row])
        print "\n",


def buildMatrix(height):
    rows = 2 * height -1
    cols = 2 * (3**(height-1)) -1
    matrix = [["0"] * cols for i in range(rows)]
    return matrix


def getTreeHeight(root):
    """
    获得树的高度
    """
    if root is None:
        return 0
    return max(getTreeHeight(root.loNode), getTreeHeight(root.eqNode), getTreeHeight(root.hiNode)) + 1


def preOrderTraves(root, height=0, layer=1, flag=0, lastPos=[], matrix=[]):
    """
    前序遍历
    左，中， 右顺序
    @height: 树的高度
    @layer: 当前节点所处的层次
    @flag: 标记当前节点
    @lastPos: (i, j) 上一个位置
    """
    i,j = -1, -1
    if root is not None:
        if layer == 1:
            j = (2 * (3**(height-1)) -1) / 2
            i = 0
        else:
            i, j = lastPos[0], lastPos[1]
            if flag == 0:
                i += 1
                j -= 1 
            elif flag == 1:
                i += 1
            else:
                i += 1
                j += 1
        matrix[i][j] = root.splitchar
    else:
        return
    if root.loNode is not None:
        matrix[i+1][j-1] = "/"
        preOrderTraves(root.loNode, height, layer + 1, 0, [i+1, j-1], matrix)
    if root.eqNode is not None:
        matrix[i+1][j] = "|"
        preOrderTraves(root.eqNode, height, layer + 1, 1, [i+1, j], matrix)
    if root.hiNode is not None:
        matrix[i+1][j+1] = "\\"
        preOrderTraves(root.hiNode, height, layer + 1, 2, [i+1, j+1], matrix)


def outputBalancedDict(outputDict, sort_dict, offset, length):
    if length < 1:
        return 
    mid = length / 2
    outputDict.append(sort_dict[mid + offset])
    outputBalancedDict(outputDict, sort_dict, offset, mid)
    outputBalancedDict(outputDict, sort_dict, offset + mid + 1, length - mid -1)


def sortDict(rawDict):
    """
    中文排序
    """
    import locale
    return sorted(rawDict, cmp=locale.strcoll)

save_file = open("tire.txt", "w+")
sys.stdout = save_file
#a = [u"大学生", u"中心", u"活动", u"大学", u"生活"]
a = [u"大", u"大学", u"大学生", u"活动", u"生活", u"中", u"中心", u"心"]
#a = [u"大学生", u"生活"]
print "before sorted:",json.dumps(a)
b = sortDict(a)
print "after sorted:",json.dumps(b)
#a = [u"大学生", u"生活"]
outputDict = []
outputBalancedDict(outputDict, b, 0, len(b))
print "after balance adjust:",json.dumps(outputDict)

root = TSNode(outputDict[0][0])
tst = TernarySearchTrie(root)

for word in outputDict:
    node = tst.addWord(word)
    node.nodeValue = word

height = getTreeHeight(root)
matrix = buildMatrix(height)

layer = 1
preOrderTraves(root, height, layer, -1, [0, 0], matrix)

printMatrix(matrix)
node = tst.getNode(u"大学生", root)
if node:
    print "yes"
sys.stdout = saveStdout
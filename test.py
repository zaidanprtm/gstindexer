from anytree import *
import pymysql.cursors
import re


def connectDB():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='crawler',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(
                "SELECT id_pagecontent, title FROM page_information LIMIT 10")
            result = cursor.fetchall()
            # print(result)
        for data in result:
            # print(data)
            data["title"] = data["title"].lower()
            data["title"] = re.sub(
                r'\?|\.|\!|\/|\;|\:|\-', "", data["title"])
            print(data)
        return result


def nodeToString(node):
    node = str(node)
    delimiter = ","
    index = node.index(delimiter)
    node = node[:index]
    # remove 12 first character on node
    node = node[12:]
    size = len(node)
    node = node[:size-2]
    node = node.replace("/", "")
    return node


# compare string adalah fungsi untuk membandingkan 2 string apakah memiliki substring yang sama
def compare_strings(a, b):
    # a itu node, b itu sufiks yang mau ditambah
    if a is None or b is None:  # jika salah satu dari 2 string adalah none maka return False
        return False
    # if b in a:
    #     a = a.replace(b, "")
    size = min(len(a), len(b))
    # inisiasi status awal di mana defaultnya false dan tidak ada string yang sama
    status = False
    sameString = ""
    sufCut = ""
    parentNameCut = ""
    i = 0

    while i < size and a[i] == b[i]:
        # while a[i] == b[i]:
        status = True
        sameString += a[i]
        parentNameCut = a.removeprefix(sameString)
        sufCut = b.removeprefix(sameString)
        i += 1
    return status, sameString, parentNameCut, sufCut


data = [
    {
        "id_pagecontent": 1,
        "title": "cata"
    },
    {
        "id_pagecontent": 2,
        "title": "actttt"
    },
    {
        "id_pagecontent": 3,
        "title": "hatt"
    },
]


def addChild(suf, parent, tree, index):
    # for pre, fill, node in RenderTree(tree):
    #     print("%s%s" % (pre, node.name))
    result = findall_by_attr(tree, parent, maxlevel=2)
    try:
        # Try to return the first found node and stop the search
        result = result[0]
        # print(node.name)
    except StopIteration:
        # Handle the case where there are no matching nodes
        print("No matching nodes found")
    # print("res", result)
    # print("tree, ", tree)
    # print("parent, ", parent)
    children = result.children
    for child in children:
        # print("+++++++++++++++++++++++++++++++++++++++++++++=")
        # print("suf: ", suf)
        # print("node: ", child.name)
        status, sameString, parentNameCut, sufCut = compare_strings(
            child.name, suf)
        if status == False:
            # print("cek next node")
            continue
        if parentNameCut == "":
            # print("normal")
            if sufCut == "":
                # print(child)
                # print("node index =", type(child.index))
                # print("index saat ini: ", index)
                if index not in child.index:
                    child.index.append(index)
                return tree
            return addChild(suf=sufCut, parent=child.name, tree=child, index=index)
        child.name = sameString
        if child.children == []:
            # print("gaada anak")
            Node(sufCut, parent=child, index=[index])
            Node(parentNameCut, parent=child, index=child.index)
            return tree
        # if child.children != []:
        # print("ada anak")
        # print("anak siapa: ", child.name)
        nodeParentCut = Node(parentNameCut, index=child.index)
        nodeParentCut.children = child.children
        # print("-------------------------------------------")
        # for pre, fill, node in RenderTree(nodeParentCut):
        #     print("%s%s" % (pre, node.name))
        # print("-------------------------------------------")
        nodeParentCut.parent = child
        Node(sufCut, parent=child, index=[index])
        return tree
    Node(suf, parent=result, index=[index])
    return tree


def makeTree2(data):
    root = Node("root")
    for title in data:
        for word in title["title"].split():
            wordIndex = title["id_pagecontent"]
            word += "$"
            for i in range(len(word)):
                suf = word[i:]
                addChild(suf=suf, parent="root", tree=root, index=wordIndex)
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.name))
            # print(RenderTree(root))
    return root


def searchTree(root, arrWord):
    traverse = []
    traverseResult = []
    for word in arrWord.split():
        word = word.lower()
        result = []
        tree = root
        word += "$"
        for i in range(len(word)):
            char = word[i]
            find = search_char_in_tree(tree, char)
            if find:
                tree = find
                traverse.append(find)
                result.append(find)
        traverseResult.append(result[-1])
    return traverse, traverseResult, tree


def search_char_in_tree(node, char):
    for child in node.children:
        name = child.name
        if name == char or name[0] == char:
            return child
    return False


def searchWithFrequency(tree, p, f):
    traverse = []
    traverseResult = []
    word = p.lower()
    result = []
    tree = tree
    for i in range(len(word)):
        char = word[i]
        find = search_char_in_tree(tree, char)
        if find:
            tree = find
            traverse.append(find)
            result.append(find)
    traverseResult.append(result[-1])
    # print(traverse)
    # for node in traverseResult:
    #     print(node)
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))
    print(RenderTree(tree))
    sameAmount = 0
    allListDocument = []
    for node in PostOrderIter(tree):
        if "$" not in node.name:
            continue
        print(node)
        allListDocument.append(node.index)
    print(allListDocument)
    listCount = []
    for listDocument in allListDocument:
        for idx in listDocument:
            print("-------")
            print(listCount)
            status, sameIdx = checkList(idx, listCount)
            if len(listCount) > 0 and status == True:
                listCount[sameIdx]["count"] += 1
                continue
            obj = {
                "index": idx,
                "count": 1
            }
            listCount.append(obj)
    print(listCount)
    for indexCount in listCount:
        if indexCount["count"] >= f:
            sameAmount += 1
    print(sameAmount)
    tree.count = sameAmount
    print(RenderTree(tree))


def checkList(index, arr):
    for i in range(len(arr)):
        if arr[i]["index"] == index:
            return True, i
    return False, 0


def rankResult(result):
    print(result)
    allListDocument = []
    for node in result:
        allListDocument.append(node.index)
    print(allListDocument)
    listCount = []
    for listDocument in allListDocument:
        for idx in listDocument:
            status, sameIdx = checkList(idx, listCount)
            if len(listCount) > 0 and status == True:
                listCount[sameIdx]["count"] += 1
                continue
            obj = {
                "index": idx,
                "count": 1
            }
            listCount.append(obj)
    rankedList = sorted(listCount, key=lambda d: d['count'], reverse=True)
    return rankedList


gst = makeTree2(connectDB())
kata = input("masukkan kata yang ingin dicari: ")
# frekuensi = int(input("masukkan frekuensi yang ingin dicari: "))
# searchWithFrequency(gst, kata, frekuensi)
traverse, traverseResult, resultTree = searchTree(gst, kata)
connectDB()
print(rankResult(traverseResult))
# print(traverse)
# for node in traverseResult:
#     print(node)
# print(traverseResult)
# connectDB()
# print(gst)


# def makeTree(arrayInput):
#     root = Node("root")
#     for word in arrayInput:
#         word += "$"
#         for i in range(len(word)):
#             # children = root.children
#             # print(children)
#             addSuf = False
#             suf = word[i:]
#             # print(suf)
#             for node in LevelOrderIter(root, maxlevel=2):
#                 name = str(node.name)
#                 # print(name)
#                 if name != "root" and name != "$":
#                     status, sameString, parentNameCut, sufCut = compare_strings(
#                         name, suf)
#                     # print(status)
#                     if status == True:
#                         print("suf: ", suf)
#                         print("node yang sama: ", node.name)
#                         print("ortunya: ", node.parent.name)
#                         print("anaknya: ", node.children)
#                         if node.children == []:
#                             print("anak kosong")
#                             if node.parent != root:
#                                 # print("ini")
#                                 break
#                             # else:
#                             # print("suf: ", suf)
#                             # print("edge: ", node.name)
#                             node.name = sameString
#                             pastSuffix = name.removeprefix(sameString)
#                             suf = suf.removeprefix(sameString)
#                             if suf != "":
#                                 Node(suf, parent=node)
#                             if pastSuffix != "":
#                                 Node(pastSuffix, parent=node)
#                             addSuf = True
#                         if node.children != []:
#                             print("ada anak")
#                             if node.parent != root:
#                                 break
#                             # else:
#                             # print(suf)
#                             # print("edge: ", node.name)
#                             node.name = sameString
#                             if name.removeprefix(sameString) != "":
#                                 pastSuffix = Node(
#                                     name.removeprefix(sameString))
#                                 pastSuffix.children = node.children
#                                 suf = suf.removeprefix(sameString)
#                                 if suf != "":
#                                     pastSuffix.parent = node
#                                     Node(suf, parent=node)
#                                 addSuf = True
#                             else:
#                                 suf = suf.removeprefix(sameString)
#                                 if suf != "":
#                                     Node(suf, parent=node)
#                                 addSuf = True
#                     # elif status == False and suf in children:
#                     #     break
#                     # else:
#                     #     Node(suf, parent=root)
#             if addSuf == False:
#                 Node(suf, parent=root)
#             for pre, fill, node in RenderTree(root):
#                 print("%s%s" % (pre, node.name))
#     # print(children)


# print(children)
# print(suf)
# suftree.append(suf)
# print(node)
# print(list(root.children))
# print(suftree)

# print(RenderTree(root))
# print(compare_strings("g", "g$"))
# for pre, fill, node in RenderTree(root):
# print("%s%s" % (pre, node.name))

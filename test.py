from anytree import *
import pymysql.cursors
import re
import pickle


def updateTitle():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='crawl2',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_page, title FROM page_information")
            result = cursor.fetchall()
        for data in result:
            id_page = data["id_page"]
            data["title"] = data["title"].lower()
            data["title"] = re.sub('[^A-Za-z0-9 ]+', "", data["title"])
            title = data["title"]
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE page_information set title = %s where id_page = %s", (title, id_page))
        return result


def getResult(result):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='crawl2',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    with connection:
        for page in result:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_page, title, url FROM page_information WHERE id_page = %s", (page["index"]))
                data = cursor.fetchall()
                print("query: " + page["query"])
                print(str(result.index(page)+1) + ". " + data[0]["title"])
                print(data[0]["url"])
                print("\n")


def getPage():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='crawl2',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_page, title FROM page_information")
            result = cursor.fetchall()
            # for data in result:
            #     print(data)
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


def makeTree(data):
    root = Node("root")
    for title in data:
        for word in title["title"].split():
            wordIndex = title["id_page"]
            word += "$"
            for i in range(len(word)):
                suf = word[i:]
                addChild(suf=suf, parent="root", tree=root, index=wordIndex)
            # for pre, fill, node in RenderTree(root):
            #     print("%s%s" % (pre, node.name))
            # print(RenderTree(root))
    return root


def updateTree(tree, data):
    root = tree
    for title in data:
        for word in title["title"].split():
            wordIndex = title["id_page"]
            word += "$"
            for i in range(len(word)):
                suf = word[i:]
                addChild(suf=suf, parent="root", tree=root, index=wordIndex)
            # for pre, fill, node in RenderTree(root):
            #     print("%s%s" % (pre, node.name))
            # print(RenderTree(root))
    return root


def searchTree(root, arrWord):
    traverse = []
    searchResult = []
    for word in arrWord.split():
        word = word.lower()
        dictResult = {
            "query": word,
            "result": ""
        }
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
        dictResult["result"] = result[-1]
        searchResult.append(dictResult)
    return traverse, searchResult


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
    # print(result)
    allListDocument = []
    listCount = []
    for i in result:
        allListDocument.append(i["result"].index)
    # print(allListDocument)
    for i in range(len(allListDocument)):
        for idx in allListDocument[i]:
            status, sameIdx = checkList(idx, listCount)
            if len(listCount) > 0 and status == True:
                listCount[sameIdx]["count"] += 1
                listCount[sameIdx]["query"] += " " + result[i]["query"]
                continue
            obj = {
                "index": idx,
                "count": 1,
                "query": result[i]["query"]
            }
            listCount.append(obj)
    rankedList = sorted(listCount, key=lambda d: d['count'], reverse=True)
    # print(rankedList)
    return rankedList


def storeData(tree):
    # initializing data to be stored in file

    # Its important to use binary mode
    dbfile = open('gst', 'ab')

    # source, destination
    pickle.dump(tree, dbfile)
    dbfile.close()


def loadData():
    # for reading also binary mode is important
    dbfile = open('gst', 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    # print(RenderTree(db))
    return db


def updateData(newgst):
    with open('gst', 'rb') as file:
        gst = pickle.load(file)
        file.close()
    gst = newgst
    with open('gst', 'wb') as file:
        pickle.dumps(gst, file)
        file.close()


data = [
    {
        "id_page": 1,
        "title": "cata"
    },
    {
        "id_page": 2,
        "title": "actttt"
    },
    {
        "id_page": 3,
        "title": "hatt"
    },
]


def main():
    read = loadData()
    getPage()
    kata = input("masukkan kata yang ingin dicari: ")
    if (kata == ""):
        print("Query tidak boleh kosong")
        main()
    traverse, traverseResult = searchTree(read, kata)
    rankedResult = rankResult(traverseResult)
    # print(rankedResult)
    print("Hasil pencarian: \n")
    getResult(rankedResult)


gst = makeTree(getPage())
store = storeData(gst)
main()
# getPage()
# updateTitle()
# newgst = updateTree(gst, connectDB())
# updateData(newgst)
# loadData()
# frekuensi = int(input("masukkan frekuensi yang ingin dicari: "))
# searchWithFrequency(gst, kata, frekuensi)
# print(traverse)
# for node in traverseResult:
#     print(node)
# print(traverseResult)
# connectDB()
# print(gst)

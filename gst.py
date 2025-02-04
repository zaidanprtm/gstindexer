from anytree import *
import pymysql.cursors
import re
import pickle
import time


def getTitle():
    # Connect ke title database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='crawl3',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_page, title FROM page_information LIMIT 5")
            result = cursor.fetchall()
        for data in result:
            print(data)
        for data in result:
            # menjadikan title lower case untuk dimasukkan ke tree
            data["title"] = data["title"].lower()
            # cleaning title dari simbol untuk input tree
            data["title"] = re.sub('[^A-Za-z0-9 ]+', " ", data["title"])
            print(data)
        return result


def getResult(result):
    # connect ke database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='crawl3',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    with connection:
        for i in range(5):
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_page, title, url FROM page_information WHERE id_page = %s", (result[i]["index"]))
            data = cursor.fetchall()
            # tampilkan data ke terminal
            print("query: " + result[i]["query"])
            print("count: " + str(result[i]["count"]))
            print(str(i+1) + ". " + data[0]["title"])
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


# compare string adalah fungsi untuk membandingkan 2 string apakah memiliki substring yang sama
def compare_strings(a, b):
    # a itu node, b itu sufiks yang mau ditambah
    if a is None or b is None:  # jika salah satu dari 2 string adalah none maka return False
        return False
    size = min(len(a), len(b))
    # inisiasi status awal di mana defaultnya false dan tidak ada string yang sama
    status = False
    sameString = ""
    sufCut = ""
    parentNameCut = ""
    i = 0

    while i < size and a[i] == b[i]:  # membandingkan node dengan sufiks
        status = True
        sameString += a[i]
        parentNameCut = a.removeprefix(sameString)
        sufCut = b.removeprefix(sameString)
        i += 1
    # mengembalikan status perbandingan, string yang sama, node yang telah dipotong, dan sufiks yang telah dipotong
    return status, sameString, parentNameCut, sufCut

# addChild adalah fungsi untuk menambah anak pada tree atau membentuk GST


def addChild(suf, parent, tree, index):
    # mencari apakah sudah ada node tersebut di dalam tree
    result = findall_by_attr(tree, parent, maxlevel=2)
    try:
        # mengembalikan node yang ditemukan
        result = result[0]
    except StopIteration:
        # jika tidak ada node yang ditemukan
        print("No matching nodes found")
    children = result.children
    # proses add sufiks pada tree
    for child in children:
        # membandingkan sufiks yang ingin ditambah dengan node yang sudah ada apakah ada substring yang sama
        status, sameString, parentNameCut, sufCut = compare_strings(
            child.name, suf)
        # jika tidak sama maka lanjut untuk dilakukan perbandingan dengan node selanjutnya
        if status == False:
            continue
        # jika sudah ada substring yang sama maka akan dicek apakah sufiks sudah ada atau belum pada tree
        if parentNameCut == "":
            # jika sufiks sudah ada maka tinggal tambahkan id title di indeks sufiks
            if sufCut == "":
                if index not in child.index:
                    child.index.append(index)
                return tree
            return addChild(suf=sufCut, parent=child.name, tree=child, index=index)
        # jika sudah ada substring yang sama dan sufiksnya belum ada maka akan dicek apakah substring yang sudah ada memiliki anak atau tidak
        child.name = sameString
        # jika substring yang sama tidak memiliki anak maka tinggal menambahkan sufiks yang belum ada menjadi anak dari substring yang sudah ada
        if child.children == []:
            Node(sufCut, parent=child, index=[index])
            Node(parentNameCut, parent=child, index=child.index)
            return tree
        # jika substring yang sama memiliki anak maka anak dari substring yang lama nya harus dipisahkan dengan sufiks yang akan ditambahkan
        nodeParentCut = Node(parentNameCut, index=child.index)
        nodeParentCut.children = child.children
        nodeParentCut.parent = child
        Node(sufCut, parent=child, index=[index])
        return tree
    # penambahan sufiks pada tree jika belum ada di tree
    Node(suf, parent=result, index=[index])
    return tree


def makeTree(data):
    # inisiasi root
    root = Node("root")
    for title in data:
        # pemisahan setiap kata pada title untuk diproses
        for word in title["title"].split():
            wordIndex = title["id_page"]
            # penambahan terminal node untuk pembentukan GST
            word += "$"
            # proses memasukkan tiap sufiks dari kata pada title
            for i in range(len(word)):
                suf = word[i:]
                addChild(suf=suf, parent="root", tree=root, index=wordIndex)
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
    # menyiapkan variabel untuk hasil pencarian dan node mana saja yang sudah dilalui
    traverse = []
    searchResult = []
    # proses pencarian tiap kata dari kalimat yang ingin dicari
    for word in arrWord.split():
        word = word.lower()
        # variabel untuk hasil pencarian yang dihubungkan dengan query atau kata yang dicari
        dictResult = {
            "query": word,
            "result": ""
        }
        result = []
        tree = root
        word += "$"
        # melakukan pencarian dengan mencari dari huruf pertama di tree
        for i in range(len(word)):
            char = word[i]
            find = search_char_in_tree(tree, char)
            # jika huruf yang dicari ketemu di tree maka lanjutkan pencarian dengan huruf selanjutnya di node tersebut
            if find:
                tree = find
                traverse.append(find)
                result.append(find)
        # mengembalikan hasil pencarian dari query yang dicari
        dictResult["result"] = result[-1]
        searchResult.append(dictResult)
    return traverse, searchResult

# fungsi untuk mencari sebuah karakter huruf pada tree


def search_char_in_tree(node, char):
    # pencarian huruf pada anak dari tree
    for child in node.children:
        name = child.name
        # jika ada yang sama maka kembalikan node tersebut
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

# fungsi untuk check apakah kata muncul


def checkList(index, arr):
    for i in range(len(arr)):
        if arr[i]["index"] == index:
            return True, i
    return False, 0


def rankResult(result):
    # inisiasi variabel untuk menyimpan index dari hasil pencarian untuk dihitung
    allListDocument = []
    listCount = []
    for i in result:
        allListDocument.append(i["result"].index)
    # hitung nilai count untuk setiap indeks
    for i in range(len(allListDocument)):
        for idx in allListDocument[i]:
            # cek apakah setiap kata memiliki indeks yang sama
            status, sameIdx = checkList(idx, listCount)
            # jika ada indeks yang sama maka tambahkan nilai count
            if len(listCount) > 0 and status == True:
                listCount[sameIdx]["count"] += 1
                listCount[sameIdx]["query"] += " " + result[i]["query"]
                continue
            # variabel hasil penghitungan count untuk setiap indeks hasil pencarian
            obj = {
                "index": idx,
                "count": 1,
                "query": result[i]["query"]
            }
            listCount.append(obj)
    # urutkan indeks dari jumlah count terbesar sehingga dokumen pertama adalah yang paling relevan
    rankedList = sorted(listCount, key=lambda d: d['count'], reverse=True)
    return rankedList


def storeData(tree):
    # Membuat file bernama gst
    dbfile = open('gst', 'ab')

    # mengisi file gst dengan tree yang sudah jadi
    pickle.dump(tree, dbfile)
    # menutup file setelah diisi
    dbfile.close()


def loadData():
    # membuka file bernama gst
    dbfile = open('gst', 'rb')
    # load data tree yang berada di dalam file
    db = pickle.load(dbfile)
    dbfile.close()
    return db


def main():
    # getTitle()
    # gst = makeTree(getTitle())
    # store = storeData(gst)
    read = loadData()
    kata = input("masukkan kata yang ingin dicari: ")
    start = time.perf_counter()
    if (kata == ""):
        print("Query tidak boleh kosong")
        main()
    traverse, searchResult = searchTree(read, kata)
    rankedResult = rankResult(searchResult)
    done = time.perf_counter()
    print(f"Waktu pencarian: {done - start:0.4f} detik")
    print("Hasil pencarian: \n")
    getResult(rankedResult)


main()

# def nodeToString(node):
#     node = str(node)
#     delimiter = ","
#     index = node.index(delimiter)
#     node = node[:index]
#     # remove 12 first character on node
#     node = node[12:]
#     size = len(node)
#     node = node[:size-2]
#     node = node.replace("/", "")
#     return node


# def updateData(newgst):
#     with open('gst', 'rb') as file:
#         gst = pickle.load(file)
#         file.close()
#     gst = newgst
#     with open('gst', 'wb') as file:
#         pickle.dumps(gst, file)
#         file.close()

from anytree import *

# compare string adalah fungsi untuk membandingkan 2 string apakah memiliki substring yang sama


def nodeToString(node):
    node = str(node)
    # remove 12 first character on node
    node = node[12:]
    size = len(node)
    node = node[:size-2]
    node = node.replace("/", "")
    return node


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
        "id": 1,
        "judul": "kunci kurang"
    },
    {
        "id": 2,
        "judul": "kunci rusak"
    },
    {
        "id": 3,
        "judul": "rusak kurang"
    },
]
# wordInput = input("masukkan kata: ")
# arrWord = wordInput.split()
# print(arrWord)


def addChild(suf, parent, tree, index):
    # for pre, fill, node in RenderTree(tree):
    #     print("%s%s" % (pre, node.name))
    result = find_by_attr(tree, parent, maxlevel=2)
    print("res", result)
    print("tree, ", tree)
    print("parent, ", parent)
    children = result.children
    for child in children:
        print("+++++++++++++++++++++++++++++++++++++++++++++=")
        print("suf: ", suf)
        print("node: ", child.name)
        status, sameString, parentNameCut, sufCut = compare_strings(
            child.name, suf)
        if status == False:
            print("cek next node")
            continue
        if parentNameCut == "":
            print("normal")
            if sufCut == "":
                print(child)
                print("node index =", type(child.index))
                print("index saat ini: ", index)
                if index not in child.index:
                    child.index.append(index)
                return tree
            return addChild(suf=sufCut, parent=child.name, tree=tree, index=index)
        child.name = sameString
        if child.children == []:
            print("gaada anak")
            Node(sufCut, parent=child, index=[index])
            Node(parentNameCut, parent=child, index=[index])
            return tree
        # if child.children != []:
        print("ada anak")
        print("anak siapa: ", child.name)
        nodeParentCut = Node(parentNameCut, index=[index])
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
        for word in title["judul"].split():
            wordIndex = title["id"]
            word += "$"
            for i in range(len(word)):
                print("=================================================")
                suf = word[i:]
                addChild(suf=suf, parent="root", tree=root, index=wordIndex)
            # for pre, fill, node in RenderTree(root):
            #     print("%s%s" % (pre, node.name))
            print(RenderTree(root))


def makeTree(arrayInput):
    root = Node("root")
    for word in arrayInput:
        word += "$"
        for i in range(len(word)):
            # children = root.children
            # print(children)
            addSuf = False
            suf = word[i:]
            # print(suf)
            for node in LevelOrderIter(root, maxlevel=2):
                name = str(node.name)
                # print(name)
                if name != "root" and name != "$":
                    status, sameString, parentNameCut, sufCut = compare_strings(
                        name, suf)
                    # print(status)
                    if status == True:
                        print("suf: ", suf)
                        print("node yang sama: ", node.name)
                        print("ortunya: ", node.parent.name)
                        print("anaknya: ", node.children)
                        if node.children == []:
                            print("anak kosong")
                            if node.parent != root:
                                # print("ini")
                                break
                            # else:
                            # print("suf: ", suf)
                            # print("edge: ", node.name)
                            node.name = sameString
                            pastSuffix = name.removeprefix(sameString)
                            suf = suf.removeprefix(sameString)
                            if suf != "":
                                Node(suf, parent=node)
                            if pastSuffix != "":
                                Node(pastSuffix, parent=node)
                            addSuf = True
                        if node.children != []:
                            print("ada anak")
                            if node.parent != root:
                                break
                            # else:
                            # print(suf)
                            # print("edge: ", node.name)
                            node.name = sameString
                            if name.removeprefix(sameString) != "":
                                pastSuffix = Node(
                                    name.removeprefix(sameString))
                                pastSuffix.children = node.children
                                suf = suf.removeprefix(sameString)
                                if suf != "":
                                    pastSuffix.parent = node
                                    Node(suf, parent=node)
                                addSuf = True
                            else:
                                suf = suf.removeprefix(sameString)
                                if suf != "":
                                    Node(suf, parent=node)
                                addSuf = True
                    # elif status == False and suf in children:
                    #     break
                    # else:
                    #     Node(suf, parent=root)
            if addSuf == False:
                Node(suf, parent=root)
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.name))
    # print(children)


makeTree2(data)
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

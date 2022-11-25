from anytree import Node, RenderTree, LevelOrderIter


def compare_strings(a, b):
    if a is None or b is None:
        return False
    # if b in a:
    #     a = a.replace(b, "")
    size = min(len(a), len(b))
    status = False
    sameString = ""
    i = 0

    while i < size and a[i] == b[i]:
        # while a[i] == b[i]:
        status = True
        sameString += a[i]
        i += 1
    return status, sameString


wordInput = input("masukkan kata: ")
arrWord = wordInput.split()
print(arrWord)


def makeTree(arrayInput):
    root = Node("root")
    for word in arrayInput:
        word += "$"
        for i in range(len(word)):
            children = root.children
            # print(children)
            addSuf = False
            suf = word[i:]
            # print(suf)
            for node in LevelOrderIter(root):
                name = str(node.name)
                # print(name)
                if name != "root" and name != "$":
                    status, sameString = compare_strings(name, suf)
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


makeTree(arrWord)
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

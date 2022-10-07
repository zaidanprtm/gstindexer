from anytree import Node, RenderTree


def compare_strings(a, b):
    if a is None or b is None:
        return False
    size = min(len(a), len(b))
    status = False
    sameString = ""
    i = 0

    while i < size and a[0] == b[0]:
        if a[i] == b[i]:
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
            addSuf = False
            suf = word[i:]
            # print(suf)
            for pre, fill, node in RenderTree(root):
                name = str(node.name)
                # print(name)
                if name != "root" and name != "$":
                    status, sameString = compare_strings(name, suf)
                    # print(status)
                    if status == True:
                        if node.parent != root:
                            break
                        else:
                            node.name = sameString
                            pastSuffix = name.removeprefix(sameString)
                            suf = suf.removeprefix(sameString)
                            if suf != "":
                                Node(suf, parent=node)
                            if pastSuffix != "":
                                Node(pastSuffix, parent=node)
                            addSuf = True
                    # elif status == False and suf in children:
                    #     break
                    # else:
                    #     Node(suf, parent=root)
            if addSuf == False:
                Node(suf, parent=root)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
    print(children)


makeTree(arrWord)
# print(children)
# print(suf)
# suftree.append(suf)
# print(node)
# print(list(root.children))
# print(suftree)

# print(RenderTree(root))
# print(compare_strings("baca", "ca"))
# for pre, fill, node in RenderTree(root):
#     print("%s%s" % (pre, node.name))

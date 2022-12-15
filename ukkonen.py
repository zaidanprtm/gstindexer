from asyncio.windows_events import NULL
from anytree import Node, RenderTree
# root = Node("root")

# marc = Node("Marc", parent=root, edge="marc")
# lian = Node("Lian", parent=marc)
# dan = Node("Dan", parent=root)
# jet = Node("Jet", parent=dan)
# jan = Node("Jan", parent=dan)
# joe = Node("Joe", parent=dan)

# for pre, fill, node in RenderTree(root):
#     print("%s%s" % (pre, node.name))
# print(RenderTree(root))

# def checkString(string, tree):
#     for pre, fill, node in RenderTree(tree):
#         if node.name == string and len(node.children) != 0:
#             return True, "prefix"
#         elif node.name == string and len(node.children) == 0:
#             return True, "suffix"
#         # else:
#         #     return False


def checkExist(node, character):
    # node = Node(node)
    for i in node.children:
        if i.name[0] == character:
            return True
    return False


def substring_after(s, delim):
    return s.partition(delim)[2]


def compare_strings(node, strInput):
    size = min(len(node), len(strInput))
    status = False
    sameString = ""
    i = 0
    if node is None or strInput is None or strInput == "":
        return status, sameString
    if len(node) < len(strInput):
        return status, sameString
    elif node[0] != strInput[0]:
        return status, sameString

    while i < size:
        if node[i] == strInput[i]:
            status = True
            sameString += node[i]
        i += 1
    return status, sameString


def nodeToString(node):
    node = str(node)
    # remove 12 first character on node
    node = node[12:]
    size = len(node)
    node = node[:size-2]
    node = node.replace("/", "")
    return node


def makeTreeFromArray(titles):
    root = Node("root")
    for title in titles:
        arrTitle = title.split()
        for word in arrTitle:
            makeTree(root, word)
    return root


def makeTree(root, word):
    # root = Node("root")
    word += "$"
    # construct T1
    if Node(word[0]) not in root.children:
        Node(word[0], parent=root)

    for i in range(len(word)-1):
        # print("i=", i)
        phase = i + 1
        for j in range(phase+1):
            print("i=", str(i) + ", phase=", str(phase) + ", j=", str(j))
            # print("j=", j)
            if j > i:
                beta = ""
            beta = word[j:i+1]
            if j == i:
                beta = word[i]
            nextChar = word[i+1]
            print("beta = ", beta)
            print("s[i+1] = ", nextChar)
            for pre, fill, k in RenderTree(root):
                name = str(k.name)
                if name == "root":
                    continue

                if j == 0:
                    k.name += nextChar
                # print(k.name)
                # rule 1
                # print(k)
                # print("node = ", nodeToString(k))
                # if nodeToString(k) == beta and Node(beta+nextChar) not in RenderTree(root):
                #     print("RULE 1")
                #     k.name += nextChar
                #     break
                # rule 2
                if beta == "" and checkExist(root, nextChar) == False:
                    print("RULE 2A")
                    Node(nextChar, parent=root)
                    break
                statusBeta, sameString = compare_strings(nodeToString(k), beta)
                if statusBeta == True and sameString == beta and Node(beta+nextChar) not in RenderTree(root) and nodeToString(k) == name:
                    # print(name)
                    # print(sameString)
                    # if substring_after(name, beta)[0] != beta:
                    print("RULE 2B")
                    k.name = beta
                    pastSuffix = substring_after(name, sameString)
                    Node(pastSuffix, parent=k)
                    Node(nextChar, parent=k)
                    break
                # rule 3
                # elif Node(nextChar) not in root.children:
                statusMix, sameStringMix = compare_strings(
                    nodeToString(k), beta+nextChar)
                if statusMix == True and sameStringMix == beta+nextChar:
                    print("RULE 3")
                    break
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.name))


titles = ["banana"]
tree = makeTreeFromArray(titles)
# for pre, fill, node in RenderTree(tree):
#     print("%s%s" % (pre, node.name))

# print(compare_strings("abxac", "xa"))
# print(checkChildren("Jet", dan))
# print(checkString("awikwok", root))
# print(checkString("Dan", root))
# print(checkString("Joe", root))

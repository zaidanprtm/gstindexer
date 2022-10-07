from suffix_tree import Tree

tree = Tree({'A': 'xabxac'})
print(tree)
print(tree.find('abx'))
print(tree.find('abc'))

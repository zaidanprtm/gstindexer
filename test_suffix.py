import anytree
from anytree import *

# Create a generalized suffix tree from a list of strings


def create_gst(strings):
    # Create a root node
    root = anytree.Node("root")

    # Add a child node for each string
    for string in strings:
        child = anytree.Node(string)
        child.parent = root

    return root

# Create an induced generalized suffix tree from a generalized suffix tree


def create_induced_gst(gst, strings):
    # Create a root node for the induced GST
    induced_root = anytree.Node("induced_root")

    # Iterate through the nodes in the GST
    for node in anytree.PreOrderIter(gst):
        # Check if the node's label is in the list of strings
        if node.name in strings:
            # If it is, add a child node to the induced GST with the same label
            induced_child = anytree.Node(node.name)
            induced_child.parent = induced_root
        else:
            # If it isn't, add a child node to the induced GST with the label "other"
            induced_child = anytree.Node("other")
            induced_child.parent = induced_root

    return induced_root


# Example usage
strings = ["abc", "def", "ghi"]
gst = create_gst(strings)
induced_gst = create_induced_gst(gst, ["abc", "def"])

print(RenderTree(gst))
print(RenderTree(induced_gst))

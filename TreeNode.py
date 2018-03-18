class TreeNode:
    def __init__(self,att,att_dict,classes,children=None,child_examples=None):
        self.attribute = att
        self.children = children
        self.child_examples = child_examples
        self.att_dict = att_dict
        self.classes = classes

    def add_child(self, node, list_index):
        self.children.insert(list_index, node)
        return 0

    # add examples for a child to this node
    def add_examples(self, examples, i):
        self.child_examples.insert(i, examples)

    def print_node(self, indent, i):
        printstr = ""
        for s in range(0,indent):
            printstr += "   "
        print(printstr,self.attribute, " = ", self.att_dict.get(self.attribute)[i], self.child_examples[i])

    def print_tree(self, level = None):
        if level is None:
            level = 0
        for child in range(0,len(self.children)):
            if type(self.children[child]) is int:
                self.print_leaf(level, child, self.children[child])
            else:
                self.print_node(level, child)
                self.children[child].print_tree(level+1)

    def print_leaf(self, level, i, val):
        printstr = ""
        for s in range(0,level):
            printstr += "   "
        print(printstr,self.attribute, " = ", self.att_dict.get(self.attribute)[i], ": ", self.classes[val].upper(), self.child_examples[i])

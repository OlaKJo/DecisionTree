class TreeNode:
    def __init__(self,att,children=None,examples=None,parent=None,):
        self.attribute = att
        self.parent = parent
        self.children = children

    def add_child(self, node, list_index):
        self.children.insert(node, list_index)

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return not (self.rightChild or self.leftChild)

    # Set examples for this node
    def set_examples(self, examples):
        self.examples = examples

    def get_examples(self):
        return self.examples

    def has_any_children(self):
        return self.rightChild or self.leftChild

    def print_node(self, indent, i):
        printstr = ""
        for s in range(0,indent):
            printstr += "   "
        print(printstr,self.att, " = ", i)

    def print_tree(self, level):
        for child in range(0,len(self.children)):
            if type(self.children[child]) is int:
                print_leaf(level, self.children[child])
            else:
                print_node(level, child)
                print_tree(self.children[child], level+1)

    def print_leaf(self, level, val):
        printstr = ""
        for s in range(0,indent):
            printstr += "   "
        print(printstr,self.att, " = ", i, ": ", val)


    def replace_node_data(self,key,value,lc,rc):
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

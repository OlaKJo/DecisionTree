class TreeNode:
    def __init__(self,att,children=None,examples=None,parent=None,):
        self.attribute = att
        self.parent = parent
        self.children = children

    def add_child(self, node, list_index):
        self.children.insert(list_index, node)
        return 0

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
        print(printstr,self.attribute, " = ", i)

    def print_tree(self, level):
        for child in range(0,len(self.children)):
            if type(self.children[child]) is str:
                self.print_leaf(level, child, self.children[child])
            else:
                self.print_node(level, child)
                self.children[child].print_tree(level+1)

    def print_leaf(self, level, i, val):
        printstr = ""
        for s in range(0,level):
            printstr += "   "
        print(printstr,self.attribute, " = ", i, ": ", val)


    def replace_node_data(self,key,value,lc,rc):
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

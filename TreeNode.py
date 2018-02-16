class TreeNode:
    def __init__(self,att,children=None,examples=None,parent=None,):
        self.attribute = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.children = children

    def add_child(node, list_index):
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

    def print_node(self):
        print(self.att)

    def replace_node_data(self,key,value,lc,rc):
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

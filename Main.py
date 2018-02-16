import Reader
from TreeNode import TreeNode
attributes, classes, data = Reader.read_file("testfile")

node = TreeNode("Patrons", 32);
node.printNode()

print (attributes)
print (classes)
for line in data:
    print (line)

result_tree = DTL(data, attributes, data)


def DTL(examples, attributes, parent_examples):
    if len(examples) == 0:
        return plurality_value(parent_examples)
    elif check_if_all_same(parent_examples):
        return get_class(parent_examples(0))
    elif if all(x is None for x in attributes):
        return plurality_value(examples)
    else
        next_attribute = get_next_attribute(attributes, examples)
        node = TreeNode(next_attribute)
        v_values = set(column(examples, attributes.index(next_attribute))
        for i in v_values:
            child_examples = [x for x in examples if x(attributes.index(next_attribute)) == i]
            attributes(attributes.index(next_attribute)) = None
            subtree = DTL(child_examples, attributes, examples)
            node.add_child(subtree, i)
        return node



def plurality_value(examples):
    goals = column(examples, len(examples(0)-1))
    exsset = set(goals)
    A = [len([x for x in goals if x==y]) for y in exsset]
    maxA = max(A)
    maxGoals = [exsset(i) for i in [1:len(exsset)-1] if A(i)==maxA]
    r = randint(0, len(maxGoals))
    return maxGoals(r)

    #goals = column(examples, len(examples(0)))
    #counts = {}
    #    for i in goals:
    #        if i in counts:
    #   counts[i] += 1
    #        else:
    #            counts[i] = 1
    #return 1

def get_next_attribute(attributes, examples):

    return attributes(0)

def check_if_all_same(examples):

    return False

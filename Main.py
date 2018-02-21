import Reader
import math
from random import randint
from TreeNode import TreeNode

def main():
    attributes, classes, data = Reader.read_file("Restaurant")

    #node = TreeNode("Patrons", 32);
    # node.printNode()

    print (attributes)
    print (classes)
    for line in data:
        print (line)

    # result_tree = DTL(data, attributes, data)
    # print(plurality_value(data))


    #print(check_if_all_same(data))
    #get_next_attribute(attributes, data)
    root = DTL(data, attributes, data)
    root.print_tree(0)


def DTL(examples, attributes, parent_examples):
    if len(examples) == 0:
        return plurality_value(parent_examples)
    elif check_if_all_same(examples):
        return get_class(examples[0])
    elif all(x is None for x in attributes):
        return plurality_value(examples)
    else:
        next_attribute = get_next_attribute(attributes, examples)
        node = TreeNode(next_attribute, list())
        v_values = set(column(examples, attributes.index(next_attribute) + 1))
        next_attribute_index = attributes.index(next_attribute)
        attributes[attributes.index(next_attribute)] = None
        for i in v_values:
            child_examples = [x for x in examples if x[next_attribute_index + 1] == i]
            subtree = DTL(child_examples, attributes, examples)
            node.add_child(subtree, int(i))
        return node



def plurality_value(examples):
    goals = column(examples, len(examples[0])-1)
    exsset = set(goals)
    A = [len([x for x in goals if x==y]) for y in exsset]
    maxA = max(A)
    i = 0
    maxGoals = list()
    for x in exsset:
        if A[i] == maxA:
            maxGoals.append(x)
        i += 1
    r = 0 if len(maxGoals) == 1 else randint(0, len(maxGoals) - 1)
    return maxGoals[r]

def get_next_attribute(attributes, examples):
    current_champion = 0
    while attributes[current_champion] == None:
        current_champion += 1
    current_gain = gain(current_champion, examples)
    for challenger in list(range(current_champion + 1,len(attributes))):
        if attributes[challenger] == None:
            break
        challenger_gain = gain(challenger, examples)
        if challenger_gain > current_gain:
            current_champion = challenger
            current_gain = challenger_gain

    return attributes[current_champion]

def gain(i, examples):
    nbrpos = len([x for x in examples if x[len(x)-1]=='1'])
    q = nbrpos/len(examples)
    gain = B(q) - remainder(i, examples)
    print(i,gain)
    return gain

def B(q):
    if (q == 0 or q == 1):
        return -math.log(1,2)
    return -(q*math.log(q,2) + (1 - q)*math.log((1-q),2))

def remainder(i, examples):
    col = column(examples, i+1)
    exsset = set(col)
    branches = [[row for row in examples if row[i+1]==val] for val in exsset]
    rem_sum = 0
    for branch in branches:
        nbrpos = len([x for x in branch if x[len(x)-1]=='1'])
        rem_sum += len(branch)*B( nbrpos/len(branch) )
    return rem_sum/len(examples)


def check_if_all_same(examples):
    goals = column(examples, len(examples[0])-1)
    exsset = set(goals)
    return False if len(exsset) > 1 else True

def get_class(example):
    return example[len(example) - 1]

def column(matrix, i):
    return [row[i] for row in matrix]

main()

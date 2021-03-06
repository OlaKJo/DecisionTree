import Reader
import math
from random import randint
from TreeNode import TreeNode
from scipy.stats import chi2
import sys

P_VALUE = 0.05

CHI2_95 =   [3.84145882069413, 5.99146454710798,    7.81472790325118,
            9.48772903678115,	11.0704976935164,	12.5915872437440,
            14.0671404493402,	15.5073130558655,	16.9189776046204,
            18.3070380532751,	19.6751375726825,	21.0260698174831,
            22.3620324948269,	23.6847913048406,	24.9957901397286,
            26.2962276048642,	27.5871116382753,	28.8692994303926,
            30.1435272056462,	31.4104328442309,	32.6705733409173,
            33.9244384714438,	35.1724616269081,	36.4150285018073,
            37.6524841334828]



def main():
    """Main method of Decision Tree Project.
    Calls the operational functions to create a Decision Tree and a pruned tree
    """

    attributes, classes, data, att_dict = Reader.read_file(sys.argv[1])

    print("The attributes are:")
    print (attributes)
    print("The classes are:")
    print (classes)
    print("The example data used is: ")
    for line in data:
        print (line)
    print()

    root = DTL(data, attributes, data, data, att_dict, classes)
    print("decision tree: ")
    root.print_tree()
    print("")
    print("pruned tree: ")
    prune(root, root, data, classes)
    root.print_tree()


def DTL(examples, attributes, parent_examples, orig_examples, att_dict, classes):
    """Holds the main algorithm componentes for creatin a Decision tree.
    Recursive function with base cases for:
    - no more examples available
    - all remaining examples have the same class
    - no more attributes available
    Recursive step calls get_next_attribute() to decide which node to add next
    """

    #orig_examples is used to be able to loop all v_values, even if some of the possible
    #v_values are no longer present in examples at a given level of the tree
    if len(examples) == 0:
        return plurality_value(parent_examples)
    elif check_if_all_same(examples):
        return get_class(examples[0])
    elif all(x is None for x in attributes):
        return plurality_value(examples)
    else:
        next_attribute = get_next_attribute(attributes, examples, classes)
        node = TreeNode(next_attribute, att_dict, classes, list(), list())
        v_values = set(column(orig_examples, attributes.index(next_attribute) + 1))
        next_attribute_index = attributes.index(next_attribute)
        attributes[attributes.index(next_attribute)] = None
        for i in v_values:
            child_examples = [x for x in examples if x[next_attribute_index + 1] == i]
            node.add_examples(column(child_examples,0), int(i))
            subtree = DTL(child_examples, attributes, examples, orig_examples, att_dict, classes)
            node.add_child(subtree, int(i))
        return node

def prune(curr_node, node_parent, data, classes):
    """
    Clears an already created decision tree from nodes and paths which do not
    contribute statistically to the decision being made. Takes as its initial
    parameters the root of the tree, the root of the tree, and the entire data set.
    The method is then called recursively on any child nodes until leaves are found.
    Leaves are pruned if not found useful enough.
    """
    root = (curr_node == node_parent)

    leaf = True
    parent = curr_node
    children = curr_node.children
    for child in children:
        if type(child) is TreeNode:
            prune(child, curr_node, data, classes)
    for child in children:
        if type(child) is TreeNode:
            leaf = False
            break
    if leaf:
        if no_info_gain(curr_node, data, classes) :
            if not root:
                ind = node_parent.children.index(curr_node)
                node_parent.children.remove(curr_node)
                node_parent.children.insert(ind, plurality_value(get_node_examples(curr_node,data)))
            else:
                print("Attemped to prune root of tree")

    return curr_node

def get_node_examples(node, examples):
    """
    returns a sub set of examples. The examples that are coupled to the given node.
    """
    sub_examples_list = list()
    for branch in node.child_examples:
        for x in branch:
            for row in examples:
                if row[0] == x:
                    sub_examples_list.append(row)
                    continue
    sub_examples = [None] * len(sub_examples_list)
    for i in range(0, len(sub_examples_list)):
        sub_examples[i] = sub_examples_list[i]
    return sub_examples



def no_info_gain(node, data, classes):
    """
    returns true if the attribute, given its data, contributes significantly to
    discimination in the decision making process
    """
    pk = list()
    nk = list()
    for k in range(0, len(node.child_examples)):
        pk.insert(k, 0)
        nk.insert(k, 0)
        for x in node.child_examples[k]:
            for row in data:
                if row[0] == x:
                    curr_class = row[len(row)-1]
                    if curr_class == 0:
                        pk[k] += 1
                    else:
                        nk[k] += 1
                    continue
    p = sum(pk)
    n = sum(nk)
    pk_hat = list()
    nk_hat = list()
    Delta = 0
    v_minus = 0
    for k in range(0, len(node.child_examples)):
        if len(node.child_examples[k]) == 0:
            pk_hat.insert(k, 0)
            nk_hat.insert(k, 0)
            v_minus += 1
            continue
        pk_hat.insert(k, p*(pk[k]+nk[k])/(p+n))
        nk_hat.insert(k, n*(pk[k]+nk[k])/(p+n))
        Delta += pow(pk[k] - pk_hat[k],2)/pk_hat[k] + pow(nk[k] - nk_hat[k],2)/nk_hat[k]
    v = len(pk) - 1 - v_minus
    #Select whether to use table values or calculate using CHI2_PARAM and scipy instead.
    #chi2_tab = CHI2_95[v - 1]
    #chi2_sci = chi2.ppf(CHI2_PARAM, v)
    chi2_sci = chi2.ppf(P_VALUE, v)
    #print("Delta value for node ", node.attribute, " is: ", Delta, ", chi2 value is: ", chi2_sci)
    return Delta >= chi2_sci


def plurality_value(examples):
    """
    Returns the most common class among the examples. Randomizes the return value
    in case of ties.
    """
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

def get_next_attribute(attributes, examples, classes):
    """
    Returns the remaining attribute which has the highest information gain.
    """
    current_champion = 0
    while attributes[current_champion] == None:
        current_champion += 1
    current_gain = gain(current_champion, examples, classes)
    for challenger in list(range(current_champion + 1,len(attributes))):
        if attributes[challenger] == None:
            continue
        challenger_gain = gain(challenger, examples, classes)
        if challenger_gain > current_gain:
            current_champion = challenger
            current_gain = challenger_gain

    return attributes[current_champion]

def gain(i, examples, classes):
    """
    calculates the information gain of a set of examples, using entropy and
    remainder
    """
    nbrpos = len([x for x in examples if x[len(x)-1]==0])
    q = nbrpos/len(examples)
    gain = B(q) - remainder(i, examples, classes)
    # print(i,gain)
    return gain

def B(q):
    """
    Returns the entropy of q
    """
    if (q == 0 or q == 1):
        return -math.log(1,2)
    return -(q*math.log(q,2) + (1 - q)*math.log((1-q),2))

def remainder(i, examples, classes):
    """
    Returns the remainder of attribute at index i in 'attributes' given
    examples.
    """
    col = column(examples, i+1)
    exsset = set(col)
    branches = [[row for row in examples if row[i+1]==val] for val in exsset]
    rem_sum = 0
    for branch in branches:
        nbrpos = len([x for x in branch if x[len(x)-1]==0])
        rem_sum += len(branch)*B( nbrpos/len(branch) )
    return rem_sum/len(examples)


def check_if_all_same(examples):
    """
    returns true if all examples have the same class
    """
    goals = column(examples, len(examples[0])-1)
    exsset = set(goals)
    return False if len(exsset) > 1 else True

def get_class(example):
    return example[len(example) - 1]

def column(matrix, i):
    return [row[i] for row in matrix]

main()

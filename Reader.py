import re
# method to read and save attributes and classes (and data) from an ARFF file
def read_file(file_name):
    attributes = list()
    classes = None
    data = None
    att_dict = {}
    file = open(file_name, "r")
    lines = file.readlines()
    # loop all the lines of the ARFF file to find lines containing attributes
    # and data
    for i in range(0, len(lines) - 1):
        # remove '\n' from end of string
        line = lines[i].rstrip('\n')
        if len(line) == 0:
            continue
        words = re.split(r'\s+', line)
        if words[0][0] == "%":
            continue
        if words[0].lower() == "@relation":
            continue
        if words[0].lower() == "@attribute":
            if words[1].lower() == "class":
                classes = (words[2][1:(len(words[2]) - 1)]).split(",")
                continue
            curr_attribute = words[1].lower()
            alternatives = (words[2][1:(len(words[2]) - 1)]).split(",")

            att_dict[curr_attribute] = alternatives
            attributes.append(words[1].lower())
        elif words[0].lower() == "@data":
            data = read_data(lines[i+1:len(lines)], len(attributes) + 1, attributes, att_dict, classes)
    return attributes, classes, data, att_dict

# method to save data found after '@DATA' tag in ARFF file
def read_data(lines, x_limit, attributes, att_dict, classes):
    #data = [[0 for i in range(0,x_limit)] for j in range(0,len(lines))]
    vect_data = list()
    for i in range(0, len(lines)):
        line = lines[i].rstrip('\n')
        line_data = line.split(",")
        row = list();
        row.append("x" + str(i+1))
        for j in range(0, len(line_data) - 1):
            row.append(numerize(line_data[j], att_dict[attributes[j]]))
        row.append(numerize(line_data[len(line_data) - 1], classes))
        vect_data.append(row);
    return vect_data

def vectorize(value, pos_vals):
    return [int(pos_vals[x] == value) for x in range(0,len(pos_vals))]

def numerize(value, pos_vals):
    return pos_vals.index(value)

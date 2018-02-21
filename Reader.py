# method to read and save attributes and classes (and data) from an ARFF file
def read_file(filename):
    attributes = list()
    classes = None
    data = None
    file = open(filename, "r")
    lines = file.readlines()
    # loop all the lines of the ARFF file to find lines containing attributes
    # and data
    for i in range(0, len(lines) - 1):
        # remove '\n' from end of string
        line = lines[i].rstrip('\n')
        if len(line) == 0:
            continue
        words = line.split(" ")
        if words[0][0] == "%":
            continue
        if words[0].lower() == "@relation":
            continue
        if words[0].lower() == "@attribute":
            if words[1].lower() == "class":
                classes = (words[2][1:(len(words[2]) - 1)]).split(",")
                continue
            attributes.append(words[1].lower())
        elif words[0].lower() == "@data":
            data = read_data(lines[i+1:len(lines)], len(attributes) + 1)
    return attributes, classes, data

# method to save data found after '@DATA' tag in ARFF file
def read_data(lines, x_limit):
    data = [[0 for i in range(0,x_limit)] for j in range(0,len(lines))]
    for i in range(0, len(lines)):
        line = "x" + str(i+1) + "," + lines[i].rstrip('\n')
        data[i] = line.split(",")
    return data

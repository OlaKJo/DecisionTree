def read_file(filename):
    attributes = list()
    classes = None
    data = None
    file = open(filename, "r")
    lines = file.readlines()
    for i in range(0, len(lines) - 1):
        line = lines[i][0:len(lines[i])-2]
        if len(line) == 0:
            continue
        words = line.split(" ")
        if words[0][0] == "%":
            continue
        if words[0].lower() == "@relation":
            continue
        if words[0].lower() == "@attribute":
            if words[1].lower() == "class":
                print("setting classes")
                classes = (words[2][1:(len(words[2]) - 2)]).split(",")
                continue
            attributes.append(words[1].lower())
        elif words[0].lower() == "@data":
            print("setting data")
            data = read_data(lines[i+1:len(lines)-1], len(attributes) + 1)
    return attributes, classes, data


def read_data(lines, x_limit):
    data = [[0 for i in range(x_limit)] for j in range(len(lines) - 1)]
    for i in range(0, len(lines) - 1):
        line = lines[i][0:len(lines[i])-2]
        data[i] = line.split(",")
    return data

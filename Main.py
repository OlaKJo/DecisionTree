import Reader

attributes, classes, data = Reader.read_file("testfile")

print (attributes)
print (classes)
for line in data:
    print (line)

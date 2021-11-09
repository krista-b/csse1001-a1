def find_functions(filename):
    with open(filename, "r") as file, \
        open("functions.txt","w") as output:
            for line in file:
                if line.startswith("def "):
                    output.write(line)

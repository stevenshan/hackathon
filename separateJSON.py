# split a JSON file into smaller parts

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python separateJSON.py [file name.json]")
        exit()

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        raise ValueError("File does not exist.")

    file = open(filename, "r")
    text = file.read()
    file.close()

    length = len(text)
    balance = 0
    i = 1 
    buff = [""] * 20
    buff_i = 0

    if not os.path.exists("groups/"):
        os.makedirs("groups/")

    count = 0
    def write(count, buff, buff_i):
        file = open("groups/" + str(count) + ".json", "w")
        t = ",".join(buff[:buff_i])
        file.write("[" + t + "]")
        file.close()

    checkpoint = length // 20
    while i < length:
        c = text[i]
        buff[buff_i] += c
        if c == "{":
            balance += 1
        elif c == "}" and balance == 1:
            buff_i += 1
            if buff_i != 20:
                buff[buff_i] = ""
            balance -= 1
            i += 1
        elif c == "}":
            balance -= 1
        if buff_i == 20:
            write(count, buff, buff_i)
            count += 1
            buff_i = 0
            buff[0] = ""

        i += 1
        if (i % checkpoint == 0):
            print(i / checkpoint)

    if buff_i != 0:
        write()
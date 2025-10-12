from io import TextIOWrapper

def getLines(f: TextIOWrapper):
    string = ""
    try:
        while True:
            data = bytes(8)
            n = f.read(len(data))
            if not n:
                break;
            
            # add reading to data
            data = data + n.encode()
            
            # find \n in data
            idx = data.find(b'\n')
            
            # if we found an index
            if idx != -1:
                # save from data to the idx in string
                string += data[:idx].decode()
                data = data[idx + 1:]
                yield string
                string = ""

            string += data.decode()

        if len(string) != 0:
            yield string
    finally:
        f.close()


def main():
    file = open("./message.txt", "r")
    
    for line in getLines(file):
        print("read: " + line)

if __name__ == "__main__":
    main()

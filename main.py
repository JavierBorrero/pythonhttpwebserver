def main():
    file = open("./message.txt", "r")
    
    string = ""
    while True:
        data = bytes(8)
        n = file.read(len(data))
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
            print("read: " + string)
            string = ""

        string += data.decode()

    if len(string) != 0:
        print("read: " + string)

if __name__ == "__main__":
    main()

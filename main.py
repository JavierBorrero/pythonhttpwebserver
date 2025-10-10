def main():
    file = open("./message.txt", "r")

    while True:
        data = file.read(8)
        if not data:
            break;
        print("read: " + data)
    
main()

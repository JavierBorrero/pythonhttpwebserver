import socket

def getLines(f: socket.socket):
    string = ""
    try:
        while True:
            data = bytes(8)
            n = f.recv(len(data))
            if not n:
                break;
            
            # add reading to data
            data = data + n
            
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
    server = socket.create_server(("localhost", 1234))

    while True:
        conn, addr = server.accept()
    
        for line in getLines(conn):
            print("read: " + line)


if __name__ == "__main__":
    main()

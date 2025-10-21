import socket
from internal.request.request import request_from_reader

#def getLines(f):
#    string = ""
#    try:
#        while True:
#            data = bytes(8)
#            n = f.read(len(data))
#            if not n:
#                break;
#            
#            # add reading to data
#            data = data + n.encode()
#            
#            # find \n in data
#            idx = data.find(b'\n')
#            
#            # if we found an index
#            if idx != -1:
#                # save from data to the idx in string
#                string += data[:idx].decode()
#                data = data[idx + 1:]
#                yield string
#                string = ""
#
#            string += data.decode()
#        
#        if len(string) != 0:
#            yield string
#
#    finally:
#        f.close()


def main():
    server = socket.create_server(("localhost", 1234))

    while True:
        conn, addr = server.accept()
        file_conn = conn.makefile('rb')

        request = request_from_reader(file_conn)
        #'''
        #makefile() returns a file object associated with the socket

        #A file object is an object exposing a file-oriented API
        #(with methods such as read() or write()) to an underlying resource
        #'''
        #for line in getLines(conn.makefile('r')):
        #    print("read: " + line)
        print("Request Line: ")
        print("- Method: ", request.request_line.method)
        print("- Target: ", request.request_line.request_target)
        print("- Version: ", request.request_line.http_version)


if __name__ == "__main__":
    main()

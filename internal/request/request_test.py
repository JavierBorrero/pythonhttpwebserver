import unittest

from internal.request.request import request_from_reader


class ChunkReader:
    data: str
    num_bytes_per_read: int
    pos: int

    def __init__(self, data: str, num_bytes_per_read: int, pos: int) -> None:
        self.data = data
        self.num_bytes_per_read = num_bytes_per_read
        self.pos = pos

    def copy_bytes(self, dst: bytearray, src: bytes) -> int:
        n = min(len(dst), len(src))
        dst[:n] = src[:n]
        return n

    def read(self, b: bytearray) -> tuple[int, BaseException | None]:
        if self.pos >= len(self.data):
            return 0, EOFError()

        end_index = self.pos + self.num_bytes_per_read
        if end_index > len(self.data):
            end_index = len(self.data)
        
        n = self.copy_bytes(b, self.data[self.pos:end_index].encode())

        self.pos += n

        if n > self.num_bytes_per_read:
            n = self.num_bytes_per_read
            self.pos -= n - self.num_bytes_per_read
        
        return n, None

class TestRequest(unittest.TestCase):
    #def test_request_line_parse(self):

        #reader = ChunkReader(
        #        data="GET / HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n",
        #        num_bytes_per_read=3,
        #        pos=0)
        #request = request_from_reader(reader)
        #self.assertEqual("GET", request.request_line.method)
        #self.assertEqual("/", request.request_line.request_target)
        #self.assertEqual("1.1", request.request_line.http_version)

        #reader = ChunkReader(
        #        data="GET /coffee HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n",
        #        num_bytes_per_read=1,
        #        pos=0)
        #request = request_from_reader(reader)
        #self.assertEqual("GET", request.request_line.method)
        #self.assertEqual("/coffee", request.request_line.request_target)
        #self.assertEqual("1.1", request.request_line.http_version)
        # Good GET Request line
        #request = request_from_reader(StringIO("GET / HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n"))
        #self.assertEqual("GET", request.request_line.method)
        #self.assertEqual("/", request.request_line.request_target)
        #self.assertEqual("1.1", request.request_line.http_version)
        #
        ## Good GET Request line with path
        #request = request_from_reader(StringIO("GET /coffee HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n"))
        #self.assertEqual("GET", request.request_line.method)
        #self.assertEqual("/coffee", request.request_line.request_target)
        #self.assertEqual("1.1", request.request_line.http_version)

        ## Invalid number of parts in request line
        #request = request_from_reader(StringIO("/coffee HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n"))
        #self.assertEqual("", request.request_line.method)
        #self.assertEqual("", request.request_line.request_target)
        #self.assertEqual("", request.request_line.http_version)

    def test_headers_parse(self):
        # Standard headers
        reader = ChunkReader(
                data="GET / HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n",
                num_bytes_per_read=3,
                pos=0)
        request = request_from_reader(reader)
        self.assertEqual("localhost:1234", request.headers.get("host"))
        self.assertEqual("curl/8.16.0", request.headers.get("user-agent"))
        self.assertEqual("*/*", request.headers.get("accept"))

        # Malformed headers
        reader = ChunkReader(
                data="GET / HTTP/1.1\r\nHost localhost:1234\r\n\r\n",
                num_bytes_per_read=3,
                pos=0)
        request = request_from_reader(reader)
        self.assertEqual({}, request.headers.headers)

if __name__ == '__main__':
    unittest.main()

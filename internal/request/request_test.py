from dataclasses import dataclass
import unittest

from io import StringIO

from request import request_from_reader


class TestRequest(unittest.TestCase):
    def test_request_line_parse(self):
        # Good GET Request line
        request = request_from_reader(StringIO("GET / HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n"))
        self.assertEqual("GET", request.request_line.method)
        self.assertEqual("/", request.request_line.request_target)
        self.assertEqual("1.1", request.request_line.http_version)
        
        # Good GET Request line with path
        request = request_from_reader(StringIO("GET /coffee HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n"))
        self.assertEqual("GET", request.request_line.method)
        self.assertEqual("/coffee", request.request_line.request_target)
        self.assertEqual("1.1", request.request_line.http_version)

        # Invalid number of parts in request line
        request = request_from_reader(StringIO("/coffee HTTP/1.1\r\nHost: localhost:1234\r\nUser-Agent: curl/8.16.0\r\nAccept: */*\r\n\r\n"))
        self.assertEqual("", request.request_line.method)
        self.assertEqual("", request.request_line.request_target)
        self.assertEqual("", request.request_line.http_version)

if __name__ == '__main__':
    unittest.main()

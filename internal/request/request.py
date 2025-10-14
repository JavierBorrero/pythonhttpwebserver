from dataclasses import dataclass
from typing import Tuple
import io

@dataclass
class RequestLine:
    http_version: str = ""
    request_target: str = ""
    method: str = ""

@dataclass
class Request:
    request_line: RequestLine

NO_ERROR = ""
ERROR_MALFORMED_REQUEST_LINE = "malformed request-line"

SEPARATOR = "\r\n"

def parse_request_line(s: str) -> Tuple[RequestLine, str, str]:
    idx = s.index(SEPARATOR)
    
    # havent first found \r\n, not able to parse start line
    if idx == -1:
        return RequestLine(), s, NO_ERROR
    
    start_line = s[:idx]
    rest_of_msg = s[idx + len(SEPARATOR):]

    parts = str.split(start_line, " ")
    
    # if we dont have method, path and http protocol
    if len(parts) != 3:
        return RequestLine(), rest_of_msg, ERROR_MALFORMED_REQUEST_LINE
    
    http_parts = str.split(parts[2], "/")

    if len(http_parts) != 2 or http_parts[0] != "HTTP" or http_parts[1] != "1.1":
        return RequestLine(), rest_of_msg, ERROR_MALFORMED_REQUEST_LINE

    request_line = RequestLine(method=parts[0], request_target=parts[1], http_version=http_parts[1])
    
    return request_line, rest_of_msg, NO_ERROR

'''
io.Reader[T] -> Generic protocol for reading from a file or other
input stream. T will usually be str or bytes, but can be any type
that is read from the stream
'''
def request_from_reader(reader: io.Reader) -> Request:

    data = None

    if type(data) == bytes:
        data = reader.read().decode()
    else:
        data = reader.read()

    rl, _, err = parse_request_line(data)
    
    return Request(request_line=rl)

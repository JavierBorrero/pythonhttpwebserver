from dataclasses import dataclass
from enum import Enum
from typing import override

from internal.headers.headers import Headers

NO_ERROR = ""
ERROR_MALFORMED_REQUEST_LINE = "malformed request-line"
SEPARATOR = "\r\n".encode()

class ParserState(Enum):
    INIT = "init",
    DONE = "done",
    HEADERS = "headers",

@dataclass
class RequestLine:
    http_version: str = ""
    request_target: str = ""
    method: str = ""

class Request:
    request_line: RequestLine
    headers: Headers
    state: ParserState

    def __init__(self, request_line: RequestLine, headers: Headers, state: ParserState) -> None:
        self.request_line = request_line
        self.headers = headers
        self.state = state
    
    @override
    def __str__(self) -> str:
        return f"Request(\n  request_line={self.request_line},\n  headers={self.headers.headers},\n  state={self.state}\n)"

    def parse(self, data: bytearray) -> int:
        read = 0
        current_data = data[read:]

        match self.state:
            case ParserState.INIT:
                rl, n, err = parse_request_line(current_data)
                if err:
                    return 0

                if n == 0:
                    return read

                self.request_line = rl
                read += n
                
                self.state = ParserState.HEADERS
            
            case ParserState.HEADERS:
                # normally current_data will look like this:
                # GET / HTTP/1.1\r\nHost:
                # but it needs to look like this:
                # Host: ...
                # so i do this:
                # self.headers.parse(current_data[idx+len(SEPARATOR):])
                try:
                    idx = bytearray.index(current_data, SEPARATOR)
                except ValueError:
                    return 0
                n, done, err = self.headers.parse(current_data[idx+len(SEPARATOR):])

                if err:
                    return 0

                read += n

                if done:
                    self.state = ParserState.DONE

            case ParserState.DONE:
                return read
        return read

    def done(self) -> bool:
        return self.state == ParserState.DONE

def parse_request_line(b: bytearray) -> tuple[RequestLine, int, str]:
    try:
        idx = bytearray.index(b, SEPARATOR)
    except ValueError:
        # havent first found \r\n, not able to parse start line
        return RequestLine(), 0, NO_ERROR

    start_line = b[:idx]
    read = idx

    parts = bytearray.split(start_line, " ".encode())
    
    # if we dont have method, path and http protocol
    if len(parts) != 3:
        return RequestLine(), 0, ERROR_MALFORMED_REQUEST_LINE
    
    http_parts = bytearray.split(parts[2], "/".encode())

    if len(http_parts) != 2 or http_parts[0].decode() != "HTTP" or http_parts[1].decode() != "1.1":
        return RequestLine(), 0, ERROR_MALFORMED_REQUEST_LINE

    request_line = RequestLine(method=parts[0].decode(), request_target=parts[1].decode(), http_version=http_parts[1].decode())
    
    return request_line, read, NO_ERROR

def request_from_reader(reader) -> Request:
    request = Request(request_line=RequestLine(), headers=Headers(), state=ParserState.INIT)

    buf = bytearray(1024)
    buf_len = 0
    
    while not request.done():
        mv = memoryview(buf)[buf_len:]
        n, err = reader.read(mv)
        # n = 3 - err = None
        if err != None:
            return request
        
        buf_len += n
        
        readN = request.parse(buf[:buf_len])
        
        buf[:buf_len - readN] = buf[readN:buf_len]
        buf_len -= readN
    
    return request

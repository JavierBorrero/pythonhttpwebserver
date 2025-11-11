rn = "\r\n".encode()
NO_ERROR = ""
ERROR_MALFORMED_FIELD_LINE = "malformed field line"
ERROR_MALFORMED_FIELD_NAME = "malformed field name"
ERROR_INVALID_TOKEN = "invalid token in field name"

class Headers:
    headers: dict[str, str]
    
    def __init__(self, data: dict[str, str] | None = None)-> None:
        if data is None:
            data = {}
        self.headers = data

    def get(self, name: str) -> str:
        return self.headers[name.lower()]

    def set(self, name: str, value: str):
        name = name.lower()

        try:
            v = self.headers[name]

            if v:
                self.headers[name] = f"{v},{value}"
        except:
            self.headers[name] = value


    def parse(self, data: bytearray) -> tuple[int, bool, str]:
        read = 0
        done = False

        while True:
            try:
                idx = bytearray.index(data[read:], rn)
            except ValueError:
                break
            
            # Empty header
            if idx == 0:
                done = True
                read += len(rn)
                break

            name, value, err = parse_header(data[read:read+idx])
            if err != NO_ERROR:
                return 0, False, err

            if not is_token(name.encode()):
                return 0, False, ERROR_INVALID_TOKEN

            read += idx + len(rn)
            #self.headers[name] = value
            self.set(name, value)

        return read, done, NO_ERROR

def parse_header(field_line: bytearray) -> tuple[str, str, str]:

    parts = bytearray.split(field_line, ":".encode(), 1)

    if len(parts) != 2:
        return "", "", ERROR_MALFORMED_FIELD_LINE

    name = parts[0]
    value = parts[1].decode().strip()

    if bytearray.endswith(name, " ".encode()):
        return "", "", ERROR_MALFORMED_FIELD_NAME

    return name.decode(), value, NO_ERROR

def is_token(str: bytes) -> bool:

    for b in str:
        ch = chr(b)
        match ch:
            case _ if ch.isalpha():
                continue
            case _ if ch.isdigit():
                continue
            case "!" | "#" | "$" | "%" | "&" | "'" | "*" | "+" | "-" | "." | "^" | "_" | "`" | "|" | "~":
                continue
            case _:
                return False

    return True

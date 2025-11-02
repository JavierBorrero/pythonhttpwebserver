rn = "\r\n".encode()
NO_ERROR = ""
ERROR_MALFORMED_FIELD_LINE = "malformed field line"
ERROR_MALFORMED_FIELD_NAME = "malformed field name"

class Headers:
    data: dict[str, str]
    
    def __init__(self, data: dict[str, str] = {}) -> None:
        self.data = data

    def parse(self, data: bytearray) -> tuple[int, bool]:
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
                return 0, False

            read += idx + len(rn)
            self.data[name] = value

        return read, done

def parse_header(field_line: bytearray) -> tuple[str, str, str]:

    parts = bytearray.split(field_line, ":".encode(), 1)

    if len(parts) != 2:
        return "", "", ERROR_MALFORMED_FIELD_LINE

    name = parts[0]
    value = parts[1].decode().strip()

    if bytearray.endswith(name, " ".encode()):
        return "", "", ERROR_MALFORMED_FIELD_NAME

    return name.decode(), value, NO_ERROR

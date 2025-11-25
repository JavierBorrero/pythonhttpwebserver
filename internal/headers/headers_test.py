import unittest

from headers import ERROR_INVALID_TOKEN, ERROR_MALFORMED_FIELD_LINE, ERROR_MALFORMED_FIELD_NAME, Headers

class TestRequest(unittest.TestCase):
    def test_header_parse(self):
        
        # Valid single header
        headers = Headers()
        data = bytearray("Host: localhost:1234\r\nTestTest:    msgmsg    \r\n\r\n".encode())
        n, done, err = headers.parse(data)
        self.assertEqual("", err)
        self.assertEqual("localhost:1234", headers.get("HOST"))
        self.assertEqual("msgmsg", headers.get("TestTest"))
        self.assertEqual(49, n)
        self.assertTrue(done)

        # Invalid spacing header
        headers = Headers()
        data = bytearray("      Host : localhost:1234       \r\n\r\n".encode())
        n, done, err = headers.parse(data)
        self.assertEqual(err, ERROR_MALFORMED_FIELD_NAME)
        self.assertEqual(0, n)
        self.assertFalse(done)

        # Invalid field name token
        headers = Headers()
        data = bytearray("H@st: localhost:1234\r\n\r\n".encode())
        n, done, err = headers.parse(data)
        self.assertEqual(err, ERROR_INVALID_TOKEN)
        self.assertEqual(0, n)
        self.assertFalse(done)

        # Valid multiple field values
        headers = Headers()
        data = bytearray("Host: localhost:1234\r\nHost: localhost:1234\r\n".encode())
        n, done, err = headers.parse(data)
        self.assertEqual("localhost:1234,localhost:1234", headers.get("HOST"))
        self.assertEqual(44, n)
        self.assertFalse(done)

if __name__ == '__main__':
    unittest.main()

import unittest

from headers import Headers

class TestRequest(unittest.TestCase):
    def test_header_parse(self):
        
        # Valid single header
        headers = Headers()
        data = bytearray("Host: localhost:1234\r\nTestTest:    msgmsg    \r\n\r\n".encode())
        n, done = headers.parse(data)
        self.assertEqual("localhost:1234", headers.get("HOST"))
        self.assertEqual("msgmsg", headers.get("TestTest"))
        self.assertEqual(49, n)
        self.assertTrue(done)

        # Invalid spacing header
        headers = Headers()
        data = bytearray("      Host : localhost:1234       \r\n\r\n".encode())
        n, done = headers.parse(data)
        self.assertEqual("localhost:1234", headers.get("HOST"))
        self.assertEqual(0, n)
        self.assertFalse(done)

        # Invalid spacing header
        headers = Headers()
        data = bytearray("H@st: localhost:1234\r\n\r\n".encode())
        n, done = headers.parse(data)
        self.assertEqual("localhost:1234", headers.get("HOST"))
        self.assertEqual(0, n)
        self.assertFalse(done)

if __name__ == '__main__':
    unittest.main()

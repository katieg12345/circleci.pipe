import unittest
import requests

class TestReach(unittest.TestCase):

    def test_reach(self):
        url = "http://127.0.0.1:8080"
        try:
            response = requests.get(url)
            print (response, flush=True)
            self.assertEqual(response.status_code, 200)
        except:
            self.fail("Website is not reachable")

if __name__ == '__main__':
    unittest.main()

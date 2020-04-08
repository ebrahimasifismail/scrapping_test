import sys, os, unittest, requests
sys.path.append(os.path.abspath('..'))
from myworker import MyWorker


class TestCase(unittest.TestCase):

    def test_url(self):
        response = requests.get("https://gist.github.com/discover?page=1")
        self.assertEqual(200, response.status_code)


    def check_my_worker_response(self):
        response_data = MyWorker(['.*?function', '.*?def', '.*?php', '.*?class', '.*?import', '.*?from', '.*?div'], 10).run()
        self.assertEqual(1, response_data.response_code)

    def check_my_worker_response_data(self):
        response_data = MyWorker(['.*?function', '.*?def', '.*?php', '.*?class', '.*?import', '.*?from', '.*?div'], 10).run()
        self.assertGreaterEqual(len(response_data.data), 1)

if __name__ == '__main__': 
    unittest.main() 
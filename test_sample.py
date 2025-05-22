import unittest
import subprocess

class TestSample(unittest.TestCase):
    def test_hello_world(self):
        # Run sample.py and capture its output
        result = subprocess.run(['python', 'sample.py'], capture_output=True, text=True)
        # Assert that the output is "Hello, world!"
        self.assertEqual(result.stdout.strip(), "Hello, world!")

if __name__ == '__main__':
    unittest.main()

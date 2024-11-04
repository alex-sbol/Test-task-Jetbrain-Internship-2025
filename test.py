import unittest
import time
from program_B import ProgramB, calculate_median

class TestProgramB(unittest.TestCase):
    def setUp(self):
        self.program_b = ProgramB()
        self.program_b.start_process()

    def tearDown(self):
        if self.program_b.process is not None:
            self.program_b.stop_process()

    def test_hi_command(self):
        response = self.program_b.send_message('Hi')
        self.assertEqual(response, 'Hi')

    def test_getrandom_command(self):
        response = self.program_b.send_message('GetRandom')
        self.assertIsNotNone(response)
        try:
            number = int(response)
            self.assertTrue(0 <= number <= 100)
        except ValueError:
            self.fail(f"Response is not a valid integer: {response}")

    def test_shutdown_command(self):
        self.program_b.send_message('Shutdown')
        time.sleep(0.5)  # Allow time for the process to shut down
        self.assertIsNotNone(self.program_b.process.poll())

    def test_calculate_median(self):
        self.assertEqual(calculate_median([1, 3, 5]), 3)
        self.assertEqual(calculate_median([1, 3, 5, 7]), 4)
        self.assertIsNone(calculate_median([]))
        self.assertEqual(calculate_median([42]), 42)

if __name__ == '__main__':
    unittest.main()

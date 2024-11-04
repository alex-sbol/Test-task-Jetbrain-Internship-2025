import subprocess
import time
import sys
from typing import Optional

class ProgramB:
    def __init__(self, path_to_program_a: str = "program_a.py") -> None:
        """Initialize ProgramB with the path to Program A."""
        self.path_to_program_a = path_to_program_a
        self.process: Optional[subprocess.Popen] = None

    def start_process(self) -> None:
        """Start Program A as a subprocess."""
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.path_to_program_a],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Program A started successfully.")
        except Exception as e:
            print(f"Failed to start Program A: {e}")
            self.process = None

    def send_message(self, message: str, timeout: int = 10) -> Optional[str]:
        """Send a message to Program A and receive a response.

        Args:
            message: The command to send to Program A.
            timeout: Maximum time to wait for a response in seconds.

        Returns:
            The response from Program A, or None if no response was received.
        """
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("Program A is not running.")

        try:
            # Send command to Program A
            self.process.stdin.write(message + '\n')
            self.process.stdin.flush()

            # Read the response within a timeout
            start_time = time.time()
            while True:
                if time.time() - start_time > timeout:
                    raise TimeoutError("Response from Program A timed out")

                response = self.process.stdout.readline()
                if response:
                    return response.strip()

                time.sleep(0.1)

        except BrokenPipeError:
            print("Broken pipe error: Program A might have crashed.")
            self.process = None
            return None
        except TimeoutError as e:
            print(e)
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def stop_process(self) -> None:
        """Send the Shutdown command to Program A to terminate it."""
        if self.process:
            print("Sending Shutdown command to Program A...")
            self.send_message("Shutdown")
            try:
                self.process.wait(timeout=2)
                print("Program A terminated.")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("Program A killed after timeout.")
            self.process = None

def calculate_median(numbers: list) -> Optional[float]:
    """Calculate the median of a list of numbers.

    Args:
        numbers: A sorted list of numbers.

    Returns:
        The median value, or None if the list is empty.
    """
    n = len(numbers)
    if n == 0:
        return None
    if n % 2 == 1:
        return numbers[n // 2]
    else:
        return (numbers[n // 2 - 1] + numbers[n // 2]) / 2

def main() -> None:
    """Main function to control Program A and process its outputs."""
    program_b = ProgramB()
    program_b.start_process()

    try:
        # Send "Hi" command and verify the response
        response = program_b.send_message('Hi')
        if response == 'Hi':
            print('Received correct response from Program A for "Hi" command.')
        else:
            print(f'Unexpected response for "Hi" command: {response}')

        # Retrieve 100 random numbers
        random_numbers = []
        for _ in range(100):
            response = program_b.send_message('GetRandom')
            if response is not None:
                try:
                    number = int(response)
                    random_numbers.append(number)
                except ValueError:
                    print(f'Invalid response for "GetRandom" command: {response}')
            else:
                print('No response received for "GetRandom" command.')

        # Send "Shutdown" command to terminate Program A
        program_b.stop_process()

        # Sort the numbers and print the sorted list
        sorted_numbers = sorted(random_numbers)
        print('Sorted random numbers:')
        print(sorted_numbers)

        # Calculate and print the median and average
        average = sum(sorted_numbers) / len(sorted_numbers)
        median = calculate_median(sorted_numbers)
        print(f'Average: {average}')
        print(f'Median: {median}')

    finally:
        if program_b.process is not None:
            program_b.stop_process()

if __name__ == "__main__":
    main()

import sys
import random

def get_random_int() -> int:
    """Generate a pseudo-random integer between 0 and 100."""
    return random.randint(0, 100)

def main() -> None:
    """Main loop to read commands from stdin, process them, and respond to stdout."""
    for line in sys.stdin:
        line = line.strip()  # Remove leading/trailing whitespace and newlines
        try:
            if line == "Shutdown":
                break
            elif line == "Hi":
                print("Hi")
                sys.stdout.flush()
            elif line == "GetRandom":
                print(get_random_int())
                sys.stdout.flush()
            else:
                # Ignore unknown commands
                pass
        except Exception as e:
            # Send error response
            error_response = {"status": "error", "message": str(e)}
            print(error_response)
            sys.stdout.flush()

    print("Program A has been shutdown")
    sys.stdout.flush()

if __name__ == "__main__":
    main()

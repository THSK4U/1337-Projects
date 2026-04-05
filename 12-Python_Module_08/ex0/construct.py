import sys
import os
import site


def main():
    if sys.prefix != sys.base_prefix:
        print("MATRIX STATUS: Welcome to the construct")
        print("\nCurrent Python:", sys.executable)
        print("Virtual Environment:", os.path.basename(sys.prefix))
        print("Environment Path:", sys.prefix)

        print("""\nSUCCESS: You're in an isolated environment!
Safe to install packages without affecting
the global system.""")

        print("\nPackage installation path:")
        print(site.getsitepackages()[0])
    else:
        print("MATRIX STATUS: You're still plugged in")
        print("\nCurrent Python:", sys.executable)
        print("Virtual Environment: None detected")

        print("""\nWARNING: You're in the global environment!
The machines can see everything you install.

To enter the construct, run:
python -m venv matrix_env
source matrix_env/bin/activate # On Unix
matrix_env
Scripts
activate # On Windows

Then run this program again.""")


if __name__ == "__main__":
    main()

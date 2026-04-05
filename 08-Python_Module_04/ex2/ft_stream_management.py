import sys


def main():
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")

    in1 = input("Input Stream active. Enter archivist ID: ")
    in2 = input("Input Stream active. Enter status report: ")

    print()
    print(f"[STANDARD] Archive status from {in1}: {in2}", file=sys.stdout)
    print("[ALERT] System diagnostic: Communication channels verified",
          file=sys.stderr)
    sys.stdout.write("[STANDARD] Data transmission complete\n")
    print("\nThree-channel communication test successful.")


main()

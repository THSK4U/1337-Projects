def main():
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===")

    print()
    print("CRISIS ALERT: Attempting access to 'lost_archive.txt'...")
    try:
        with open(r"lost_archive.txt") as access:
            pass
    except FileNotFoundError:
        print("""RESPONSE: Archive not found in storage matrix
STATUS: Crisis handled, system stable""")

    print()
    print("CRISIS ALERT: Attempting access to 'classified_vault.txt'...")
    try:
        with open(r"classified_vault.txt") as access:
            pass
    except PermissionError:
        print("""RESPONSE: Security protocols deny access
STATUS: Crisis handled, security maintained""")

    print()
    print("ROUTINE ACCESS: Attempting access to 'standard_archive.txt'...")
    try:
        with open(r"data-generator-tools/standard_archive.txt") as access:
            print(f"SUCCESS: Archive recovered - '{access.read()}'")
        print("STATUS: Normal operations resumed")
    except (PermissionError, FileNotFoundError):
        print("""RESPONSE: Security protocols deny access
RESPONSE: Archive not found in storage matrix""")

    print()
    print("All crisis scenarios handled successfully. Archives secure.")


main()

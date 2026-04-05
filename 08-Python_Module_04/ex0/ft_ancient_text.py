def main():
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===")
    fd = open(r"data-generator-tools/ancient_fragment.txt", "r")
    print(f"""
Accessing Storage Vault: {fd.name}
Connection established...""")

    read_file = fd.read()
    print(f"""
RECOVERED DATA:
{read_file}""")

    print("Data recovery complete. Storage unit disconnected.")
    fd.close()


main()

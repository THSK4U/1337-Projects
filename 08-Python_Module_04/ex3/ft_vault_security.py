def main():
    print("""=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===
Initiating secure vault access...
Vault connection established with failsafe protocols
""")
    with open(r"data-generator-tools/classified_data.txt", "r") as f:
        print(f"SECURE EXTRACTION:\n{f.read()}")

    with open(r"data-generator-tools/classified_data.txt", "w") as f:
        f.write("[CLASSIFIED] New security protocols archived\n")

    with open(r"data-generator-tools/classified_data.txt") as r:
        print(f"""SECURE PRESERVATION:
{r.read()}
Vault automatically sealed upon completion\n""")

    print("All vault operations completed with maximum security.")


main()

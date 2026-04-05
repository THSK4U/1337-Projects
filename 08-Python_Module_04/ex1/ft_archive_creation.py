data_list = ["New quantum algorithm discovered",
             "Efficiency increased by 347%",
             "Archived by Data Archivist trainee"]


def main():
    i = 1
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===")
    fd = open(r"new_discovery.txt", "w")

    print(f"""
Initializing new storage unit: {fd.name}
Storage unit created successfully...""")
    print("\nInscribing preservation data...")
    for data in data_list:
        fd.write(f"[ENTRY 00{i}] {data}\n")
        print(f"[ENTRY 00{i}] {data}")
        i += 1

    fd.close()
    print(f"""
Data inscription complete. Storage unit sealed.
Archive '{fd.name}' ready for long-term preservation.""")


main()

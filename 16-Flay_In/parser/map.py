def read_map(path_file: str) -> dict[str, list]:
    """Reads and parses the raw text file of a map.

    Args:
        path_file (str): The absolute or relative path to the map file.

    Returns:
        dict[str, list]: A dictionary where keys are the map configuration
            variables (e.g., 'hub', 'connection') and values are lists
            of their string definitions.
    """
    lines = []
    dict_lines: dict[str, list] = {}
    with open(path_file, mode="r") as f:
        lines = [line.rstrip() for line in f]
        if not lines:
            raise ValueError("Map file is empty.")

    for line in lines:
        if line and not line.startswith("#") and ":" in line:
            key = line.split(": ")
            if not len(key) == 2:
                raise ValueError("Invalid line format. Use 'key: value'.")
            if key[0] in dict_lines:
                dict_lines[key[0]].append(key[1])
            else:
                dict_lines[key[0]] = [key[1]]
    return dict_lines

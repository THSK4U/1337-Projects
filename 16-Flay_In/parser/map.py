from parser.exceptions import InvalidSyntax, MapError


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
            raise MapError("Map file is empty.")

    for index, line in enumerate(lines, start=1):
        if line and not line.startswith("#") and ":" in line:
            key = line.split(": ")
            if not len(key) == 2:
                raise InvalidSyntax(
                    index,
                    f"Invalid line format. Use 'key: value'. Got: '{line}'")
            if key[0] in dict_lines:
                dict_lines[key[0]].append((index, key[1]))
            else:
                dict_lines[key[0]] = [(index, key[1])]
        elif not line or line.startswith('#'):
            continue
        else:
            raise InvalidSyntax(
                index,
                f"Invalid line format. Use 'key: value'. Got: '{line}'")
    return dict_lines

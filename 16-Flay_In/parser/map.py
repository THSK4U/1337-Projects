def read_map(path_file: str) -> dict[str, list]:
    lines = []
    dict_lines = {}
    with open(path_file, mode="r") as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        if line and not line.startswith("#") and ":" in line:
            key = line.split(": ")
            if key[0] in dict_lines:
                dict_lines[key[0]].append(key[1])
            else:
                dict_lines[key[0]] = [key[1]]
    return dict_lines


if __name__ == "__main__":
    dict_lines = read_map(r"/home/tsellak/FLY/maps/hard/01_maze_nightmare.txt")
    print(dict_lines.keys())

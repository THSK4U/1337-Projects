import math
import sys


def create_position(x, y, z):
    return (x, y, z)


def distance_between(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def parsing_coord(coord):
    parts = coord.split(',')
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError as e:
        print(f"Error parsing coordinate: {e}")
        print(f"Error details - Type: ValueError, Args: {e.args}")


def main():
    print("=== Game Coordinate System ===")
    pos1 = (0, 0, 0)
    if len(sys.argv) > 1:
        coord_str = sys.argv[1]
        print(f"\nParsing coordinates: \"{coord_str}\"")
        parsed_pos = parsing_coord(coord_str)
        if parsed_pos:
            print(f"Parsed position: {parsed_pos}")
            print(f"Distance between {pos1} and {parsed_pos}:",
                  f" {distance_between(pos1, parsed_pos):.2f}")
    else:
        pos = create_position(10, 20, 5)
        print(f"\nPosition created: {pos}")
        print(f"Distance between {pos1} and {pos}:",
              f"{distance_between(pos1, pos):.2f}")

        coord_str = "3,4,0"
        print(f"\nParsing coordinates: \"{coord_str}\"")
        parsed_pos = parsing_coord(coord_str)
        print(f"Parsed position: {parsed_pos}")
        if parsed_pos:
            print(f"Distance between {pos1} and {parsed_pos}:",
                  f" {distance_between(pos1, parsed_pos)}")

        coord_str = "abc,def,gh"
        print(f"\nParsing invalid coordinates: \"{coord_str}\"")
        parsing_coord(coord_str)

    if parsed_pos:
        print("\nUnpacking demonstration:")
        print("Player at ", end="")
        print(f"x={parsed_pos[0]}, y={parsed_pos[1]}, z={parsed_pos[2]}")
        print("Coordinates: ", end="")
        print(f"X={parsed_pos[0]}, Y={parsed_pos[1]}, Z={parsed_pos[2]}")


main()

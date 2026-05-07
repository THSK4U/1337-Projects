from parser.exceptions import PathNotFound
from parser.solver import solver
from parser import visualizer
from parser import parser

files = {
    "easy": [
        {"1": "./maps/easy/01_linear_path.txt"},
        {"2": "./maps/easy/02_simple_fork.txt"},
        {"3": "./maps/easy/03_basic_capacity.txt"},
    ],
    "medium": [
        {"1": "./maps/medium/01_dead_end_trap.txt"},
        {"2": "./maps/medium/02_circular_loop.txt"},
        {"3": "./maps/medium/03_priority_puzzle.txt"},
    ],
    "hard": [
        {"1": "./maps/hard/01_maze_nightmare.txt"},
        {"2": "./maps/hard/02_capacity_hell.txt"},
        {"3": "./maps/hard/03_ultimate_challenge.txt"},
    ],
    "challenger": [
        {"1": "./maps/challenger/01_the_impossible_dream.txt"}
    ],
}


def choose_map() -> str:
    """Displays a CLI menu allowing the user to select the simulation map.

    Returns:
        str: The absolute file path of the chosen map file.
    """
    print("\n--- Flay_IN Maps Menu ---")
    menu_items: list[str] = []
    idx = 1
    for category, map_list in files.items():
        print(f"\n[{category.capitalize()}]")
        for map_dict in map_list:
            for key, path in map_dict.items():
                name = path.split('/')[-1]
                print(f"  {idx}. {name}")
                menu_items.append(path)
                idx += 1

    while True:
        try:
            prompt = (f"\nEnter the number of the map you want "
                      f"to run (1-{len(menu_items)}): ")
            choice = input(prompt)
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(menu_items):
                return menu_items[choice_idx]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            exit(0)


def choose_visual() -> int:
    """CLI menu allowing the user to select the output format mode."""
    print('''\n--- Simulation Mode ---\n
    1. Visual (Arcade)
    2. See all Maps turn''')
    while True:
        try:
            choice_idx = int(input(
                "\nEnter the number of type visualizer you need (1 or 2): "))
            if 0 < choice_idx < 3:
                return choice_idx
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            exit(0)


def main() -> None:
    """The main entry point bridging user inputs, map parsing and solving."""
    try:

        # visual_idx = choose_visual()

        # if visual_idx == 1:

        # path_file = choose_map()
        path_file = files['easy'][1]['2']
        print(f"\nRunning map: {path_file}")

        graph_dict = parser.Graph(path_file)
        solve = solver(graph_dict)

        path_solve = solve.get_path(k=4)

        if len(path_solve):
            best_path = path_solve[min(path_solve)]
        else:
            raise PathNotFound("No valid path found.")

        move_drones = solve.solve(best_path)

        # visualizer.start_graph(graph_dict, move_drones)

        # elif visual_idx == 2:
        #     for file in files:
        #         print(file)
        #         for path_dict in files[file]:
        #             for key, value in path_dict.items():
        #                 path_file = value

        #                 graph_dict = parser.Graph(path_file)
        #                 solve = solver(graph_dict)

        #                 path_solve = solve.get_path(k=4)

        #                 if len(path_solve):
        #                     best_path = path_solve[min(path_solve)]
        #                 else:
        #                     raise PathNotFound("No valid path found.")

        #                 move_drones = solve.solve(best_path)

    except Exception as e:
        print(f"Error: {e}")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        exit(0)


if __name__ == "__main__":
    main()

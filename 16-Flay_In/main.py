from parser.solver import solver
from parser import visualizer
from parser import parser

files = {
    "easy": [
        {"1": "/home/tsellak/FL/maps/easy/01_linear_path.txt"},
        {"2": "/home/tsellak/FL/maps/easy/02_simple_fork.txt"},
        {"3": "/home/tsellak/FL/maps/easy/03_basic_capacity.txt"},
    ],
    "medium": [
        {"1": "/home/tsellak/FL/maps/medium/01_dead_end_trap.txt"},
        {"2": "/home/tsellak/FL/maps/medium/02_circular_loop.txt"},
        {"3": "/home/tsellak/FL/maps/medium/03_priority_puzzle.txt"},
    ],
    "hard": [
        {"1": "/home/tsellak/FL/maps/hard/01_maze_nightmare.txt"},
        {"2": "/home/tsellak/FL/maps/hard/02_capacity_hell.txt"},
        {"3": "/home/tsellak/FL/maps/hard/03_ultimate_challenge.txt"},
    ],
    "challenger": [
        {"1": "/home/tsellak/FL/maps/challenger/01_the_impossible_dream.txt"}
    ],
}


def main() -> None:
    # path_file = files['challenger'][0]['1']

    # graph_dict = parser.Graph(path_file)
    # solve = solver(graph_dict)

    # path_solve = solve.get_path(k=4)

    # # print(path_solve)

    # if len(path_solve):
    #     path_solve = path_solve[min(path_solve)]
    #     # print(path_solve)
    # else:
    #     raise

    # move_drones = solve.solve(path_solve)

    # visualizer.start_graph(graph_dict, move_drones)

    for file in files:
        print(file)
        for path_dict in files[file]:
            for key, value in path_dict.items():
                path_file = value

                graph_dict = parser.Graph(path_file)
                solve = solver(graph_dict)

                path_solve = solve.get_path(k=4)

                if len(path_solve):
                    path_solve = path_solve[min(path_solve)]
                else:
                    raise

                move_drones = solve.solve(path_solve)


if __name__ == "__main__":
    main()

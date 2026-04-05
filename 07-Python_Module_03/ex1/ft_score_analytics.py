import sys

i = 1
len_argv = len(sys.argv)
print("=== Player Score Analytics ===")

if len_argv > 1:
    score = []
    try:
        while len_argv > i:
            score += [int(sys.argv[i])]
            i += 1

        print("Scores processed:", score)
        print("Total players:", len(score))
        print("Total score:", sum(score))
        print("Average score:", sum(score) / len(score))
        print("High score:", max(score))
        print("Low score:", min(score))
        print("Score range:", max(score) - min(score))
    except ValueError:
        print("Use only numbers")
else:
    print(f"No scores provided. Usage: python3 {sys.argv[0]}",
          " <score1> <score2> ...")

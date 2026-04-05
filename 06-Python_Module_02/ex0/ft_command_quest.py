import sys

i = 1
len_argv = len(sys.argv)
print("=== Command Quest ===")

if len_argv < 2:
    print("No arguments provided!")
print("Program name:", sys.argv[0])

if len_argv > 1:
    print("Arguments received:", (len_argv - 1))

while i < len_argv:
    print(f"Argument {i}: {sys.argv[i]}")
    i += 1

print("Total arguments:", len_argv)

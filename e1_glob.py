# Experiment 1: the `glob` module — find files by a path pattern.
#
# glob.glob(pattern) returns a list of paths matching the pattern.
# `*` matches anything (within one path segment). So "*.txt" matches
# every .txt file in the current directory.
#
# Once you have the list of paths, iterate and `open()` each one to do
# something with the contents.

import glob


my_files = glob.glob("*.txt")
print(my_files)

for file_path in my_files:
    with open(file_path, "r") as file:
        print(file.read())

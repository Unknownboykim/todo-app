# Experiment 1: the `glob` module — find files by a path pattern.
#
# glob.glob(pattern) returns a list of paths matching the pattern.
# `*` matches anything (within one path segment). So "*.txt" matches
# every .txt file in the current directory.
#
# Once you have the list of paths, iterate and `open()` each one to do
# something with the contents.

# 147. Code Experiments - Experiment 1 (Section 15)
# Experiment 1: the `glob` module — find files by a path pattern.
#
# glob.glob(pattern) returns a list of paths matching the pattern.
# `*` matches anything (within one path segment). So "*.txt" matches
# every .txt file in the current directory.
#
# Once you have the list of paths, iterate and `open()` each one to do
# something with the contents.
#
# SECTION 15 FIX: the pattern is "files/*.txt" (not "*.txt"), so it
# reads the text files INSIDE the files folder (ideas.txt, projects.txt),
# like in the lecture. "*.txt" only found todos.txt.

import glob     # standard module: comes with Python, no install

my_files = glob.glob("files/*.txt")     # a LIST of paths
print(my_files)     # ['files/ideas.txt', 'files/projects.txt']

# Loop over the paths and print each file's text.
for file_path in my_files:
    with open(file_path, "r") as file:
        print(file.read())
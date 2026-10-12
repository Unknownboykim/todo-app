# Experiment 3: the `shutil` module — "shell utilities" for file ops
# like copying, moving, and creating archives.
#
# shutil.make_archive(base_name, format, root_dir) creates a zip/tar of
# the given directory. Here we zip up the current directory (".") into
# a file called "output.zip" (the ".zip" is added automatically).

# 147. Code Experiments - Experiment 3 (Section 15)
# Experiment 3: the `shutil` module — "shell utilities" for file ops
# like copying, moving, and creating archives.
#
# shutil.make_archive(base_name, format, root_dir) creates a zip/tar of
# the given directory. The ".zip" is added automatically.
#
# SECTION 15 FIX: zips the "files" folder (not "." = the whole project).
# Zipping "." put EVERYTHING in output.zip, even output.zip itself.

import shutil   # standard module


# base_name "output" -> output.zip, format "zip", root_dir "files"
shutil.make_archive("output", "zip", "files")

# Experiment 3: the `shutil` module — "shell utilities" for file ops
# like copying, moving, and creating archives.
#
# shutil.make_archive(base_name, format, root_dir) creates a zip/tar of
# the given directory. Here we zip up the current directory (".") into
# a file called "output.zip" (the ".zip" is added automatically).

import shutil


shutil.make_archive("output", "zip", ".")

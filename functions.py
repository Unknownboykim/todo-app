# =====================================================================
# functions.py  -  Todo app BACKEND, SECTION 15 version
# get_todos() reads todos.txt, write_todos() saves it. main.py imports
# this file:  import functions
# =====================================================================

# functions.py  (137. Organising the Code in Modules)
# Helper functions for the todo program. They were CUT from main.py and
# PASTED here. main.py brings them in with:
#     from functions import get_todos, write_todos
# On its own this file is a SCRIPT; when main.py imports it, it is a MODULE.
# This file must stay in the SAME folder as main.py.
#
# All comments below were moved here together with the two functions.
#
# FINAL CODE NOTES (day14.1):
#   - main.py uses  import functions  (way 2), so it calls
#     functions.get_todos() and functions.write_todos(todos).
#   - The parameter is named  filepath  (no underscore). It is the same
#     thing the comments below call file_path.
#   - get_todos uses  file_local  instead of  file  (no shadowing).
#   - Single quotes 'r' and 'w' work the same as "r" and "w".
#   - No test code at the bottom: the 138 experiment was removed.
#     (Section 15 version: the __name__ == "__main__" test IS kept at
#     the bottom, see the end of this file.)


# ---------------------------------------------------------------------
# 146: CONSTANT (Section 15)
# ---------------------------------------------------------------------
# The file name is written ONCE, here, and used as the default below.
# UPPERCASE name = a CONSTANT: a fixed value you don't reassign.
# Python's own standard modules use the same style (look at the top of
# time.py with Go To > Implementation(s)).
# To use a different file, change only this line.
FILEPATH = "todos.txt"


# Define the function at the top, outside the while loop.
# Remember: def + name + () + colon.
# file_path inside the () is the PARAMETER (117). It's a LOCAL
# variable that gets its value from the call: get_todos("todos.txt")
# sets file_path = "todos.txt".
# 127: file_path="todos.txt" is a DEFAULT. Calling get_todos() with no
# argument uses "todos.txt".
# Final code: the parameter is named filepath (same as file_path).
# 146: the default is now the constant FILEPATH (same value).
def get_todos(filepath=FILEPATH):
    # 128: DOCSTRING. First line inside the function, triple quotes.
    # help(get_todos) shows it.
    """ Read a text file and return the list of
    to-do items.
    """
    # 4 spaces: this line belongs to the function.
    # Open todos.txt in read mode ("r"). Read mode only — the write
    # ("w") blocks below are NOT the same code and are NOT replaced.
    # file_path replaces the hardcoded "todos.txt" (117), so the CALLER
    # decides which file to open.
    # Final code: filepath, single quotes 'r', and file_local instead of
    # file. file_local avoids shadowing any other `file` name (the same
    # SHADOWING idea as todos_local). Works exactly the same.
    with open(filepath, 'r') as file_local:
        # 8 spaces: 4 for the function + 4 for the with block.
        # readlines() returns a list, e.g. ["Study\n", "Exercise\n"]
        # todos_local is LOCAL: it only exists inside get_todos().
        # Named todos_local (not todos) to avoid shadowing the outer
        # `todos` variable used in the loop.
        # Final code: file_local.readlines() because the file object is
        # now called file_local.
        todos_local = file_local.readlines()
    # Back to 4 spaces: the with block is over (file is closed), but
    # we're still inside the function.
    # return hands the list back to whoever CALLED get_todos().
    # Be careful: return the SAME name you created (todos_local).
    return todos_local


# SECOND function (118). TWO parameters, separated by a comma:
#   file_path -> WHERE to write
#   todos_arg -> WHAT to write (the list)
# Both are LOCAL. todos_arg (not todos) avoids shadowing the global todos.
# 127: ORDER SWAPPED. todos_arg (non-default) must come FIRST,
# file_path (default) AFTER. Otherwise: SyntaxError.
# Final code: filepath (same as file_path).
# 146: the default is now the constant FILEPATH (same value).
def write_todos(todos_arg, filepath=FILEPATH):
    # 128: DOCSTRING (short, so one line).
    # Final code wording: "in the text file" (same meaning).
    """ Write the to-do items list in the text file."""
    # Open the file in write mode ("w"). file_path replaces the
    # hardcoded "todos.txt".
    # Final code: filepath and single quotes 'w'.
    with open(filepath, 'w') as file:
        # Write the list that was passed in (the tennis ball).
        file.writelines(todos_arg)
    # NO return: this is a PROCEDURE. It changes the file and gives
    # nothing back (Python returns None automatically).


# Two blank lines above: style recommendation after a function.


# 138. Code Experiments
# (Done in the lecture, then REMOVED: the final code has nothing below
# the two functions. The guard lines are kept here as comments only.)
#
# Top-level code in a module runs WHEN THE MODULE IS IMPORTED. If you
# write `print("hello from functions")` here at module level (not inside
# a def), that line runs as soon as main.py does `from functions import ...`.
# Usually that's not what you want for test code.
#
# The fix is the __name__ == "__main__" guard. __name__ is a hidden
# string variable Python creates in every file:
#
#     - When you run THIS file directly:   __name__ == "__main__"
#     - When this file is imported:        __name__ == "functions"
#
# So code under the guard only runs when you click Run on functions.py.
# The def lines above are OUTSIDE the if, so the functions still load
# on import.
#
# Phone: call it directly and it rings; another app using it in the
# background keeps it silent.
#
#   Run functions.py -> prints "hello from functions" and the todo list
#   Run main.py      -> these two lines are SKIPPED, app starts clean
# if __name__ == "__main__":
#     print("hello from functions")
#     # Quick smoke test you might run while developing this file:
#     print(get_todos())



# Top-level code in a module runs WHEN THE MODULE IS IMPORTED. If you
# write `print("hello from functions")` here at module level, that line
# runs as soon as `main.py` does `from functions import ...`. Usually
# that's not what you want for ad-hoc test code.
#
# The fix is the __name__ == "__main__" guard:
#
#     - When you run THIS file directly:   __name__ == "__main__"
#     - When this file is imported:        __name__ == "functions"
#
# So code under the guard only runs when this module is the entrypoint.
# That makes it the perfect place for quick tests / demo prints that
# you only want when developing the module.

if __name__ == "__main__":
    print("hello from functions")
    # Quick smoke test you might run while developing this file:
    print(get_todos())
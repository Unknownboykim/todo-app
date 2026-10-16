# =====================================================================
# functions.py  -  Todo app BACKEND, SECTION 18 version
# get_todos() reads todos.txt, write_todos() saves it.
# Two frontends import this file:  import functions
#   cli.py  -> the command line app (main.py, renamed in 156)
#   gui.py  -> the GUI app (156), working buttons in Section 17,
#              Complete/Exit, popups, clock and gui.exe in Section 18
# =====================================================================

# ---------------------------------------------------------------------
# SECTION 18: how gui.py uses this file (the code here is NOT changed)
# ---------------------------------------------------------------------
# 174 Complete: todos = functions.get_todos()     read the list
#               todos.remove(todo_to_complete)    delete the selected todo
#               functions.write_todos(todos)      save the list
# 174 Exit:     does not use this file (only break).
# 175 Popups, clock, theme: only gui.py changes. If nothing is selected,
#               the IndexError happens in gui.py (values["todos"][0])
#               BEFORE get_todos() is called, so this file never sees it.
# 176 Image buttons: only gui.py changes.
# 177 Bonus (zip extractor): uses zip_extractor.py, not this file.
#
# 180 Standalone executable (gui.exe):
#   - If todos.txt does NOT exist, open(filepath, 'r') in get_todos()
#     crashes with FileNotFoundError ("No such file or directory in
#     functions.py", line 47 of the 180 transcript).
#   - The fix is in gui.py, NOT here: gui.py runs
#         if not os.path.exists("todos.txt"):
#             with open("todos.txt", "w") as file:
#                 pass
#     BEFORE it calls functions.get_todos(), so the file always exists.
#   - PyInstaller packs this file INTO gui.exe automatically, because
#     gui.py has  import functions . You don't give functions.py to users.
#   - FILEPATH = "todos.txt" is a RELATIVE path: gui.exe reads and writes
#     todos.txt in the folder where gui.exe runs (the dist folder).
#   - The __name__ == "__main__" test at the bottom does NOT run inside
#     gui.exe, because there this file is IMPORTED (__name__ == "functions").

# ---------------------------------------------------------------------
# SECTION 17: how gui.py uses this file (the code here is NOT changed)
# ---------------------------------------------------------------------
# 165 Add:   todos = functions.get_todos()        read the list
#            todos.append(values["todo"] + "\n")  add the new todo
#            functions.write_todos(todos)         save the list
# 166 Edit:  todos = functions.get_todos()
#            index = todos.index(todo_to_edit)    find the old todo
#            todos[index] = new_todo + "\n"       replace it
#            functions.write_todos(todos)
# 166 List box: sg.Listbox(values=functions.get_todos(), ...)
#            the list box shows the list that get_todos() returns.
# No argument is passed: FILEPATH ("todos.txt") is the default.
# Each todo in the list ends with "\n" (readlines keeps it), which is why
# the GUI adds "\n" when it writes a new or edited todo.

# ---------------------------------------------------------------------
# 155: FRONTEND vs BACKEND (Section 16)
# ---------------------------------------------------------------------
# FRONTEND = the code that builds the user interface (what the user
#            sees and uses): cli.py (command line) or gui.py (GUI).
# BACKEND  = the code that does the processing: THIS file. It reads and
#            writes todos.txt and gives the data to the frontend in a
#            well-structured format: a Python list.
# This file has no input() and no print() for the user, so ANY frontend
# can use it. Section 16 does NOT change the code here: the GUI uses the
# exact same get_todos() and write_todos().
# That is why we wrote functions: if this code were still inside main.py,
# adding a GUI would be a mess. With functions, the frontend and backend
# are DECOUPLED (separated), so one backend serves both interfaces.

# functions.py  (137. Organising the Code in Modules)
# Helper functions for the todo program. They were CUT from cli.py
# (called main.py until 156) and PASTED here. cli.py brings them in with:
#     from functions import get_todos, write_todos
# On its own this file is a SCRIPT; when cli.py imports it, it is a MODULE.
# This file must stay in the SAME folder as cli.py.
#
# All comments below were moved here together with the two functions.
#
# FINAL CODE NOTES (day14.1):
#   - cli.py uses  import functions  (way 2), so it calls
#     functions.get_todos() and functions.write_todos(todos).
#   - The parameter is named  filepath  (no underscore). It is the same
#     thing the comments below call file_path.
#   - get_todos uses  file_local  instead of  file  (no shadowing).
#   - Single quotes 'r' and 'w' work the same as "r" and "w".
#   - No test code at the bottom: the 138 experiment was removed.
#     (Section 15-18 version: the __name__ == "__main__" test IS kept
#     at the bottom, see the end of this file.)


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
# a def), that line runs as soon as cli.py does `from functions import ...`.
# Usually that's not what you want for test code.
#
# The fix is the __name__ == "__main__" guard. __name__ is a hidden
# string variable Python creates in every file:
#
#     - When you run THIS file directly:   __name__ == "__main__"
#     - When this file is imported:        __name__ == "functions"

# So code under the guard only runs when you click Run on functions.py.
# The def lines above are OUTSIDE the if, so the functions still load
# on import.
#
# Phone: call it directly and it rings; another app using it in the
# background keeps it silent.
#
#   Run functions.py -> prints "hello from functions" and the todo list
#   Run cli.py      -> these two lines are SKIPPED, app starts clean
#   Run gui.py      -> SKIPPED too (gui.py also imports this file)
# if __name__ == "__main__":
#     print("hello from functions")
#     # Quick smoke test you might run while developing this file:
#     print(get_todos())



# Top-level code in a module runs WHEN THE MODULE IS IMPORTED. If you
# write `print("hello from functions")` here at module level, that line
# runs as soon as `cli.py` does `from functions import ...`. Usually
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
# Persist the todos to disk so they survive between program runs.
# Concepts:
#   - open(path, mode) returns a file object.
#       mode "r" = read   "w" = write (overwrites)
#   - file.readlines()  -> returns a list, one string per line
#                          (each line keeps its trailing "\n")
#   - file.read()       -> returns the whole file as a single string
#   - file.writelines(list)  writes each string in the list to the file
#   - file.write(text)       writes a single string
#   - file.close()  always close when you're done with a file.
#                   (`with open(...)` closes it for you automatically.)
#
# IMPORTANT: opening with "w" wipes the file. So the "add" handler must
# first READ the existing todos, append the new one to the list, and
# only THEN write the whole list back. Each todo needs a trailing "\n"
# so they end up on separate lines in the file.

# Strip the trailing "\n" from each todo before printing, so the output
# doesn't have blank lines between items.
# (The newlines come from the file — readlines() keeps them. print() also
#  adds its own newline, so each item ends up with two.)
#
# This lecture introduces LIST COMPREHENSIONS — a one-line way to build
# a new list by applying an expression to every item of another iterable.
#
# General shape:
#     [<expression>  for <item>  in <iterable>]
#
# Equivalent for-loop version:
#     new_todos = []
#     for item in todos:
#         new_todos.append(item.strip("\n"))
#
# Ardit shows both ways in the lecture, and points out that for this
# specific case you could also just do `item = item.strip("\n")` inside
# the existing for loop — but list comprehensions are the idiomatic tool
# whenever you want to transform a list into a new list.

# Experiments with COMMENTS in Python.
#
# A comment starts with `#` — everything after the hash on that line is
# ignored by the interpreter. Two main uses:
#
# 1. Disable a line of code without deleting it (e.g. to keep an
#    alternative implementation around for reference). PyCharm will
#    underline unused code, but a comment line stays out of the way.
#
# 2. Describe what a block of code does, when the code itself isn't
#    self-explanatory. Write the comment on the line ABOVE the code it
#    describes.
#
# Don't OVER-comment. A comment that just restates what the code obviously
# does is noise. Pick clear variable names and you'll need fewer comments.
# `todos` tells you exactly what the list holds; `data` would not.

# Each one now: reads the file, modifies the list, writes it back.
#
# Edit case:
#   1. Get the todo number to edit, convert to int, subtract 1 for
#      0-based indexing.
#   2. Read existing todos from the file.
#   3. Ask for the new todo and replace todos[number] with it. Add a
#      trailing "\n" so it stays on its own line in the file.
#   4. Write the updated list back.
#
# Complete case:
#   1. Get the todo number to complete, convert to int, subtract 1.
#   2. Read existing todos.
#   3. Grab the text of the todo being removed (strip the newline so the
#      message is clean), then pop it from the list.
#   4. Write the updated list back.
#   5. Print a "Todo X was removed from the list." confirmation.

# Goal: let the user type the action AND its argument on one line —
# e.g. "add play chess" instead of being prompted twice.
#
# Why match-case can't do this:
#   `case "add" in user_action:` is a SYNTAX error.
#   `case` only accepts literal patterns (like the string "add"), not
#   expressions like `"add" in user_action`.
# So we switch from match-case to if/elif blocks, which DO accept
# arbitrary boolean expressions as their conditions.

# Optimization: use elif so only ONE branch runs per iteration. With
# plain `if`s, Python checks every condition even after one matched —
# wasted work.
#
# How if / elif / else works:
#   - Python checks the conditions from TOP to BOTTOM.
#   - The FIRST condition that is True runs, and all the rest are
#     SKIPPED (not even checked).
#   - If NONE of them is True, the `else` block runs.
#
# Example: the user types "complete 2"
#   starts with "add"?       No  -> check the next one
#   starts with "show"?      No  -> check the next one
#   starts with "edit"?      No  -> check the next one
#   starts with "complete"?  YES -> run this block, skip "exit" and else
#
# Tip: because conditions are checked top-down, put the command users
# type MOST OFTEN at the top. Fewer checks = faster program.
#
# Also: extend the same single-line pattern to edit and complete:
#   "edit 2"      -> user_action[5:] -> "2"
#   "complete 2"  -> user_action[9:] -> "2"
# Wrap with int() to turn the slice into a number.
#
# Add an `else` branch for unrecognized commands so the user gets a
# clear "Command is not valid." message instead of silent failure.
#
# Rule: an if/elif/else block always STARTS with `if`. You can add as
# many `elif`s as you need, and at most ONE `else`, always at the end.

# Two bugs fixed in an earlier lecture.
#
# BUG 1 — Easy. Todos written to the file were missing a trailing "\n",
# so multiple todos ended up on a single line:
#     1-clean the bagfix the drawer        (wrong)
# Fix: add "\n" to the slice when adding (`+ "\n"` in the add branch).
#
# BUG 2 — Subtle. `"add" in user_action` checks if "add" appears
# ANYWHERE in the input. Typing "edit add a new member" ran the ADD
# branch (checked first) and saved " add a new member" as a NEW todo.
# Python showed NO error, just wrong output.
#
# Fix: use `user_action.startswith("add")`, which is True only when the
# text BEGINS with that word:
#   "edit add a new member".startswith("add")   -> False
#   "edit add a new member".startswith("edit")  -> True

# Use try/except to handle anticipated errors gracefully instead of
# crashing the program.
#
# Two specific errors:
#   - `ValueError` from int("fix bug") when the user types something
#     like "edit fix bug" instead of "edit 2".
#   - `IndexError` from todos[24] when the user references a todo
#     number that doesn't exist (e.g. "complete 23" with only 2 items).
#
# Pattern:
#     try:
#         risky_code()
#     except SomeError:
#         print("user-friendly message")
#         continue        # restart the while loop iteration
#
# How it works:
#   1. Python runs the code inside `try` line by line.
#   2. If NO error happens, the `except` part is skipped completely.
#   3. If an error DOES happen, Python stops the `try` part right there
#      (the lines after the error do NOT run) and jumps to `except`.
#   4. `except ValueError:` only catches ValueError. A different error
#      (like IndexError) is NOT caught and still crashes the program.
#
# `continue` is the opposite of `break` — it skips the rest of THIS
# iteration and goes back to the top of the loop. So after showing the
# error message, the user gets prompted again.
#
#   break     -> leave the loop completely   (program goes to "Bye!")
#   continue  -> jump back to the top        (asks for a command again)

# Introduce CUSTOM FUNCTIONS to remove repetitive code.
#
# The problem: REDUNDANCY. The same two-line block
#     with open("todos.txt", "r") as file:
#         todos = file.readlines()
# was repeated FOUR times (in add, show, edit and complete).
# Pull it into a function so each branch becomes one line:
#     todos = get_todos()
#
# Think of a function as a SLOT: you put some code inside it, give the
# slot a name, and then just CALL the name whenever you need that code.
#
# Function definition syntax:
#     def function_name():
#         body...
#         return some_value
#
#   def     -> keyword that starts a function definition
#   name    -> same rules as variable names:
#                no number at the start, no spaces, underscores are OK
#   ()      -> empty for now; functions that take ARGUMENTS come later
#   :       -> the body starts on the next line
#   body    -> indented 4 spaces (the recommendation)
#   return  -> a keyword; sends ONE value back out of the function
#
# Style: define functions at the TOP of the file, OUTSIDE the loop,
# and leave TWO blank lines between a function and the rest of the code.
#
# Function DEFINITION vs function CALL:
#   def get_todos(): ...     -> the DEFINITION (the instructions)
#   get_todos()              -> a CALL (run those instructions now)
#
# Built-ins like input(), open(), print() are also functions —
# `print("hi")` is a function CALL of a function defined elsewhere.
#
# Where are the built-ins defined? In the C language. C is the language
# the Python interpreter (the program you installed from python.org)
# is written in, so you can't see their code.
#   PyCharm: right-click open -> Go To -> Implementation(s)
#            shows only a DOCSTRING (the function's description) and
#            `pass`. That's a fake stand-in PyCharm makes, not real code.
#   help(open) in the Python console shows the same docstring.
# Later in the course you'll use functions that ARE written in Python.
#
# VARIABLE SCOPE (lecture example, separate file):
#     def greet():
#         message = "hello"
#         new_message = message.capitalize()
#         return new_message
#
#     greeting = greet()
#     print(greeting)        # OUTPUT: Hello
#     print(new_message)     # NameError: name 'new_message' is not defined
#
# Step by step:
#   1. greet() is called.
#   2. message gets "hello".
#   3. new_message gets "Hello" (capital H).
#   4. return sends "Hello" back out.
#   5. greeting = "Hello", and print shows it.
#
# Why the NameError? Variables created INSIDE a function are LOCAL —
# they only exist inside that function. Outside it, they don't exist.
#   local  -> created inside a function   (message, new_message)
#   global -> created outside functions   (greeting)
#
# Cafe analogy:
#   You say "I want a coffee."           -> the function CALL
#   Beans, machine, water, the process   -> the function's LOCAL variables
#   The cup of coffee handed to you      -> the RETURN value
# As the customer you only get the coffee, not the beans or the machine.
# Likewise you only get what `return` gives back, by CALLING the
# function — not by using its internal variable names.
#
# SHADOWING: the variable inside the function should NOT have the same
# name as a variable used in the outer code (PyCharm shows "shadows name
# from outer scope"). It's a recommendation, not an error. Renaming the
# function's local variable to `todos_local` (or refactoring with
# PyCharm: Refactor > Rename) keeps things unambiguous.
#
# In the lecture, `file` gets the same complaint (the loop below also
# uses `file`), and it's renamed to `file_local`. This file still uses
# `file` inside get_todos(), so PyCharm may underline it — the program
# works either way.


# Give `get_todos` a PARAMETER so the caller can choose which file to read.
#
# Coffee shop analogy: when a customer orders, they don't just say
# "coffee" — they also say "milk" or "sugar". Those extra words are
# inputs to the coffee-making process. Same idea here: the function
# can accept inputs that influence what it does.
#
# Terminology:
#   - PARAMETER: the name in the function definition (`file_path` below).
#   - ARGUMENT:  the value you pass when calling the function
#                (`"todos.txt"` in the calls below).
#
# You can pass the argument positionally — get_todos("todos.txt") — or
# by keyword — get_todos(file_path="todos.txt"). Both work; positional
# is shorter, keyword is more explicit.
#
# ---------------------------------------------------------------------
# From the lecture transcript (117. Optimising the Code)
# ---------------------------------------------------------------------
# Barista: when you say "coffee", the word coffee is the INPUT you give
# to the coffee-making process. The barista takes your input and
# returns the cup of coffee.
#
# Some functions get no input (get_todos() before this lecture).
# Some functions get input, also called ARGUMENTS.
#   input("Type add...")  -> input() gets an argument
#   print(row)            -> print() gets an argument
#
# What input should get_todos get? To give us the todos, it needs to
# know WHERE the file is: the file path.
#
# HARDCODED = the actual value is written in as a string, not a
# variable. Before this lecture, "todos.txt" was hardcoded inside the
# function:
#     with open("todos.txt", "r") as file:
# Better: turn it into a variable (a parameter) named file_path:
#     def get_todos(file_path):
#         with open(file_path, "r") as file:
# and give the value in each call:
#     todos = get_todos("todos.txt")
# This is done in all 4 calls (add, show, edit, complete).
#
# What happens when the script runs:
#   1. The interpreter reads the def like a RECIPE. It only checks the
#      syntax. It does NOT run the lines.
#   2. It runs the loop. When it reaches get_todos("todos.txt"), it
#      goes BACK to the def and runs those lines.
#   3. file_path is replaced with "todos.txt". Inside the function it's
#      as if this line were there (implicitly, you don't write it):
#          file_path = "todos.txt"
#      So file_path is a LOCAL variable.
#   4. The function opens the file, reads it, makes the list, returns
#      the list.
#   5. The list is captured in the todos variable.
#
# greet example with a parameter (test.py):
#     def greet(message):              # message is now a parameter
#         new_message = message.capitalize()
#         return new_message
#
#
#     greeting = greet("hi")
#     print(greeting)                  # OUTPUT: Hi
# message = "hello" was REMOVED from inside, so it's not hardcoded.
# Even lowercase "hi" comes out as "Hi" because of capitalize().
#
# Getting the value from the user instead:
#     user_entry = input("What greeting do you want? ")
#     greeting = greet(user_entry)
#     print(greeting)
# OUTPUT:
#     What greeting do you want? good afternoon
#     Good afternoon
#
# Terminology (as Ardit explains it):
#   def get_todos(file_path):        -> file_path is the PARAMETER
#   get_todos(file_path="todos.txt") -> file_path is the ARGUMENT,
#                                       "todos.txt" is the ARGUMENT VALUE
# (The header above calls "todos.txt" the argument. Same idea; Ardit
#  just separates the argument name from its value.)
#
# Naming the argument in the call is OPTIONAL:
#   get_todos("todos.txt")             -> shorter
#   get_todos(file_path="todos.txt")   -> more context for the reader
# There's no specific recommendation. Ardit leaves the name out because
# "todos.txt" is obviously a file path.
#
# Style:
#   get_todos(file_path="todos.txt")     -> recommended (no spaces)
#   get_todos(file_path = "todos.txt")   -> not recommended
#   todos = get_todos("todos.txt")       -> normal variable: spaces around =

#
# Add a SECOND function — `write_todos(file_path, todos_arg)` — to wrap
# the repeated 2-line write block.
#
# This function takes TWO arguments (multiple parameters separated by
# commas) and DOESN'T return anything. It's a PROCEDURE — its job is
# the side effect (writing to a file), not producing a return value.
# (Functions without `return` implicitly return `None`, which we don't
#  bother capturing.)
#
# Naming note: the argument is called `todos_arg` to avoid shadowing
# the outer `todos` variable.
#
# ---------------------------------------------------------------------
# From the lecture transcript (118. Optimising the Code Further)
# ---------------------------------------------------------------------
# Barista: the client can say MORE than "coffee", e.g. "milk" or
# "sugar". Those are MULTIPLE ARGUMENTS. The coffee is the result of
# all of them together.
#
# get_todos only needs ONE argument. The only thing that could change
# is the file path, so that's what comes from the outside. No more
# arguments are added to get_todos.
#
# Still repetitive: the 2 WRITE lines
#     with open("todos.txt", "w") as file:
#         file.writelines(todos)
# appear 3 times (add, edit, complete). So: a second function.
#   get_todos   -> GIVES us the todos
#   write_todos -> WRITES the todos in the file
#
# What does write_todos need to know from whoever calls it?
#   Program  = the CAFE (where everything happens)
#   The add block (the if branch) = the CLIENT that calls the function
#   The function = the coffee-making process
# To write todos in a file, it needs to know TWO things:
#   1. the file path          -> file_path
#   2. what to write in it    -> todos_arg (the list)
# Separate parameters with a comma: def write_todos(file_path, todos_arg):
#
# Parameters are LOCAL variables, so give them names different from the
# GLOBAL ones: todos_arg ("for argument's sake"), not todos.
# Then replace the literal "todos.txt" with file_path, and todos with
# todos_arg inside the function.
#
# Call: write_todos("todos.txt", todos)
#   -> NOT assigned to a variable, and the function has NO return.
#
# Why no return? It's a PROCEDURE. It modifies something (the text
# file) but we don't need any value back. It goes somewhere, does the
# job, and that's it.
#   todos = get_todos("todos.txt")    -> returns a list, so capture it
#   write_todos("todos.txt", todos)   -> returns nothing to capture
# A function with no return actually returns None, which is useless:
#   x = write_todos("todos.txt", todos)
#   print(x)                          # OUTPUT: None
#
# What happens on the call write_todos("todos.txt", todos):
#   1. The interpreter reads the def lines (syntax only, no running).
#   2. It runs the lines that are NOT in a function, top to bottom.
#   3. At the call, "todos.txt" becomes the value of file_path, and the
#      list in todos becomes the value of todos_arg. Both are arguments
#      AND local variables inside the function.
#
# Tennis ball: the list is a ball thrown from one person (variable) to
# another. First todos has it, then todos_arg has it, then the function
# places it in the text file.
#
# Complete, step by step:
#   1. The user enters the number of the todo to complete.
#   2. get_todos reads the existing todos into the todos list.
#   3. pop removes the todo, so the list is updated.
#   4. The list is sent to write_todos, which writes it to todos.txt.
#
# Benefit: no repetitive code. To change how reading or writing works,
# change it in ONE place (get_todos or write_todos), not everywhere.
#
# Terminology:
#   def write_todos(file_path, todos_arg):  -> PARAMETERS
#   write_todos(file_path="todos.txt", todos_arg=todos)
#       file_path=, todos_arg=  -> ARGUMENTS
#       "todos.txt", todos      -> ARGUMENT VALUES
# Naming the arguments is OPTIONAL; the goal is clean, readable code.
# Ardit leaves them out: "todos.txt" obviously looks like a file path.
#
# Style:
#   write_todos(file_path="todos.txt")    -> no spaces around = in a call
#   todos_local = file.readlines()        -> spaces around = for normal
#                                            variables (local or global)
#
# ---------------------------------------------------------------------
# SECTION 13: Flexible Functions (Default Arguments, Docstrings)
# ---------------------------------------------------------------------
# 127. Optimising the Code (DEFAULT ARGUMENTS)
#
# Barista: you say "I want a coffee", not "I want a coffee in a cup".
# The cup is the DEFAULT. "todos.txt" is always the file, so stop
# repeating it in every call.
#
# Syntax: give the parameter a value in the def:
#     def get_todos(file_path="todos.txt"):
# Call: todos = get_todos()   -> file_path = "todos.txt" automatically.
# Default argument = default parameter (same thing).
#
# Override: get_todos("todo1.txt") uses that file instead.
# If it doesn't exist: FileNotFoundError: No such file or directory.
#
# todos_arg stays NON-default: each branch sends a different list, so
# there is nothing to assume.
#
# RULE: non-default parameters FIRST, default parameters AFTER.
#     def write_todos(file_path="todos.txt", todos_arg):   # wrong
#     SyntaxError: parameter without a default follows parameter
#                  with a default
#     def write_todos(todos_arg, file_path="todos.txt"):   # correct
#
# Order matters in calls: 1st value -> 1st parameter.
#     write_todos("todos.txt", todos)  # list goes into file_path
#     TypeError: expected str, bytes or os.PathLike object, not list
# Fixes:
#     write_todos(todos, "todos.txt")                      # right order
#     write_todos(file_path="todos.txt", todos_arg=todos)  # names given
#     write_todos(todos)                                   # best
#
# Built-ins: input() has a default prompt (None), so input() works.
# len() has no default: len() -> TypeError: len() takes exactly one
# argument (0 given).
#
# What changed in the code: 9 lines (2 def lines, 7 calls).
#
# 128. Documenting the Code (DOCSTRINGS)
#
# A docstring is a function's description, in triple quotes, on the
# FIRST line inside the function. help() shows it:
#     help(len)  -> Return the number of items in a container.
#     help(get_todos) ->
#         get_todos(file_path='todos.txt')
#             Read a text file and return the list of
#             to-do items.
# Short one: one line. Long one: split it, closing """ on its own line.
# Start with a verb: Read, Write, Return.
# Comment (#) = for someone READING the code; Python ignores it.
# Docstring  = for someone USING the function; help() shows it.
# Recommendation: write a docstring for every function.
#
# 129. Code Experiments (MULTI-LINE STRINGS)
#
# Triple quotes OUTSIDE a function, stored in a variable = a
# multi-line string. Line breaks are kept, no \n needed:
#     text = """The Principles of Productivity:
#       - Deep work
#     """
# A normal string with \ at each line end prints as ONE line.
#
# 130. Bonus Example (DECOUPLING) - separate file (bonus13.py), the todo
# app does NOT change.
#
# Decoupling = split a function so each one does ONE job.
#     def parse(feet_inches):       # job 1: "4 10" -> 4.0, 10.0
#         ...
#         return feet, inches       # returns a tuple (4.0, 10.0)
#     def convert(feet, inches):    # job 2: numbers -> meters
#         return feet * 0.3048 + inches * 0.0254
#     f, i = parse("4 10")          # unpack: f = 4.0, i = 10.0
#     print(convert(f, i))          # OUTPUT: 1.4732
# Why: easier to debug, parse() can be reused, one clear job per name.
# get_todos (read) and write_todos (write) already follow this idea.
#
# ---------------------------------------------------------------------
# SECTION 14: Modularize for Maintainability (Local Modules)
# ---------------------------------------------------------------------
# 137. Organising the Code in Modules
#
# Improvement, not a fix: the program works exactly the same. As programs
# grow, functions and separate files keep the code organized.
#
# Barista: the coffee isn't made at your table, that would be messy.
# It's made in a separate prep area. Same here: get_todos and
# write_todos were CUT from this file and PASTED into functions.py.
#   cli.py      -> WHAT the program does (the menu loop below)
#   functions.py -> HOW it reads and writes the file
#
# After moving them, PyCharm shows "Unresolved reference 'get_todos'":
# this file doesn't know those names anymore. Without an import:
#     NameError: name 'get_todos' is not defined
# The fix is the IMPORT line below. It is the doorway between files:
# "go to functions.py and bring get_todos and write_todos into this file".
#
# cli.py and functions.py must be in the SAME folder, otherwise:
#     ModuleNotFoundError: No module named 'functions'
#
# Two ways to import (both work, same output):
#   1. from functions import get_todos, write_todos
#          todos = get_todos()
#      Short calls. But you must list every name (forget one -> NameError)
#      and you can't tell where get_todos came from.
#   2. import functions
#          todos = functions.get_todos()
#      Brings in the whole file. Shows where each function comes from
#      (same dot as user_action.strip()). Ardit recommends this one.
# THIS VERSION uses way 2 (import functions), the style Ardit recommends.
# Every call has "functions." in front. Your main (33).py uses way 1;
# both work and give the same output.
#
# Side demo in the video (NOT in this code): Ardit put functions.py in a
# folder named "modules", so the import became
#     from modules import functions
# then moved it back, because this small app doesn't need a folder.
# Rule: the import line matches where the file is RIGHT NOW. It's the
# same functions.py file; only its location changed.
#
# Words: functions.py is a SCRIPT on its own. When another file
# imports it, it is called a MODULE.
#
# 138. Code Experiments (IMPORT RUNS THE WHOLE FILE)
#
# Put print("hello from functions") at the bottom of functions.py and
# run cli.py -> it prints "hello from functions". The import line ran
# every line of functions.py.
# Change it to print(x) -> NameError: name 'x' is not defined. The
# traceback starts at the import line here and ends in functions.py.
#
# Fix for test code: put it under  if __name__ == "__main__":
#   Run functions.py directly -> __name__ == "__main__"   -> runs
#   cli.py imports it        -> __name__ == "functions"  -> skipped
# See the comments at the bottom of functions.py (the experiment code
# itself was removed in the final version).
#
# 139. Bonus Examples (MODULES IN A FOLDER) - separate project
# (bonus14.py), the todo app does NOT change.
#     from bonus.converters14 import convert
#     from bonus.parsers14 import parse
#     #    folder  file          function
# parse and convert came from bonus13.py (130). In PyCharm: highlight
# the def, right-click > Refactor > Move..., type the new file name
# (e.g. bonus/parsers14.py). PyCharm moves it AND writes the import.
# Why not "import functions" there? There is no functions.py in that
# project. The import uses the REAL folder and file names.

# ---------------------------------------------------------------------
# main (33) header: Recap of Section 14
# ---------------------------------------------------------------------
# Recap of Section 14. The helpers live in functions.py; cli.py imports
# them. Two import styles work:
#
#     from functions import get_todos, write_todos      # named import
#     import functions                                  # module import
#     # then call as functions.get_todos() etc.

# FINAL CODE NOTES (day14.1):
#   - Line 1 keeps way 1 as a comment, so Python ignores it:
#         # from functions import get_todos, write_todos
#   - In functions.py the parameter is named filepath (the comments here
#     call it file_path; same thing).
#   - ADD: "\n" is added inside append():  todos.append(todo + '\n')
#   - EDIT: there is an extra print(number) line (a check from the lecture).
#   - COMPLETE: get_todos() runs BEFORE index = number - 1.
#   - Some strings use single quotes ('show', '\n'). Same as double quotes.

# 137: IMPORT LINE (way 2). Brings in the WHOLE functions.py module
# (same folder). Nothing is copied into this file by name, so every call
# must say where the function lives:  functions.get_todos()
# Mixing styles breaks it:  get_todos()  ->  NameError: name 'get_todos'
# is not defined.

# from functions import get_todos, write_todos
import functions
# from functions import get_todos, write_todos

import time
now = time.strftime("%b %d, %Y %H:%M:%S")
print(f"It is {now}.")

# Keep running the program repeatedly until the user chooses "exit".
while True:

    # Ask the user which command they want to use.
    # input() returns whatever the user types as a string.
    # The argument is typed on the same line:
    #   "add play chess", "edit 2", "complete 2"
    # This line CREATES the variable user_action.
    user_action = input("Type add, show, edit, complete or exit: ")

    # Remove extra spaces from the beginning/end of the user's input.
    #
    # The = sign splits this line into two parts:
    #
    #     user_action   =   user_action.strip()
    #     ───────────       ───────────────────
    #     BEFORE the =      AFTER the =
    #     (where to SAVE)   (what to DO)
    #
    # Python always does the part AFTER the = first:
    #
    #   Step 1: user_action.strip()
    #           Take what's in user_action right now ("  add chess  ")
    #           and make a cleaned copy ("add chess").
    #
    #   Step 2: user_action =
    #           Save that cleaned copy into user_action.
    #           The old messy value is replaced.
    #
    # This is NOT an error, because user_action already exists.
    # The input() line above created it.
    #
    # We need the "user_action =" part because .strip() does not change
    # user_action by itself. It only makes a cleaned copy. Without saving
    # the copy, the spaces would still be there.
    #
    # Can I use a different name, like "action"? YES.
    #
    #   action = user_action.strip()
    #
    # Now:  user_action = "  add chess"   (messy, spaces still there)
    #       action      = "add chess"     (clean)
    #
    # RULE: every line after this must use action, the clean one.
    #   Correct:  todo = action[4:]       -> "chess"
    #   Wrong:    todo = user_action[4:]  -> "d chess"  (no error, wrong todo)
    #
    # The course reuses user_action so there's only one name to remember.
    #
    # strip() also matters for startswith(): "  add chess" does NOT
    # start with "add" because of the spaces. After strip(), it does.
    user_action = user_action.strip()

    # ---------------------------------------------------------
    # ADD   (checked FIRST)
    # ---------------------------------------------------------
    # startswith("add") is True only if the input BEGINS with "add".
    #   "add play chess".startswith("add")         -> True
    #   "edit add a new member".startswith("add")  -> False
    if user_action.startswith("add"):

        # Slice off the first 4 characters ("add ") to keep only the todo.
        #   user_action[4:]  -> everything from index 4 onwards
        #                       (a=0, d=1, d=2, space=3, then the todo starts)
        # Example: "add play chess"[4:] -> "play chess"
        # "\n" adds a newline to the end so each todo
        # is stored on its own line in the file. (This is the BUG 1 fix.)
        # Final code: the "\n" is NOT added here. It is added below, in
        # todos.append(todo + '\n'). Same result in the file.
        todo = user_action[4:]

        # FUNCTION CALL: replaces the 2 read lines that used to be here.
        # get_todos() now does this work:
        # Open todos.txt in read mode ("r").
        # "as file" stores the opened file object in the variable file.
        # Read every line from the file.
        # readlines() returns a list of strings.
        # Example: ["Study\n", "Exercise\n"]
        # The returned list is stored in todos. todos is GLOBAL (outside
        # any function); it gets the value todos_local had inside.
        # Don't forget the () — without them it's not a call.
        # 117: "todos.txt" is the ARGUMENT VALUE. It goes into
        # file_path inside get_todos().
        # 127: no argument now. The default "todos.txt" is used.
        # 137: functions.get_todos() -> "get_todos from the functions module".
        # Same dot as user_action.strip().
        todos = functions.get_todos()

        # Add the new todo to the end of the list.
        # Final code: + '\n' here puts the todo on its own line in the file
        # (the BUG 1 fix, moved from the slice line above).
        todos.append(todo + '\n')

        # FUNCTION CALL (118): replaces the 2 write lines that used to
        # be here. write_todos() now does this work:
        # Open todos.txt in write mode ("w").
        # "w" allows us to replace the file's contents.
        # WRITE mode: NOT replaced by get_todos().
        # Write every todo in the list back into the file.
        # "todos.txt" goes into file_path, todos goes into todos_arg.
        # No "x =" in front: write_todos returns nothing (None).
        # 127: only the list. todos goes into todos_arg (1st),
        # file_path uses its default "todos.txt".
        # 137: functions.write_todos(todos) -> "write_todos from the functions
        # module". No "x =" in front: it still returns nothing.
        functions.write_todos(todos)

    # ---------------------------------------------------------
    # SHOW   (only checked if ADD did NOT match)
    # ---------------------------------------------------------
    # The user types just "show", with nothing after it.
    elif user_action.startswith('show'):

        # FUNCTION CALL: replaces the 2 read lines. get_todos() now does:
        # Open todos.txt in read mode.
        # Read all lines from the file into the todos list.
        # 117: "todos.txt" is the ARGUMENT VALUE. It goes into
        # file_path inside get_todos().
        # 127: no argument now. The default "todos.txt" is used.
        # 137: functions.get_todos() -> "get_todos from the functions module".
        # Same dot as user_action.strip().
        todos = functions.get_todos()

        # Loop through every todo.
        # enumerate() gives us both:
        # index = position in the list
        # item = actual todo
        for index, item in enumerate(todos):

            # Remove the "\n" from the end of the todo.
            # This prevents an unwanted line break when printing.
            item = item.strip('\n')

            # Create a display string.
            # index + 1 makes the displayed numbers start at 1
            # instead of Python's normal 0-based indexing.
            row = f"{index + 1}-{item}" # print "1-Apple"

            # Display the todo on the screen.
            print(row)

    # ---------------------------------------------------------
    # EDIT   (only checked if ADD and SHOW did NOT match)
    # ---------------------------------------------------------
    elif user_action.startswith('edit'):

        # try: run the code below. If a ValueError happens anywhere
        # inside it, jump straight to `except ValueError:`.
        try:

            # Get the number from the user's input instead of asking again.
            # The user types something like "edit 2":
            #
            #     position:  0  1  2  3  4  5
            #     text:      e  d  i  t  _  2      (_ = space)
            #                               ↑
            #                         [5:] starts here
            #
            #   user_action[5:] -> "2"
            #
            # The slice gives a STRING ("2"), not a number.
            # int() converts it to the number 2.
            #
            # THIS is the risky line:
            #   "edit fix bug" -> int("fix bug") -> ValueError
            # When that happens, the lines below are SKIPPED and Python
            # jumps to `except ValueError:`.
            number = int(user_action[5:])

            # Final code: prints the number the user typed, e.g. "edit 2"
            # prints 2 before "Enter new todo:". A check left from the
            # lecture; you can delete this line, the app works the same.
            print(number)

            # Convert the user's number to a Python list index.
            # Users count from 1, but Python lists start from 0.
            # Example: 3 becomes index 2 because Python starts counting indexes at 0.
            # In [a, b, c], a is index 0, b is index 1, and c is index 2.
            # So when the user chooses 3 (the third item), we subtract 1:
            # 3 - 1 = 2, which gives us the index of the third item.
            #
            # Example: "edit 2" -> number is 2 -> 2 - 1 = 1 -> number is now 1 index
            # This line prints NOTHING. It only changes the value in number.
            number = number - 1

            # FUNCTION CALL: replaces the 2 read lines. get_todos() now does:
            # Open todos.txt in read mode.
            # Read all existing todos into a list.
            # 117: "todos.txt" is the ARGUMENT VALUE. It goes into
            # file_path inside get_todos().
            # 127: no argument now. The default "todos.txt" is used.
            # 137: functions.get_todos() -> "get_todos from the functions module".
            # Same dot as user_action.strip().
            todos = functions.get_todos()

            # Ask the user what the new todo should be.
            new_todo = input("Enter new todo: ")

            # Replace the selected todo with the new todo.
            # "\n" keeps the todo on its own line in the file.
            #
            # number is now 1 index, so todos[number] means todos[1]:
            #
            #   todos = ["play soccer\n", "read book\n"]
            #             todos[0]         todos[1]  <- this one gets replaced
            #
            # Full path:
            #   user types "edit 2"
            #     -> [5:] gives "2"
            #     -> int() gives 2
            #     -> 2 - 1 gives 1
            #     -> todos[1] ("read book") is replaced with the new todo
            #
            # OUTPUT (what the user sees on the screen):
            #
            #   Type add, show, edit, complete or exit: show
            #   1-play soccer
            #   2-read book
            #   Type add, show, edit, complete or exit: edit 2
            #   Enter new todo: watch movie
            #   Type add, show, edit, complete or exit: show
            #   1-play soccer
            #   2-watch movie       <- "read book" was replaced
            todos[number] = new_todo + '\n'

            # FUNCTION CALL (118): replaces the 2 write lines.
            # write_todos() now does:
            # Open the file in write mode.
            # WRITE mode: NOT replaced by get_todos().
            # Write the updated list back to the file.
            # 127: only the list. todos goes into todos_arg (1st),
            # file_path uses its default "todos.txt".
            # 137: functions.write_todos(todos) -> "write_todos from the functions
            # module". No "x =" in front: it still returns nothing.
            functions.write_todos(todos)

        # Runs ONLY if a ValueError happened inside the try part above.
        #
        # OUTPUT (what the user sees on the screen):
        #
        #   Type add, show, edit, complete or exit: edit fix bug
        #   Your command is not valid.
        #   Type add, show, edit, complete or exit:      <- asked again
        #
        # NOTE: only ValueError is caught here. "edit 23" with only 2.
        # ValueError happens anywhere a function gets the right type of thing but a bad value.
        # int("2")        -> 2           (works)
        # int("fix bug")  -> ValueError  ("fix bug" isn't a number)
        # In our app: "edit fix bug" instead of "edit 2".
        # todos raises IndexError, which is NOT caught, so it still crashes.
        except ValueError:
            # Show a friendly message instead of a crash.
            print("Your command is not valid.")
            # Go back to the top of the while loop and ask again.
            continue

    # ---------------------------------------------------------
    # COMPLETE   (only checked if ADD, SHOW and EDIT did NOT match)
    # ---------------------------------------------------------
    elif user_action.startswith('complete'):
        # try: run the code below. If an IndexError happens anywhere
        # inside it, jump straight to `except IndexError:`.
        try:
            # Get the number from the user's input instead of asking again.
            # The user types something like "complete 2":
            #
            #     position:  0  1  2  3  4  5  6  7  8  9
            #     text:      c  o  m  p  l  e  t  e  _  2      (_ = space)
            #                                           ↑
            #                                     [9:] starts here
            #
            #   user_action[9:] -> "2"
            #
            # [9:] takes EVERYTHING from position 9 to the end, so two-digit
            # numbers work too: "complete 12"[9:] -> "12"
            # int() converts the string "2" to the number 2.
            number = int(user_action[9:])

            # FUNCTION CALL: replaces the 2 read lines
            # (the 4th place the repeated code was). get_todos() now does:
            # Open todos.txt in read mode.
            # Read all todos from the file.
            # 117: "todos.txt" is the ARGUMENT VALUE. It goes into
            # file_path inside get_todos().
            # 127: no argument now. The default "todos.txt" is used.
            # 137: functions.get_todos() -> "get_todos from the functions module".
            # Same dot as user_action.strip().
            todos = functions.get_todos()

            # Convert the user's number to a zero-based list index.
            # Example: "complete 2" -> number is 2 -> 2 - 1 = 1 -> index is 1
            # This line prints NOTHING. It only saves the value in index.
            #
            # Here the result goes into a NEW name (index), so number stays 2.
            # EDIT reuses number instead. Both work the same.
            # Final code: this line comes AFTER get_todos(). The order doesn't
            # matter here; both just need to happen before todos[index].
            index = number - 1

            # Get the todo that will be removed.
            # [index] accesses that item in the list.
            # strip("\n") removes the newline from the end.
            #
            # index is 1, so todos[index] means todos[1]:
            #
            #   todos = ["play soccer\n", "read book\n"]
            #             todos[0]         todos[1]  <- this one
            #
            # todo_to_remove becomes "read book"
            #
            # THIS is the risky line:
            #   "complete 23" -> index 22 -> todos[22] -> IndexError
            #   (the list only has todos[0] and todos[1])
            # When that happens, the lines below are SKIPPED and Python
            # jumps to `except IndexError:`.
            todo_to_remove = todos[index].strip('\n')

            # Remove the selected todo from the list.
            # pop() removes the item at the specified position.
            # index is 1, so todos.pop(1) removes "read book"
            # The list becomes ["play soccer\n"]
            todos.pop(index)

            # FUNCTION CALL (118): replaces the 2 write lines
            # (the 3rd place the repeated code was). write_todos() now does:
            # Open the file in write mode.
            # WRITE mode: NOT replaced by get_todos().
            # Save the updated list back to the file.
            # 127: only the list. todos goes into todos_arg (1st),
            # file_path uses its default "todos.txt".
            # 137: functions.write_todos(todos) -> "write_todos from the functions
            # module". No "x =" in front: it still returns nothing.
            functions.write_todos(todos)

            # Create a confirmation message using an f-string.
            # The value of todo_to_remove is inserted into the string.
            message = f"Todo {todo_to_remove} was removed from the list."

            # Display the confirmation message.
            #
            # OUTPUT (what the user sees on the screen):
            #
            #   Type add, show, edit, complete or exit: show
            #   1-play soccer
            #   2-read book
            #   Type add, show, edit, complete or exit: complete 2
            #   Todo read book was removed from the list.
            #   Type add, show, edit, complete or exit: show
            #   1-play soccer       <- "read book" is gone
            print(message)

        # Runs ONLY if an IndexError happened inside the try part above.
        #
        # OUTPUT (what the user sees on the screen):
        #
        #   Type add, show, edit, complete or exit: complete 23
        #   There is no item with that number.
        #   Type add, show, edit, complete or exit:      <- asked again
        #
        # Because the error happened BEFORE pop() and the file write,
        # nothing was removed and the file is unchanged.
        #
        # NOTE: only IndexError is caught here. "complete fix bug" raises
        # The error Python raises when you ask for a list position that doesn't exist.
        # todos = ["play soccer\n", "read book\n"]   # positions 0 and 1 only
        # todos[1]   -> "read book\n"   (works)
        # todos[22]  -> IndexError      (there's no position 22)
        # In our app: "complete 23" when there are only 2 todos.
        # ValueError, which is NOT caught, so it still crashes.
        except IndexError:

            # Show a friendly message instead of a crash.
            print("There is no item with that number.")

            # Go back to the top of the while loop and ask again.
            continue

    # ---------------------------------------------------------
    # EXIT
    # ---------------------------------------------------------
    elif user_action.startswith('exit'):

        # Stop the while loop.
        # Execution jumps to the code after the loop.
        break

    # ---------------------------------------------------------
    # ELSE   (runs only if NONE of the conditions above were True)
    # ---------------------------------------------------------
    # Example: the user types "crash" or "hello".
    # The input doesn't start with add, show, edit, complete or exit,
    # so Python lands here.
    else:

        # Tell the user their command wasn't recognized.
        # The loop then starts again and asks for a new command.
        print("Command is not valid.")


# This runs after the while loop ends.
# It prints a goodbye message after the user chooses "exit".
print("Bye!")

# OUTPUT (lecture test run):
#   Type add, show, edit, complete or exit: add make soup
#   Type add, show, edit, complete or exit: add make pizza
#   Type add, show, edit, complete or exit: show
#   1-make soup
#   2-make pizza
#
# OUTPUT (117 test run, after adding the parameter):
#   Type add, show, edit, complete or exit: show
#   1-make soup
#   2-make pizza
# Same as before: the program works the same, only the function changed.
#
# OUTPUT (118 test run, with write_todos):
#   Type add, show, edit, complete or exit: add clean the code
#   Type add, show, edit, complete or exit: show
#   1-make soup
#   2-make pizza
#   3-clean the code
#   Type add, show, edit, complete or exit: complete 2
#   Todo make pizza was removed from the list.
#   Type add, show, edit, complete or exit: show
#   1-make soup
#   2-clean the code
#
# OUTPUT (127/128 test run, with defaults and docstrings):
#   Same as before. Only how the functions are written changed.
#
# OUTPUT (137 test run, with functions.py + import):
#   Same as before. The code is only split into two files.
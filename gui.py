# Make the GUI interactive — clicking "Add" stores the typed todo in
# todos.txt via the backend functions.
#
# THE EVENT LOOP
# `window.read()` returns a tuple: (event, values)
#   event  -> a label/identifier of what happened. For a button click,
#             it's the button's text ("Add"). When the window's close
#             button is clicked, it's sg.WIN_CLOSED.
#   values -> a dict mapping each widget's KEY to its current value.
#             So values["todo"] is whatever's typed in the input box.
#
# Wrap the read() call in `while True:` so the program keeps responding
# to user actions until the user closes the window.
#
# WIDGET KEYS
# Each widget that the program wants to identify needs a `key=` argument
# so it shows up in the values dict by that name. Without it, FreeSimpleGUI
# uses an auto-generated key.
#
# WIN_CLOSED HANDLING
# Always include a `case sg.WIN_CLOSED:` branch — without it, closing
# the window via the OS X button causes an error on the next read().
#
# FONT
# Pass `font=("Helvetica", 20)` to the Window constructor to size up
# all the widgets at once.
# =====================================================================
# gui.py  -  GUI FRONTEND of the todo app
# Section 16 (156): the window, label, input box, Add button
# Section 17 (165): bigger font + the Add button WORKS
# =====================================================================
# 155: FRONTEND = what the user sees and uses (this file).
#      BACKEND  = functions.py (reads/writes todos.txt).

# The backend: get_todos() and write_todos() (same ones cli.py uses).
import functions

# 156: third-party GUI library (install: Settings > Project >
# Python Interpreter > + > FreeSimpleGUI). "as sg" = short name.
import FreeSimpleGUI as sg

label = sg.Text("Type in a to-do")                      # a label
# 165: key="todo" is the ID of this box. Its typed text appears in
# the values dictionary under that key: values["todo"].
# (Without key=, FreeSimpleGUI uses the key 0.)
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button("Add")       # its label "Add" becomes the event

# The window. layout = list of lists, each inner list = one row (157):
#   row 1: label      row 2: input box + Add button
# 165: font=(family, size) makes everything bigger. One argument per
# line keeps lines under 79 characters (recommended Python length).
window = sg.Window("My To-Do App",
                   layout=[[label], [input_box, add_button]],
                   font=("Helvetica", 20))

# 165: THE EVENT LOOP. while True keeps the window open: each click is
# one run of the loop. Without it, the program ends after one click.
while True:
    # read() shows the window and WAITS for an event. It returns a
    # tuple, split into 2 variables (like x, y = (3, 4)):
    #   event  = label of the button pressed, e.g. "Add"
    #   values = dictionary of key: typed text, e.g. {"todo": "Hi"}
    event, values = window.read()
    print(event)        # e.g. Add      (for learning; see each event)
    print(values)       # e.g. {'todo': 'Hi'}

    # match checks which event happened: one case per button.
    match event:
        case "Add":
            # 1. Read the current list from todos.txt.
            todos = functions.get_todos("todos.txt")
            # 2. Get the typed text and add a line break, so each todo
            #    is on its own line in the file.
            new_todo = values["todo"] + "\n"
            # 3. Add it to the END of the list.
            todos.append(new_todo)
            # 4. Save the whole list back to todos.txt.
            functions.write_todos(todos, "todos.txt")
            # ("todos.txt" isn't needed: FILEPATH is already the default.
            #  functions.get_todos() and functions.write_todos(todos)
            #  do the same thing.)
        case sg.WIN_CLOSED:
            # The window's X button was clicked (event = None).
            # Leave the loop so the program ends cleanly.
            break

# Runs after break: close the window. NOT indented (outside the loop).
window.close()
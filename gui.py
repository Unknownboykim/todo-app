# =====================================================================
# gui.py  -  GUI FRONTEND of the todo app, SECTION 17 (final)
# 165: bigger font + the Add button works (event loop)
# 166: list box + Edit button + update() + clicking a todo
# 167: experiments (break vs exit(), layout in a variable)
# Backend: functions.py (get_todos, write_todos). Not changed.
# =====================================================================

# ---------------------------------------------------------------------
# 165. Implementing an "Add Todo" Button
# ---------------------------------------------------------------------
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
# (Tested with FreeSimpleGUI: no error message, but the loop never
# ends and keeps printing None. Either way, you need the case.)
#
# FONT
# Pass `font=("Helvetica", 20)` to the Window constructor to size up
# all the widgets at once.

# ---------------------------------------------------------------------
# 166. Implementing an "Edit" Button
# ---------------------------------------------------------------------
# Add an Edit button + a list box that shows existing todos.
#
# NEW WIDGET: sg.Listbox
#   values        -> the initial list of strings to show
#   key           -> identifier so we can read what the user selected
#                    (values["todos"] is a LIST of selected items;
#                    use [0] to grab the first/only one).
#   enable_events -> True so clicking a row fires an event (we just
#                    rely on it for `values["todos"]` here).
#   size          -> (width_in_chars, height_in_rows)
#
# The edit case:
#   1. Read the currently-selected todo from values["todos"][0].
#   2. Read the new text from the input box (values["todo"]).
#   3. Get the full list from the file, find the old todo's index,
#      replace it with the new text (+"\n"), and write the list back.
#   4. Call window["todos"].update(values=todos) to refresh the
#      listbox in REAL TIME — otherwise the GUI keeps showing the
#      stale list until the user restarts the app.
#
# We do the same `window["todos"].update(...)` at the end of the Add
# case so newly-added todos appear in the listbox immediately.
#
# 166 ALSO (case "todos"): clicking a todo in the list box is an event
# too (event = "todos", the list box's key, because enable_events=True).
# We use it to copy the selected todo into the input box, so the user
# can change it there and press Edit.

# ---------------------------------------------------------------------
# 167. Code Experiments
# ---------------------------------------------------------------------
# Two experiments related to the GUI code.
#
# --- Experiment 1: break vs exit() in the close handler ---
# When the user closes the window, the WIN_CLOSED branch runs:
#
#     case sg.WIN_CLOSED:
#         break
#
# `break` exits the while loop. Anything written AFTER the loop still
# runs:
#
#     while True: ...
#     print("bye")          # runs after break
#     window.close()
#
# If you replace `break` with `exit()` (Python's built-in), the program
# stops IMMEDIATELY — the print and window.close() lines after the
# loop would NOT run.
#
# For a GUI you usually want `break` so any cleanup code after the
# loop (logging, saving state, calling window.close()) still happens.
#
# --- Experiment 2: dynamic layouts ---
# The layout argument doesn't have to be written inline. You can build
# it up first as a regular variable, and pass that variable in.
#
#     button_labels = ["Apply", "Close", "Reset"]
#     layout = []
#     for label_text in button_labels:
#         layout.append([sg.Button(label_text)])
#     window = sg.Window("Demo", layout=layout)
#
# This is essential when the number/contents of buttons or rows depend
# on data you don't know ahead of time (e.g. a list of files from disk).

# 155: FRONTEND = what the user sees and uses (this file).
#      BACKEND  = functions.py (reads/writes todos.txt).

# 156: third-party GUI library (install: Settings > Project >
# Python Interpreter > + > FreeSimpleGUI). "as sg" = short name.
import FreeSimpleGUI as sg
# The backend: get_todos() and write_todos() (same ones cli.py uses).
import functions


label = sg.Text("Type in a to-do")                      # a label
# 165: key="todo" is the ID of this box. Its typed text appears in
# the values dictionary under that key: values["todo"].
# (Without key=, FreeSimpleGUI uses the key 0.)
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button("Add")       # its label "Add" becomes the event

# 166: key="todos" = the LIST BOX's ID (a DIFFERENT key from "todo").
# values=functions.get_todos(): the list comes from todos.txt.
# Listbox with a lowercase b (ListBox = AttributeError).
list_box = sg.Listbox(values=functions.get_todos(), key="todos",
                      enable_events=True, size=(45, 10))
edit_button = sg.Button("Edit")     # same Button TYPE, a new INSTANCE

# The window. layout = list of lists, each inner list = one row (157):
#   row 1: label   row 2: input box + Add   row 3: list box + Edit (166)
# 165: font=(family, size) makes everything bigger. One argument per
# line keeps lines under 79 characters (recommended Python length).
window = sg.Window("My To-Do App",
                   layout=[
                       [label],
                       [input_box, add_button],
                       [list_box, edit_button],
                   ],
                   font=("Helvetica", 20))

# 165: THE EVENT LOOP. while True keeps the window open: each click is
# one run of the loop. Without it, the program ends after one click.
while True:
    # read() shows the window and WAITS for an event. It returns a
    # tuple, split into 2 variables (like x, y = (3, 4)):
    #   event  = what happened: "Add", "Edit", "todos" or WIN_CLOSED
    #   values = {"todo": text in the box, "todos": [selected item]}
    event, values = window.read()

    # match checks which event happened: one case per button.
    match event:
        case "Add":
            # 1. Read the current list from todos.txt.
            todos = functions.get_todos()
            # 2. Get the typed text and add a line break, so each todo
            #    is on its own line in the file.
            new_todo = values["todo"] + "\n"
            # 3. Add it to the END of the list.
            todos.append(new_todo)
            # 4. Save the whole list back to todos.txt.
            functions.write_todos(todos)
            # 166: refresh the list box so the new todo shows right away.
            window["todos"].update(values=todos)
        case "Edit":
            # 166: the selected todo. values["todos"] is a LIST, e.g.
            # ['Clean the code\n'], so [0] gives the string.
            # (Edit with nothing selected -> IndexError; fixed later.)
            todo_to_edit = values["todos"][0]
            # The new text from the input box. .strip("\n") removes the
            # line break that comes along when a todo is copied in from
            # the list box, so "+ \n" below never makes a blank line.
            new_todo = values["todo"].strip("\n")

            todos = functions.get_todos()
            # Find WHERE the old todo is (its index) and replace it.
            index = todos.index(todo_to_edit)
            todos[index] = new_todo + "\n"
            functions.write_todos(todos)

            # window["todos"] = the list box inside the window.
            # .update(values=...) shows the new list in REAL TIME.
            window["todos"].update(values=todos)
        case "todos":
            # 166: the user clicked a todo in the list box: copy it into
            # the input box. (update takes value=, singular, here)
            window["todo"].update(value=values["todos"][0])
        case sg.WIN_CLOSED:
            # The window's X button was clicked (event = None).
            # 167: break stops ONLY the while loop; the lines after the
            # loop still run. exit() would stop the WHOLE program here.
            break

# Runs after break. NOT indented (outside the loop).
print("bye")          # only runs because we use break, not exit()
window.close()
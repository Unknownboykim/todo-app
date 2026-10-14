# =====================================================================
# gui.py  -  GUI FRONTEND of the todo app, SECTION 18
# 165: bigger font + the Add button works (event loop)
# 166: list box + Edit button + update() + clicking a todo
# 167: experiments (break vs exit(), layout in a variable)
# 174: Complete button + Exit button
# 175: popups for errors, live clock, theme
# 176: images as buttons (Add and Complete)
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

# ---------------------------------------------------------------------
# 174. Implement "Complete" and "Exit" Buttons
# ---------------------------------------------------------------------
# Add a Complete button (removes the selected todo) and an Exit button
# (a friendlier way to close the program than the OS window-close X).
#
# Complete case steps:
#   1. Read the selected todo: values["todos"][0].
#   2. Get the full list, call list.remove(todo) to drop it, write back.
#   3. Refresh the listbox so the deleted todo disappears immediately.
#   4. Clear the input box too, since it might still show the old text:
#         window["todo"].update(value="")
#      Note: .update on a single-value widget takes `value=`,
#      whereas .update on a Listbox takes `values=` (plural).
#
# Exit case: simply `break` out of the while loop. Same effect as the
# WIN_CLOSED case — both ways to leave converge on `window.close()`.

# ---------------------------------------------------------------------
# 175. Final Touches
# ---------------------------------------------------------------------
# Three "finishing touches" to make the app feel polished:
#
# 1. ERROR HANDLING with user-friendly popups.
#    Pressing Edit or Complete without selecting a todo raises
#    IndexError on values["todos"][0]. Wrap each branch in try/except
#    and show a sg.popup() instead of crashing.
#    (Don't print() error messages — GUI users never see the console.)
#
# 2. LIVE CLOCK at the top of the window.
#    - Add an empty sg.Text(key="clock") in its own first row.
#    - Pass `window.read(timeout=200)` so the loop wakes up every
#      200 ms even without a user event.
#    - On every iteration, update the clock label with the current
#      time from `time.strftime(...)`.
#
# 3. THEME + sizing.
#    Call sg.theme("DarkPurple4") (or any theme name — see the
#    FreeSimpleGUI themes gallery) BEFORE creating the window.

# ---------------------------------------------------------------------
# 176. Code Experiments
# ---------------------------------------------------------------------
# Experiments: use IMAGES as buttons.
#
# Place two PNG files (e.g. add.png, edit.png) in the same folder as
# this script — the lecture attaches them as resources.
#
# sg.Button arguments used here:
#   button_text         drop the visible text label (set to empty)
#   image_filename      path to the image to show on the button
#   image_subsample     int divisor to shrink the image
#   mouseover_colors    colors when the user hovers (gives feedback;
#                       otherwise the button looks "dead")
#   tooltip             text shown when the cursor hovers over it
#   key                 needed because there's no text label to match
#                       against in the match-case branch
#
# Because the button text is empty, the event dispatched is now the
# button's KEY ("Add", "Edit", ...) — so the existing
# `case "Add":` etc. branches still work.
#
# Notes on the code below:
#   - The lecture resources have add.png and complete.png (no edit.png),
#     so Add and Complete are image buttons and Edit keeps its text.
#     The PNG files must be in the SAME folder as gui.py.
#   - The video uses image_source="add.png" and size=2. Your version,
#     image_filename=... + image_subsample=4, works too: image_filename
#     is another name for the image file, image_subsample=4 shows the
#     image 4 times smaller (good for a big PNG).

# 155: FRONTEND = what the user sees and uses (this file).
#      BACKEND  = functions.py (reads/writes todos.txt).

# 156: third-party GUI library (install: Settings > Project >
# Python Interpreter > + > FreeSimpleGUI). "as sg" = short name.
import FreeSimpleGUI as sg
# The backend: get_todos() and write_todos() (same ones cli.py uses).
import functions
# 175: the STANDARD module time, for the clock (same as cli.py, 146).
import time

import os

if not os.path.exists("todos.txt"):
    with open("todos.txt", "w") as file:
        pass  # Creates an empty file if it doesn't exist

# 175: THEME. Call it BEFORE creating the widgets and the window.
# Theme names: search "PySimpleGUI themes" (images); the same names work
# in FreeSimpleGUI, e.g. "DarkPurple4", "Black". sg.theme_list() lists all.
sg.theme("DarkPurple4")

# 175: an empty label for the clock, in its own first row. Not called
# "time", because that is the name of the module we imported.
# key="clock" so the loop can find and update it.
clock = sg.Text("", key="clock")
label = sg.Text("Type in a to-do")                      # a label
# 165: key="todo" is the ID of this box. Its typed text appears in
# the values dictionary under that key: values["todo"].
# (Without key=, FreeSimpleGUI uses the key 0.)
input_box = sg.InputText(tooltip="Enter todo", key="todo")
# 176: an IMAGE button. No label text, so key="Add" is needed: the
# event is now the KEY (without a key the event would be "", and
# case "Add" would never match).
#   image_source     the image file shown on the button
#   size=2           a narrow button (size=10 left it too wide)
#   mouseover_colors color when the mouse is over it (without it the
#                    button seemed to disappear on hover). Use names from
#                    the PySimpleGUI color chart, e.g. "LightBlue2".
#   tooltip          tells the user what the image button does
add_button = sg.Button(size=2, image_source="add.png",
                       mouseover_colors="LightBlue2",
                       tooltip="Add todo", key="Add")

# 166: key="todos" = the LIST BOX's ID (a DIFFERENT key from "todo").
# values=functions.get_todos(): the list comes from todos.txt.
# Listbox with a lowercase b (ListBox = AttributeError).
list_box = sg.Listbox(values=functions.get_todos(), key="todos",
                      enable_events=True, size=(45, 10))
edit_button = sg.Button("Edit")     # same Button TYPE, a new INSTANCE
# 174: two more Button instances. Their labels become the events.
# 176 exercise: the same for Complete, with complete.png.
complete_button = sg.Button(size=2, image_source="complete.png",
                            mouseover_colors="LightBlue2",
                            tooltip="Complete todo", key="Complete")
exit_button = sg.Button("Exit")

# The window. layout = list of lists, each inner list = one row (157):
#   row 0: clock (175)   row 1: label   row 2: input box + Add
#   row 3: list box + Edit (166) + Complete (174)   row 4: Exit (174)
# One row per line, so the layout is easy to read.
# 165: font=(family, size) makes everything bigger. One argument per
# line keeps lines under 79 characters (recommended Python length).
window = sg.Window("My To-Do App",
                   layout=[
                       [clock],                     # 175: the clock row
                       [label],
                       [input_box, add_button],
                       [list_box, edit_button, complete_button],
                       [exit_button],
                   ],
                   font=("Helvetica", 20))

# 165: THE EVENT LOOP. while True keeps the window open: each click is
# one run of the loop. Without it, the program ends after one click.
while True:
    # read() shows the window and WAITS for an event. It returns a
    # tuple, split into 2 variables (like x, y = (3, 4)):
    #   event  = what happened: "Add", "Edit", "todos", "Complete",
    #            "Exit", WIN_CLOSED, or "__TIMEOUT__" (175)
    #   values = {"todo": text in the box, "todos": [selected item]}
    #
    # 175: timeout=200 -> read() also returns every 200 milliseconds
    # (event "__TIMEOUT__") even when the user does nothing. Without it,
    # the loop only runs after a click, so the clock would not tick.
    # 1000 ms = 1 second; 10 also works but runs the loop very often.
    event, values = window.read(timeout=200)
    # 175: on EVERY loop run, put the current date and time in the clock.
    window["clock"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))

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
            # 175: try/except. Edit with nothing selected -> values["todos"]
            # is [] -> [0] raises IndexError. Show a popup instead of crashing.
            try:
                # 166: the selected todo. values["todos"] is a LIST, e.g.
                # ['Clean the code\n'], so [0] gives the string.
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
            except IndexError:
                # GUI users never see the command line, so no print():
                # sg.popup() opens a small window with the message and OK.
                # font= works like the Window font argument.
                sg.popup("Please select an item first.", font=("Helvetica", 20))
        case "todos":
            # 166: the user clicked a todo in the list box: copy it into
            # the input box. (update takes value=, singular, here)
            # if: only when something IS selected (an empty selection
            # would give IndexError, e.g. after the list was refreshed).
            if values["todos"]:
                window["todo"].update(value=values["todos"][0])
        case "Complete":
            # 175: same try/except as Edit.
            try:
                # 174: the selected todo, e.g. 'Get the car\n'.
                todo_to_complete = values["todos"][0]
                todos = functions.get_todos()
                # list.remove(item) deletes that item from the list,
                # e.g. a = [1, 2, 3]; a.remove(3) -> a = [1, 2]
                todos.remove(todo_to_complete)
                functions.write_todos(todos)            # save to todos.txt
                window["todos"].update(values=todos)    # list box: values= (a list)
                # Empty the input box, which still showed the completed todo.
                window["todo"].update(value="")         # input box: value= (one value)
            except IndexError:
                sg.popup("Please select an item first.", font=("Helvetica", 20))
        case "Exit":
            # 174: the Exit button closes the program the same way as
            # the X button: leave the loop, then window.close() runs.
            break
        case sg.WIN_CLOSED:
            # The window's X button was clicked (event = None).
            # 167: break stops ONLY the while loop; the lines after the
            # loop still run. exit() would stop the WHOLE program here.
            break

# Runs after break (Exit or X). NOT indented (outside the loop).
window.close()
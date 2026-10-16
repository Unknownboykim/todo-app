# =====================================================================
# web.py  -  WEB FRONTEND of the todo app, SECTION 19
# 184: first Streamlit page (title, subheader, text, checkboxes, input)
# 185: Adding New Todo Items on the Web App (key + on_change)
# Backend: functions.py (get_todos, write_todos). Not changed.
# Run in the PyCharm TERMINAL:  streamlit run web.py
# =====================================================================

# ---------------------------------------------------------------------
# 185. Adding New Todo Items on the Web App
# ---------------------------------------------------------------------
# Wire up the text input so pressing Enter on a new todo APPENDS it
# to todos.txt.
#
# Two Streamlit features we use here:
#
# 1. KEY argument
#    Every widget can be given a unique `key=`. That key becomes the
#    widget's slot in `st.session_state` — a special dict-like object
#    that holds the current value of each widget.
#       st.session_state["new_todo"] -> whatever's typed in the input
#
# 2. on_change callback
#    Pass a function to `on_change=`. Streamlit calls that function
#    whenever the widget's value changes. Inside the callback we can
#    read st.session_state["new_todo"], append it to the list, and
#    write the file back.
#
# Don't forget the trailing "\n" so each todo gets its own line in
# todos.txt. The file format is unchanged from the CLI/GUI versions —
# functions.py keeps working as-is.
#
# WHAT HAPPENS WHEN YOU TYPE "Buy milk" AND PRESS ENTER:
#   1. The input's value changes -> Streamlit calls add_todo() FIRST.
#   2. add_todo() saves "Buy milk\n" into todos.txt.
#   3. Streamlit re-runs the WHOLE script from the top:
#      get_todos() reads the file again -> the new checkbox appears.
#
# BEFORE YOU START (185 transcript): open todos.txt and make sure the
# file ends with ONE line break after the last todo (the cursor sits on
# the empty line below it). Otherwise the first new todo is glued to the
# last one, e.g. "Get paperClean the bag".
#
# DEBUG LINES used in the video (add them to test, then delete):
#   print(todo)            inside add_todo(): shows the typed text in
#                          the terminal -> the function runs FIRST
#   st.session_state       at the bottom: shows the dictionary-like
#                          session state on the page, e.g.
#                          {"new_todo": "Clean the bag"}
#
# Commit message used in the video:  Implement add new todo items feature

# The backend: get_todos() and write_todos() (same ones cli.py and
# gui.py use).
import functions
# Third-party library for web apps. "as st" = short name.
import streamlit as st


# Read the list from todos.txt, e.g. ["Study\n", "Clean room\n"].
# This line runs again on EVERY re-run, so the list is always fresh.
todos = functions.get_todos()


# 185: the CALLBACK function. It is NOT called here: we only DEFINE it.
# Streamlit calls it later, when the text input changes (on_change).
# Defined ABOVE the text input, because the input needs to know it.
def add_todo():
    # st.session_state["new_todo"] = the text in the input box
    # (because the input has key="new_todo").
    # + "\n" so the todo gets its own line in todos.txt.
    todo = st.session_state["new_todo"] + "\n"
    # todos is the list read at the top. append = add to the END.
    todos.append(todo)
    # Save the whole list back to todos.txt.
    functions.write_todos(todos)


# Big heading, smaller heading, normal text (184).
st.title("My Todo App")
st.subheader("This is my todo app.")
st.write("This app is to increase your productivity.")

# One checkbox per todo (184). The todo text is the checkbox LABEL.
# Because add_todo() already saved the new todo, this loop now goes
# through the UPDATED list, so the new checkbox appears (185 transcript).
# CAREFUL: every line in todos.txt must be DIFFERENT. Two same todos
# (or two empty lines) -> two checkboxes with the same label ->
# StreamlitDuplicateElementId. So don't add a todo that is already in
# the list, and don't press Enter on an empty box.
# (Ardit gives the checkboxes a key later, for the Complete feature.)
for todo in todos:
    st.checkbox(todo)

# The text box for a new todo.
#   label=""           no visible label (Streamlit prints a warning
#                      about the empty label in the terminal; the app
#                      still works)
#   placeholder=       grey hint text inside the box
#   on_change=add_todo 185 NEW: the function to call when the text
#                      changes (pressing Enter). NO () after add_todo:
#                      we pass the function itself, we don't call it.
#   key="new_todo"     185 NEW: the name of this box in
#                      st.session_state, used inside add_todo().
st.text_input(label="", placeholder="Add new todo...",
              on_change=add_todo, key="new_todo")
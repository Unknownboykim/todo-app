# First Streamlit version of the todo app — UI only, no interactivity yet.
#
# INSTALL
#     pip install streamlit
# (or in PyCharm: Python Packages -> search "streamlit" -> Install.)
#
# RUN
# Unlike a normal Python script, Streamlit apps need their own runner:
#     streamlit run web.py
# That command starts a small local server and opens the app in your
# browser at http://localhost:8501 (or 8502 if 8501 is busy).
#
# HOW STREAMLIT WORKS
# Each function call (st.title, st.write, st.checkbox, ...) adds a
# widget to the page. The ORDER OF THE CALLS = the order they appear
# on the page (top to bottom). To change layout, just reorder the calls.
#
# When the user does anything that changes state (presses Enter in an
# input, clicks a checkbox), Streamlit re-runs the WHOLE SCRIPT from
# the top with the new values. Keep that mental model in mind.
#
# THIRD FRONTEND (Section 19)
#   cli.py -> command line   gui.py -> desktop window   web.py -> web page
# All three use the SAME backend: functions.py (get_todos, write_todos).
# functions.py is NOT changed. web.py must be in the same folder as
# functions.py and todos.txt.

# The backend: get_todos() reads todos.txt and returns a list.
import functions
# Third-party library for web apps. "as st" = short name (like "as sg").
import streamlit as st


# Read the todos from todos.txt, e.g. ["Study\n", "Clean room\n"].
# No argument: the default FILEPATH ("todos.txt") is used.
# Because Streamlit re-runs the whole script, this line runs again on
# every change, so the page always shows the latest list.
todos = functions.get_todos()

# Big heading at the top of the page (like an HTML <h1>).
st.title("My Todo App")
# Smaller heading under the title.
st.subheader("This is my todo app.")
# Normal text (a paragraph).
st.write("This app is to increase your productivity.")

# One checkbox per todo. The todo text is the checkbox LABEL.
# for loop: todo = "Study\n", then "Clean room\n", ...
# The "\n" at the end does not show on the page.
# NOTE: if two todos have the SAME text, Streamlit stops with
# StreamlitDuplicateElementId (two checkboxes with the same label get
# the same ID). The fix is a unique key, e.g. st.checkbox(todo, key=todo)
# -- the course adds key= when the checkboxes become interactive.
for todo in todos:
    st.checkbox(todo)

# A text box to type a new todo. Not connected to anything yet: typing
# and pressing Enter does nothing (interactivity comes next).
#   label=""        no visible label above the box
#   placeholder=    grey hint text inside the box until you type
# label="" works, but Streamlit shows a WARNING in the terminal:
#   "`label` got an empty value ... Please provide a non-empty label
#    and hide it with label_visibility if needed."
# It is only a warning; the app still runs. To remove it you can write:
#   st.text_input(label="Enter a todo", placeholder="Add new todo...",
#                 label_visibility="collapsed")
st.text_input(label="", placeholder="Add new todo...")
# =====================================================================
# web.py  -  WEB FRONTEND of the todo app, SECTION 19
# 184: first Streamlit page (title, subheader, text, checkboxes, input)
# 185: Adding New Todo Items on the Web App (key + on_change)
# 186: Completing todo items (checkbox key + pop + rerun)
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

# ---------------------------------------------------------------------
# 186. Completing Todo Items on the Web App (your notes)
# ---------------------------------------------------------------------
# Final web-app feature: checking a checkbox MARKS the todo complete
# (removes it from todos.txt and from the UI).
#
# Steps in the loop:
#   1. Iterate with enumerate() so we have the index of each todo.
#   2. Give each checkbox a unique key — the todo string itself works
#      (each line in todos.txt is unique anyway). That makes it show
#      up in st.session_state.
#   3. The variable `st.checkbox(...)` returns is True when checked,
#      False otherwise.
#   4. If True: pop by index, save the file, delete the key from
#      session_state (otherwise the next rerun would still "remember"
#      it as checked), and force a rerun so the UI refreshes
#      immediately.
#
# `st.experimental_rerun()` (renamed to `st.rerun()` in newer Streamlit
# versions) stops the current run and starts a fresh one with the
# updated todos.

# ---------------------------------------------------------------------
# 186. Complete a todo (check its checkbox -> it is removed)
# ---------------------------------------------------------------------
# st.session_state only shows widgets that HAVE A KEY. The text input
# had key="new_todo", the checkboxes had none, so they were missing.
# Give each checkbox key=todo (the todo text). Then session_state is:
#   {"new_todo": "", "Buy grocery\n": False, "Fix the floor\n": False}
# A checked checkbox -> its value becomes True.
#
# key="hello" for ALL checkboxes would NOT work: every checkbox would
# get the same key (the video shows only ONE pair). The key must be
# DIFFERENT for each todo, so the todo text itself is used.
#
# When a checkbox is checked:
#   1. todos.pop(index)            remove that todo from the list
#   2. functions.write_todos(todos) save the list to todos.txt
#   3. del st.session_state[todo]  remove its pair from session_state
#   4. st.rerun()                  run the script again, so the page
#                                  shows the list WITHOUT that todo
#
# st.experimental_rerun() (in the video) was RENAMED to st.rerun().
# The video says: "probably you just need to write rerun instead of
# experimental rerun". In new Streamlit, experimental_rerun no longer
# exists -> AttributeError. So use st.rerun().
#
# DEBUG used in the video (add to test, then delete):
#   st.session_state   at the bottom: shows the dictionary on the page
#   print(checkbox)    inside the loop: prints True in the terminal
#                      when a box is checked

# The backend: get_todos() and write_todos() (same ones cli.py and
# gui.py use).
import functions
# Third-party library for web apps. "as st" = short name.
import streamlit as st


# Read the list from todos.txt, e.g. ["Study\n", "Clean room\n"].
# This line runs again on EVERY re-run, so the list is always fresh.
todos = functions.get_todos()


# 185: the CALLBACK function. It is NOT called here: we only DEFINE it.
# Streamlit calls it when the text input changes (on_change=add_todo).
def add_todo():
    # The text in the input box (it has key="new_todo") + a line break.
    todo = st.session_state["new_todo"] + "\n"
    # Add it to the END of the list, then save the list to todos.txt.
    todos.append(todo)
    functions.write_todos(todos)


# Big heading, smaller heading, normal text (184).
st.title("My Todo App")
st.subheader("This is my todo app.")
st.write("This app is to increase your productivity.")

# 186: enumerate gives the INDEX too, which pop() needs.
#   a = ["item1", "item2"]
#   for index, todo in enumerate(a):  -> (0, "item1"), (1, "item2")
for index, todo in enumerate(todos):
    # 186: key=todo -> each checkbox has its OWN key (the todo text), so
    # it shows up in st.session_state.
    # st.checkbox returns True if checked, False if not. Store it.
    # CAREFUL: two todos with the SAME text get the SAME key ->
    # StreamlitDuplicateElementKey. Keep every todo different.
    checkbox = st.checkbox(todo, key=todo)
    # True only when the user checked this box.
    if checkbox:
        # Remove the todo at this position from the list.
        todos.pop(index)
        # Save the updated list (without that todo) to todos.txt.
        functions.write_todos(todos)
        # Remove its pair from session_state (del = delete a dict key).
        del st.session_state[todo]
        # Run the whole script again, so the page shows the new list.
        # (video: st.experimental_rerun() -> now st.rerun())
        st.rerun()

# The text box for a new todo (184 + 185).
#   label=""           no visible label (Streamlit warns in the terminal,
#                      but the app works)
#   placeholder=       grey hint text inside the box
#   on_change=add_todo 185: call add_todo when the text changes (Enter).
#                      NO () -> we pass the function, we don't call it.
#   key="new_todo"     185: the name of this box in st.session_state.
st.text_input(label="", placeholder="Add new todo...",
              on_change=add_todo, key="new_todo")
# 176. Code Experiments (image buttons)
# Needs add.png and complete.png next to this file. Do NOT build the exe from it.
import FreeSimpleGUI as sg
import functions
import time                                                  # 175 NEW

sg.theme("Black")                                            # 175 NEW

clock = sg.Text("", key="clock")                             # 175 NEW
label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
# 176 NEW: image button (add.png must be in the same folder as gui.py)
add_button = sg.Button(size=2, image_source="add.png",
                       mouseover_colors="LightBlue2",
                       tooltip="Add todo", key="Add")
list_box = sg.Listbox(values=functions.get_todos(), key="todos",
                      enable_events=True, size=(45, 10))
edit_button = sg.Button("Edit")
# 176 NEW: image button (complete.png must be in the same folder)
complete_button = sg.Button(size=2, image_source="complete.png",
                            mouseover_colors="LightBlue2",
                            tooltip="Complete todo", key="Complete")
exit_button = sg.Button("Exit")

window = sg.Window("My To-Do App",
                   layout=[[clock],                          # 175 NEW row
                           [label],
                           [input_box, add_button],
                           [list_box, edit_button, complete_button],
                           [exit_button]],
                   font=("Helvetica", 20))

while True:
    event, values = window.read(timeout=200)                 # 175 NEW timeout
    window["clock"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))  # 175
    match event:
        case "Add":
            todos = functions.get_todos()
            new_todo = values["todo"] + "\n"
            todos.append(new_todo)
            functions.write_todos(todos)
            window["todos"].update(values=todos)
        case "Edit":
            try:                                              # 175 NEW
                todo_to_edit = values["todos"][0]
                new_todo = values["todo"].strip("\n")
                todos = functions.get_todos()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo + "\n"
                functions.write_todos(todos)
                window["todos"].update(values=todos)
            except IndexError:                                # 175 NEW
                sg.popup("Please select an item first.", font=("Helvetica", 20))
        case "Complete":
            try:                                              # 175 NEW
                todo_to_complete = values["todos"][0]
                todos = functions.get_todos()
                todos.remove(todo_to_complete)
                functions.write_todos(todos)
                window["todos"].update(values=todos)
                window["todo"].update(value="")
            except IndexError:                                # 175 NEW
                sg.popup("Please select an item first.", font=("Helvetica", 20))
        case "Exit":
            break
        case "todos":
            if values["todos"]:
                window["todo"].update(value=values["todos"][0])
        case sg.WIN_CLOSED:
            break

window.close()
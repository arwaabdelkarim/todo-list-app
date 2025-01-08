import functions
import FreeSimpleGUI as gui
import time
import os

if not os.path.exists("todo,txt"):
    with open("todo.txt", "w") as file:
        pass


gui.theme("DarkPurple4")
label_time = gui.Text(key="time", text_color="white")
label = gui.Text("Type in a todo item")
input_box = gui.InputText(tooltip="Enter a todo", key="todo")
add_button = gui.Button("Add")
edit_button = gui.Button("Edit")
complete_button = gui.Button("Complete")
exit_button = gui.Button("Exit")

list_box = gui.Listbox(values=functions.get_todos(),
                       key='todos',
                       enable_events=True,
                       size=(45,10)
                       )

layout = [[label_time],
         [label],
         [input_box, add_button],
         [list_box,edit_button, complete_button],
         [exit_button]
          ]

window = gui.Window("My Todo App",
                    layout= layout,
                    font=('Helvetica', 15))


while True:
    event, values = window.read(timeout=200)
    if event in (gui.WIN_CLOSED, "Exit"):
        break
    window["time"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))
    print(values)
    match event:
        case "Add":
            if values["todo"] == '':
                gui.popup("Please enter a todo", font= ('Helvetica', 15))
                continue
            todos = functions.get_todos()
            new_todo = values["todo"] + '\n'
            todos.append(new_todo)
            functions.write_todos(todos)
            window['todos'].update(values=todos)
            window['todo'].update(value='')
        case "Edit":
            try:
                todo_to_edit = values['todos'][0]
                new_todo = values['todo']
                todos = functions.get_todos()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo
                functions.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except IndexError:
                gui.popup("Please select a todo to edit", font= ('Helvetica', 15))
        case 'Complete':
            try:
                todo_to_complete = values['todos'][0]
                todos = functions.get_todos()
                todos.remove(todo_to_complete)
                functions.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except IndexError:
                gui.popup("Please select a todo to complete", font= ('Helvetica', 15))
        case "Exit":
            break
        case 'todos':
            window['todo'].update(value=values['todos'][0])
        case gui.WIN_CLOSED:
            break
window.close()

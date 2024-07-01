import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.tasks = []
        self.load_tasks()

        # Task input fields
        self.task_name_var = tk.StringVar()
        self.task_due_date_var = tk.StringVar()
        self.task_priority_var = tk.StringVar(value="Medium")
        self.task_category_var = tk.StringVar(value="General")
        self.search_var = tk.StringVar()


        tk.Label(root, text="Task Name:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.task_name_var).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Due Date:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.task_due_date_var).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Priority:").grid(row=3, column=0, padx=10, pady=5)
        tk.OptionMenu(root, self.task_priority_var, "High", "Medium", "Low").grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Category:").grid(row=4, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.task_category_var).grid(row=4, column=1, padx=10, pady=5)

        # Task list display
        self.task_frame = tk.Frame(root)
        self.task_frame.grid(row=1, column=3, rowspan=8, padx=10, pady=5)

        # Buttons at the top
        button_frame = tk.Frame(root)
        button_frame.grid(row=0, column=0, columnspan=8, pady=5)

        tk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Task", command=self.update_task).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Filter", command=self.filter_tasks).grid(row=0, column=3, padx=5)

        tk.Label(root, text="Search:").grid(row=5, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.search_var).grid(row=5, column=1, padx=10, pady=5)
        tk.Button(root, text="Search", command=self.search_tasks).grid(row=6, column=0, columnspan=2, pady=5)

        self.display_tasks()
    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                for line in file:
                    task = eval(line.strip())
                    if 'category' not in task:
                        task['category'] = 'General'
                    self.tasks.append(task)
        
    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(str(task) + "\n")

    def add_task(self):
        task = {
            "name": self.task_name_var.get(),
            "due_date": self.task_due_date_var.get(),
            "priority": self.task_priority_var.get(),
            "category": self.task_category_var.get(),
            "status": "Incomplete"
        }
        self.tasks.append(task)
        self.save_tasks()
        self.display_tasks()

    def update_task(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            index = selected_task_index
            self.tasks[index] = {
                "name": self.task_name_var.get(),
                "due_date": self.task_due_date_var.get(),
                "priority": self.task_priority_var.get(),
                "category": self.task_category_var.get(),
                "status": self.tasks[index]["status"]
            }
            self.save_tasks()
            self.display_tasks()

    def delete_task(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            index = selected_task_index
            self.tasks.pop(index)
            self.save_tasks()
            self.display_tasks()

    def mark_as_complete(self, index):
        self.tasks[index]["status"] = "Complete" if self.tasks[index]["status"] == "Incomplete" else "Incomplete"
        self.save_tasks()
        self.display_tasks()

    def get_selected_task_index(self):
        for widget in self.task_frame.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                if widget.var.get() == 1:
                    return widget.index

    def display_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        for index, task in enumerate(self.tasks):
            task_str = f"{task['name']} - {task['due_date']} - {task['priority']} - {task['category']} - {task['status']}"
            var = tk.IntVar(value=1 if task['status'] == "Complete" else 0)
            checkbutton = tk.Checkbutton(self.task_frame, text=task_str, variable=var, command=lambda i=index: self.mark_as_complete(i))
            checkbutton.var = var
            checkbutton.index = index
            if task['status'] == "Complete":
                checkbutton.config(fg="grey", font=("Arial", 10, "overstrike"))
            checkbutton.pack(anchor="w")

    def filter_tasks(self):
        category = simpledialog.askstring("Filter", "Enter category to filter by:")
        filtered_tasks = [task for task in self.tasks if task["category"] == category]
        self.display_filtered_tasks(filtered_tasks)

    def display_filtered_tasks(self, tasks):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        for index, task in enumerate(tasks):
            task_str = f"{task['name']} - {task['due_date']} - {task['priority']} - {task['category']} - {task['status']}"
            var = tk.IntVar(value=1 if task['status'] == "Complete" else 0)
            checkbutton = tk.Checkbutton(self.task_frame, text=task_str, variable=var, command=lambda i=index: self.mark_as_complete(i))
            checkbutton.var = var
            checkbutton.index = index
            if task['status'] == "Complete":
                checkbutton.config(fg="grey", font=("Arial", 10, "overstrike"))
            checkbutton.pack(anchor="w")

    def search_tasks(self):
        keyword = self.search_var.get().lower()
        searched_tasks = [task for task in self.tasks if keyword in task["name"].lower()]
        self.display_filtered_tasks(searched_tasks)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

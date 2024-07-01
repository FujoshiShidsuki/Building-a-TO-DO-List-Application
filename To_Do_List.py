import tkinter as tk
from tkinter import messagebox
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

        tk.Label(root, text="Task Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.task_name_var).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Due Date:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.task_due_date_var).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Priority:").grid(row=2, column=0, padx=10, pady=5)
        tk.OptionMenu(root, self.task_priority_var, "High", "Medium", "Low").grid(row=2, column=1, padx=10, pady=5)
        
        # Task list display
        self.task_listbox = tk.Listbox(root, height=10, width=50)
        self.task_listbox.grid(row=0, column=3, rowspan=6, padx=10, pady=5)
        self.task_listbox.bind('<<ListboxSelect>>', self.load_task_details)
        
        # Buttons
        tk.Button(root, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Update Task", command=self.update_task).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Delete Task", command=self.delete_task).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Mark as Complete", command=self.mark_as_complete).grid(row=6, column=0, columnspan=2, pady=5)

        self.display_tasks()

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                for line in file:
                    self.tasks.append(eval(line.strip()))
        
    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(str(task) + "\n")

    def add_task(self):
        task = {
            "name": self.task_name_var.get(),
            "due_date": self.task_due_date_var.get(),
            "priority": self.task_priority_var.get(),
            "status": "Incomplete"
        }
        self.tasks.append(task)
        self.save_tasks()
        self.display_tasks()

    def update_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.tasks[index] = {
                "name": self.task_name_var.get(),
                "due_date": self.task_due_date_var.get(),
                "priority": self.task_priority_var.get(),
                "status": self.tasks[index]["status"]
            }
            self.save_tasks()
            self.display_tasks()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.tasks.pop(index)
            self.save_tasks()
            self.display_tasks()

    def mark_as_complete(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.tasks[index]["status"] = "Complete"
            self.save_tasks()
            self.display_tasks()

    def load_task_details(self, event):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            task = self.tasks[index]
            self.task_name_var.set(task["name"])
            self.task_due_date_var.set(task["due_date"])
            self.task_priority_var.set(task["priority"])

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task['name']} - {task['due_date']} - {task['priority']} - {task['status']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

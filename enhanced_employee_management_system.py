import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("600x400")
        self.root.configure(bg="#2f4f7f")

        # Create font styles
        self.title_font = ("Arial", 24, "bold")
        self.label_font = ("Arial", 14)
        self.button_font = ("Arial", 12)

        # Initialize employee data
        self.employees = {}

        # Load data from file
        self.load_data()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Create title label
        self.title_label = tk.Label(self.root, text="Employee Management System", font=self.title_font, bg="#2f4f7f", fg="#ffffff")
        self.title_label.pack(pady=20)

        # Create frame for search and input fields
        input_frame = tk.Frame(self.root, bg="#2f4f7f")
        input_frame.pack(pady=10)

        # Create search entry and button
        search_frame = tk.Frame(input_frame, bg="#2f4f7f")
        search_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.search_entry = tk.Entry(search_frame, font=self.label_font, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_button = tk.Button(search_frame, text="Search", font=self.button_font, command=self.search_employee, bg="#FFC107", fg="#000000")
        self.search_button.pack(side=tk.LEFT, padx=10)

        # Create employee ID label and entry
        self.id_label = tk.Label(input_frame, text="Employee ID:", font=self.label_font, bg="#2f4f7f", fg="#ffffff")
        self.id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.id_entry = tk.Entry(input_frame, font=self.label_font, width=30)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create employee name label and entry
        self.name_label = tk.Label(input_frame, text="Employee Name:", font=self.label_font, bg="#2f4f7f", fg="#ffffff")
        self.name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(input_frame, font=self.label_font, width=30)
        self.name_entry.grid(row=2, column=1, padx=10, pady=5)

        # Create employee department label and entry
        self.dept_label = tk.Label(input_frame, text="Department:", font=self.label_font, bg="#2f4f7f", fg="#ffffff")
        self.dept_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.dept_entry = tk.Entry(input_frame, font=self.label_font, width=30)
        self.dept_entry.grid(row=3, column=1, padx=10, pady=5)

        # Create frame for buttons
        button_frame = tk.Frame(self.root, bg="#2f4f7f")
        button_frame.pack(pady=10)

        # Create add employee button
        self.add_button = tk.Button(button_frame, text="Add Employee", font=self.button_font, command=self.add_employee, bg="#4CAF50", fg="#ffffff")
        self.add_button.pack(side=tk.LEFT, padx=10)

        # Create remove employee button
        self.remove_button = tk.Button(button_frame, text="Remove Employee", font=self.button_font, command=self.open_remove_employee_window, bg="#f44336", fg="#ffffff")
        self.remove_button.pack(side=tk.LEFT, padx=10)

        # Create display employees button
        self.display_button = tk.Button(button_frame, text="Display Employees", font=self.button_font, command=self.display_employees, bg="#03A9F4", fg="#ffffff")
        self.display_button.pack(side=tk.LEFT, padx=10)

        # Create status bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, font=("Arial", 12), bg="#2f4f7f", fg="#ffffff")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def add_employee(self):
        # Get employee data from entries
        employee_id = self.id_entry.get().strip()
        employee_name = self.name_entry.get().strip()
        department = self.dept_entry.get().strip()

        # Validate input
        if not employee_id or not employee_name or not department:
            messagebox.showerror("Error", "All fields are required!")
            return

        if employee_id in self.employees:
            messagebox.showerror("Error", "Employee ID already exists!")
            return

        if not employee_id.isalnum():
            messagebox.showerror("Error", "Employee ID must be alphanumeric!")
            return

        # Add employee to dictionary
        self.employees[employee_id] = {"name": employee_name, "department": department}

        # Clear entries
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dept_entry.delete(0, tk.END)

        # Save data to file
        self.save_data()

        # Update status bar
        self.status_var.set("Employee added successfully!")

    def open_remove_employee_window(self):
        # Create a new window for removing an employee
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Employee")
        remove_window.geometry("300x150")
        remove_window.configure(bg="#03A9F4")

        # Create employee ID label and entry
        id_label = tk.Label(remove_window, text="Employee ID:", font=self.label_font, bg="#03A9F4", fg="#ffffff")
        id_label.pack(pady=10)
        id_entry = tk.Entry(remove_window, font=self.label_font, width=30)
        id_entry.pack(pady=5)

        # Create remove button
        remove_button = tk.Button(remove_window, text="Remove Employee", font=self.button_font, command=lambda: self.remove_employee(id_entry.get().strip(), remove_window), bg="#f44336", fg="#ffffff")
        remove_button.pack(pady=10)

    def remove_employee(self, employee_id, window):
        # Check if employee exists
        if not employee_id:
            messagebox.showerror("Error", "Employee ID is required!")
            return

        if employee_id in self.employees:
            # Delete employee from dictionary
            del self.employees[employee_id]

            # Save data to file
            self.save_data()

            # Display success message
            messagebox.showinfo("Success", "Employee removed successfully!")
        else:
            # Display error message
            messagebox.showerror("Error", "Employee not found!")

        # Update status bar
        self.status_var.set("")

        # Close the remove employee window
        window.destroy()

    def display_employees(self):
        # Create display window
        display_window = tk.Toplevel(self.root)
        display_window.title("Employees")
        display_window.geometry("500x300")
        display_window.configure(bg="#03A9F4")

        # Create Treeview for displaying employees
        columns = ("ID", "Name", "Department")
        tree = ttk.Treeview(display_window, columns=columns, show='headings')

        # Define column headings
        tree.heading("ID", text="Employee ID")
        tree.heading("Name", text="Name")
        tree.heading("Department", text="Department")

        # Define column widths
        tree.column("ID", width=100)
        tree.column("Name", width=200)
        tree.column("Department", width=150)

        # Add Treeview to the window
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Set background color for Treeview rows
        tree.tag_configure("row", background="#03A9F4", foreground="#ffffff")

        # Insert data into Treeview
        for employee_id, employee_data in self.employees.items():
            tree.insert("", tk.END, values=(employee_id, employee_data["name"], employee_data["department"]), tags=("row",))

    def search_employee(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showerror("Error", "Search term cannot be empty!")
            return

        search_results = {id: data for id, data in self.employees.items() if search_term in id.lower() or search_term in data["name"].lower()}

        if not search_results:
            messagebox.showinfo("No Results", "No employees found matching the search term.")
            return

        # Create search results window
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Results")
        search_window.geometry("500x300")
        search_window.configure(bg="#03A9F4")

        # Create Treeview for search results
        columns = ("ID", "Name", "Department")
        tree = ttk.Treeview(search_window, columns=columns, show='headings')

        # Define column headings
        tree.heading("ID", text="Employee ID")
        tree.heading("Name", text="Name")
        tree.heading("Department", text="Department")

        # Define column widths
        tree.column("ID", width=100)
        tree.column("Name", width=200)
        tree.column("Department", width=150)

        # Add Treeview to the window
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Set background color for Treeview rows
        tree.tag_configure("row", background="#03A9F4", foreground="#ffffff")

        # Insert data into Treeview
        for employee_id, employee_data in search_results.items():
            tree.insert("", tk.END, values=(employee_id, employee_data["name"], employee_data["department"]), tags=("row",))

    def save_data(self):
        # Save employee data to a JSON file
        try:
            with open("employees.json", "w") as file:
                json.dump(self.employees, file, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    def load_data(self):
        # Load employee data from a JSON file if it exists
        if os.path.exists("employees.json"):
            try:
                with open("employees.json", "r") as file:
                    self.employees = json.load(file)
            except IOError as e:
                messagebox.showerror("Error", f"An error occurred while loading the file: {e}")
            except json.JSONDecodeError:
                messagebox.showwarning("Warning", "Data file is corrupt or empty.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()

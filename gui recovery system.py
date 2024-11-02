import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import os

# Ensure the log file exists
log_file = 'event_logs.txt'
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        f.write("Event Logs:\n")

# Function to create a recovery system
def create_recovery_system():
    api_url = "http://127.0.0.1:5000/v2/systems"

    # Input the system's ID and name (could be enhanced with more fields)
    system_id = len(recovery_systems) + 1
    system_name = f"Recovery System {system_id}"
    data = {"id": system_id, "name": system_name}

    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        recovery_systems.append(data)  # Update local system list
        update_system_list()  # Update the display in the GUI
        messagebox.showinfo("Success", f"{system_name} created successfully!")
    else:
        messagebox.showerror("Error", "Failed to create recovery system.")

# Function to list recovery systems and display them in the GUI
def list_recovery_systems():
    api_url = "http://127.0.0.1:5000/v2/systems"
    response = requests.get(api_url)

    if response.status_code == 200:
        global recovery_systems
        recovery_systems = response.json()
        update_system_list()  # Update the display with the fetched systems
    else:
        messagebox.showerror("Error", "Failed to fetch recovery systems.")

# Function to reboot the system to recovery mode
def reboot_to_recovery_mode():
    api_url = "http://127.0.0.1:5000/v2/reboot"

    if not recovery_systems:
        messagebox.showerror("Error", "No systems available to reboot.")
        return

    system_name = recovery_systems[-1]["name"]  # Reboot the last created system
    data = {"name": system_name}
    headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        messagebox.showinfo("Reboot", response.json()["message"])
    else:
        messagebox.showerror("Error", "Failed to reboot system.")

# Function to fetch and display event logs
def view_logs():
    api_url = "http://127.0.0.1:5000/v2/logs"
    response = requests.get(api_url)

    if response.status_code == 200:
        logs = response.json()
        logs_display.delete(1.0, tk.END)
        for log in logs:
            logs_display.insert(tk.END, f"{log.strip()}\n")
    else:
        messagebox.showerror("Error", "Failed to fetch event logs.")

# Function to update the system list in the GUI
def update_system_list():
    for item in system_listbox.get_children():
        system_listbox.delete(item)

    for system in recovery_systems:
        system_listbox.insert("", "end", values=(system['id'], system['name']))

# Initial recovery systems (could be fetched from the server)
recovery_systems = []

# GUI setup
root = tk.Tk()
root.title("Recovery System GUI")
root.geometry("500x400")

# Create buttons for each function
create_button = tk.Button(root, text="Create Recovery System", command=create_recovery_system)
create_button.pack(pady=10)

list_button = tk.Button(root, text="Fetch & List Recovery Systems", command=list_recovery_systems)
list_button.pack(pady=10)

reboot_button = tk.Button(root, text="Reboot to Recovery Mode", command=reboot_to_recovery_mode)
reboot_button.pack(pady=10)

logs_button = tk.Button(root, text="View Event Logs", command=view_logs)
logs_button.pack(pady=10)

# Listbox to display recovery systems
columns = ('ID', 'Name')
system_listbox = ttk.Treeview(root, columns=columns, show='headings')
system_listbox.heading('ID', text='ID')
system_listbox.heading('Name', text='Name')
system_listbox.pack(pady=10, fill='both', expand=True)

# Text box to display event logs
logs_display = tk.Text(root, height=5)
logs_display.pack(pady=10, fill='both', expand=True)

# Start the GUI main loop
root.mainloop()
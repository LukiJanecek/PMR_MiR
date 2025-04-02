import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import json

class RestApiGui:
    def __init__(self, root):
        self.root = root
        self.root.title("REST API GUI")
        self.root.geometry("600x400")
        
        self.client_socket = None
        self.data_scenarios = []  # To store downloaded data
        self.create_login_ui()
        
    def create_login_ui(self):
        self.clear_window()
        
        tk.Label(self.root, text="Select Role:").pack()
        self.auth_var = tk.StringVar()
        self.auth_menu = tk.OptionMenu(self.root, self.auth_var, "distributor", "admin", "student")
        self.auth_menu.pack()

        tk.Label(self.root, text="Select Robot:").pack()
        self.robot_var = tk.StringVar()
        self.robot_menu = tk.OptionMenu(self.root, self.robot_var, "MiR100", "MiR250", "MiR500")
        self.robot_menu.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_robot)
        self.connect_button.pack(pady=10)
    
    def connect_to_robot(self):
        auth_code = self.auth_var.get()
        robot_number = self.robot_var.get()
        
        if not auth_code or not robot_number:
            messagebox.showerror("Error", "Please select both Role and Robot.")
            return
        
        self.client_socket = True  # Simulated connection
        messagebox.showinfo("Info", f"Successfully connected to {robot_number} as {auth_code}!")
        self.create_data_ui()
    
    def create_data_ui(self):
        self.clear_window()
        
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)
        
        self.download_button = tk.Button(left_frame, text="Download Data", command=self.download_data)
        self.download_button.pack(anchor='w')
        
        tk.Label(left_frame, text="Select Mission:").pack(anchor='w')
        self.mission_var = tk.StringVar()
        self.mission_menu = tk.OptionMenu(left_frame, self.mission_var, "")
        self.mission_menu.pack(anchor='w')
        
        tk.Label(left_frame, text="Select Map:").pack(anchor='w')
        self.map_var = tk.StringVar()
        self.map_menu = tk.OptionMenu(left_frame, self.map_var, "")
        self.map_menu.pack(anchor='w')
        
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.data_listbox = tk.Text(right_frame, wrap=tk.WORD)
        self.data_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
    
    def download_data(self):
        # Simulated JSON response
        json_response = {
            "scenarios": ["Mission A", "Mission B", "Mission C"],
            "maps": ["Map 1", "Map 2", "Map 3"],
            "full_data": {"Mission A": {"info": "Details about Mission A"},
                           "Mission B": {"info": "Details about Mission B"},
                           "Mission C": {"info": "Details about Mission C"}}
        }
        
        self.data_scenarios = json_response["scenarios"]
        maps = json_response["maps"]
        
        # Update dropdowns
        self.mission_menu['menu'].delete(0, 'end')
        self.map_menu['menu'].delete(0, 'end')
        
        for mission in self.data_scenarios:
            self.mission_menu['menu'].add_command(label=mission, command=tk._setit(self.mission_var, mission))
        for map_name in maps:
            self.map_menu['menu'].add_command(label=map_name, command=tk._setit(self.map_var, map_name))
        
        # Display full JSON data in text widget
        self.data_listbox.delete(1.0, tk.END)
        self.data_listbox.insert(tk.END, json.dumps(json_response["full_data"], indent=4))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        messagebox.showinfo("Info", f"Data saved as scenarios_{timestamp}.txt")
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = RestApiGui(root)
    root.mainloop()

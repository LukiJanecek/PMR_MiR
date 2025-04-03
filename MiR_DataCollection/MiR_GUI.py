import MiR_BE
import MiR_BE_TEMPORARY

import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import json

from tkinter import Menu

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class RestApiGui:
    def __init__(self, root):
        self.root = root
        self.root.title("MiR REST API GUI")

        width = 250
        height = 170

        self.place_to_center_tool(250, 170)

        self.create_login_ui()
        
    def create_login_ui(self):
        self.clear_window()

        
        tk.Label(self.root, text="Select Role:").pack()
        self.auth_var = tk.StringVar()
        self.auth_var.set("student")
        self.auth_menu = tk.OptionMenu(self.root, self.auth_var, "distributor", "admin", "student")
        self.auth_menu.pack()

        tk.Label(self.root, text="Select Robot:").pack()
        self.robot_var = tk.StringVar()
        self.robot_var.set("MiR100")
        self.robot_menu = tk.OptionMenu(self.root, self.robot_var, "MiR100", "MiR250", "MiR500")
        self.robot_menu.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=lambda: self.try_connect(self.auth_var.get(), self.robot_var.get()))
        self.connect_button.pack(pady=10)

    def try_connect(self, auth_code, robot_number):
        if not auth_code or not robot_number:
            messagebox.showerror("Error", "Please select both Role and Robot.")
            return
      
        success = MiR_BE_TEMPORARY.connect_to_robot(auth_code, robot_number)
        if not success:
            messagebox.showerror("Error", f"Failed to connect to {robot_number} as {auth_code}.")
            return
        if success:
            messagebox.showinfo("Info", f"Successfully connected to {robot_number} as {auth_code}!")
            self.main_data_ui()

        
    def main_data_ui(self):
        self.clear_window()
        self.place_to_center_tool(450, 400)

        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)

        # Rámec pro tlačítka vedle sebe
        button_frame = tk.Frame(left_frame)
        button_frame.pack(anchor='w', pady=(0, 10))

        self.downloadData_button = tk.Button(button_frame, text="Download data", command=self.download_data)
        self.downloadData_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(button_frame, text="Start", command=self.startMission)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Rámec pro tlačítka vedle sebe
        button_frame = tk.Frame(left_frame)
        button_frame.pack(anchor='w', pady=(0, 10))

        tk.Label(button_frame, text="Select Map:").pack(side=tk.LEFT)
        self.map_var = tk.StringVar()
        self.map_menu = tk.OptionMenu(button_frame, self.map_var, "")
        self.map_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(button_frame, text="Select Mission:").pack(side=tk.LEFT)
        self.mission_var = tk.StringVar()
        self.mission_menu = tk.OptionMenu(button_frame, self.mission_var, "")
        self.mission_menu.pack(side=tk.LEFT, padx=5)

        # Listbox pod tlačítky
        self.dataMaps_listbox = tk.Text(left_frame, wrap=tk.WORD, height=15, width=50)
        self.dataMaps_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def download_data(self):
        
        maps = MiR_BE_TEMPORARY.get_map()
        if not maps:
            messagebox.showerror("Error", "Failed to retrieve maps.")
            return
        
        missions = MiR_BE_TEMPORARY.get_mission()
        if not missions:
            messagebox.showerror("Error", "Failed to retrieve missions.")
            return
      
        self.maps = maps
        self.missions = missions

        self.dataMaps_listbox.delete(1.0, tk.END)

        self.dataMaps_listbox.insert(tk.END, "Maps:\n")
        for map_item in self.maps:
            self.dataMaps_listbox.insert(tk.END, f"{map_item}\n")

        self.dataMaps_listbox.insert(tk.END, "\nMissions:\n")
        for mission_item in self.missions:
            self.dataMaps_listbox.insert(tk.END, f"{mission_item}\n")

        self.map_menu['menu'].delete(0, 'end')
        for map_item in self.maps:
            self.map_menu['menu'].add_command(label=map_item, command=tk._setit(self.map_var, map_item))

        self.mission_menu['menu'].delete(0, 'end')
        for mission_item in self.missions:
            self.mission_menu['menu'].add_command(label=mission_item, command=tk._setit(self.mission_var, mission_item))

    def startMission(self):   
        map = self.map_var.get()
        mission = self.mission_var.get()

        if not map or not mission:
          messagebox.showerror("Error", "Please select both Map and Mission.")
          return
      
        success = MiR_BE_TEMPORARY.start_mission(map, mission)
        if not success:
          messagebox.showerror("Error", f"Failed to start map: {map} and mission: {mission}.")
          return
        if success:
          messagebox.showinfo("Error", f"Successfully started map: {map} and mission: {mission}.")
          self.process_data_ui()


    def process_data_ui(self):
        self.clear_window()
        self.place_to_center_tool(600, 400)
        
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        self.data_categories = ["Brakes", "Temp", "Battery", "Current", "Speed"]
        self.data = {item: [random.randint(0, 100) for _ in range(10)] for item in self.data_categories}
        
        data_menu = Menu(menu_bar, tearoff=0)
        for item in self.data_categories:
            data_menu.add_command(label=item, command=lambda i=item: self.update_plot(i))
        menu_bar.add_cascade(label="Select Data", menu=data_menu)
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.listbox = tk.Listbox(main_frame, height=20, width=30)
        self.listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.update_plot("Brakes")

    def update_plot(self, category):
        """Aktualizuje listbox a graf pro vybranou kategorii."""
        self.listbox.delete(0, tk.END)
        values = self.data[category]
        for val in values:
            self.listbox.insert(tk.END, val)
        
        self.ax.clear()
        self.ax.plot(values, marker='o', linestyle='-')
        self.ax.set_title(category)
        self.ax.set_ylabel("Value")
        self.ax.set_xlabel("Time")
        self.canvas.draw()


    def place_to_center_tool(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y-100}")
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = RestApiGui(root)
    root.mainloop()


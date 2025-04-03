import MiR_BE
import MiR_BE_TEMPORARY

import tkinter as tk
from tkinter import messagebox, Menu
import requests
from datetime import datetime
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class RestApiGui:
    def __init__(self, root):
        self.root = root
        self.root.title("MiR REST API GUI")

        self.place_to_center_tool(450, 400)
        self.create_login_ui()
        
        # Data pro grafy
        self.data_categories = ["Brakes", "Temp", "Battery", "Current", "Speed"]
        self.data = {item: [random.randint(0, 100) for _ in range(10)] for item in self.data_categories}

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
        
        messagebox.showinfo("Info", f"Successfully connected to {robot_number} as {auth_code}!")
        self.main_data_ui()

    def main_data_ui(self):
        self.clear_window()
        self.place_to_center_tool(600, 400)
        
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
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

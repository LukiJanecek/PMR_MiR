import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class RestApiGui:
    def __init__(self, root):
        self.root = root
        self.root.title("REST API GUI")
        self.root.geometry("800x500")

        self.client_socket = None
        
        # Levá část pro výběr
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(left_frame, text="Authorization Code:").pack()
        self.auth_var = tk.StringVar()
        self.auth_menu = tk.OptionMenu(left_frame, self.auth_var, "distributor", "admin", "student")
        self.auth_menu.pack()

        tk.Label(left_frame, text="Robot Number:").pack()
        self.robot_var = tk.StringVar()
        self.robot_menu = tk.OptionMenu(left_frame, self.robot_var, "500", "251", "250", "100")
        self.robot_menu.pack()

        self.connect_button = tk.Button(left_frame, text="Connect to Robot", command=self.connect_to_robot)
        self.connect_button.pack(pady=10)

        self.command_button = tk.Button(left_frame, text="Execute Command", command=self.execute_command, state=tk.DISABLED)
        self.command_button.pack(pady=10)

        # Pravá část pro graf
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.LEFT, padx=10, pady=10)

        fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(fig, master=right_frame)
        self.canvas.get_tk_widget().pack()

        
        # Zavření okna a ukončení procesů
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect_to_robot(self):
        auth_code = self.auth_var.get()
        robot_number = self.robot_var.get()

        if not auth_code or not robot_number:
            messagebox.showerror("Error", "Please select both Authorization Code and Robot Number.")
            return

        ip_addresses = {
            "100": "MIR_IP_100",
            "250": "MIR_IP_250",
            "251": "MIR_IP_251",
            "500": "MIR_IP_500"
        }

        self.active_ipAddress = ip_addresses.get(robot_number, "Unknown")

        if self.active_ipAddress == "Unknown":
            messagebox.showerror("Error", "Invalid robot number selected.")
            return

        self.client_socket = True  # Simulace připojení
        messagebox.showinfo("Info", f"Successfully connected to MiR {robot_number} as {auth_code}!")
        self.command_button.config(state=tk.NORMAL)

    def execute_command(self):
        data_name = "swagger"
        dataCommand = "swagger"
        mir_data = {"/Motors/Brake": {"values": {"Voltage": "24V", "Board temperature": "40°C"}}}  # Simulace

        if mir_data:
            messagebox.showinfo("Info", "Data successfully retrieved!")
            voltage = mir_data["/Motors/Brake"]["values"].get("Voltage", "N/A")
            board_temperature = mir_data["/Motors/Brake"]["values"].get("Board temperature", "N/A")
            messagebox.showinfo("Data", f"Voltage: {voltage} V\nBoard temperature: {board_temperature} °C")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            messagebox.showinfo("Info", f"Data saved as mir_{data_name}_{timestamp}")

    def on_close(self):
        if self.client_socket:
            # Před zavřením okna ukončíme socket nebo jakýkoli jiný proces
            print("Closing connection...")
            self.client_socket = None
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = RestApiGui(root)
    root.mainloop()

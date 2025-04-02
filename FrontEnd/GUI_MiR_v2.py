import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import json
import socket

MIR_IP_100 = "192.168.1.100"
MIR_IP_250 = "192.168.1.250"
MIR_IP_251 = "192.168.1.251"
MIR_IP_500 = "192.168.1.150"
MIR_port = 443
MIR_100_url = f"http://{MIR_IP_100}:{MIR_port}"
MIR_250_url = f"http://{MIR_IP_250}:{MIR_port}"
MIR_251_url = f"http://{MIR_IP_251}:{MIR_port}"
MIR_500_url = f"http://{MIR_IP_500}:{MIR_port}"
authorization_code_student = "Basic c3R1ZGVudDoyNjRjOGMzODFiZjE2Yzk4MmE0ZTU5YjBkZDRjNmY3ODA4YzUxYTA1ZjY0YzM1ZGI0MmNjNzhhMmE3Mjg3NWJi"
authorization_code_admin = "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA=="
authorization_code_distributor = "Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=="
usernameStudent = "student"
passwordStudent = "student"
usernameAdmin = "admin"
passwordAdmin = "admin"
usernameDistributor = "distributor"
passwordDistributor = "distributor"
API_KEY = "your_api_key_here"
HEADERS = {"Authorization": f"{authorization_code_distributor}", "Content-Type": "application/json"}
fileDirectory = "Data/MIR_data"

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
        self.auth_var.set("distributor")  # Default value
        self.auth_menu = tk.OptionMenu(self.root, self.auth_var, "distributor", "admin", "student")
        self.auth_menu.pack()

        tk.Label(self.root, text="Select Robot:").pack()
        self.robot_var = tk.StringVar()
        self.robot_var.set("100")  # Default value
        self.robot_menu = tk.OptionMenu(self.root, self.robot_var, "100", "250", "500")
        self.robot_menu.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_robot)
        self.connect_button.pack(pady=10)

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

    def connect_to_ip(self, ip_address, port, api_key):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_address, port))
            print(f"Connected to {ip_address}:{port}")
            authorization_request = f"GET / HTTP/1.1\r\nHost: {ip_address}\r\nAuthorization: Bearer {api_key}\r\n\r\n"
            client_socket.sendall(authorization_request.encode('utf-8'))
            response = client_socket.recv(4096).decode('utf-8')
            return client_socket
        except socket.error as e:
            print(f"Error in connection: {e}")
            return None

    def close_connection(self, client_socket):
        try:
            if client_socket:
                client_socket.close()
                print("Connection closed.")
                return True
            else:
                print("No connection to close.")
                return False
        except Exception as e:
            print(f"Error while closing connection: {e}")
            return False

    def get_status(self, ip_address):
        #"""Získá celkový stav robota."""
        url = f"http://{ip_address}/api/v2.0/status"
        return self.fetch_data(url)

    def get_missions(self, ip_address):
        #"""Získá seznam dostupných misí."""
        url = f"http://{ip_address}/api/v2.0/missions"
        return self.fetch_data(url)

    def get_position(self):
        #"""Získá aktuální pozici robota."""
        status = self.get_status()
        if status and "position" in status:
            return status["position"]
        return None

    def get_mission_queue(self, ip_address):
        #"""Získá seznam misí ve frontě."""
        url = f"http://{ip_address}/api/v2.0/mission_queue"
        return self.fetch_data(url)

    def fetch_data(self, url):
        #"""Pomocná funkce pro získání dat z daného endpointu."""
        try:
            response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Chyba při získávání dat z {url}: {e}")
            return None

    def get_data(self, ip_address, command):
        try:
            url = f"http://{ip_address}/api/v2.0.0/{command}"

            response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error in fetching data from {ip_address}: {e}")
            return None

    def connect_to_robot(self):
        robot_number = self.robot_var.get()
        print(f"Selected robot number: {robot_number}")  # Log selected robot number
        authorization_code = self.get_authorization_code(self.auth_var.get())
        
        if robot_number and authorization_code:
            robot_ip = self.get_robot_ip(robot_number)
            if robot_ip:
                print(f"Connecting to IP: {robot_ip}")  # Log robot IP
                client_socket = self.connect_to_ip(robot_ip, MIR_port, authorization_code)
                if client_socket:
                    print("Connected successfully.")
                    self.create_data_ui()  # Call method to switch to the next window (UI)
                else:
                    messagebox.showerror("Connection Error", "Failed to connect to the robot.")
            else:
                print(f"Invalid robot number. Available options: 500, 250, 100.")  # Log invalid robot
        else:
            print("Invalid robot number or authorization code.")
        return None


    def get_robot_ip(self, robot_number):
          if robot_number == "500":
              return MIR_IP_500
          elif robot_number == "251":
              return MIR_IP_251
          elif robot_number == "250":
              return MIR_IP_250
          elif robot_number == "100":
              return MIR_IP_100
          else:
              print(f"Invalid robot number selected: {robot_number}")  # Log invalid robot number
              return None


    def get_authorization_code(self, role):
        if role == "distributor":
            return authorization_code_distributor
        elif role == "admin":
            return authorization_code_admin
        elif role == "student":
            return authorization_code_student
        else:
            print("Invalid role.")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = RestApiGui(root)
    root.mainloop()

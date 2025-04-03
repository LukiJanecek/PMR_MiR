def connect_to_robot(auth_code, robot_number):
        return True  # Simulated successful connection

        auth_code = self.auth_var.get()
        robot_number = self.robot_var.get()
        
        if not auth_code or not robot_number:
            messagebox.showerror("Error", "Please select both Role and Robot.")
            return
        
        self.client_socket = True  # Simulated connection
        messagebox.showinfo("Info", f"Successfully connected to {robot_number} as {auth_code}!")
        self.create_data_ui()




def get_map():
    json_response = {
        "scenarios": ["Mission A", "Mission B", "Mission C"],
        "maps": ["Map 1", "Map 2", "Map 3"],
        "full_data": {
            "Mission A": {"info": "Details about Mission A"},
            "Mission B": {"info": "Details about Mission B"},
            "Mission C": {"info": "Details about Mission C"}
        }
    }
    
    return list(json_response["maps"])


def get_mission():
    json_response = {
        "missions": ["Mission A", "Mission B", "Mission C"],
        "maps": ["Map 1", "Map 2", "Map 3"],
        "full_data": {
            "Mission A": {"info": "Details about Mission A"},
            "Mission B": {"info": "Details about Mission B"},
            "Mission C": {"info": "Details about Mission C"}
        }
    }
    
    return list(json_response["missions"])

def start_mission(map, mission):

    return True
        
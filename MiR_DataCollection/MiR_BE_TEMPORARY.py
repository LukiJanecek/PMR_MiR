def connect_to_robot(auth_code, robot_number):
        return True  # Simulated successful connection



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
        
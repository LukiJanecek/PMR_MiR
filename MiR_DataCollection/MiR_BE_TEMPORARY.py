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


def close_connection():
    return True


def get_all_maps():
    command = "maps"
    
    response = getData(command)
    if not response:
        print("Could not retrieve maps.")
        return []
    
    # vyhledávání map, která nás zajímají 
    preferred_maps = ["map1", "map2", "map3"]  # Příklad preferovaných map
    filtered_maps = [
        {"name": m["name"], "guid": m["guid"]}
        for m in response
        if m.get("name") in preferred_maps
    ]

    return filtered_maps

def get_all_missions():
    command = "missions"
    
    response = getData(command)
    if not response:
        print("Could not retrieve missions.")
        return []
    
    # vyhledávání misí, která nás zajímají
    preferred_missions = ["StartMission", "ChargeBattery", "DeliveryA", "Dny otevřených dveří"]
    filtered_missions = [
        {"name": m["name"], "guid": m["guid"]}
        for m in response
        if m.get("name") in preferred_missions
    ]

    return filtered_missions

def set_map(map_id):
    command = "status"
    url = f"http://{active_ip_address}/api/v2.0.0/{command}"

    payload = {
        "map_id": map_id
    }

    try:
        response = requests.put(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            print("🗺️ Map successfully set as active.")
            return True
        else:
            print(f"❌ Failed to set map. Status code: {response.status_code}")
            print("Response:", response.text)
            return False
    except Exception as e:
        print(f"❌ Error setting map: {e}")
        return False

def start_mission(mission_id):
    command = "mission_queue"
    url = f"http://{active_ip_address}/api/v2.0.0/{command}"

    payload = {
        "mission_id": mission_id
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 201:
            print("✅ Mission successfully started!")
            return True
        else:
            print(f"❌ Failed to start mission. Status code: {response.status_code}")
            print("Response:", response.text)
            return False
    except Exception as e:
        print(f"❌ Error starting mission: {e}")
        return False

def measure_data_during_mission(kat):
    start_time = time.time()
    voltage_data = []
    temperature_data = []

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            print("⏱️ Timeout reached, stopping measurement.")
            break

        result, mission_finished = getDesiredData()
        if mission_finished:
            print("✅ Mission ended.")
            break

        if result:
            voltage, temp = result
            voltage_data.append(voltage)
            temperature_data.append(temp)

        time.sleep(interval_seconds)

    return voltage_data, temperature_data
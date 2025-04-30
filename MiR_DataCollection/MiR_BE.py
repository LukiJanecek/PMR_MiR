import os 
import requests
import socket 
import json
import csv 
from datetime import datetime
import time 

import MiR_parameters as param

#############################################################################################
# Functions for BE
def connect_to_ip(ip_address, port, api_key):
    try:
        param.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        param.client_socket.connect((ip_address, port))
        print(f"Connected to {ip_address}:{port}")
        authorization_request = f"GET / HTTP/1.1\r\nHost: {ip_address}\r\nAuthorization: Bearer {api_key}\r\n\r\n"
        param.client_socket.sendall(authorization_request.encode('utf-8'))
        response = param.client_socket.recv(4096).decode('utf-8')
        return True  
    except socket.error as e:
        print(f"Error in connection: {e}")
        return False
    
def getData(command):
    try:
        if param.activeRobot == "100":
            param.active_ip_address = param.MIR_IP_100
        elif param.activeRobot == "250":
            param.active_ip_address = param.MIR_IP_250
        elif param.activeRobot == "251":
            param.active_ip_address = param.MIR_IP_251
        elif param.activeRobot == "500":
            param.active_ip_address = param.MIR_IP_500
        else:
            print("Invalid robot number. Available options: 500, 251, 250, 100.")
            return False
        
        url = f"http://{param.active_ip_address}/api/v2.0.0/{command}"
        print(url)
        
        HEADERS = {"Authorization": f"{param.activeAuthKey}", "Content-Type": "application/json"}

        response = requests.get(url, headers = HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error in fetching data from {param.active_ip_address}: {e}")
        return False
    
def getDesiredData(): 
    command = f"mission_queue/{param.activeMission}"
    url = f"http://{param.active_ip_address}/api/v2.0.0/{command}"
    HEADERS = {"Authorization": f"{param.activeAuthKey}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        mission_status = response.json()

        state = mission_status.get("state", "")
        print(f"🔄 Mission state: {state}")

        if state != "Executing":
            print("✅ Mission is not running. Skipping measurement.")
            return None, True

    except requests.RequestException as e:
        print(f"❌ Error while checking mission state: {e}")
        return None, True

    # === Pokud mise běží, stáhni diagnostická data ===
    data_command = "experimental/diagnostics"
    data_url = f"http://{param.active_ip_address}/api/v2.0.0/{data_command}"

    try:
        response = requests.get(data_url, headers=HEADERS)
        response.raise_for_status()
        mir_data = response.json()
    except requests.RequestException as e:
        print(f"⚠️ Failed to retrieve diagnostic data: {e}")
        return None, False

    brake_info = mir_data.get("/Motors/Brake", {}).get("values", {})

    voltage = brake_info.get("Voltage", "N/A")
    temperature = brake_info.get("Board temperature", "N/A")

    print(f"🔋 Voltage: {voltage} V | 🌡️ Temp: {temperature} °C")
    return (voltage, temperature), False

def delete_mission_queue():
    command = "mission_queue"
    url = f"http://{param.active_ip_address}/api/v2.0.0/{command}"
     
    try:
        HEADERS = {"Authorization": f"{param.activeAuthKey}", "Content-Type": "application/json"}
        response = requests.delete(url, headers = HEADERS)
        if response.status_code == 204:
            print("🛑 Mission(s) successfully stopped.")
            return True
        else:
            print(f"❌ Failed to stop missions. Status code: {response.status_code}")
            print("Response:", response.text)
            return False
    except Exception as e:
        print(f"❌ Error stopping missions: {e}")
        return False    
    
def get_mission_queue():
    command = "mission_queue"
    url = f"http://{param.active_ip_address}/api/v2.0.0/{command}"
    HEADERS = {"Authorization": f"{param.activeAuthKey}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Failed to get mission queue. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error retrieving mission queue: {e}")
        return None

def isMissionRunning(mission_queue_id, attempts = 10, delay = 100, timeout = 200):
    command = "mission_queue"
    url = f"http://{param.active_ip_address}/api/v2.0.0/{command}/{mission_queue_id}"
    HEADERS = {"Authorization": f"{param.activeAuthKey}", "Content-Type": "application/json"}
    start_time = time.time()

    while time.time() - start_time < timeout:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        status = response.json()["state"]
        
        print(f"Mission state: {status}")
        
        if status == "Executing":
            print("Mission is now running.")
            return True
        elif status in ["Done", "Failed", "Aborted"]:
            print(f"Mission ended prematurely with state: {status}")
            return False

        time.sleep(1)

    print("Timeout waiting for mission to start.")
    return False
    
    
    for attempt in range(attempts):
        #time.sleep(delay)
        queue = get_mission_queue()

        if queue and isinstance(queue, list) and len(queue) > 0:
            latest_mission = queue[-1]  # kontrolujeme POSLEDNÍ misi ve frontě
            state = latest_mission.get("state", "").lower()

            print(f"🔍 Last mission in queue state: {state}")

            if state in ["executing", "active", "running"]:
                return True
        else:
            print("⚠️ Mission queue data is empty or invalid.")

    return False

#############################################################################################
# Functions for FE

def connect_to_robot(robot_number, auth_key):
    try:
        param.activeRobot = robot_number

        if auth_key == "student":
            param.activeAuthKey = param.authorization_code_student
        elif auth_key == "admin":
            param.activeAuthKey = param.authorization_code_admin
        elif auth_key == "distributor":
            param.activeAuthKey = param.authorization_code_distributor
        else:
            print("Invalid authorization key. Available options: student, admin, distributor.")
            return False
        
        if param.activeRobot == "100":
            return connect_to_ip(param.MIR_IP_100, param.MIR_port, param.activeAuthKey)
        elif param.activeRobot == "250":
            return connect_to_ip(param.MIR_IP_250, param.MIR_port, param.activeAuthKey)
        elif param.activeRobot == "251":
            return connect_to_ip(param.MIR_IP_251, param.MIR_port, param.activeAuthKey)
        elif param.activeRobot == "500":
            return connect_to_ip(param.MIR_IP_500, param.MIR_port, param.activeAuthKey)
        else:
            print("Invalid robot number. Available options: 500, 251, 250, 100.")
            return False
    except socket.error as e:
        print(f"Socket error: {e}")
        return False

def close_connection():
    try:
        if param.client_socket:
            param.client_socket.close()
            print("Connection closed.")
            return True
        else:
            print("No connection to close.")
            return False
    except Exception as e:
        print(f"Error while closing connection: {e}")
        return False
    
def get_all_maps():
    command = "maps"
    response = getData(command)
    if not response:
        print("Could not retrieve maps.")
        return []
    
    # vyhledávání map, která nás zajímají 
    preferred_maps = ["KAS0249"]  # Příklad preferovaných map
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
    preferred_missions = ["KAS0249_1", "KAS0249_2"]
    filtered_missions = [
        {"name": m["name"], "guid": m["guid"]}
        for m in response
        if m.get("name") in preferred_missions
    ]

    return filtered_missions

def set_map(map_id):
    command = "status"
    url = f"http://{param.active_ip_address}/api/v2.0.0/{command}"
    HEADERS = {"Authorization": f"{param.activeAuthKey}", "Content-Type": "application/json"}

    payload = {
        "map_id": map_id
    }

    try:
        # actual map 
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        current_status = response.json()
        current_map_id = current_status.get("map_id", None)

        if current_map_id == map_id:
            print("✅ Map is already active – no change needed.")
            return True, False  # True = OK, False = není třeba zásah

        # change map
        response = requests.put(url, headers = HEADERS, json=payload)
        if response.status_code == 200:
            print("🗺️ Map successfully set as active.")
            print("⚠️ Please make sure to confirm the map change on the robot’s touchscreen if needed.")
            return True, True
        else:
            print(f"❌ Failed to set map. Status code: {response.status_code}")
            print("Response:", response.text)
            return False, False
    except Exception as e:
        print(f"❌ Error setting map: {e}")
        return False, False

def start_mission(mission_id):    
    
    # delete actual queue
    delete_mission_queue()
    
    command = "mission_queue"
    url = f"http://{param.active_ip_address}/api/v2.0.0/{command}"

    payload = {
        "mission_id": mission_id
    }

    try:
        HEADERS = {"Authorization": f"{param.activeAuthKey}", "Content-Type": "application/json"}
        response = requests.post(url, headers = HEADERS, json=payload)
        response.raise_for_status()
        mission_queue_id = response.json()["id"]
        print(f"Mission started in queue with ID: {mission_queue_id}")

        if response.status_code == 201:
            print("✅ Mission successfully started!")

            # verify mission queue 
            if isMissionRunning(mission_queue_id):
                print("🚀 Mission is now running!")
                param.activeMission = mission_queue_id
                return True
            else:
                print("❌ Mission not running after multiple checks.")
                return False
        else:
            print(f"❌ Failed to start mission. Status code: {response.status_code}")
            print("Response:", response.text)
            return False
    except Exception as e:
        print(f"❌ Error starting mission: {e}")
        return False

def dataMeasuring():
    result, mission_finished = getDesiredData()
        
    if mission_finished:
        print("✅ Mission ended.")
        return mission_finished, param.dataBreaksVoltage, param.dataBreaksTemperature, param.dataBreaksTimestamps

    if result:
        voltage, temp = result
        print(f"🔋 Voltage: {voltage} V | 🌡️ Temp: {temp} °C")
        param.dataBreaksVoltage.append(voltage)
        param.dataBreaksTemperature.append(temp)
        param.dataBreaksTimestamps.append(datetime.now())
    
    return mission_finished, param.dataBreaksVoltage, param.dataBreaksTemperature, param.dataBreaksTimestamps

def save_to_json(data, fileName, folder):
    try:
        os.makedirs(folder, exist_ok = True)  # Vytvoří složku, pokud neexistuje
        full_path = os.path.join(folder, f"{fileName}.json")
        
        with open(full_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {full_path}.")
        return True
    except Exception as e:
        print(f"Error saving data to JSON: {e}")
        return False

def save_to_csv(data, fileName, folder):
    try:
        os.makedirs(folder, exist_ok = True)  # Vytvoří složku, pokud neexistuje
        full_path = os.path.join(folder, f"{fileName}.csv")
        
        with open(full_path, mode='w', newline='') as csv_file:
            if isinstance(data, list):  # Pokud jsou data list slovníků (JSON Array)
                if len(data) > 0:
                    keys = data[0].keys()
                    writer = csv.DictWriter(csv_file, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
            elif isinstance(data, dict):  # Pokud jsou data slovník (JSON Object)
                writer = csv.writer(csv_file)
                for key, value in data.items():
                    writer.writerow([key, value])
        print(f"Data successfully saved to {full_path}.")
        return True
    except Exception as e:
        print(f"Error saving data to CSV: {e}")
        return False

#############################################################################################


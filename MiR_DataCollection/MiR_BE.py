import os 
import requests
import socket 
import json
import csv 
from datetime import datetime
import time 

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

fileDirectory = "Data/MIR_data"

activeRobot = None
activeAuthKey = None

HEADERS = {"Authorization": f"{activeAuthKey}", "Content-Type": "application/json"}

dataVoltage : list = []
dataTemperature : list = []

#############################################################################################
# Functions for BE
def connect_to_ip(ip_address, port, api_key):
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
        return False
    
def getData(command):
    try:
        if activeRobot == "100":
            active_ip_address = MIR_IP_100
        elif activeRobot == "250":
            active_ip_address = MIR_IP_250
        elif activeRobot == "251":
            active_ip_address = MIR_IP_251
        elif activeRobot == "500":
            active_ip_address = MIR_IP_500
        else:
            print("Invalid robot number. Available options: 500, 251, 250, 100.")
            return False
        
        url = f"http://{active_ip_address}/api/v2.0.0/{command}"
        
        response = requests.get(url, headers = HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error in fetching data from {active_ip_address}: {e}")
        return False
    
def getDesiredData():    
    mission_command = "mission"
    activeMission_status = getData(mission_command)

    if not activeMission_status:
        print("No active mission found.")
        return None, True
    
    data_command =  "experimental/diagnostics"   
    mir_data = getData(data_command)    
    if not mir_data:
        print("⚠️ Failed to retrieve data.")
        return None, False

    brake_info = mir_data.get("/Motors/Brake", {}).get("values", {})

    voltage = brake_info.get("Voltage", "N/A")
    temperature = brake_info.get("Board temperature", "N/A")

    print(f"🔋 Voltage: {voltage} V | 🌡️ Temp: {temperature} °C")
    return (voltage, temperature), False
    

#############################################################################################
# Functions for FE

def connect_to_robot(robot_number, auth_key):
    try:
        activeRobot = robot_number
        activeAuthKey = auth_key
        
        if activeRobot == "100":
            return connect_to_ip(MIR_IP_100, MIR_port, activeAuthKey)
        elif activeRobot == "250":
            return connect_to_ip(MIR_IP_250, MIR_port, activeAuthKey)
        elif activeRobot == "251":
            return connect_to_ip(MIR_IP_251, MIR_port, activeAuthKey)
        elif activeRobot == "500":
            return connect_to_ip(MIR_IP_500, MIR_port, activeAuthKey)
        else:
            print("Invalid robot number. Available options: 500, 251, 250, 100.")
            return False
    except socket.error as e:
        print(f"Socket error: {e}")
        return False

def close_connection(client):
    try:
        if client:
            client.close()
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

def set_map(active_ip_address, map_id):
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

def start_mission(active_ip_address, mission_id):
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
        

def delete_mission_queue(active_ip_address):
    command = "mission_queue"
    url = f"http://{active_ip_address}/api/v2.0.0/{command}"
     
    try:
        response = requests.delete(url, headers=HEADERS)
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

def measure_data_during_mission(interval_seconds = 5, timeout_seconds = 300):
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

def save_to_json(data, fileName, folder):
    try:
        os.makedirs(folder, exist_ok=True)  # Vytvoří složku, pokud neexistuje
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
        os.makedirs(folder, exist_ok=True)  # Vytvoří složku, pokud neexistuje
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


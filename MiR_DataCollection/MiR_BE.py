import os 
import requests
import socket 
import json
import csv 
from datetime import datetime

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
    
def get_maps():
    command = "maps"
    
    response = getData(command)

    return list(response)

def get_missions():
    command = "missions"
    
    response = getData(command)
    
    return list(response)

def start_mission(map, mission):
    start = 

    if start == True:
        return True
    else:
        return False
        print("Error starting mission.")

def stop_mission():
    stop = 

    if stop == True:
        return True
    else:
        print("Error starting mission.")
        return False

def getDesiredData():    
    mission_command = "mission"
    activeMission = getData(mission_command)

    if activeMission == True:
        data_command =  "experimental/diagnostics"       
        mir_data = getData(data_command)
    
        if "/Motors/Brake" in mir_data and "values" in mir_data["/Motors/Brake"]:
            voltage = mir_data["/Motors/Brake"]["values"].get("Voltage", "N/A")
            board_temperature = mir_data["/Motors/Brake"]["values"].get("Board temperature", "N/A")
            print(f"Voltage: {voltage} V")
            print(f"Board temperature: {board_temperature} °C")
            dataVoltage.append(voltage)
            dataTemperature.append(board_temperature)
            print("Data successfully retrieved.")
        return dataVoltage, False
    else: 
        print("Data for /Motors/Brake not found.")
        return list[0], True

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


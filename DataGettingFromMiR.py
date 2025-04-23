# Description: This script is used to get data from MiR robot using its API.
# Je třeba nainstalovat knihovnu requests pomocí příkazu: pip install requests
# It is necessary to install the requests library using the command: pip install requests
import os
import requests
import socket
import socketserver
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
HEADERS = {"Authorization": f"{authorization_code_distributor}", "Content-Type": "application/json"}
fileDirectory = "Data/MIR_data"

class MirCollector:
    def __init__(self, ip_address, port, name):
        self.ip_address = ip_address
        self.port = port
        self.name = name
        pass

class MirData:
    def __init__(self, data):
        self.data = data
        pass

    def __repr__(self):
        return json.dumps(self.data, indent=4)  # Formátovaný výpis dat
    
desiredData100 = [
    "/Computer/PC/CPU Load",
    "/Computer/PC/CPU Temperature",
    "/Computer/Network/Gateways",
    "/Computer/Network/Master Interface",
    "/Motors/Controller",
    "/Motors/Left",
    "/Motors/Right",
    "/Power System/Battery",
    "/Power System/Battery Management System",
    "/Power System/Battery Raw Data",
    "/Power System/Charging Status",
    "/Safety System/Communication",
    "/Safety System/Emergency Stop",
    "/Sensors/Laserscanner (Back)/Communication",
    "/Sensors/3D Camera (Left)/Connection",
    "/Sensors/3D Camera (Right)/Connection",
    "/Sensors/Laserscanner (Front)/Communication",
    "/Sensors/IMU/Accelerometer",
    "/Sensors/IMU/Connection",
    "/Sensors/IMU/Gyroscope",
    "/Serial Interface/Communication"
    ]
        
desiredData250 = [
    "/Computer/PC/CPU Load",
    "/Computer/PC/CPU Temperature",
    "/Computer/Network/Gateways",
    "/Computer/Network/Master Interface",
    "/Motors/Brake",
    "/Motors/Left",
    "/Motors/Right",
    "/Powerboard/Diagnostics/Speaker",
    "/Powerboard/Diagnostics/Voltage monitor",
    "/Powerboard/Internal IOs/Pendant",
    "/Powerboard/Internal IOs/IOs",
    "/Powerboard/CAN nodes",
    "/Powerboard/CAN Communication bus/CAN bus MC light proxy gpio",
    "/Powerboard/CAN Communication bus/CAN bus charger battery",
    "/Power System/Charger",
    "/Power System/Battery",
    "/Power System/Battery Management System",
    "/Power System/Charging Status",
    "/Safety System",
    "/Safety System/Communication",
    "/Safety System/Emergency Stop",
    "/Sensors/Laserscanner (Back)/Communication",
    "/Sensors/3D Camera (Left)/Connection",
    "/Sensors/3D Camera (Right)/Connection",
    "/Sensors/Laserscanner (Front)/Communication",
    "/Sensors/IMU/Accelerometer",
    "/Sensors/IMU/Gyroscope",
    "/Sensors/Proximity sensors/Diagnostics",
    "/Sensors/Proximity sensors/head_left",
    "/Sensors/Proximity sensors/head_right",
    "/Sensors/Proximity sensors/left_back",
    "/Sensors/Proximity sensors/left_front",
    "/Sensors/Proximity sensors/right_back",
    "/Sensors/Proximity sensors/right_front",
    "/Sensors/Proximity sensors/tail_left",
    "/Sensors/Proximity sensors/tail_right",
    "/Serial Interface/Communication"
    ]

desiredData251 = [
    "/Computer/PC/CPU Load",
    "/Computer/PC/CPU Temperature",
    "/Computer/Network/Gateways",
    "/Computer/Network/Master Interface",
    "/Motors/Brake",
    "/Motors/Left",
    "Motors/Right",
    "/Powerboard/Diagnostics/Speaker",
    "/Powerboard/Diagnostics/Voltage monitor",
    "/Powerboard/Internal IOs/Pendant",
    "/Powerboard/Internal IOs/IOs",
    "/Powerboard/CAN nodes",
    "/Powerboard/CAN Communication bus/CAN bus MC light proxy gpio",
    "/Powerboard/CAN Communication bus/CAN bus charger battery",
    "/Power System/Charger",
    "/Power System/Battery",
    "/Power System/Battery Management System",
    "/Power System/Charging Status",
    "/Safety System",
    "/Safety System/Communication",
    "/Safety System/Emergency Stop",
    "/Sensors/Laserscanner (Back)/Communication",
    "/Sensors/3D Camera (Left)/Connection",
    "/Sensors/3D Camera (Right)/Connection",
    "/Sensors/Laserscanner (Front)/Communication",
    "/Sensors/IMU/Accelerometer",
    "/Sensors/IMU/Gyroscope",
    "/Serial Interface/Communication"
    ]
        
desiredData500 = [
    "/Computer/PC/CPU Load",
    "/Computer/PC/CPU Temperature",
    "/Computer/Network/Gateways",
    "/Computer/Network/Master Interface",
    "/Motors/Brake",
    "/Motors/Left",
    "/Motors/Right",
    "/Powerboard/Diagnostics/Voltage monitor",
    "/Powerboard/Internal IOs/Pendant",
    "/Powerboard/CAN nodes",
    "/Powerboard/CAN Communication bus/CAN bus MC light proxy gpio",
    "/Powerboard/CAN Communication bus/CAN bus charger battery",
    "/Power System/Charger",
    "/Power System/Battery",
    "/Power System/Battery Management System",
    "/Power System/Charging Status",
    "/Safety System/Communication",
    "/Safety System/Emergency Stop",
    "/Sensors/Laserscanner (Back)/Communication",
    "/Sensors/3D Camera (Left)/Connection",
    "/Sensors/3D Camera (Right)/Connection",
    "/Sensors/Laserscanner (Front)/Communication",
    "/Sensors/IMU/Accelerometer",
    "/Sensors/IMU/Gyroscope",
    "/Serial Interface/Communication"
    ]

#############################################################################################

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
        return None

def close_connection(client_socket):
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

def get_status(ip_address):
    #"""Získá celkový stav robota."""
    url = f"http://{ip_address}/api/v2.0/status"
    return fetch_data(url)

def get_missions(ip_address):
    #"""Získá seznam dostupných misí."""
    url = f"http://{ip_address}/api/v2.0/missions"
    return fetch_data(url)

def get_position():
    #"""Získá aktuální pozici robota."""
    status = get_status()
    if status and "position" in status:
        return status["position"]
    return None

def get_mission_queue(ip_address):
    #"""Získá seznam misí ve frontě."""
    url = f"http://{ip_address}/api/v2.0/mission_queue"
    return fetch_data(url)

def fetch_data(url):
    #"""Pomocná funkce pro získání dat z daného endpointu."""
    try:
        response = requests.get(url, headers = HEADERS)
        response.raise_for_status()
        data = response.json()
        return MirData(data)
    except requests.exceptions.RequestException as e:
        print(f"Chyba při získávání dat z {url}: {e}")
        return None
    
def getData(ip_address, command):
    try:
        url = f"http://{ip_address}/api/v2.0.0/{command}"
        response = requests.get(url, headers = HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error in fetching data from {ip_address}: {e}")
        return None
    
def get_all_maps():
    command = "maps"
    response = getData(command)
    if not response:
        print("Could not retrieve maps.")
        return []
    
    # vyhledávání map, která nás zajímají 
    preferred_maps = ["KAS0249", "map2", "map3"]  # Příklad preferovaných map
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
    preferred_missions = ["KAS0249", "ChargeBattery", "DeliveryA", "Dny otevřených dveří"]
    filtered_missions = [
        {"name": m["name"], "guid": m["guid"]}
        for m in response
        if m.get("name") in preferred_missions
    ]

    return filtered_missions

def save_to_json(data, fileName, folder):
    try:
        os.makedirs(folder, exist_ok=True)  # Vytvoří složku, pokud neexistuje
        full_path = os.path.join(folder, f"{fileName}.json")
        
        with open(full_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {full_path}.")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

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
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def get_user_choice(prompt, options):
    while True:
        choice = input(f"{prompt} ({'/'.join(options)}): ").strip().lower()
        if choice in options:
            return choice
        else:
            print(f"Invalid choice. Available options: {', '.join(options)}.")

def connect_to_robot(robot_number, authorization_code):
    if robot_number == "500":
        return connect_to_ip(MIR_IP_500, MIR_port, authorization_code)
    elif robot_number == "251":
        return connect_to_ip(MIR_IP_251, MIR_port, authorization_code)
    elif robot_number == "250":
        return connect_to_ip(MIR_IP_250, MIR_port, authorization_code)
    elif robot_number == "100":
        return connect_to_ip(MIR_IP_100, MIR_port, authorization_code)
    else:
        print("Invalid robot number. Available options: 500, 250, 100.")
        return None

def process_data(data):
    while True:
        # Zobraz aktuálně dostupné klíče
        print(f"\nCurrent keys in data: {list(data.keys())}")

        key_to_remove = input("Enter key to delete or 'done' to finish: ").strip()

        if key_to_remove.lower() == 'done':
            break
        elif key_to_remove in data:
            # Potvrzení smazání
            confirmation = input(f"Are you sure you want to delete '{key_to_remove}'? (yes/no): ").strip().lower()
            if confirmation == 'yes':
                del data[key_to_remove]
                print(f"'{key_to_remove}' successfully deleted!")
            else:
                print(f"Deletion of '{key_to_remove}' canceled.")
        else:
            print(f"Key '{key_to_remove}' not found in data.")

    return data

#############################################################################################

if __name__ == "__main__":
    
    client_socket = None

    try:
        
        while not client_socket:
            active_authorization_code = get_user_choice(
                "Enter authorization code", 
                ["distributor", "admin", "student"]
            )

            active_robot = get_user_choice(
                "Enter robot number to connect to", 
                ["500", "251", "250", "100"]
            )

            if active_robot == "100":
                active_ipAddress = MIR_IP_100
            elif active_robot == "250":
                active_ipAddress = MIR_IP_250
            elif active_robot == "251":
                active_ipAddress = MIR_IP_251
            elif active_robot == "500":
                active_ipAddress = MIR_IP_500
            else:
                print("Invalid robot number. Available options: 500, 251, 250, 100.")


            client_socket = connect_to_robot(active_robot, active_authorization_code)

            if client_socket:
                print(f"Successfully connected to MiR {active_robot} as {active_authorization_code}!")
            else:
                print("Failed to connect. Try again.")
        
        while True:
            print("\nAvailable commands: getdata, exit")
            command = get_user_choice(
                "Enter command", 
                ["getdata", "startmission", "exit"]
            )

            if command == "exit":
                print("Exiting program.")
                break
            elif command == "getdata":
                data_name = get_user_choice(
                    "Enter the name of data to retrieve: ",
                    ["swagger", "diagnostics"]
                )

                if data_name == "swagger":
                    dataCommand = "swagger"
                elif data_name == "diagnostics":
                    dataCommand = "experimental/diagnostics"

                mir_data = getData(active_ipAddress, dataCommand)
                if mir_data:
                    print("Data successfully retrieved!")

                    # Výběr plné nebo upravené verze
                    data_type = get_user_choice("Choose data version", ["full", "filtered", "desired"])

                    if data_type == "full":
                        print("Full data will be saved.")
                    elif data_type == "filtered":
                        mir_data = process_data(mir_data)
                        print("Data have been filtered.")
                    elif data_type == "desired":
                        if active_robot == "100":
                            desiredData = desiredData100
                        elif active_robot == "250":
                            desiredData = desiredData250
                        elif active_robot == "251":
                            desiredData = desiredData251
                        elif active_robot == "500":
                            desiredData = desiredData500
                        
                        if isinstance(mir_data, dict):
                            filtered_data = {key: mir_data[key] for key in desiredData if key in mir_data}
                            mir_data = filtered_data
                            print("Only desired data will be saved.")
                        else:
                            print("Received data is not in expected format.")
                    
                    if "/Motors/Brake" in mir_data and "values" in mir_data["/Motors/Brake"]:
                        voltage = mir_data["/Motors/Brake"]["values"].get("Voltage", "N/A")
                        board_temperature = mir_data["/Motors/Brake"]["values"].get("Board temperature", "N/A")
                        print(f"Voltage: {voltage} V")
                        print(f"Board temperature: {board_temperature} °C")
                    else:
                        print("Data for /Motors/Brake not found.")

                    # Uložení dat
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_to_json(mir_data, f"mir{active_robot}_{data_name}_{data_type}_{timestamp}", fileDirectory)
                    save_to_csv(mir_data, f"mir{active_robot}_{data_name}_{data_type}_{timestamp}", fileDirectory)
                    print("Data saved!")
                else:
                    print(f"Failed to retrieve data for '{data_name}'.")
            elif command == "startmission":
                
                
                selectedmap = get_user_choice(
                    "Choose your map: ",
                    ["swagger", "diagnostics"]
                )
            else:
                print("Unknown command.")

            print("Everything ended successfully.")

    except Exception as e:
        print(f"Error in operation: {e}")

    finally:
        if not close_connection(client_socket):
            print("Failed to properly close the connection.")


# Luki was here <3 

# End of file / End of life / End of everything / End of the world as we know it / And I feel fine :)


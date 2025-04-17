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
active_ip_address = None
activeAuthKey = None
client_socket = None

voltage_data = []
temperature_data = []

dataBreaksVoltage : list = []
dataBreaksTemperature : list = []
dataBreaksTimestamps : list = []

activeMission = None


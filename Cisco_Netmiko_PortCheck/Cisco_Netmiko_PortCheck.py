from netmiko import ConnectHandler
import re
import csv

def device_connector(input_type):
    if input_type == 'MAC':
        for row in inventory:
            net_connect = ConnectHandler(device_type=row['type'], host=row['hostIP'], username="admin",
                                         password=cisco_password)

            router_interfaces = re.findall("Ethernet\d.\d", net_connect.send_command("show ip interface brief"))
            for interface in router_interfaces:
                sent_commands = [f"show mac address-tabel interface {interface}"]
                output = (net_connect.send_command(sent_commands))






inventory = csv.DictReader(open('DeviceList'))
cisco_password = input('Please enter your password')  # Take password as input so don't have to store it in the code

while True:
    user_input = input('Please enter an IP or MAC Address to search for')
    if user_input:
        search_type ='MAC'
        break
    elif user_input:
        search_type ='IP'
        break
    else:
        print('That is not an IP or MAC Address')

SearchReturn = device_connector(search_type)
if SearchReturn == '':
    print('Could Not find that MAC/IP')
else:
    print(f'That ')



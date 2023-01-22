from netmiko import ConnectHandler
import re
import csv
import pyinputplus

def device_connector(input_type):
    for row in inventory:
        net_connect = ConnectHandler(device_type=row['type'], host=row['hostIP'], username="admin",
                                     password=cisco_password)

        router_interfaces = re.findall("Ethernet\d.\d", net_connect.send_command("show ip interface brief"))

        for interface in router_interfaces:
            if input_type == 'MAC':
                sent_command = [f"show mac address-table interface {interface}"]
                if user_input in net_connect.send_command(sent_command):
                    return row['hostname'], interface
            else:
                sent_command = [f"show ip arp {interface}"]
                if user_input in net_connect.send_command(sent_command):
                    return row['hostname'], interface



ip_regex = re.compile(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')
mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

inventory = csv.DictReader(open('DeviceList'))
cisco_password = input('Please enter your password')  # Take password as input so don't have to store it in the code

while True:
    while True:
        user_input = input('Please enter an IP or MAC Address to search for')
        if ip_regex.search(user_input) is not None:
            search_type = 'MAC'
            break
        elif mac_regex.search(user_input) is not None:
            search_type = 'IP'
            break
        else:
            print('That is not an IP or MAC Address')

    SearchReturn = device_connector(search_type)
    if SearchReturn == '':
        print('Could Not find that MAC/IP')
    else:
        print(f'Found on device {SearchReturn(1)}, port {SearchReturn(2)}')

    if pyinputplus.inputYesNo('Do you want to search again? [yes/no]') == 'no':
        break





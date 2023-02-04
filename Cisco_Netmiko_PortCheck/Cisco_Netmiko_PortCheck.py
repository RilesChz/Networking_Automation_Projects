import netmiko
import re
import csv
import pyinputplus

def device_connector(input_type):
    if input_type == 'MAC':     #change the command depending on input type
        sent_command = 'show mac address-table interface'
    elif input_type == 'IP':
        sent_command = 'show ip arp'

    output = []



    for row in inventory:     #iterate through the device list
        try:
            net_connect = netmiko.ConnectHandler(device_type=row['OStype'], host=row['hostIP'], username='admin', password=cisco_password)
        except netmiko.exceptions:
            print(f'Failed to connect to {row["hostname"]}')

        router_interfaces = re.findall('Ethernet\d.\d', net_connect.send_command("show ip interface brief"))  # scrape the list of interfaces to check

        for interface in router_interfaces:
            if user_input in net_connect.send_command(f'{sent_command} {interface}'):
                output.append('Found on device ' + row['hostname'] + ' port ' + interface)
    return output



ip_regex = re.compile(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')
mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')


cisco_password = input('Please enter your password \n')  #Take password as input so don't have to store it in the code
inventory = csv.DictReader(open('DeviceList.csv'))

while True:
        user_input = input('Please enter an IP or MAC Address to search for \n')  #Validate input is an IP or MAC
        if ip_regex.search(user_input) is not None:
            print(device_connector('IP'))
            break
        elif mac_regex.search(user_input) is not None:
            print(device_connector('MAC'))
            break
        else:
            print('That is not a valid IP or MAC Address')




import netmiko
import re
import threading
import pynetbox
import credentials

nb = pynetbox.api(credentials.NetBox_IP, token=credentials.NetBox_API)  # access the netbox API


# ---------------------------------------------------------

def device_connector(device, input_type):
    if input_type == 'MAC':  # change the command depending on input type
        sent_command = 'show mac address-table interface'
    elif input_type == 'IP':
        sent_command = 'show ip arp'

    try:
        net_connect = netmiko.ConnectHandler(device_type=device.platform.name,
                                             host=device.name,
                                             username='admin', password=password_input)
        # ^ connects to the device, using the devices attributes from the netbox API

        interface_list = list(nb.dcim.interfaces.filter(device=device.name))

        for interface in interface_list:
            if 'Uplink' not in interface.description:  # do not check interface if it's an uplink
                if device.platform.name == 'cisco_ios' or 'arista_eos':
                    if user_input in net_connect.send_command(
                            f'{sent_command} {interface}'):  # send the MAC/ARP command to the interface
                        print(f'Found on device {device.name} interface {interface.name}')
                        return

        print(f'Not found on {device.name}')
        net_connect.disconnect()

    except netmiko.exceptions.NetmikoTimeoutException:  # If the connection to a device fails, don't crash the program
        print(f'Failed to connect to {device.name}')


# ---------------------------------------------------------

ip_regex = re.compile(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')
mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

password_input = input('Please enter your password \n')  # Take password as input so don't have to store it in the code

while True:
    user_input = input('Please enter an IP or MAC Address to search for \n')  # Validate input is an IP or MAC
    if ip_regex.search(user_input) is not None:
        input_type = 'IP'
        break
    elif mac_regex.search(user_input) is not None:
        input_type = 'MAC'
        break
    else:
        print('That is not a valid IP or MAC Address')

device_inventory = list(nb.dcim.devices.all())  # make a list out of the netbox device objects

threads_list = []

for device in device_inventory:
    if device.status.value == 'active':  # Only attempt connection if it is an active device
        print(f'Creating thread for: {device.name}')
        threads_list.append(threading.Thread(target=device_connector, args=(device, input_type,)))

for thread in threads_list:
    thread.start()  # start the threading
for thread in threads_list:
    thread.join()  # wait for threading to finish

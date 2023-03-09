import netmiko
import re
import pynetbox

nb = pynetbox.api(     #access netbox API
    'http://192.168.0.246',
    token='b64df0884421551e0b7b2395a995d2dd3ad9dfb5'
)

#---------------------------------------------------------

def device_connector(input_type):
    if input_type == 'MAC':     #change the command depending on input type
        sent_command = 'show mac address-table interface'
    else:
        sent_command = 'show ip arp'

    inventory = nb.dcim.devices.all() # make a list out of the netbox device objects

    for device in inventory:
        try:
            net_connect = netmiko.ConnectHandler(device_type=device.platform.slug, host=device.primary_ip.dns_name, username='admin', password=password_input)
           #^ connects to the device, using the devices attributes from the netbox API

            device_interfaces = re.findall('Ethernet\d.\d', net_connect.send_command("show ip interface brief"))
            #^ scrape the list of interfaces to check

            for interface in device_interfaces:
                if interface == 'Ethernet0/0' or 'Ethernet0/1':
                    pass   #do nothing, as these are uplinks
                else:
                    if user_input in net_connect.send_command(f'{sent_command} {interface}'):   #send the MAC/ARP command to the interface
                        output = ('Found on device ' + device.name + ' port ' + interface)


        except netmiko.exceptions.NetmikoTimeoutException:  #If the connection to a device fails, don't crash the program
            print(f'Failed to connect to {device.name}')

    if output is None:
        output = 'Could not locate that IP/MAC'

    return output

#---------------------------------------------------------

ip_regex = re.compile(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')
mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

password_input = input('Please enter your password \n')  #Take password as input so don't have to store it in the code

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







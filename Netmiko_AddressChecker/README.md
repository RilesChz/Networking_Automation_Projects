# Netmiko_AddressChecker

Python program that:

1 - Takes a user IP/MAC input 

2 - Retrieves a list of devices from netbox

3 - Connects to each device by passing different arguments to netmiko depending on the device type retrieved from netbox

4 - Connects to each device at the same time using multithreading

5 - Searches the ports on each device for that IP/MAC


==========================================

Assumptions:

1 - The routers in netbox are Cisco IOS with the interface format EthernetxX/X

2 - The switches in netbox are Arista vEOS with the interface format EthernetX

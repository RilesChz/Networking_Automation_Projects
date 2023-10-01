import netmiko
import re
import threading
import pynetbox

nb = pynetbox.api(  # access netbox API
    'http://192.168.0.246',
    token='b64df0884421551e0b7b2395a995d2dd3ad9dfb5'
)

# ---------------------------------------------------------

def device_connector(device):

    try:
        net_connect = netmiko.ConnectHandler(device_type=device.platform.name,
                                             host=device.name,
                                             username='admin', password=password_input)
        # ^ connects to the device, using the devices attributes from the netbox API



    except netmiko.exceptions.NetmikoTimeoutException:  # If the connection to a device fails, don't crash the program
        print(f'Failed to connect to {device.name}')


# ---------------------------------------------------------


password_input = input('Please enter your password \n')  # Take password as input so don't have to store it in the code

device_inventory = list(nb.dcim.devices.all())  # make a list out of the netbox device objects

threads_list = []

for device in device_inventory:
    print(f'Creating thread for: {device.name}')
    threads_list.append(threading.Thread(target=device_connector, args=(device,)))

for thread in threads_list:
 thread.start()  # start the threading
for thread in threads_list:
  thread.join()  # wait for threading to finish

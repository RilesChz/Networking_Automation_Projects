from netmiko import ConnectHandler
import re

cisco_password = input('Please enter your password')  # Take password as input so don't have to store it in the code
net_connect = ConnectHandler(device_type="cisco_ios", host="192.168.0.70", username="admin", password=cisco_password)

router_interfaces = re.findall("Ethernet\d.\d", net_connect.send_command("show ip interface brief"))
for interface in router_interfaces:
    interface_commands = [f"Interface {interface}", "no shut"]
    net_connect.send_config_set(interface_commands)

net_connect.save_config()

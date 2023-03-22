import netmiko, napalm, nornir, pynetbox
from nornir.core.task import Task, Result

# Set the required configuration:

password = 'password1'  # password_input = input('please enter your password \n')

nr = nornir.InitNornir(
    inventory={
        "plugin": "NetBoxInventory2",
        "options": {
            "nb_url": "http://192.168.0.246",
            "nb_token": "b64df0884421551e0b7b2395a995d2dd3ad9dfb5",
            "filter_parameters": {
                "platform": "cisco_ios",
            }
        }
    }
)

print(nr.inventory.hosts)




def inventory_usernames(task):
    return Result(host=task.host, result=f"{task.host.name} username is {task.host.username}")
output = nr.run(task=inventory_usernames)

print(nr.run())
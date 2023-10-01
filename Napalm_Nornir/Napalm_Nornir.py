import netmiko, napalm, nornir, pynetbox
from nornir.core.task import Task, Result

# Set the required configuration:

password_input = input('please enter your password \n')

nr = nornir.InitNornir(config_file="config.yaml")

print(nr.inventory.hosts)


def inventory_usernames(task):
    return Result(host=task.host, result=f"{task.host.name} username is {task.host.username}")


output = nr.run(task=inventory_usernames)

print(nr.run())

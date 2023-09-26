import paramiko
import time
import json
from multiprocessing.pool import ThreadPool
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('USERNAME')

switch = os.getenv('SWITCH')
switch_en = os.getenv('SWITCH_EN')
router = os.getenv('ROUTER')
router_en = os.getenv('ROUTER_EN')

new_switch = os.getenv('NEW_SWITCH')
new_switch_en = os.getenv('NEW_SWITCH_EN')
new_router = os.getenv('NEW_ROUTER')
new_router_en = os.getenv('NEW_ROUTER_EN')

port = os.getenv('PORT')

def is_switch(type):
    if type == 'switch':
        return True
    else:
        return False

def load_devices():
    with open('devices.json')as f:
        devices = json.load(f)
    return devices

def change_password(device):
    hostname = device['ip']
    type = device['type']

    if is_switch(type):
        password = switch
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port, username, password)
            channel = client.invoke_shell()
            print(f"setting {hostname}")
            channel.send('con ter\n')
            time.sleep(3)
            channel.send('enable aaa console\n')
            time.sleep(3)
            channel.send(f'username {username} password {new_switch}\n')
            time.sleep(3)
            channel.send(f'enable super-user-password {new_switch_en}\n')
            time.sleep(3)
            channel.send('write memory\n')
            time.sleep(3)
            channel.close() 
        except Exception:
            raise
    else:
        password = router
        en_password = router_en
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port, username, password)
            channel = client.invoke_shell()
            print(f"setting {hostname}")
            channel.send('enable\n')
            time.sleep(3)
            channel.send(f'{en_password}\n')
            time.sleep(3)
            channel.send('con ter\n')
            time.sleep(3)
            channel.send('enable aaa console\n')
            time.sleep(3)
            channel.send('no enable user password-masking\n')
            time.sleep(3)
            channel.send(f'username {username} password {new_router}\n')
            time.sleep(3)
            channel.send(f'enable super-user-password {new_router_en}\n')
            time.sleep(3)
            channel.send('enable user password-masking\n')
            time.sleep(3)
            channel.send('write memory\n')
            time.sleep(3)
            channel.close()
        except Exception:
            raise
    
if __name__ == '__main__':
    devices = load_devices() 

    # for device in devices:
        # change_password(device)

    with ThreadPool(processes=100) as pool:
        pool.map(change_password, devices)

    print("execution finished")
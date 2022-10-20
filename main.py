import os
from os import chmod
import time
import subprocess
from dotenv import load_dotenv
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
import ansible_runner
from Crypto.PublicKey import RSA
from settings import hetzner_server_name, hetzner_server_type, hetzner_image, user, hostname

load_dotenv()

console = Console()

console.print("Hello :smiley:")
console.rule("")

with console.status("Generating SSH Key..", spinner="dots"):
    key = RSA.generate(2048)
    pubkey = key.publickey()

user_data=f"""
#cloud-config
hostname: {hostname}
manage_etc_hosts: true
locale: en_US.UTF-8
timezone: Europe/Berlin


users:
- default
- name: {user}
  groups: sudo
  sudo: "ALL=(ALL) NOPASSWD:ALL"
  lock_passwd: true
  shell: /bin/bash
  ssh_authorized_keys:
    - {pubkey.exportKey('OpenSSH').decode()} (none)
"""

with console.status("Creating Server..", spinner="dots"):
    client = Client(token=os.getenv("HETZNER_API_TOKEN"))

    response1 = client.servers.create(
        hetzner_server_name,
        server_type=ServerType(name=hetzner_server_type),
        image=Image(name=hetzner_image),
        user_data=user_data
    )

    server = response1.server

    server_ip = server.public_net.ipv4.ip
    
console.log(f"Server IP is: {server_ip}")

with console.status("Configuring Ansible...", spinner="dots"):
    hosts = f"""
    [servers]
    server ansible_host={server_ip}

    [all:vars]
    ansible_user={user}
    """
    f = open("ansible/inventory/hosts", "w")
    f.write(hosts)
    f.close()
    
    f = open("ansible/env/ssh_key", 'wb') 
    chmod("ansible/env/ssh_key", 0o600)
    f.write(key.exportKey('PEM'))
    f.close()
    
    bashCommand = "ansible-galaxy install -r ansible/project/requirements.yml --force"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)


secs = 35
for i in track(range(secs), description=f"Waiting {secs} seconds for the server to be reachable..."):
    time.sleep(1)  

console.log(f"Running Ansible Playbook..")
console.rule("")

r = ansible_runner.run(private_data_dir='ansible', playbook='main.yml')

    
    
client.servers.delete(server)






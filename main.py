import os
from os import chmod
import time
import subprocess
from subprocess import DEVNULL, STDOUT, check_call
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
import ansible_runner
from Crypto.PublicKey import RSA
from settings import *

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
    client = Client(token=hetzner_api_token)

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
    # creating hosts file
    hosts = f"[servers]\nserver ansible_host={server_ip}\n[all:vars]\nansible_user={user}"
    
    f = open("ansible/inventory/hosts", "w")
    f.write(hosts)
    f.close()
    
    # creating vars file
    settings = f"USER: {user}\nENTRYPOINT: {entrypoint}\nOUTPUT_DIR: {output_dir}\nSMTP_RECIPIENT: {smtp_recipient}\nSMTP_HOST: {smtp_host}"
    
    f = open("ansible/project/vars/settings.yml", "w")
    f.write(settings)
    f.close()
    
    # creating vault file
    settings = f"HETZNER_BOX_USER: {hetzner_box_user}\nHETZNER_BOX_PW: {hetzner_box_pw}\nSMTP_ADDRESS: {smtp_address}\nSMTP_PW: {smtp_pw}"

    f = open("ansible/project/vars/vault.yml", "w")
    f.write(settings)
    f.close()
    
    #creating vault pw file for encrypting vault
    f = open("vault_pw", "w")
    f.write(vault_pw)
    f.close()
    
    passwords = f'---\n"^Vault password:\\\s*?$": "{vault_pw}"'

    #creating passwords file for ansible runner
    f = open("ansible/env/passwords", "w")
    f.write(   passwords)
    f.close()
    
    # encrypting vault
    bashCommand = "ansible-vault encrypt ansible/project/vars/vault.yml \
    --vault-password-file=vault_pw"
    process = subprocess.Popen(bashCommand.split(), stdout=DEVNULL, stderr=STDOUT)
    process.wait()
    os.remove("vault_pw") 
    
    # writing private ssh key to ansible runner environment
    f = open("ansible/env/ssh_key", 'wb') 
    chmod("ansible/env/ssh_key", 0o600)
    f.write(key.exportKey('PEM'))
    f.close()
    
    #  installing ansible requirements
    bashCommand = "ansible-galaxy install -r ansible/project/requirements.yml --force"
    process = subprocess.Popen(bashCommand.split(), stdout=DEVNULL, stderr=STDOUT)


secs = 35
for i in track(range(secs), description=f"Waiting {secs} seconds for the server to be reachable..."):
    time.sleep(1)  

console.log(f"Running Ansible Playbook..")
console.rule("")

r = ansible_runner.run(private_data_dir='ansible', playbook='main.yml')

client.servers.delete(server)






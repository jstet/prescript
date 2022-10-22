import os
from os import chmod
import time
import subprocess
from subprocess import DEVNULL, STDOUT
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from rich.console import Console
from rich.progress import track
import ansible_runner
from Crypto.PublicKey import RSA
from github import Github
import settings
from helpers import write_file

console = Console()

console.print("Hello :smiley:")
console.rule("")

with console.status("Generating SSH Key for Ansible..", spinner="dots"):
    key = RSA.generate(2048)
    ans_key = key.exportKey('PEM')
    ans_pubkey = key.publickey().exportKey('OpenSSH').decode()
console.log("SSH Key for Ansible generated.")

with console.status("Generating SSH Key for Github Repo.", spinner="dots"):
    key = RSA.generate(2048)
    github_key = key.exportKey('PEM')
    github_pubkey = key.publickey().exportKey('OpenSSH').decode()
console.log("SSH Key for Github generated.")

user_data = f"""
#cloud-config
hostname: {settings.hostname}
manage_etc_hosts: true
locale: en_US.UTF-8
timezone: Europe/Berlin


users:
- default
- name: {settings.user}
  groups: sudo
  sudo: "ALL=(ALL) NOPASSWD:ALL"
  lock_passwd: true
  shell: /bin/bash
  ssh_authorized_keys:
    - {ans_pubkey} (none)
"""

with console.status("Creating Server..", spinner="dots"):
    client = Client(token=settings.hetzner_api_token)
    response1 = client.servers.create(
        settings.hostname,
        server_type=ServerType(name=settings.hetzner_server_type),
        image=Image(name=settings.hetzner_image),
        user_data=user_data
    )
    server = response1.server
    server_ip = server.public_net.ipv4.ip

console.log("Server created.")
console.print(f"Server IP is: {server_ip}")

with console.status("Adding deploy key to Repo..", spinner="dots"):
    g = Github(settings.github_token)
    repo = g.get_repo(settings.github_repo)
    repo.create_key(title="prescript_key", key=github_pubkey, read_only=True)
console.log("Added Public Key to Github Repo.")

with console.status("Configuring Ansible...", spinner="dots"):
    # creating hosts file
    hosts = f"[servers]\nserver ansible_host={server_ip}\n[all:vars]\nansible_user={settings.user}\nansible_ssh_extra_args='-o userknownhostsfile=/dev/null'"
    write_file("ansible/inventory/hosts", "w", hosts)

    # creating vars file
    varis = f"USER: {settings.user}\nENTRYPOINT: {settings.entrypoint}\nSERVER_ID: {server.id}\nOUTPUT_DIR: {settings.output_dir}\n\
SMTP_RECIPIENT: {settings.smtp_recipient}\nSMTP_HOST: {settings.smtp_host}\nGITHUB_REPO: {settings.github_repo}\nENTRYPOINT_DIR: {settings.entrypoint_dir}\nHETZNER_BOX_DIR: {settings.hetzner_box_dir}"
    write_file("ansible/project/vars/settings.yml", "w", varis)

    # creating vault file
    vault = f"HETZNER_API_TOKEN: {settings.hetzner_api_token}\nHETZNER_BOX_USER: {settings.hetzner_box_user}\nHETZNER_BOX_PW: {settings.hetzner_box_pw}\n\
SMTP_ADDRESS: {settings.smtp_address}\nSMTP_PW: {settings.smtp_pw}"
    write_file("ansible/project/vars/vault.yml", "w", vault)

    # creating vault pw file for encrypting vault
    write_file("vault_pw", "w", settings.vault_pw)

    # creating passwords file for ansible runner
    passwords = f'---\n"^Vault password:\\\s*?$": "{settings.vault_pw}"'
    write_file("ansible/env/passwords", "w", passwords)
    
    # creating file with private ssh key for github so ansible can connect to repo
    write_file("ansible/project/files/github_ssh_key", "wb", github_key)
    chmod("ansible/project/files/github_ssh_key", 0o600)

    # encrypting vault
    bashCommand = "ansible-vault encrypt ansible/project/vars/vault.yml \
    --vault-password-file=vault_pw"
    process = subprocess.Popen(
        bashCommand.split(), stdout=DEVNULL, stderr=STDOUT)
    process.wait()
    # removing vault_pw file because we don't need it anymore
    os.remove("vault_pw")

    # writing private ssh key to ansible runner environment
    write_file("ansible/env/ssh_key", "wb", ans_key)
    chmod("ansible/env/ssh_key", 0o600)

    # installing ansible requirements
    bashCommand = "ansible-galaxy install -r ansible/project/requirements.yml --force"
    process = subprocess.Popen(
        bashCommand.split(), stdout=DEVNULL, stderr=STDOUT)

console.log("Ansible configured.")

secs = 35
for i in track(range(secs), description=f"Waiting {secs} seconds for the server to be reachable..."):
    time.sleep(1)

console.log("Server should be reachable.")

with console.status("Running Ansible Playbook...", spinner="dots"):
    r = ansible_runner.run(private_data_dir='ansible', playbook='main.yml')

console.log("Ansible Playbook finished.")
console.print("All done.")
console.print("Your script is now running on the server. Go outside and take a walk or smth...")

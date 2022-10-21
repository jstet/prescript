import os
from dotenv import load_dotenv

load_dotenv()

hetzner_api_token=os.getenv("HETZNER_API_TOKEN")
hetzner_box_user=os.getenv("HETZNER_BOX_USER")
hetzner_box_pw=os.getenv("HETZNER_BOX_PW")
vault_pw=os.getenv("ANSIBLE_VAULT_PW")
smtp_address=os.getenv("SMTP_ADDRESS")
smtp_pw=os.getenv("SMTP_PW")
# Name of Server in Hetzner Cloud
hetzner_server_name="random-name"
# https://docs.hetzner.com/cloud/servers/overview/
hetzner_server_type="cx11"
# https://docs.hetzner.com/robot/dedicated-server/operating-systems/standard-images/
hetzner_image="ubuntu-20.04"
# Server User
user="user"
# Hostname of server
hostname="test"
# Entrypoint of your script
entrypoint="main.py"
# Directory your script writes output to
output_dir="data"
# To which mail reports should be sent to
smtp_recipient="mail@jstet.net"
smtp_host='mail.your-server.de'
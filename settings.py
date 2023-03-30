import os
from dotenv import load_dotenv

load_dotenv()

hetzner_api_token = os.getenv("HETZNER_API_TOKEN")
hetzner_box_user = os.getenv("HETZNER_BOX_USER")
hetzner_box_pw = os.getenv("HETZNER_BOX_PW")
github_token = os.getenv("GITHUB_TOKEN")
vault_pw = os.getenv("ANSIBLE_VAULT_PW")
smtp_address = os.getenv("SMTP_ADDRESS")
smtp_pw = os.getenv("SMTP_PW")
# https://docs.hetzner.com/cloud/servers/overview/
hetzner_server_type = "ccx11"
# https://docs.hetzner.com/robot/dedicated-server/operating-systems/standard-images/
hetzner_image = "debian-11"
# Directory of your storage box the output should be saved to. Note: Script will fail if it doesn't exist. Leave blank for root folder.
hetzner_box_dir = "prescript"
# Server User
user = "user"
# Hostname of server. Rules for  hostnames apply: https://en.wikipedia.org/wiki/Hostname
hostname = "fds-download"
# Directory of your script. This is where supervisor will cd too and execute the script in. Relative to root folder. Leave blank if script is in root folder.
entrypoint_dir = "db/python_scripts"
# entrypoint of your script. Relative to entrypoint folder
entrypoint = "main.py"
# Directory your script writes output to. Relative to root folder
output_dir = "db/python_scripts/data"
# mail address reports should be sent to
smtp_recipient = "mail@jstet.net"
# the address your smtp server can be reached on
smtp_host = 'mail.your-server.de'
# The repo that contains the script
github_repo = "CorrelAid/fds_dashboard"

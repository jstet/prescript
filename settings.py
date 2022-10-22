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
# Name of Server in Hetzner Cloud
hetzner_server_name = "random-name"
# https://docs.hetzner.com/cloud/servers/overview/
hetzner_server_type = "cx11"
# https://docs.hetzner.com/robot/dedicated-server/operating-systems/standard-images/
hetzner_image = "ubuntu-20.04"
# Directory of your storage box the output should be saved to
hetzner_box_dir = "prescript"
# Server User
user = "user"
# Hostname of server
hostname = "test"
# Directory of your script. Relative to root folder
entrypoint_dir = "python_scripts"
# entrypoint of your script. Relative to entrypoint folder
entrypoint = "initial_data_gen.py"
# Directory your script writes output to. Relative to root folder
output_dir = "data"
# mail address reports should be sent to
smtp_recipient = "mail@jstet.net"
# the address your smtp server can be reached on
smtp_host = 'mail.your-server.de'
# The repo that contains the script
github_repo = "CorrelAid/kn_fds_statistics_database"

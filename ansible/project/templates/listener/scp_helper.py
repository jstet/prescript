import paramiko
from scp import SCPClient
import datetime
from dotenv import load_dotenv
load_dotenv()


def send_file():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="{{  HETZNER_BOX_USER  }}.your-storagebox.de",
                username="{{  HETZNER_BOX_USER  }}",
                password="{{  HETZNER_BOX_PW  }}",
                look_for_keys=False)
    # SCPCLient takes a paramiko transport as its only argument
    scp = SCPClient(ssh.get_transport())
    now = datetime.datetime.now().strftime("%H_%S_%d_%m_%Y")
    scp.put("home/{{  USER  }}/script/{{  OUTPUT_DIR  }}",
            f"{{ HETZNER_BOX_DIR  }}/prescript_output_{now}", recursive=True)
    scp.close()

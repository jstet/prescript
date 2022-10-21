import paramiko
from scp import SCPClient
import datetime
from dotenv import load_dotenv
load_dotenv()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="{{  HETZNER_BOX_USER  }}.your-storagebox.de", 
            username="{{  HETZNER_BOX_USER  }}",
            password="{{  HETZNER_BOX_PW  }}",
            look_for_keys=False)


# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())


def send_file():
    now = datetime.datetime.now().strftime("%s_%d_%m_%Y")
    scp.put("home/{{  USER  }}/script/{{  OUTPUT_DIR  }}", f"/prescript_output_{now}", recursive=True)
    scp.close()

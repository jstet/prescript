import sys
from scp_helper import send_file
from email_helper import send_email
from hcloud import Client


def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    while 1:
        # Hey Supervisor, I'm ready for some action
        write_stdout('READY\n')

        # Reading the header from STDIN
        line = sys.stdin.readline()
        write_stderr(line)

        # read event payload and print it to stderr
        headers = dict([x.split(':') for x in line.split()])
        data = sys.stdin.read(int(headers['len']))
        write_stderr(data)   
        if headers["eventname"] == "PROCESS_STATE_EXITED":
            data_dict = dict([x.split(":") for x in str.split()])
            exp = int(data_dict["expected"])
            if exp == 0:
                send_file()
                send_email(True)
                client = Client(token="{{  HETZNER_API_TOKEN  }}")
                server = client.servers.get_by_id("{{  SERVER_ID  }}")
                # client.servers.delete(server)
            if exp == 1:
                send_file()
                send_email(False)
            
        
        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')


if __name__ == '__main__':
    main()

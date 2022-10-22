# Prescript 

### Prescript automates the creation and preparation of a server to then also automatically run a Python script on it. Ideal for many API requests or ML model training.

Prescript creates a server in the Hetzner Cloud with adjustable parameters. It then adds a deploy key to your scripts repo, configures an Ansible environment and runs an Ansible playbook that first prepares the server by implementing the usual security measures, among other things. Then, the scripts repo is cloned (using the previously added deploy key) and executed using Supervisor. An event listener detects when the script has finished, sends the ouput to a Hetzner storage box and sends a notification email. Finally, the server and the deploy key are deleted. 

You need to evaluate whether it is worth using prescript, because it takes some time to run it. I measured a runtime (once) of 5 min 9 secs for Hetzner server type CX11.

**Use this script at your own risk. Creating servers on Hetzner Cloud generates costs.**

## Requirements
- A script that has one entrypoint and outputs results to a folder
- Ansible
- Github Access Token
- Hetzner Cloud Account
- Hetzner Storage Box
- SMTP Server

## Instructions

1. Create Hetzner account and add a project to your cloud
3. [Create Hetzner Storage Box](https://docs.hetzner.com/de/robot/storage-box/general). You can reuse the box.
4. Install Ansible
5. Clone Repo
6. Install python  requirements
7. Write.env file:
.
    ```bash
    HETZNER_API_TOKEN=token
    ``` 
    Infos on Hetzner API Token [here](https://docs.hetzner.cloud/#authentication ).
    
    ```bash
    HETZNER_BOX_USER=u182187 
    HETZNER_BOX_PW=pw
    ``` 
    Infos on Storage Box access [here](https://docs.hetzner.com/de/robot/storage-box/).
    
    ```bash
    ANSIBLE_VAULT_PW=pw
    ``` 
    Choose a random password.
    
    ```bash
    GITHUB_TOKEN=token
    ``` 
    Infos on Github Tokens [here](https://docs.github.com/en/authentication /keeping-your-account-and-data-secure/creating-a-person al-access-token).
    
    ```bash
    SMTP_ADDRESS=mail@example.com
    SMTP_PW=pw
    ``` 
    The login data for your SMTP server.
6. Adjust settings. See settings.py for info.
7. Hetzner blocks default smtp port. [Hetzner does this by default](https://docs.hetzner.com/de/cloud/servers/faq/#warum-kann-ich-keine-mails-von-meinem-server-verschicken). With Hetzner Mail you can also use port 587 and starttls so thats what I'm doing. Edit email_helper.py if this doesnt work for your smtp provider.
7. once script has finished, see [here](https://docs.hetzner.com/de/robot/storage-box/access/access-overview) for file retrieval options

## Script Requirements
- Yor scripts repo has to contain a subdirectory where the script writes output to
- Your scripts directory has to contain a requirements.txt


## Misc
### Connect to Server
To connect to the server created by prescript, you have to use the generated private SSH key.

```
ssh -i ansible/env/ssh_key user@ip
```
### Logs
Also find a log file in your storage box. Everything your script sends to stdout or stderr will be saved there. Personally I use rich to send stuff to stdout.




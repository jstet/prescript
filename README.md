# Prescript (WIP)

Script to set up a server for remotely running some other script. Ideal for many API requests or ML model training.

Prescript creates a server in the Hetzner Cloud with adjustable parameters. It then configures an Ansible environment and runs an Ansible playbook that first prepares the server by implementing the usual security measures, among other things. Then, the desired script is cloned and executed using Supervisor. An event listener detects when the script has finished, sends the ouput to a Hetzner storage box and sends a notification email. Finally, the server is automatically deleted. 

Use this script at your own risk. Creating servers on Hetzner Cloud costs money.

## Requirements
- A script that has one entrypoint and outputs results to a folder
- Ansible
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
7. Make sure your server doesnt block default smtp port. [Hetzner does this by default](https://docs.hetzner.com/de/cloud/servers/faq/#warum-kann-ich-keine-mails-von-meinem-server-verschicken). With Hetzner Mail you can also use port 587 and starttls. Edit email_helper.py if this doesnt work for your smtp provider.
7. once script has finished, see [here](https://docs.hetzner.com/de/robot/storage-box/access/access-overview) for file retrieval options

## Script Requirements
- Yor script directory has to contain a subdirectory where the script writes output to
- Your script directory has to contain a requirements.txt

## Misc
### Connect to Server
To connect to the server created by prescript, you have to use the generated private SSH key.

```
ssh -i ansible/env/ssh_key user@ip
```



# Script server
WIP

Script to set up a server for remotely running some script e.g. many api requests or ML training.

## Instructions
1. Create Hetzner account and add a project to your cloud
3. [Create Hetzner Storage Box](https://docs.hetzner.com/de/robot/storage-box/general). You can reuse the box.
4. Install Ansible
5. Clone Repo
6. Install python requirements
7. Write API Token to .env file. Infos [here](https://docs.hetzner.cloud/#overview)
```
echo "HETZNER_API_TOKEN=Qu36JMGVZsOZxhNFxYCwJzoJSYmxUSKiMZJAJHLtqXIvyZ70EACTZWSin795hE9r" > .env
``` 
6. Adjust settings. See settings.py for info.
7. Make sure your server doesnt block default smtp port. [Hetzner does this by default](https://docs.hetzner.com/de/cloud/servers/faq/#warum-kann-ich-keine-mails-von-meinem-server-verschicken). With Hetzner Mail you can also use port 587 and starttls. Edit email_helper.py if this doesnt work for your smtp provider.
7. Once script has finished, see [here](https://docs.hetzner.com/de/robot/storage-box/access/access-overview) for file retrieval options

## Script Requirements
- Yor script directory has to contain a subdirectory where the script writes output to
- Your script directory has to contain a requirements.txt

## Misc
### Connect to Server
To connect to the server created by the script, you have to use the generated private SSH key.

'''
ssh -i ansible/env/ssh_key user@ip
'''



## Sources:
- https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps#
- https://jayden-chua.medium.com/use-supervisor-to-run-your-python-tests-13e91171d6d3
- https://mrkaran.dev/posts/supervisor-notifications/


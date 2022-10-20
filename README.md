# Script server
WIP

Script to set up a server for remotely running some script e.g. many api requests or ML training.

## Instructions
1. Install Ansible
1. Clone Repo
2. Install python requirements
3. Write API Token to .env file. Infos [here](https://docs.hetzner.cloud/#overview)
```
echo "HETZNER_API_TOKEN=Qu36JMGVZsOZxhNFxYCwJzoJSYmxUSKiMZJAJHLtqXIvyZ70EACTZWSin795hE9r" > .env
``` 
4. Adjust settings. See settings.py for info.

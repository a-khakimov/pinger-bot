# Pinger-Bot

This bot need to poll the status of the basic bot, with a view to its prompt recovery if he falls.
The main task is to send him messages every 5 minutes and receive a response. If the answer is no, he will write in General chat that the bot fell.

## How use it?

The following tools are required for its operation:

* python
* vk api

```bash
sudo apt install python3 python3-pip
pip3 install vk
```

Add to **.authdata.json** the following fields:

```json
{
    "app_id" : "id",             
    "user_login" : "login",     
    "user_password" : "pass",   
    "bot_id" : "id",            
    "discussion_id" : "id"     
}
```

Run

```bash
python3 pinger-bot.py
```

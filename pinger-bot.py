import vk
import time
import json
import logging
import threading

logging.basicConfig(filename="pinger-bot.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")

def notifyDevelopers(vkapi, discussionID, notification):
    logging.info("notifyDevelopers: Bot has fallen")
    print("notifyDevelopers: Bot has fallen")
    vkapi.messages.send(chat_id=discussionID, message=notification)


def getResponse(vkapi, botID):
    response = vkapi.messages.get(time_offset=1)
    if response['items']:
        userID = response['items'][0]['user_id']
        readState = response['items'][0]['read_state']             
        if userID == int(botID) and readState == 0:    # if this is my bot
            logging.info("getResponse: Bot alive")
            print("getResponse: Bot alive")
            return True
        else:
            logging.info("getResponse: Bot not alive")
            print("getResponse: Bot not alive")
            return False


# thread for sender
def sender(vkapi, botID, waitTime=300):
    while True:
        logging.info("sender: Are you alive?")
        print("sender: Are you alive?")
        vkapi.messages.send(user_id=botID, message='Ты живой?')
        time.sleep(waitTime)


# thread for receiver
def receiver(vkapi, botID, discussionID, waitTime=300):
    checkTimer = 0
    while True:
        if getResponse(vkapi, botID):
            checkTimer = 0
            
        elif checkTimer > waitTime:            
            notifyTimer = 0
            while not getResponse(vkapi, botID):
                if notifyTimer > waitTime:
                    notifyTimer = 0
                    notifyDevelopers(vkapi, discussionID,
                                     '☠ Ваш бот не отвечает, по ходу он #упал ☠')
                    logging.info("receiver: checkTimer > waitTime : notify developers")
                    print("receiver: checkTimer > waitTime : notify developers - ",
                          checkTimer)
                notifyTimer += 1
                time.sleep(1)
            checkTimer = 0
        time.sleep(1)
        checkTimer += 1


def main():

    with open('.authdata.json') as json_data:
        data = json.load(json_data)
        json_data.close()
        
    appID         = data['app_id']
    userLogin     = data['user_login']
    userPassword  = data['user_password']
    bot_id        = data['bot_id']
    discussion_id = data['discussion_id']

    logging.info("Pending start...")
    
    vk_session = vk.AuthSession(app_id=appID, user_login=userLogin, user_password=userPassword, scope='wall, messages')
    vkapi = vk.API(vk_session, v='5.35', lang='ru', timeout=10)
    
    sender_thread = threading.Thread(target=sender, args=(vkapi, bot_id, ))
    receiver_thread = threading.Thread(target=receiver, args=(vkapi, bot_id, discussion_id, ))

    sender_thread.start()
    receiver_thread.start()

    sender_thread.join()
    receiver_thread.join()
    

if __name__ == '__main__':
    main()

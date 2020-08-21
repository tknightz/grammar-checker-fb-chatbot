from flask import Flask, request
from pymessenger.bot import Bot
from process_message import Process

app = Flask(__name__)       # Initializing our Flask application
ACCESS_TOKEN = 'YOUR-APP-TOKEN'
VERIFY_TOKEN = 'YOUR-FB-VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

# Importing standard route and two requst types: GET and POST.
# We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was not GET, it  must be POSTand we can just proceed with sending a message
    # back to user
    else:
            # get whatever message a user sent the bot
        output = request.get_json()
        print('-----------------')
        print(output)
        print('-----------------')
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('postback'):
                    print('+ Add new users '+message['sender']['id'])
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        user_res = message['message'].get('text')
                        response_sent_text = process_message(user_res)
                        send_message(recipient_id, response_sent_text)
                    # if user send us a GIF, photo, video or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_text = 'We not support attachments.'
                        send_message(recipient_id, response_sent_text)
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by Facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def process_message(message):
    # message will be processed in class Process
    response = Process(message)
    return response.sendResponse()


# Uses PyMessenger to send response to the user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


# Add description here about this if statement.
if __name__ == "__main__":
    app.run()

from flask import Flask, request, current_app
import json
import requests
import os
from . import bot
from .utilities import find_user, make_response

PAT = os.environ.get('PAT', None)
verify_token = os.environ.get('VERIFY_TOKEN', None)


@bot.route('/', methods = ['GET'])
def worker_verification():
    if PAT is not None and verify_token is not None:
        if request.args.get('hub.verify_token', '') == verify_token:
            print("Verification successful!")
            return request.args.get('hub.challenge', '')
        else:
            print("Verification failed!")
            return 'Error, wrong validation token'
    else:
        return "Could not get verification tokens."

@bot.route('/', methods = ['POST'])
def worker_messaging():
    try:
        messages = request.get_json()
        if messages['object'] == 'page':
            for message in messages['entry']:
                for msg in message['messaging']:
                    if (msg.get('message')) or  (msg.get('postback')):
                        sender_id = msg['sender']['id']
                        user = find_user(sender_id, PAT)

                        print(msg)

                        if msg.get('postback'):
                            received = msg['postback']['payload']
                            if received == 'start':
                                make_response(sender_id, 'message', 'greeting', PAT)
                                make_response(sender_id, 'message', 'products', PAT)
                        elif msg.get('message'):
                            received = msg["message"]
                            if received.get("quick_reply"):
                                option = received["quick_reply"]["payload"]
                                if option.lower() == 'start-sh':
                                    make_response(sender_id, 'quick', 'start_shopping', PAT)
                                elif option.lower() == 'yes_cr':
                                    pass
                                elif option.lower() == 'already_p':
                                    make_response(sender_id, 'message', 'have', PAT)
                                elif option.low() == 'location':
                                    make_response(sender_id, 'number', 'number', PAT)
                                elif option[0] == "+":
                                    make_response(sender_id, 'quick', 'start_post', PAT)
                                elif option.lower() == 'yes':
                                    make_response(sender_id, 'message', 'pictures', PAT)
                            elif received.get('text'):
                                option = received["text"]

                                page = validate_url(option)
                                if page:
                                    page_id = get_page_id(page)
                                    if page_id:
                                        make_response(sender_id, 'message', 'valid_page', PAT)
                                        make_response(sender_id, 'message', 'start_man', PAT)
                                    else:
                                        make_response(sender_id, 'message', 'invalid_page', PAT)
                                else:
                                    if option.lower() == 'shoes':
                                        make_response(sender_id, 'location', 'location', PAT)
                            elif received.get('attachments'):
                                imgs = received['attachments']
                                for img in imgs:
                                    url = img['payload']['url']




    except Exception as e:
        raise e

    return 'OK', 200

@bot.errorhandler(404)
def handle_error(ex):
    print(ex)
    print(request.url_rule.rule)



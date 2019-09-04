import json
import os

import logging
import requests
import sys

formatter = '[%(asctime)-15s] %(levelname)s [%(filename)s.%(funcName)s#L%(lineno)d] - %(message)s'

logging.basicConfig(level = logging.DEBUG, format = formatter)

# Create logger instance
logger = logging.getLogger('api')
resp_path = os.path.abspath("responses.json")

assets = {
	"quick": {
		"usage" : ["introduction"],
		"type" : "quick_replies"
	},
	"message" : {
		"type": "text"
	},
	"list" : {
		"type" : "list"
	}
}


headers = {
	'Content-Type' : 'application/json'
}

graph = "https://graph.facebook.com/v3.3/me/messages?access_token={}"
__all__ = ['find_user']

_CURRENT_MODULE_ = sys.modules[__name__]

answers = []

def get_response(path):
	responses = {}
	print(resp_path)
	try:
		with open(path, "r") as store:
			responses = json.load(store)
			store.close()
	except (IOError, OSError):
		return responses
	return responses

def make_response(_id, t, k, token, **kwargs):
    loaded = None
    message = None

    path = "responses.json"
    response = get_response(path)
    if response:
        loaded = response.get(k, None)
    else:
        return None
    if not loaded:
        logger.error("Could not find specified option in provided responses.")
        return None

    handler_name = 'make_{}_replies'.format(t)
    req = 'send_{}_replies'.format(t)
    logger.info(type(req))
    #_type = assets[t]["type"]
    try:
        handler = getattr(_CURRENT_MODULE_, handler_name)
        message = handler(loaded)
        api_request = getattr(_CURRENT_MODULE_, req)
        if t == 'message':
            if k == 'greeting':
                msg = loaded.get('text', None) + find_user(_id, token) + loaded.get('end', None) '!'
                logger.info(message)
                api_request(_id, msg, token)
                api_request(_id, loaded["description"], token)
            else:
                api_request(_id, loaded.get('text', None), token)
        elif t == 'quick':
            text = loaded.get('text', None)
            api_request(_id, text, message, token)
        elif t == 'list':
            logger.info(message)
            api_request(_id, message, token)
        elif t == 'location':
            text = loaded.get('text', None)
            api_request(_id, text, message, token)
        elif t == 'number':
            text = loaded.get('text', None)
            api_request(_id, text, message, token)
        else:
            pass

    except AttributeError as e:
        logger.warning('Could not find handler for {}'.format(t))
        logger.error(e, exec_info = True)
    return True

def make_number_replies(payload):
    replies = []
    reply = {}
    reply["content_type"] = "user_phone_number"
    print(reply)
    replies.append(reply)

    return replies


def send_number_replies(_id, txt, msg, token):
	data = json.dumps({
		"recipient":{
			"id": _id
		},
		"message": {
			"text": txt,
			"quick_replies": msg
		}
		})
	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made quick responses request!")
	else:
		logger.error('{} :{}'.format(r.status_code, r.text))

def make_location_replies(payload):
    replies = []

    for i in range(len(payload.get("options", None))):
        reply = {}
        reply["content_type"] = "location"
        reply["title"] = payload["options"][i]
        reply["payload"] = payload["payload"][i]
        print(reply)
        replies.append(reply)

    return replies

def send_location_replies(_id, txt, msg, token):
	data = json.dumps({
		"recipient":{
			"id": _id
		},
		"message": {
			"text": txt,
			"quick_replies": msg
		}
		})
	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made quick responses request!")
	else:
		logger.error('{} :{}'.format(r.status_code, r.text))


def make_quick_replies(payload):
	replies = []

	for i in range(len(payload.get("options", None))):
		reply = {}
		reply["content_type"] = "text"
		reply["title"] = payload["options"][i]
		reply["payload"] = payload["payload"][i]
		print(reply)
		replies.append(reply)

	return replies


def make_postback_replies(payload, postback):
	replies = []

	for i in range(len(payload.get("choices", None))):
		reply = {}

		reply["type"] = "postback"
		reply["title"] = payload["choices"][i]
		reply["payload"] = postback
		replies.append(reply)
	print(replies)
	return replies


def make_message_replies(text):
	payload = {
		"message": text
	}

	return payload


def send_message_replies(_id, text, token):
	data = json.dumps({
		"recipient":{
			"id": _id
		},
		"message": {
			"text": text
		}
		})
	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made messages responses request!")
	else:
		logger.error('{} : {}'.format(r.status_code, r.text))



def send_quick_replies(_id, txt, msg, token):
	data = json.dumps({
		"recipient":{
			"id": _id
		},
		"message": {
			"text": txt,
			"quick_replies": msg
		}
		})
	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made quick responses request!")
	else:
		logger.error('{} :{}'.format(r.status_code, r.text))

def make_generic_message(payload, obj):
	pass

def make_list_replies(payload):
	replies = []

	options = payload.get('options', None)

	for i in range(len(options)):
		reply = {}
		reply["title"] = options[i]["product"]
		reply["subtitle"] = options[i]["description"]
		reply["buttons"] = make_postback_replies(options[i], options[i]["payload"])
		replies.append(reply)
	return replies

def send_list_replies(id, payload, token):
	data = json.dumps({
        "recipient":{
            "id": id
        },
        "message":{
            "attachment":{
            "type":"template",
            "payload":{
                "template_type":"list",
				"top_element_style": "compact",
                "elements": payload
            	}
            }
    	}
	})

	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made postback responses request!")
	else:
		logger.error('{} :{}'.format(r.status_code, r.text))

def send_carousel(id, payload, token):
	data = json.dumps({
        "recipient":{
            "id": id
        },
        "message":{
            "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements": payload
            }
            }
        }
		})

	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made postback responses request!")
	else:
		logger.error('{} :{}'.format(r.status_code, r.text))

def send_postback_replies(_id, txt, buttons, token):
	data = json.dumps({
		"recipient":{
			"id": _id
		},
		"message":{
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"button",
					"text": txt,
					"buttons": buttons
				}
			}
			}
		})

	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made postback responses request!")
	else:
		logger.error('{} :{}'.format(r.status_code, r.text))

def create_media_reply(payload):
    replies = []

    for i in range(len(payload.get("products", None))):
        reply = {}
        reply["media_type"] = "text"
        reply["attachment_id"] = payload["options"][i]
        reply["payload"] = payload["payload"][i]
        print(reply)
        replies.append(reply)

    return replies

def send_media_reply(id, payload, token):
	data = json.dumps({
			"recipient":{
			"id": id
		},
		"message":{
			"attachment":{
			"type":"template",
			"payload":{
				"template_type":"media",
				"elements": payload
				}
			}
		}
	})

	r = requests.post(graph.format(token), headers = headers, data = data)
	if r.status_code == 200:
		logger.info("Successfully made postback responses request!")
	else:
		logger.error('{} :{}'.format(r.status_code, r.text))

def find_user(id, token):
	headers = {
	'Content-Type' : 'application/json'
	}
	r = requests.get('https://graph.facebook.com/v3.3/' + id + '?fields=first_name,last_name&access_token=' + token , headers = headers)
	nm = r.json()
	return nm['first_name']

def get_language(id, token):
	headers = {
		'Content-Type' : 'application/json'
	}

	r = requests.get('https://graph.facebook.com/v3.3/' + id + '?fields=locale&access_token=' + token, headers = headers)
	nm = r.json()
	print(nm)
	return nm['locale'][:2]

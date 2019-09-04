import requests
import json

headers = {
	'Content-Type' : 'application/json'
}
id = 623241951418023

url = 'https://scontent.xx.fbcdn.net/v/t1.15752-9/67608031_316534222395015_4601033863878148096_n.png?_nc_cat=104&_nc_oc=AQllvY0tTm7-sr3I1N-Hm4MfFdi0vKuO6JNXTdTbP96dpPNwrDsYL2u7VhvrCJpLgtQOUA1-QkfIkNGx19-vI2al&_nc_ad=z-m&_nc_cid=0&_nc_zor=9&_nc_ht=scontent.xx&oh=9e5cd7bc50e738b0d9288d0719449e92&oe=5DEEA334'

UAT = 'EAAJDYAliLj0BAAlX5tftYnKmckGpbshIdu0EDPXCsVtOq9g1AMCwdHeOfdZB9huopqosXn3xukO6L2d0g2ZBikkwMKrZCWEK3yU58JEGauSFUFHrC9Oio0cnYB3ZBVxfhZC0gSO80cTm8K1ToWDGELhE275wZCyNOgClZCOLXUTLmfa8mDiokZBcAW3dsugNVWJIhRsbwcfZAiAZDZD'
def post_photo():
    data = json.dumps({
        'url': url
    })
    fb = 'https://graph.facebook.com/{0}/photos?spublished=false&access_token={2}'.format(id, url, UAT)

    r = requests.post(fb, headers = headers, data= data)
    response = json.loads(r.content)
    img = response["id"]



def make_post():
    data = json.dumps({
       'message': 'Hello There!',
       "attached_media": [
           {"media_fbid":653954418346776}]
    })
    fb = 'https://graph.facebook.com/{0}/feed?published=true&access_token={1}'.format(id, UAT)

    r = requests.post(fb, headers = headers, data = data)
    response = json.loads(r.content)
    print(response)

make_post()
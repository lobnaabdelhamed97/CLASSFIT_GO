import base64
import json
import requests
from utils import game_utils


def generateBasicHeader():
    # api_id = app.config['ZOOM_ID']
    # api_secret = app.config['ZOOM_SECRET']
    ZOOM_ID = "bXN7_ttaTFeYzHrEqnHztA"
    ZOOM_SECRET = "1LKhbaGMfI3McWRYo1g3j1TQLuGr7WVb"
    data = ZOOM_ID + ':' + ZOOM_SECRET
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encode_data = str(encodedBytes, "utf-8")
    return encode_data


def refreshAccessToken(player_id, refresh_token):
    if int(player_id) < 1:
        return False
    if str(refresh_token) == "":
        return False

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    token_url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": "Basic %s" % generateBasicHeader(),
        'content-type': "application/x-www-form-urlencoded"
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response = json.loads(response.text)
    if response != {}:
        if 'refresh_token' in response:
            token = response['access_token']
            game_utils.update_access_token(response['refresh_token'], player_id)
            if str(game_utils.update_access_token).__contains__("something happened:"):
                raise Exception(game_utils.update_access_token)

        return response

    return False


def createMeeting(user_id, meeting_data, token):
    headers = {'authorization': "Bearer " + token, 'content-type': "application/json"}
    url = "https://zoom.us/v2/users/%s/meetings" % user_id
    data = json.dumps(meeting_data, default=decode_bytes, indent=4)
    response = requests.post(url, headers=headers, data=data)
    response = json.loads(response.text)
    return response


def decode_bytes(data):
    return data.decode('utf-8')

from urllib.request import urlopen
import json


def check_session(request, session_name):
    return session_name in request.session  # Boolean: True/False


def read_json_internet(url):
    data = []
    try:
        url_response = urlopen(url)
        data = json.loads(url_response.read().decode())
    except Exception as ex:
        print(ex)
    return data
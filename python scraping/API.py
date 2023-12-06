import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

def getCountry(ipAddress):
    try:
        response = urlopen('http://ip-api.com/json/' + ipAddress).read().decode('utf-8')
        responseJson = json.loads(response)
        return responseJson.get('countryCode')
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('Failed to reach a server.')
        print('Reason: ', e.reason)
    except json.JSONDecodeError:
        print('JSON decoding failed.')

print(getCountry('194.136.126.53'))

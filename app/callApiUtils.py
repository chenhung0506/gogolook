import const
import log
import json
import requests
from urllib import parse

class CallApi(object):
    def post_request(self, url, headers, data):
        try:
            if headers.get("Content-Type") == "application/json":
                log.debug("application/json")
                data = json.dumps(data)
            elif headers.get("Content-Type") == "application/x-www-form-urlencoded":
                log.debug("application/x-www-form-urlencoded")
                data = parse.urlencode(data)

            log.info("call api: " + str(url) + "\nwith data: " + str(json.dumps(data)))
            log.info("header: " + str(json.dumps(headers)))
            response = requests.request("POST", url, data=data, headers=headers)
            if response.status_code != 200:
                raise Exception('Response status: ' + str(response.status_code) + ', message: ' + response.text)
            return response

        except Exception as e:
            log.error(utils.except_raise(e))
            raise Exception(e)

    def get_request(self, url, headers):
        try:
            log.info("call api: " + url)
            log.debug("header: " + str(headers))
            response = requests.request("GET", url, headers=headers)
            if response.status_code != 200:
                raise Exception('Response status: ' + str(response.status_code) + ', message: ' + response.text)
            return response

        except Exception as e:
            log.error(utils.except_raise(e))
            raise Exception(e)
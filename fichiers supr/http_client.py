import json
import requests


IP_ADRESS = '127.0.0.1'
HTTP_PORT = 26686


class HTTPClient:
    """
    Implements an HTTP client
    """

    def __init__(self, ip=IP_ADRESS, port=HTTP_PORT):
        self.url = "http://" + ip + ":" + str(port)

    def send(self, data):
        """
        Send the data to the Dashboard server. The data must be a dict that can be dumped to JSON.
        """
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        session = requests.Session()
        session.trust_env = False
        r = session.post(self.url, data=data_json, headers=headers, verify=False)
        r.raise_for_status()

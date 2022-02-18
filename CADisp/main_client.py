"""


from optparse import OptionParser

from cadisp.clients import PushClient

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a", "--action", help="manual, auto_available, autonomous, end_zone, critical, "
                                             "safety_stop or shutdown")
    parser.add_option("-i", "--ip", default="127.0.0.1", help="Target IP")
    parser.add_option("-p", "--port", type="int", default=9308, help="Target port")
    (options, args) = parser.parse_args()

    client = PushClient(options.ip, options.port)
    client.send({"action": options.action})
    client.quit()
"""
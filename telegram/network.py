###############################################
#
#           Модуль с сетевыми фичами
#
###############################################


from re import match, search

from pythonping import ping
from time import time

class Pinger:

    def __init__(self):
        self.__class__.last_ping = int(time())

    def check_ping(self, msg):
        host = self._parse_host(msg)
        if host:
            if self._can_i():
                self.__class__.last_ping = int(time())
                return ping(host)
            else:
                return 'Пингую не чаще одного раза в 5 секунд'

    def _can_i(self):
        """
        Прошло ли 5 секунд с последней попытки пинга
        """
        return int(time()) > self.last_ping + 5

    def _parse_host(self, string):
        params = string.split()
        host_pattern = '((\d{1,3}\.*){4})|([A-Za-z0-9.\-_]+)'
        if 'пинг' in string.lower() or 'ping' in string.lower():
            host = None
            for param in params:
                if match(host_pattern, param) and '.' in param:
                    host = search(host_pattern, param)[0]
                if host:
                    return host

if __name__ == '__main__':
    p = Pinger()
    p.check_ping('ping ident.me')
    # ping('8.8.8.8')
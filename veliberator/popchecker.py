"""Pop checker waiting for actions"""
from poplib import POP3, POP3_SSL

from veliberator.settings import *

pop_checker_class = MAIL_SSL and POP3_SSL or POP3

class PopChecker(pop_checker_class):
    """object for checking messages on POP server"""
    
    def __init__(self, server=MAIL_SERVER, port=MAIL_PORT,
                 login=MAIL_ACCOUNT, password=MAIL_PASSWORD):
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        pop_checker_class.__init__(self, self.server, self.port)

    def authenticate(self):
        self.user(self.login)
        self.pass_(self.password)

    


pop_checker = PopChecker()







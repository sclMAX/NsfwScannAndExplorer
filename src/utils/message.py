from src.utils import constants
class Message(object):
    msg = ''
    tipo = constants.NORMAL

    def __init__(self, msg, tipo = constants.NORMAL):
        self.msg = msg
        self.tipo = tipo
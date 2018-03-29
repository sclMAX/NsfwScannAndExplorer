from src.utils import constants


class Message(object):
    msg = ''
    tipo = constants.NORMAL
    isAnimate = False

    def __init__(self, msg, isAnimate=False, tipo=constants.NORMAL):
        self.msg = msg
        self.tipo = tipo
        self.isAnimate = isAnimate

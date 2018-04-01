from src.utils import constants

NORMAL = 1000
WARNING = 1001
DANGER = 1002

class Message(object):
    msg = ''
    tipo = constants.NORMAL
    isAnimate = False
    isLog = True

    def __init__(self, msg, isAnimate=False, tipo=constants.NORMAL, isLog = True):
        self.msg = msg
        self.tipo = tipo
        self.isAnimate = isAnimate
        self.isLog = isLog
    
    def setMsg(self, msg):
        self.msg = msg
    
    def setTipo(self, tipo):
        self.tipo = tipo

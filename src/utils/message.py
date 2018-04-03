
NORMAL = 1000
WARNING = 1001
DANGER = 1002


class Message(object):
    msg: str = ''
    tipo: int = NORMAL
    isAnimate: bool = False
    isLog: bool = True

    def __init__(self, msg: str, isAnimate=False, tipo=NORMAL, isLog=True):
        self.msg = msg
        self.tipo = tipo
        self.isAnimate = isAnimate
        self.isLog = isLog

    def setMsg(self, msg):
        self.msg = msg

    def setTipo(self, tipo):
        self.tipo = tipo

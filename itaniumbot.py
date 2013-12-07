from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import os
import socket

def loadavg():
    return "One minute load average: %s" % os.getloadavg()[0]

class ItaniumBot(irc.IRCClient):
    nickname = "CSL" + socket.gethostname()
    commands = {"load": loadavg}
    
    def signedOn(self):
        self.join("#tjhsst-cluster")

    def privmsg(self, user, channel, msg):
        if msg.startswith(self.nickname + ": "):
            msg = msg.replace(self.nickname + ": ", "")
        elif msg.startswith("!"):
            msg = msg[1:]
        else:
            return
        msg = msg.split()
        command = msg[0]
        args = msg[1:]
        try:
            self.msg(channel, self.commands[command](*args))
        except Exception, e:
            self.msg(channel, "error: %s" % e)
        

class ItaniumBotFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        p = ItaniumBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

reactor.connectTCP("irc.freenode.org", 6667, ItaniumBotFactory())
reactor.run()

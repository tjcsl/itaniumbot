from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import os
import importlib
import socket

class ItaniumBot(irc.IRCClient):
    nickname = "CSL" + socket.gethostname()
    
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
        command, args = msg[0], msg[1:]
        if command == "reload":
            try:
                self.modules = self.factory.load_modules()
                self.msg(channel, "Modules reloaded successfully.")
            except Exception, e:
                self.msg(channel, "error: %s" % e)
            return
        if command == "list":
            self.msg(channel, ", ".join([i.replace("modules.", "") for i in self.modules]))
            return
        try:
            command = "modules." + command
            self.msg(channel, self.modules[command].run(*args))
        except Exception, e:
            pass
        

class ItaniumBotFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        p = ItaniumBot()
        p.modules = self.load_modules()
        p.factory = self
        return p
    
    def load_modules(self):
        modlist = os.listdir("modules")
        modlist = [i for i in modlist if "__init__" not in i]
        modlist = ["modules.%s" % (i[:-3]) for i in modlist if i.endswith(".py")]
        mods = {i: importlib.import_module(i) for i in modlist}
        return mods

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

reactor.connectTCP("irc.freenode.org", 6667, ItaniumBotFactory())
reactor.run()

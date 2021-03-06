from phenomena.connection import OSCMessageSender
from phenomena.connection import RawMessageSender

HOST = '127.0.0.1'


class Phenomena:

    def addParticle(self, particle, **kwargs):
        params={'particle_name': particle, 'theta': kwargs.get('theta',0), 'phi': kwargs.get('phi',0), 'p':kwargs.get('p',0), 'E':kwargs.get('E',0)}
        received_message = self._sendMessage("node", "ADD", **params)
        return received_message
    
    def simpleAddParticle(self, particle):
        params = [particle]
        received_message = self._sendMessage("/ADD", None, *params)
        return received_message

    def simplePurgeParticles(self):
        received_message = self._sendMessage("/PURGE", None)
        return received_message
    
    def purgeParticles(self):
        received_message = self._sendMessage(module_path="node.accumulator", command_name="PURGE")
        return received_message

    def _sendMessage(self, module_path, command_name, *args, **kwargs):
        message_sender = OSCMessageSender(HOST)
        return message_sender.sendMessage(module_path, command_name, *args, **kwargs)


if __name__ == '__main__':
    import time
    import random
    phenomena = Phenomena()
    begin_time = time.time()

    loop_1 = random.randint(1, 10)
    print("LOOP 1: {0}".format(loop_1))
    for i in range(loop_1):
        loop_2 = random.randint(1, 10)
        print("LOOP 2: {0}".format(loop_2))
        for i in range(loop_2):
            print(phenomena.simpleAddParticle("Z0"))
            time.sleep(0.5)
        time.sleep(5)
        print(phenomena.simplePurgeParticles())
        time.sleep(25)
    print("Total time: {0}".format(time.time() - begin_time))

from phenomena.mappings import MappingsController
from phenomena import connection
from phenomena.nodes import get_save_node
from phenomena.particles.particle_action import ParticleActionNodeChain
from phenomena.particles import Particle
from phenomena.utils import get_logger
from phenomena.connection import OSCBundledMessageSender

class PosadaAudioNode(ParticleActionNodeChain):
    #_IP =  "172.16.7.183"
    _IP = "127.0.0.1"
    #_IP = "172.16.4.23"
    #_IP = "172.16.17.143"
    _PORT = 12346
    def __init__(self):
        super(ParticleActionNodeChain, self).__init__()
        self._mapping_controller = MappingsController()
        self._log = get_logger("nodes.video_node")
        self._node = get_save_node()

    def addParticle(self, particle):
        assert issubclass(type(particle), Particle)
        try:
            self._addParticlesMessage([particle])
            #self._sendMessage(msg)
        except Exception as ex:
            message = "Failed adding Particle on {0} cause: {1}".format(self.__class__.__name__, ex.message)
            self._log.exception(message)
            raise Exception(message)
        finally:
            self._node.getNextNode(self).addParticle(particle)

    def removeParticle(self, particle):
        assert issubclass(type(particle), Particle)
        try:
            self._removeParticlesMessage(particle)
            #self._sendMessage(msg)
        except:
            self._log.exception("Failed removing Particle on {0}".format(self.__class__.__name__))
        finally:
            self._node.getNextNode(self).removeParticle(particle)

    def transformParticle(self, particle, new_particles):
        add_message = self._addParticlesMessage(new_particles)
        rm_message = self._removeParticlesMessage([particle])
        all_messages = rm_message + add_message
        self._node.getNextNode(self).transformParticle(particle, new_particles)
        #self._sendMessage(all_messages)

    def purgeParticles(self):
        new_message = {}
        new_message['CMD'] = "PURGE"
        new_message['PARAMS'] = {}
        self._sendMessage("particle", new_message)

    def getIdentifier(self):
        return "PosadaAudioController"

    def setNextNode(self, n_node):
        self._node.setNextNode(self, n_node)

    def setPastNode(self, p_node):
        self._node.setPastNode(self, p_node)

    def execute(self, incoming_message):
        pass

    def _addParticlesMessage(self, particles_list):
        new_messages = []
        for particle in particles_list:
            new_message = {}
            new_particle = self._mapping_controller.translateParticle(particle)
            new_message['CMD'] = "ADD"
            new_message['PARAMS'] = new_particle.toDictionary()
            new_messages.append(new_message)
            self._sendMessage("particle", new_message)
        return new_messages

    def _removeParticlesMessage(self, particles_list):
        new_messages = []
        for particle in particles_list:
            new_message = {}
            new_message['CMD'] = "REMOVE"
            new_message['PARAMS'] = {'id':particle.id};
            new_messages.append(new_message)
            self._sendMessage("particle", new_message)
        return new_messages

    def _sendMessage(self, module_path, message):
        self._log.info("Sending new Message to: {0}!".format(module_path))
        self._log.debug("Message: {0}".format(message))
        message_sender = OSCBundledMessageSender(PosadaAudioNode._IP, PosadaAudioNode._PORT)
        command_name = message.pop("CMD")
        message_sender.sendMessage(module_path, command_name = command_name, **message['PARAMS'])

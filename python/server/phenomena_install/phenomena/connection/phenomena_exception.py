import builtins as exceptions

class ModuleNotFoundException(Exception):

    def __init__(self, module_path):
        super(ModuleNotFoundException, self).__init__("Module: {0} path not found!".format(module_path))

class DeserializationException(Exception):
    def __init__(self, message):
        super(DeserializationException, self).__init__("Unable to Deserialize Message: {0}".format(message))

class MessageFormatError(Exception):
    def __init__(self):
        super(MessageFormatError, self).__init__("Message Format Error")

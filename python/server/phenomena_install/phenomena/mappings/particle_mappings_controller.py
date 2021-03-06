from .mappings_available import ConstMapping, MirrorMapping, MassMapping
from phenomena.particles.particle import Particle, BasicParticle


class MappingsController:

    def __init__(self):
        self._map_dictionary = {"charge": MirrorMapping(),
                               "mass": MassMapping(),
                               "transformtime": MirrorMapping(),
                               "composition": MirrorMapping(),
                               "type": MirrorMapping(),
                               "p": MirrorMapping(),
                               "E": MirrorMapping(),
                               "vx": MirrorMapping(),
                               "vy": MirrorMapping(),
                               "vz": MirrorMapping(),
                               "beta": MirrorMapping(),
                               "symbolName": MirrorMapping()
                               }

    def translateParticle(self, particle):
        assert issubclass(type(particle), Particle)
        translated_values = {'name': particle.name}
        translated_values['id'] = particle.id
        translated_values['parent'] = particle.parent
        for characteristic, mapping in self._map_dictionary.items():
            original_value = getattr(particle, characteristic)
            translated_value = mapping.translateValue(original_value)
            translated_values[characteristic] = translated_value
        translated_particle = BasicParticle(**translated_values)
        return translated_particle

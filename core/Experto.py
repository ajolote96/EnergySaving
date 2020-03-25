from experta import *
from .models import Registro

"Declaracion de los hechos"
class RgsHecho(Fact):
    "Se declara unicamente para que funcione con la libreria de python PyKnow-Experta"
    pass

"Declaracion del sistema experto"
class Experto(KnowledgeEngine):

    "Cargamos los hechos"
    @DefFacts()
    def Carga_de_facts(self):
        Regs = Registro.objects.all()
        for Reg in Regs:
            yield RgsHecho(irms = Reg.irms, voltaje = Reg.voltaje, watts = Reg.watts, intencidadPico = Reg.intencidadPico, created = Reg.created)
from experta import *
from .models import RegistroMinuto, AutonomoConfig
from datetime import datetime, timedelta

#Declaracion de hechos, clases que heredan de Fact
class RegistroWattsMinuto(Fact):
    pass

class RegistroKwh(Fact):
    pass

class RegistroDiario(Fact):
    pass

class RegistroMensual(Fact):
    pass

#Declaramos el sistema experto, clase que hereda de KnowledgeEngine
class ExpertoHoras(KnowledgeEngine):

    FactsViejos = []
    SumaWatts = 0

    #Cargamos hechos de la base de datos
    @DefFacts()
    def Carga_de_facts(self):
        Regs = RegistroMinuto.objects.all()
        for Reg in Regs:
            yield RegistroWattsMinuto(watts = Reg.watts, fecha = Reg.fecha.strftime("%Y-%m-%d"), hora = Reg.hora.hour)

    #Regla para clasificar los registros por KwH gastados en cienta hora y fecha
    @Rule(
        AS.f1 << RegistroWattsMinuto(watts = MATCH._watts, fecha = MATCH._Date, hora = MATCH._hora),
        AS.f2 << RegistroWattsMinuto(watts = MATCH._watts2, fecha = MATCH._Date, hora = MATCH._hora)
        )
    def ClasificarPorKwh(self, _watts, _watts2, _Date, _hora, f1, f2):
        self.FactsViejos.append(f1)
        self.retract(f2)

        if f1 == f2:
            self.SumaWatts += float(_watts)
            Total = float(self.SumaWatts / 1000)
            self.declare(RegistroKwh(tipo = "Registro de Kwh", fecha = _Date, hora = _hora, Kwh = float("{:.2f}".format(Total))))
            self.SumaWatts = 0
        else:
            self.SumaWatts += float(_watts2)

    def CargarFactsManual(self, ListaFacts):
        for Fact in ListaFacts:
            self.declare(Fact)
        pass
    pass

class ExpertoDias(KnowledgeEngine):
    FactsViejos = []
    SumaWatts = 0

   #Regla pra clasificar los registro de Kwh gastados por dias
    @Rule(
        AS.f1 << RegistroKwh(Kwh = MATCH._wattsf1, fecha = MATCH._Date),
        AS.f2 << RegistroKwh(Kwh = MATCH._wattsf2, fecha = MATCH._Date)
    )
    def ClasificarPorDias(self, _wattsf1, _wattsf2, _Date, f1, f2):
        self.FactsViejos.append(f2)
        self.retract(f2)

        if f1 == f2:
            self.SumaWatts += float(_wattsf1)
            Fecha = datetime.strptime(_Date, "%Y-%m-%d")
            self.declare(RegistroDiario(anio = Fecha.year, mes = Fecha.month, dia = Fecha.day, Kwh = float("{:.2f}".format(self.SumaWatts))))
            self.SumaWatts = 0
        else:
            self.SumaWatts += float(_wattsf2)
        pass

    def CargarFactsManual(self, ListaFacts):
        for Fact in ListaFacts:
            self.declare(Fact)
        pass
    pass

class ExpertoMeses(KnowledgeEngine):
    FactsViejos = []
    SumaWatts = 0

    #Agrupar el consumo por meses
    @Rule(
        AS.f1 << RegistroDiario(Kwh = MATCH._wattsf1, anio = MATCH._Anio, mes = MATCH._Mes),
        AS.f2 << RegistroDiario(Kwh = MATCH._wattsf2, anio = MATCH._Anio, mes = MATCH._Mes)
    )
    def ClasificarPorMeses(self, _wattsf1, _wattsf2, _Anio, _Mes, f1, f2):
        self.FactsViejos.append(f2)
        self.retract(f2)

        if f1 == f2:
            self.SumaWatts += float(_wattsf1)
            self.declare(RegistroMensual(anio = _Anio, mes = _Mes, Kwh = float("{:.2f}".format(self.SumaWatts))))
            self.SumaWatts = 0
        else:
            self.SumaWatts += float(_wattsf2)

        pass

    def CargarFactsManual(self, ListaFacts):
        for Fact in ListaFacts:
            self.declare(Fact)
        pass
    pass

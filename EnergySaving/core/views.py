import requests, datetime, json, random, asyncio
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, request
from core.Experto import ExpertoDias, ExpertoHoras, ExpertoMeses
from .models import RegistroMinuto, AutonomoConfig

Direccion = "http://192.168.0.19/"

# Create your views here.
def Home(request):
    return render(request, "core/HomeBase.html")

def Encender(request):
    try:
        Peticion = requests.get(Direccion + 'encender')
        if Peticion.status_code == 200:
            data = {
                'code': Peticion.status_code,
                'description': "Encendido con exito"
            }
        elif Peticion.status_code == 202:
             data = {
                'code': Peticion.status_code,
                'description': "El dispositivo ya esta encendido."
            }           
        elif Peticion.status_code == 404:
            data = {
                'code': Peticion.status_code,
                'description': "No se encontro la ruta, revisala."
            }
        elif Peticion.status_code == 502:
            data = {
                'code': Peticion.status_code,
                'description': "No se pudó conectar con el ESP"
            }
        else:
            data = {
                'code': Peticion.status_code,
                'description': str(Peticion.text)
            }
    except:
        import sys
        data = {
            'code': "ERROR",
            'description': "Ya no se puedo obtener una respuesta del dispositivo"
        }
    return JsonResponse(data)

def Apagar(request):
    try:
        Peticion = requests.get(Direccion + 'apagar')
        if Peticion.status_code == 200:
            data = {
                'code': Peticion.status_code,
                'description': "Apagado"
            }
        elif Peticion.status_code == 202:
             data = {
                'code': Peticion.status_code,
                'description': "El dispositivo ya esta apagado."
            }           
        elif Peticion.status_code == 404:
            data = {
                'code': Peticion.status_code,
                'description': "No se encontro la ruta, revisala."
            }
        elif Peticion.status_code == 502:
            data = {
                'code': Peticion.status_code,
                'description': "No se pudó conectar con el ESP"
            }
        else:
            data = {
                'code': Peticion.status_code,
                'description': str(Peticion.text)
            }
    except:
        import sys
        data = {
            'code': "ERROR",
            'description': "Ya no se obtuvo una respuesta del dispositivo"
        }
    return JsonResponse(data)

def Estado(request):
    Config = AutonomoConfig.objects.get(pk=1)
    Cambio = request.GET.get('cambio')

    if Cambio == 'OK':
        Config.activado = False if Config.activado else True
        Config.save()

    try:
        Peticion = requests.get(Direccion + 'estado')
        if Peticion.status_code == 200:
            data = {
                'code': Peticion.status_code,
                'description': "Encendido",
                'horaInicio': Config.horaInicio,
                'horaFin': Config.horaFin,
                'autonomia': Config.activado
            }
        elif Peticion.status_code == 202:
             data = {
                'code': Peticion.status_code,
                'description': "En reposo",
                'horaInicio': Config.horaInicio,
                'horaFin': Config.horaFin,
                'autonomia': Config.activado
            }
        elif Peticion.status_code == 502:
            data = {
                'code': Peticion.status_code,
                'description': "No se puedo extablecer conexion con el dispositivo",
                'horaInicio': Config.horaInicio,
                'horaFin': Config.horaFin,
                'autonomia': Config.activado
            }
        else:
            data = {
                'code': Peticion.status_code,
                'description': str(Peticion.text),
                'horaInicio': Config.horaInicio,
                'horaFin': Config.horaFin,
                'autonomia': Config.activado
            }
    except:
        data = {
            'code': "ERROR",
            'description': "No se pudo conectar con el dispositivo",
            'horaInicio': Config.horaInicio,
            'horaFin': Config.horaFin,
            'autonomia': Config.activado
        }
    return JsonResponse(data)

def RecivirData(request):
    try:
        if request.method == 'GET':

            watts = request.GET.get('watts')

            fecha = datetime.datetime.now()
            RegistroMinuto.objects.create(watts=watts, fecha = fecha, hora = fecha)

            #RegistroMinuto.objects.create(irms=irms, voltaje=voltaje, watts=random.uniform(10, 50), intencidadPico=intencidadPico, fecha = fecha, hora = fecha)

            print( "Wats por minuto: " + str(watts) + ", minutos: " + str(fecha))
            Revisar_Estado_Correcto()

            return HttpResponse("OK: Datos almacenados con exito." + str(fecha))
        else:
            return HttpResponse('ERROR: Algo salio mal con la peticion http.')
    except:
        return HttpResponse("ERROR: Sucedio un error al enviar los datos.")

def ActivarExperto(request):
    engineHoras = ExpertoHoras()
    engineHoras.reset()
    engineHoras.run()

    engineDias = ExpertoDias()
    engineDias.reset()
    engineDias.CargarFactsManual(engineHoras.facts.values())
    engineDias.run()

    engineMeses = ExpertoMeses()
    engineMeses.reset()
    engineMeses.CargarFactsManual(engineDias.facts.values())
    engineMeses.run()

    engineHoras.CargarFactsManual(engineDias.facts.values())
    engineHoras.CargarFactsManual(engineMeses.facts.values())

    Listas = Ultimas_24_Horas(engineHoras.facts.values())
    ListasSemana = Ultimos_7_dias(engineDias.facts.values())
    Consumo = Consumos(engineHoras.facts.values())

    data = {
        'Fechas': Listas[0],
        'Facts': Listas[1],
        'Hoy': Consumo[0],
        'Mes': Consumo[1],
        'Ayer': Consumo[2],
        'MesPasado': Consumo[3],
        'FechasSemana': ListasSemana[0],
        'FactsSemana': ListasSemana[1]
    }
    return JsonResponse(data)

#Funciones de apoyo, no views
def Ultimas_24_Horas(EngineList):
    "Lista de ultimas 24 horas"
    Fecha = datetime.datetime.now()
    ListaFechas = []

    for num in range(24): 
        ListaFechas.append(Fecha - datetime.timedelta(hours=num))

    "Comparar con lista de facts"
    ListaFacts = []

    for Fecha in ListaFechas:
        Flag = False
        Date = "fecha='"+str(Fecha.date())+"', hora="+ str(Fecha.hour)+","

        for fact in EngineList:
            if Date in fact.__repr__() and "Registro de Kwh" in fact.__repr__():
                Flag = True
                ListaFacts.append(fact)

        if not Flag:
            Data = {
             'tipo': 'Registro de Kwh',
             'fecha': str(Fecha.date()),
             'hora': Fecha.hour,
             'Kwh': 0.0
            }
            ListaFacts.append(Data)

    return ListaFechas, ListaFacts

def Ultimos_7_dias(EngineList):
    "Lista de los ultimos 7 dias"
    Fecha = datetime.datetime.now()
    ListaFechas = []

    for num in range(7): 
        ListaFechas.append(Fecha - datetime.timedelta(days=num))

    "Comparar con lista de facts"
    ListaFacts = []

    for Fecha in ListaFechas:
        Flag = False

        for fact in EngineList:
            obj = json.loads(json.dumps(fact))            
            if "RegistroDiario" in fact.__repr__() and Fecha.day == obj["dia"] and Fecha.month == obj["mes"] and Fecha.year == obj["anio"]:
                Flag = True
                ListaFacts.append(fact)
                break

        if not Flag:
            Data = {
             'anio': Fecha.year,
             'mes': Fecha.month,
             'dia': Fecha.day,
             'Kwh': 0.0
            }
            ListaFacts.append(Data)

    return ListaFechas, ListaFacts

def Consumos(EngineList):
    FechaHoy = datetime.datetime.now()
    ConsumoHoy = 0.0
    ConsumoMes = 0.0
    ConsumoAyer = 0.0
    ConsumoMesPasado = 0.0


    MesPasado = FechaHoy.month - 1
    Anio = FechaHoy.year
    if MesPasado < 1:
        MesPasado = 12
        Anio = Anio - 1


    for fact in EngineList:
        obj = json.loads(json.dumps(fact))

        if "RegistroDiario" in fact.__repr__() and FechaHoy.day == obj["dia"] and FechaHoy.month == obj["mes"] and FechaHoy.year == obj["anio"]:
            ConsumoHoy += float(obj["Kwh"])
        
        if "RegistroMensual" in fact.__repr__() and FechaHoy.month == obj["mes"] and FechaHoy.year == obj["anio"]:
            ConsumoMes += float(obj["Kwh"])

        FechaAyer = FechaHoy - datetime.timedelta(days=1)
        FechaMesPasado = FechaHoy - datetime.timedelta(days=1)

        if "RegistroDiario" in fact.__repr__() and FechaAyer.day == obj["dia"] and FechaAyer.month == obj["mes"] and FechaAyer.year == obj["anio"]:
            ConsumoAyer += float(obj["Kwh"])
            Fecha = datetime.datetime.strptime(str(obj["anio"])+"-"+str(obj["mes"])+"-"+str(obj["dia"]), "%Y-%m-%d")
        
        if "RegistroMensual" in fact.__repr__() and MesPasado == obj["mes"] and Anio == obj["anio"]:
            ConsumoMesPasado += float(obj["Kwh"])


    return ConsumoHoy, ConsumoMes, ConsumoAyer,ConsumoMesPasado

def Revisar_Estado_Correcto():
    Config = AutonomoConfig.objects.get(pk=1)
    if Config.activado:
        Peticion = requests.get(Direccion + 'estado')
        horaActual = datetime.datetime.now().hour
        if horaActual >= Config.horaInicio and horaActual < Config.horaFin and Peticion.status_code == 200:
            requests.get(Direccion + 'apagar')
        elif (horaActual < Config.horaInicio or horaActual >= Config.horaFin) and Peticion.status_code == 202:
            requests.get(Direccion + 'encender')
        else:
            pass


def Generar():

    "Lista de los ultimos 7 dias"
    Fecha = datetime.datetime.now()
    ListaFechas = []
    print("Hola")
    for num in range(40): 
        ListaFechas.append(Fecha - datetime.timedelta(days=num))

    for Fecha in ListaFechas:

        for Reg in RegistroMinuto.objects.filter(fecha__range=["2020-06-04", "2020-06-04"]):
            if Reg.fecha != Fecha: 
                watts = round(random.uniform(0.01, 2.99), 2)
                new = float(Reg.watts) + watts
                RegistroMinuto.objects.create(watts = new, fecha = Fecha, hora = Reg.hora)
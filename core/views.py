import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from core.Experto import Experto
from .models import Registro


# Create your views here.
def Home(request):
    return render(request, "core/home.html")

def Encender(request):
    try:
        desc = request.GET.get('desc')
        data = {
            'code': "OK",
            'description': desc
        }
        requests.get("http://192.168.0.12/encender")
    except:
        import sys
        data = {
            'code': "OK",
            'description': sys.exc_info()
        }
    return JsonResponse(data)

def Apagar(request):
    try:
        desc = request.GET.get('desc')
        data = {
            'code': "OK",
            'description': desc
        }
        requests.get("http://192.168.0.12/apagar")
    except:
        import sys
        data = {
            'code': "OK",
            'description': sys.exc_info()
        }
    return JsonResponse(data)

def RecivirData(request):
    try:
        if request.method == 'GET':
            irms = request.GET.get('irms')
            voltaje = request.GET.get('voltaje')
            watts = request.GET.get('watts')
            intencidadPico = request.GET.get('intencidadPico')

            Registro.objects.create(title='Registro de medicion', description='', irms=irms, voltaje=voltaje, watts=watts, intencidadPico=intencidadPico)

            return HttpResponse("OK: Datos almacenados con exito.")
        else:
            return HttpResponse('ERROR: Algo salio mal con la peticion http.')
    except:
        return HttpResponse("ERROR: Sucedio un error al enviar los datos.")

def ActivarExperto(request):
    engine = Experto()
    engine.reset()
    engine.run()
    json = engine.facts
    return JsonResponse(json)
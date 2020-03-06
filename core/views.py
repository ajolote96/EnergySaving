import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


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
from django.shortcuts import render, HttpResponse

# Create your views here.
def Home(request):
    return render(request, "core/home.html")

def EspRequest(request):
    return HttpResponse("HOLA el proyecto va a salir a toda madre puto")
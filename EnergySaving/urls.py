from django.contrib import admin
from django.urls import path
from core import views as core_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.Home, name='Home'),
    path('Encender/', core_views.Encender, name='Encender'),
    path('Apagar/', core_views.Apagar, name='Apagar'),
    path('RecivirData/', core_views.RecivirData, name='RecivirData'),
    path('ActivarExperto',core_views.ActivarExperto, name='Experto')
]

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
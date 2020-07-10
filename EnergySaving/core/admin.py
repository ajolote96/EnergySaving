from django.contrib import admin
from .models import RegistroMinuto, AutonomoConfig

# Register your models here.

class RegistroMinutoAdmin(admin.ModelAdmin):
    pass

class AutonomoConfigAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegistroMinuto, RegistroMinutoAdmin)
admin.site.register(AutonomoConfig, AutonomoConfigAdmin)
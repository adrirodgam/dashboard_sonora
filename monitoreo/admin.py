from django.contrib import admin
from .models import Municipio, Medicion


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Medicion)
class MedicionAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'tipo', 'valor', 'timestamp')
    list_filter = ('municipio', 'tipo', 'timestamp')
    search_fields = ('municipio__nombre',)
from django.contrib import admin

from .models import Evento, Seleccion, Usuario

# Crear evento

class InlineSeleccion(admin.TabularInline):
    model = Seleccion
    extra = 1
    exclude = ['dni']
    readonly_fields = ['recuento', 'usuarios']

class EventoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['tituloEvento', 'siguienteEvento']}),
        ('Detalles del evento', {'fields': ['fechaEvento', 'activo']}),
        ('Información sobre alérgenos', {'fields': ['permitirAlergenos', 'alergenos']})
    ]
    inlines = [InlineSeleccion]
    list_display = ('tituloEvento', 'fechaEvento', 'activo')
    list_filter = ['fechaEvento',]
    readonly_fields = ['alergenos', 'apuntados']
    search_fields = ['tituloEvento']

admin.site.register(Evento, EventoAdmin)

class Usuarios(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellidos')
    search_fields = ['dni', 'nombre', 'apellidos']

admin.site.register(Usuario, Usuarios)


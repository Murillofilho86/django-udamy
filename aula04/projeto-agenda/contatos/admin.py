from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'data_criacao', 'mostrar')
    list_display_links = ['nome']
    # list_filter = ('nome', 'telefone')
    list_per_page = 10
    search_fields = ('nome', 'telefone')
    list_editable = ['mostrar']

# Register your models here.
admin.site.register(Categoria),
admin.site.register(Contato, ContatoAdmin),


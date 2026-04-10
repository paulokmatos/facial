from django.contrib import admin
from .models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'face_label')
    search_fields = ('nome', 'cpf')
    readonly_fields = ('face_label',)

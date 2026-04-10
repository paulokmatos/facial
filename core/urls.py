from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('pessoas/', views.lista_pessoas, name='lista_pessoas'),
    path('reconhecer/', views.reconhecer, name='reconhecer'),
    path('verificar/', views.verificar_rosto, name='verificar_rosto'),
    path('pessoas/<int:pk>/editar/', views.editar, name='editar'),
    path('pessoas/<int:pk>/excluir/', views.excluir, name='excluir'),
    path('retreinar/', views.retreinar_modelo, name='retreinar_modelo'),
]

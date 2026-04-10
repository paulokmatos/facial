import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Pessoa
from .forms import PessoaForm
from . import reconhecimento


def index(request):
    total = Pessoa.objects.count()
    return render(request, 'core/index.html', {'total': total})


@csrf_protect
def cadastrar(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST, request.FILES)
        if form.is_valid():
            pessoa = form.save(commit=False)
            ultimo = Pessoa.objects.order_by('-face_label').first()
            pessoa.face_label = (ultimo.face_label + 1) if ultimo else 1
            pessoa.save()
            reconhecimento.treinar_modelo()
            messages.success(request, f'Pessoa "{pessoa.nome}" cadastrada com sucesso!')
            return redirect('lista_pessoas')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados.')
    else:
        form = PessoaForm()
    return render(request, 'core/cadastrar.html', {'form': form})


def lista_pessoas(request):
    pessoas = Pessoa.objects.all()
    return render(request, 'core/lista.html', {'pessoas': pessoas})


def reconhecer(request):
    return render(request, 'core/reconhecer.html')


@csrf_protect
def editar(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    if request.method == 'POST':
        form = PessoaForm(request.POST, request.FILES, instance=pessoa)
        if form.is_valid():
            form.save()
            reconhecimento.treinar_modelo()
            messages.success(request, f'Cadastro de "{pessoa.nome}" atualizado com sucesso!')
            return redirect('lista_pessoas')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados.')
    else:
        form = PessoaForm(instance=pessoa)
    return render(request, 'core/editar.html', {'form': form, 'pessoa': pessoa})


@csrf_protect
@require_POST
def excluir(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    nome = pessoa.nome
    pessoa.delete()
    reconhecimento.treinar_modelo()
    messages.success(request, f'Cadastro de "{nome}" excluído com sucesso!')
    return redirect('lista_pessoas')


@csrf_protect
@require_POST
def retreinar_modelo(request):
    sucesso = reconhecimento.treinar_modelo()
    if sucesso:
        messages.success(request, 'Modelo re-treinado com sucesso! Verifique o console para detalhes.')
    else:
        messages.error(request, 'Falha no re-treino: nenhum rosto detectado nas fotos cadastradas.')
    return redirect('lista_pessoas')


@csrf_protect
@require_POST
def verificar_rosto(request):
    try:
        body = json.loads(request.body)
        data_url = body.get('imagem', '')
        if not data_url:
            return JsonResponse({'status': 'erro', 'mensagem': 'Imagem não fornecida.'})

        frame_bytes = reconhecimento.base64_para_bytes(data_url)
        status, dados = reconhecimento.reconhecer_rosto(frame_bytes)

        if status == 'encontrado':
            pessoa, similaridade = dados
            foto_url = request.build_absolute_uri(pessoa.foto.url) if pessoa.foto else ''
            return JsonResponse({
                'status': 'encontrado',
                'nome': pessoa.nome,
                'cpf': pessoa.cpf,
                'foto_url': foto_url,
                'similaridade': float(similaridade),
            })
        elif status == 'sem_rosto':
            return JsonResponse({'status': 'sem_rosto', 'mensagem': 'Nenhum rosto detectado no frame.'})
        elif status == 'sem_modelo':
            return JsonResponse({'status': 'erro', 'mensagem': 'Modelo não treinado. Cadastre ao menos uma pessoa.'})
        else:
            return JsonResponse({'status': 'nao_encontrado', 'mensagem': 'Rosto não reconhecido.'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'mensagem': str(e)})

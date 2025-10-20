from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Aluno


def lista_alunos(request):
    q = (request.GET.get('q') or '').strip()
    alunos = Aluno.objects.order_by('-criado_em')
    if q:
        alunos = alunos.filter(nome__icontains=q)
    return render(request, 'lista.html', {'alunos': alunos, 'q': q})


@require_http_methods(['GET', 'POST'])
def novo_aluno(request):
    if request.method == 'GET':
        return render(request, 'aluno_form.html', {
            'aluno': None,
            'nome': '',
            'matricula': '',
        })

    nome = (request.POST.get('nome') or '').strip()
    matricula = (request.POST.get('matricula') or '').strip()

    if not nome or not matricula:
        return render(request, 'aluno_form.html', {
            'aluno': None,
            'erro': 'Preencha nome e matrícula.',
            'nome': nome,
            'matricula': matricula,
        })

    if Aluno.objects.filter(matricula__iexact=matricula).exists():
        return render(request, 'aluno_form.html', {
            'aluno': None,
            'erro': 'Matrícula já cadastrada.',
            'nome': nome,
            'matricula': matricula,
        })

    Aluno.objects.create(nome=nome, matricula=matricula)
    messages.success(request, 'Aluno cadastrado com sucesso.')
    return redirect('lista_alunos')


def detalhe_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    return render(request, 'aluno_detalhe.html', {'aluno': aluno})


@require_http_methods(['GET', 'POST'])
def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)

    if request.method == 'GET':
        return render(request, 'aluno_form.html', {'aluno': aluno})

    nome = (request.POST.get('nome') or '').strip()
    matricula = (request.POST.get('matricula') or '').strip()

    if not nome or not matricula:
        return render(request, 'aluno_form.html', {
            'aluno': aluno,
            'erro': 'Preencha nome e matrícula.',
            'nome': nome,
            'matricula': matricula,
        })

    if Aluno.objects.filter(matricula__iexact=matricula).exclude(id=aluno.id).exists():
        return render(request, 'aluno_form.html', {
            'aluno': aluno,
            'erro': 'Matrícula já cadastrada em outro aluno.',
            'nome': nome,
            'matricula': matricula,
        })

    aluno.nome = nome
    aluno.matricula = matricula
    aluno.save()
    messages.success(request, 'Aluno atualizado com sucesso.')
    return redirect('lista_alunos')


@require_http_methods(['GET', 'POST'])
def excluir_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso.')
        return redirect('lista_alunos')
    return render(request, 'aluno_confirm_delete.html', {'aluno': aluno})

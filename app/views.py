from django.shortcuts import render
from .models import Aluno

def lista_alunos(request):
    alunos = Aluno.objects.order_by('-criado_em')
    return render(request, 'lista.html', {'alunos': alunos})
from django.shortcuts import render

# Create your views here.

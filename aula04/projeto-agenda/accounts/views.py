from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    
    user = auth.authenticate(request, username=usuario, password=senha)
    
    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        return redirect('dashboard')
    

   


def logout(request):
    auth.logout(request)
    return redirect('login')


def signup(request):
    if request.method != 'POST':
        return render(request, 'accounts/signup.html')
    
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario \
        or not senha or not senha2:
            
        messages.error(request, 'Nenhum campo estar vazio')
        return render(request, 'accounts/signup.html')
     
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido.')
        return render(request, 'accounts/signup.html')
    
    if len(senha) < 6:
        messages.error(request, 'Senha deve conter pelo menos 6 caracteres.')
        return render(request, 'accounts/signup.html')
    
    if senha != senha2:
        messages.error(request, 'Senhas devem ser iguais')
        return render(request, 'accounts/signup.html')
    
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Nome de usuário não disponível')
        return render(request, 'accounts/signup.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail não disponível')
        return render(request, 'accounts/signup.html')
    
    messages.error(request, 'Registrado com sucesso!')
    
    user = User.objects.create_user(username=usuario, email=email, 
                                    password=senha, first_name=nome, 
                                    last_name=sobrenome)
  
    user.save()
    
    return redirect('login')
    
@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

 # Exemplo de validação do django
    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    
# Exemplo de validação manual
    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais que 5 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')
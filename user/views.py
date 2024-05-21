from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from user.forms import UserForm, UserLoginForm
from .authenticate import *
from .serializer import UserSerializer
from .repositories import UserRepository
from .exception import UserException

class UserTokenizer(View):
    # método deveria ser POST pois deverá receber usuário e senha   
    def get(self, request):
        user = authenticate(username="user", password="a1b2c3")
        if user:
            return HttpResponse(generate_token(user))
        return HttpResponse("Username and/or password incorret")
    

class UserView(View):
    def get(self, request):
        repository = UserRepository(collectionName='users')
        try:
            users = list(repository.getAll())
            serializer = UserSerializer(data=users, many=True)
            if (serializer.is_valid()):
                ModelUser = serializer.save()
                objectReturn = {"weathers":ModelUser}
            else:
                objectReturn = {"error":serializer.errors}
        except UserException as e:
            objectReturn = {"error":e.message}
        
        return render(request, "home_user.html", objectReturn)
    
class UserLogin(View):

    def get(self, request):
        userLoginForm = UserLoginForm()
        return render(request, "login_user.html", {"form": userLoginForm})
    
    def post(self, request):
        repository = UserRepository(collectionName='users')
        try:
            users = list(repository.getAll())
            serializer = UserSerializer(data=users, many=True)
            if serializer.is_valid():
                username_exists = False
                for user_data in serializer.data:
                    if user_data['username'] == serializer:  # Substitua 'desired_username' pelo nome de usuário que você está verificando
                        username_exists = True
                        break

                if username_exists:
                    # Redirecionar para a view de visualização do clima
                    return redirect('Weather View')
                else:
                    # Redirecionar para a página de login
                    return redirect('User Login')
            else:
                objectReturn = {"error": serializer.errors}
        except UserException as e:
            objectReturn = {"error": e.message}

        return redirect('Weather View')
    
class UserCreate(View):
    def get(self, request):
        userForm = UserForm()

        return render(request, "form_user.html", {"form": userForm})
    
    def post(self, request):
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            serializer = UserSerializer(data=userForm.data)
            if serializer.is_valid():
                repository = UserRepository(collectionName='users')
                repository.insert(serializer.data)
            else:
                print(serializer.errors)
        else:
            print(userForm.errors)

        return redirect('User Login')
    
    
class UserDelete(View):

    def get(self, request, id):
        # Obter o repositório de clima
        repository = UserRepository(collectionName='users')
        # Excluir o registro de clima com o ID fornecido
        repository.deleteById(id)
        # Redirecionar de volta para a página principal
        return redirect('User View')
    
    
class UserEdit(View):

    def get(self, request, id):
        repository = UserRepository(collectionName='users')
        user = repository.getByID(id)
        userForm = UserForm(initial=user)
        return render(request, "form_user.html", {"form":userForm, "id": id})
    
    def post(self, request, id):
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            serializer = UserSerializer(data=userForm.data)
            serializer.id = id
            if (serializer.is_valid()):
                repository = UserRepository(collectionName='users')
                repository.update(serializer.data, id)
            else:
                print(serializer.errors)
        else:
            print(userForm.errors)

        return redirect('Weather View')

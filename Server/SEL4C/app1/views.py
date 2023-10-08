from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
import csv
from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from SEL4C.app1.serializers import UserSerializer, GroupSerializer
from .models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import hashlib as h
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

def home(request):
    return render(request, "app1/homepage.html")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre','').strip()
        grado = request.POST.get('grado','')
        disciplina = request.POST.get('disciplina','').strip()
        pais = request.POST.get('pais','').strip()
        genero = request.POST.get('genero','').strip()
        correo = request.POST.get('correo','').strip()
        username = request.POST.get('username','').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = Usuario.objects.create_user(nombre=nombre, grado=grado, disciplina=disciplina, pais=pais, genero=genero, correo=correo, username=username, password=password)
            return JsonResponse({'message':'Usuario creado exitosamente'})
        except Exception as e:
            return JsonResponse({'message':'No se pudo crear el usuario'})

    return JsonResponse({'message':'El registro requiere una POST request'})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('correo','').strip()
        password = request.POST.get('password','').strip()
        h_password = h.sha256(password.encode()).hexdigest()

        user = authenticate(request, email=email, password=h_password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Correo o contraseña inválidos')
    
    return render(request, "app1/login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('http://localhost:8000/SEL4C/')

@login_required(login_url='login')
def dashboard(request):
    return render(request, "app1/index.html")

@login_required(login_url='login')
def usersList(request):
    users = list(Usuario.objects.all())
    ctx = {'users': users}
    return render(request, "app1/users-list.html", ctx)

@login_required(login_url='login')
def userDetails(request, pk):
    usuario = Usuario.objects.get(id = pk)
    questions = list(Pregunta.objects.all())
    autodiagnosticos = list(Autodiagnostico.objects.filter(usuario=usuario))
    ctx = {'usuario':usuario, 'questions':questions, 'autodiagnosticos':autodiagnosticos}
    return render(request, "app1/user-details.html", ctx)

@login_required(login_url='login')
def buttons(request):
    return render(request, "app1/ui-buttons.html")

@login_required(login_url='login')
def cards(request):
    return render(request, "app1/ui-card.html")

@login_required(login_url='login')
def institute_view(request):
    institutes = list(Institucion.objects.all())
    ctx = {'Instituciones': institutes}
    return render(request, "app1/institutions.html", ctx)

@login_required(login_url='login')
def register_institution(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']

        try:
            institution = Institucion.objects.create(nombre=nombre)
            messages.success(request, 'Institución registrada con éxito')
        except Exception as e:
            messages.error(request, 'No fue posible registrar la institución' + str(e))
        
        return redirect('institutions')

    return render(request, "app1/register-institutions.html")

@login_required(login_url='login')
def delete_institution(request, id):
    institution = get_object_or_404(Institucion, pk=id)
    print(institution)

    if request.method == 'POST':
        try:
            institution.delete()
            messages.success(request, 'Institucion borrada con éxito')
        except Exception as e:
            messages.error(request, 'No fue posible borrar la institución' + str(e))
    
    return redirect('institutions')

# Esta  es la funcion para que lea el archivo 
@method_decorator(csrf_exempt, name='dispatch')
class ImportarDatosCSV(View):
    def post(self, request):
        ruta_archivo_csv = request.POST.get('ruta_archivo_csv', '')
        if not ruta_archivo_csv:
            return JsonResponse({'error': 'Ruta del archivo CSV no proporcionada'}, status=400)
        try:
            with open(ruta_archivo_csv, 'r', encoding='latin-1') as archivo_csv:
                csv_reader = csv.DictReader(archivo_csv)
                for row in csv_reader:
                    nombre_pais = row['nombre']
                    Pais.objects.get_or_create(nombre=nombre_pais)
            return JsonResponse({'message': 'Importación exitosa'})
        except FileNotFoundError:
            return JsonResponse({'error': 'El archivo CSV no fue encontrado'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset  = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class PaisViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class InstitucionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProgresoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Progreso.objects.all()
    serializer_class = ProgresoSerializer

class ActividadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

class EntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer

class PreguntaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class AutodiagnosticoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Autodiagnostico.objects.all()
    serializer_class = AutodiagnosticoSerializer

class RespuestaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer

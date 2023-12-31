from django.shortcuts import render, redirect, get_object_or_404
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Q
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.files.storage import FileSystemStorage
import os
from .serializers import *
from django.utils.decorators import method_decorator
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import hashlib as h
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Sum
import requests

def home(request):
    return render(request, "app1/homepage.html")

@csrf_exempt
def user_login_view(request):
    original_auth_backends = settings.AUTHENTICATION_BACKENDS
    settings.AUTHENTICATION_BACKENDS = ['SEL4C.app1.backends.CustomUserBackend']

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username','').strip()
        password = data.get('password','').strip()
        h_password = h.sha256(password.encode()).hexdigest()


        Usuario = authenticate(request, username=username, password=h_password)

        if Usuario is not None:
            response = requests.get('http://localhost:8000/Usuarios/' + str(Usuario.id))
            if response.status_code == 200:
                user_data = response.json()
                user_id = Usuario.id
                settings.AUTHENTICATION_BACKENDS = original_auth_backends
                return JsonResponse({'message':'Login exitoso', 'id':user_id})  
            else:
                settings.AUTHENTICATION_BACKENDS = original_auth_backends

                return JsonResponse({'message':'Error al obtener el usuario', 'id':0})
        else:
            settings.AUTHENTICATION_BACKENDS = original_auth_backends
            return JsonResponse({'message':'Usuario o contraseña inválidos', 'id':0})

    return JsonResponse({'message':'El login requiere una POST request'})

def login_view(request) :
    if request.method == 'POST':
        email = request.POST.get('correo','').strip()
        password = request.POST.get('password','').strip()
        h_password = h.sha256(password.encode()).hexdigest()
    
        user = authenticate(request, email=email, password=h_password)

        if user is not None:
            login(request, user)
            return render(request, 'app1/index.html')
        else:
            messages.error(request, 'Correo o contraseña inválidos')       
    
    return render(request, "app1/login.html")

def logout_view(request):
    logout(request)
    return redirect('http://0.0.0.0:8000/SEL4C/')

@login_required(login_url='login')
def dashboard(request):
    return render(request, "app1/index.html")

#@login_required(login_url='login')
def usersList(request):
    # Obtén los datos de la API de actividades
    response = ActividadesCompletadasPorUsuario.as_view()(request)
    data = response.data  # Esto contiene los datos de actividades completadas

    users = Usuario.objects.all()

    # Combina los datos de usuarios con los datos de actividades
    for user in users:
        for item in data:
            if user.id == item['usuario']:
                user.actividades_completadas = item['actividades_completadas']
                break

    ctx = {'users': users}
    return render(request, "app1/users-list.html", ctx)

#@login_required(login_url='login')
def userDetails(request, pk):
    usuario = Usuario.objects.get(id=pk)
    questions = list(Pregunta.objects.all())
    autodiagnosticos = Autodiagnostico.objects.filter(usuario=usuario)
    progreso = Progreso.objects.filter(usuario=usuario)
    # AUTODIAGNOSTICO INICIAL
    autoIniAuto = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Autocontrol')
    autoIniLider = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Liderazgo')
    autoIniCon = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Conciencia y Valor Social')
    autoIniInn = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Innovación Social y Sostenibilidad Financiera')
    # Suma las respuestas de la competencia "Autocontrol" para el usuario
    suma_autocontrolini = autoIniAuto.aggregate(total_autocontrolini=Sum('respuesta__respuesta'))['total_autocontrolini'] or 0
    suma_liderazgoini = autoIniLider.aggregate(total_liderazgoini=Sum('respuesta__respuesta'))['total_liderazgoini'] or 0
    suma_concienciaini = autoIniCon.aggregate(total_concienciaini=Sum('respuesta__respuesta'))['total_concienciaini'] or 0
    suma_innovacionini = autoIniInn.aggregate(total_innovacionini=Sum('respuesta__respuesta'))['total_innovacionini'] or 0
    # AUTODIAGNOSTICO FINAL
    autoFinAuto = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Autocontrol')
    autoFinLider = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Liderazgo')
    autoFinCon = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Conciencia y Valor Social')
    autoFinInn = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Innovación Social y Sostenibilidad Financiera')
    # Suma las respuestas de la competencia "Autocontrol" para el usuario
    suma_autocontrolfin = autoFinAuto.aggregate(total_autocontrolfin=Sum('respuesta__respuesta'))['total_autocontrolfin'] or 0
    suma_liderazgofin = autoFinLider.aggregate(total_liderazgofin=Sum('respuesta__respuesta'))['total_liderazgofin'] or 0
    suma_concienciafin = autoFinCon.aggregate(total_concienciafin=Sum('respuesta__respuesta'))['total_concienciafin'] or 0
    suma_innovacionfin = autoFinInn.aggregate(total_innovacionfin=Sum('respuesta__respuesta'))['total_innovacionfin'] or 0
    
    ctx = {
        'usuario': usuario,
        'questions': questions,
        'autodiagnosticos': autodiagnosticos,
        'suma_autocontrolini': suma_autocontrolini,
        'suma_liderazgoini': suma_liderazgoini,
        'suma_concienciaini': suma_concienciaini,
        'suma_innovacionini': suma_innovacionini,
        'suma_autocontrolfin': suma_autocontrolfin,
        'suma_liderazgofin': suma_liderazgofin,
        'suma_concienciafin': suma_concienciafin,
        'suma_innovacionfin': suma_innovacionfin,
        'progreso': progreso,
    }
    
    return render(request, "app1/user-details.html", ctx)

#@login_required(login_url='login')
def buttons(request):
    return render(request, "app1/ui-buttons.html")

#@login_required(login_url='login')
def cards(request):
    return render(request, "app1/ui-card.html")

# Función de prueba POST para crear usuarios desde la app con país e institución 
@csrf_exempt
def crearUsuarioApp(request):
    if request.method == 'POST':
        # Obtener los datos JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        
        pais_id = data.get('pais')
        institucion_id = data.get('institucion')
        
        try:
            pais = Pais.objects.get(id=pais_id)
            institucion = Institucion.objects.get(id=institucion_id)
            
            # Crear un nuevo usuario con la institución relacionada
            usuario = Usuario(
                nombre=data.get('nombre'),
                genero=data.get('genero'),
                grado=data.get('grado'),
                disciplina=data.get('disciplina'),
                pais=pais,
                institucion=institucion,
                correo=data.get('correo'),
                username=data.get('username'),
                password=h.sha256((data.get('password')).encode()).hexdigest()
            )
            
            usuario.save()
            
            return JsonResponse({'mensaje': 'Usuario creado exitosamente'})
        except Institucion.DoesNotExist:
            return JsonResponse({'error': 'La institución con el ID proporcionado no existe'}, status=400)
    else:
        return JsonResponse({'error': 'Solicitud no permitida'}, status=405)
# Función para mandar POST para los autodiagnosticos de los usuarios desde la app    
@csrf_exempt
def crearAutodiagnosticoApp(request):
    if request.method == 'POST':
        # Obtener los datos JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        
        usuario_id = data.get('usuario')
        pregunta_id = data.get('pregunta')
        respuesta_id = data.get('respuesta')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            pregunta = Pregunta.objects.get(id=pregunta_id)
            respuesta = Respuesta.objects.get(id=respuesta_id)
            
            # Crear un nuevo usuario con la institución relacionada
            autodiagnostico = Autodiagnostico(
                num_auto=data.get('num_auto'),
                usuario=usuario,
                pregunta=pregunta,
                respuesta=respuesta,
                competencia=data.get('competencia'),
                completada=data.get('completada')
            )
            
            autodiagnostico.save()
            
            return JsonResponse({'mensaje': 'Datos mandados exitosamente'})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'El usuario con el ID proporcionado no existe'}, status=400)
        except Pregunta.DoesNotExist:
            return JsonResponse({'error': 'La pregunta con el ID proporcionado no existe'}, status=400)
        except Respuesta.DoesNotExist:
            return JsonResponse({'error': 'La respuesta con el ID proporcionado no existe'}, status=400)
    else:
        return JsonResponse({'error': 'Solicitud no permitida'}, status=405)

# Función de desempeño en App
@csrf_exempt
def desempeñoApp(request, pk):
    if request.method == 'GET':
        try:
            usuario = Usuario.objects.get(id=pk)
            # AUTODIAGNOSTICO INICIAL
            autoIniAuto = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Autocontrol')
            autoIniLider = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Liderazgo')
            autoIniCon = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Conciencia y Valor Social')
            autoIniInn = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Innovación Social y Sostenibilidad Financiera')
            autoIniSis = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Pensamiento sistémico')
            autoIniCien = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Pensamiento científico')
            autoIniCrit = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Pensamiento crítico')
            autoIniInno = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Pensamiento innovador')
            # Suma las respuestas de la competencia "Autocontrol" para el usuario
            suma_autocontrolini = autoIniAuto.aggregate(total_autocontrolini=Sum('respuesta__respuesta'))['total_autocontrolini'] or 0
            suma_liderazgoini = autoIniLider.aggregate(total_liderazgoini=Sum('respuesta__respuesta'))['total_liderazgoini'] or 0
            suma_concienciaini = autoIniCon.aggregate(total_concienciaini=Sum('respuesta__respuesta'))['total_concienciaini'] or 0
            suma_innovacionini = autoIniInn.aggregate(total_innovacionini=Sum('respuesta__respuesta'))['total_innovacionini'] or 0
            suma_sistemicoini = autoIniSis.aggregate(total_sistemicoini=Sum('respuesta__respuesta'))['total_sistemicoini'] or 0
            suma_cientificoini = autoIniCien.aggregate(total_cientificoini=Sum('respuesta__respuesta'))['total_cientificoini'] or 0
            suma_criticoini = autoIniCrit.aggregate(total_criticoini=Sum('respuesta__respuesta'))['total_criticoini'] or 0
            suma_innovadorini = autoIniInno.aggregate(total_innovadorini=Sum('respuesta__respuesta'))['total_innovadorini'] or 0
            # AUTODIAGNOSTICO FINAL
            autoFinAuto = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Autocontrol')
            autoFinLider = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Liderazgo')
            autoFinCon = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Conciencia y Valor Social')
            autoFinInn = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Innovación Social y Sostenibilidad Financiera')
            autoFinSis = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Pensamiento sistémico')
            autoFinCien = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Pensamiento científico')
            autoFinCrit = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Pensamiento crítico')
            autoFinInno = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Pensamiento innovador')
            # Suma las respuestas de la competencia "Autocontrol" para el usuario
            suma_autocontrolfin = autoFinAuto.aggregate(total_autocontrolfin=Sum('respuesta__respuesta'))['total_autocontrolfin'] or 0
            suma_liderazgofin = autoFinLider.aggregate(total_liderazgofin=Sum('respuesta__respuesta'))['total_liderazgofin'] or 0
            suma_concienciafin = autoFinCon.aggregate(total_concienciafin=Sum('respuesta__respuesta'))['total_concienciafin'] or 0
            suma_innovacionfin = autoFinInn.aggregate(total_innovacionfin=Sum('respuesta__respuesta'))['total_innovacionfin'] or 0
            suma_sistemicofin = autoFinSis.aggregate(total_sistemicofin=Sum('respuesta__respuesta'))['total_sistemicofin'] or 0
            suma_cientificofin = autoFinCien.aggregate(total_cientificofin=Sum('respuesta__respuesta'))['total_cientificofin'] or 0
            suma_criticofin = autoFinCrit.aggregate(total_criticofin=Sum('respuesta__respuesta'))['total_criticofin'] or 0
            suma_innovadorfin = autoFinInno.aggregate(total_innovadorfin=Sum('respuesta__respuesta'))['total_innovadorfin'] or 0
            
            def format_number(value):
                rounded_value = round(value)
                formatted_value = "{:03d}".format(rounded_value)
                return formatted_value

            ctx = {
                'autocontrolini': format_number((suma_autocontrolini * 100) / 20),
                'liderazgoini': format_number((suma_liderazgoini * 100) / 30),
                'concienciaini': format_number((suma_concienciaini * 100) / 35),
                'innovacionini': format_number((suma_innovacionini * 100) / 35),
                'sistemicoini': format_number((suma_sistemicoini * 100) / 30),
                'cientificoini': format_number((suma_cientificoini * 100) / 35),
                'criticoini': format_number((suma_criticoini * 100) / 30),
                'innovadorini': format_number((suma_innovadorini * 100) / 30),

                'autocontrolfin': format_number((suma_autocontrolfin * 100) / 20),
                'liderazgofin': format_number((suma_liderazgofin * 100) / 30),
                'concienciafin': format_number((suma_concienciafin * 100) / 35),
                'innovacionfin': format_number((suma_innovacionfin * 100) / 35),
                'sistemicofin': format_number((suma_sistemicofin * 100) / 30),
                'cientificofin': format_number((suma_cientificofin * 100) / 35),
                'criticofin': format_number((suma_criticofin * 100) / 30),
                'innovadorfin': format_number((suma_innovadorfin * 100) / 30),
            }
            
            return JsonResponse(ctx)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'El usuario con el ID proporcionado no existe'}, status=400)

    else:
        return JsonResponse({'error': 'Solicitud no permitida'}, status=405)

#@login_required(login_url='login')
def institute_view(request):
    institutes = list(Institucion.objects.all())
    ctx = {'Instituciones': institutes}
    return render(request, "app1/institutions.html", ctx)

#@login_required(login_url='login')
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

#@login_required(login_url='login')
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
        
class SubcompetenciasAPI(APIView):
    def get(self, request, format=None):
        # Calcular el conteo de respuestas para cada subcompetencia
        autocontrol_count = Autodiagnostico.objects.filter(
            Q(pregunta__id__range=(1, 4)) & Q(respuesta__id__in=[4, 5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=2).count()

        liderazgo_count = Autodiagnostico.objects.filter(
            Q(pregunta__id__range=(5, 10)) & Q(respuesta__id__in=[4, 5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=4).count()

        conciencia_valor_social_count = Autodiagnostico.objects.filter(
            (Q(pregunta__id__range=(11, 17)) | Q(pregunta__id__range=(18, 24))) & Q(respuesta__id__in=[4, 5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=4).count()

        innovacion_social_count = Autodiagnostico.objects.filter(
            Q(pregunta__id__range=(18,24)) & Q(respuesta__id__in=[4,5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=4).count()

        # Construir la respuesta con los conteos de cada subcompetencia
        response_data = {
            'autocontrol': autocontrol_count,
            'liderazgo': liderazgo_count,
            'conciencia_valor_social': conciencia_valor_social_count,
            'innovacion_social': innovacion_social_count
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
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


class ComprobarActividadCompletada(viewsets.ModelViewSet):
    def get(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            #actividad = Actividad.objects.get(id=actividad_id)
            actividades = Actividad.objects.all()
            completado = Progreso.objects.filter(usuario=usuario).exists()
            data = {'id_actividad': actividades,
                'completado': completado,}
            
            completado_por_actividad = []
            
            for actividad in actividades:
                completado = Progreso.objects.filter(usuario=usuario, actividad=actividad).exists()
                actividad_json = {
                    "id": actividad.id,
                    "completado": completado
                }
                completado_por_actividad.append(actividad_json)

            return JsonResponse(completado_por_actividad, safe=False)
        
        except Usuario.DoesNotExist or Actividad.DoesNotExist:
            return Response({'error': 'Usuario o actividad no encontrados'}, status=400)


class ComprobarAutodiagnósticoCompletado(viewsets.ModelViewSet):
    def get(self, request, usuario_id, autodiagnostico_id):
        try:

            usuario = Usuario.objects.get(id=usuario_id)
            #autodiagnostico_objetoid = Autodiagnostico.objects.get(num_auto=autodiagnostico_id)
            num_autodiagnostico = autodiagnostico_id
            print(num_autodiagnostico)
            print(usuario)
            
            pregunta_completada1 = Autodiagnostico.objects.filter(
                num_auto = num_autodiagnostico,
                usuario=usuario,
                pregunta=24,
                completada=True
            ).exists()
            print(pregunta_completada1)

            pregunta_completada2 = Autodiagnostico.objects.filter(
                num_auto = num_autodiagnostico+1,
                usuario=usuario,
                pregunta=49,
                completada=True
            ).exists()
            print(pregunta_completada2)

            completado_por_auto = []

            data = {
                
                'usuario_id':usuario.id,
                'preguntaFinalCompletada': pregunta_completada1,
                
            }
            data2 = {
                'usuario_id':usuario.id,
                'preguntaFinalCompletada': pregunta_completada2,
            }
            completado_por_auto.append(data)
            completado_por_auto.append(data2)

            return JsonResponse(completado_por_auto, safe=False)
        
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        

class GetPerfil(viewsets.ModelViewSet):
    def get(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            #usuario = Usuario.objects.filter(id=usuario_id)

            nombre = usuario.nombre
            correo = usuario.correo
            username = usuario.username

            data = {
                'nombre': nombre,
                'correo': correo,
                'username': username,
                }
            
            perfil = []
            
            
            perfil.append(data)

            return JsonResponse(perfil, safe=False)
        
        except Usuario.DoesNotExist or Actividad.DoesNotExist:
            return Response({'error': 'Usuario o actividad no encontrados'}, status=400)
        
# Función para usuario progresos 
@csrf_exempt
def crearProgreso(request):
    if request.method == 'POST' and request.FILES['file']:
        usuario =(request.POST['usuario'])
        actividad=(request.POST['actividad'])
        filename =(request.POST['filename'])
        file =request.FILES['file']
        completado =(request.POST['completado'])
        fs = FileSystemStorage()
        path = os.path.join(fs.location, usuario,actividad, filename, file.name)
        filename = fs.save(path, file)
        uploaded_file_url = fs.url(filename)
       
        try:
            usuario = Usuario.objects.get(id=usuario)
            actividad = Actividad.objects.get(id=actividad)

            progreso = Progreso(
                usuario = usuario,
                actividad = actividad,
                filename = filename,
                file = file,
                completado = completado
            )
            
            progreso.save()
            
            return JsonResponse({'mensaje': 'Progreso creado exitosamente'})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'El Usuario proporcionado no existe'}, status=400)
        except Actividad.DoesNotExist:
            return JsonResponse({'error': 'La actividad proporcionada no existe'}, status=400)
    else:
        return JsonResponse({'error': 'Solicitud no permitida'}, status=405)
    
class ActividadesCompletadasPorUsuario(APIView):
    def get(self, request):
        users = Usuario.objects.all()
        response_data = []

        for user in users:
            actividades_completadas = Progreso.objects.filter(usuario=user, completado=True).count()
            data = {'usuario': user.id, 'actividades_completadas': actividades_completadas}
            response_data.append(data)

        return Response(response_data)
    
class perfilUpdateEditar(APIView):
    @csrf_exempt
    def put(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)

            # Obtén los datos del cuerpo de la solicitud (request body)
            nombre = request.data.get('nombre')
            correo = request.data.get('correo')
            username = request.data.get('username')

            if nombre is not None:
                usuario.nombre = nombre
            if correo is not None:
                usuario.correo = correo
            if username is not None:
                usuario.username = username

            usuario.save()  # Guarda la instancia actualizada en la base de datos

            return Response({'message': 'Perfil actualizado correctamente'}, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
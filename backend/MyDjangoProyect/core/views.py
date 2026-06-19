from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Peluqueria, Usuario, Estilista, Servicio, Cita, HorarioEstilista
from .serializers import (
    PeluqueriaSerializer,
    UsuarioSerializer,
    EstilistaSerializer,
    ServicioSerializer,
    CitaSerializer,
    HorarioEstilistaSerializer,
)

# NOTA: En desarrollo, todos los endpoints son públicos sin autenticación
# CAMBIAR A IsAuthenticated EN PRODUCCIÓN

class PeluqueriaViewSet(viewsets.ModelViewSet):
    queryset = Peluqueria.objects.all().order_by('nombre')
    serializer_class = PeluqueriaSerializer
    permission_classes = [AllowAny]  # DESARROLLO


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('nombre')
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]  # DESARROLLO


class EstilistaViewSet(viewsets.ModelViewSet):
    queryset = Estilista.objects.all().order_by('nombre')
    serializer_class = EstilistaSerializer
    permission_classes = [AllowAny]  # DESARROLLO


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all().order_by('nombre')
    serializer_class = ServicioSerializer
    permission_classes = [AllowAny]  # DESARROLLO


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().order_by('-fecha', 'hora_inicio')
    serializer_class = CitaSerializer
    permission_classes = [AllowAny]  # DESARROLLO


class HorarioEstilistaViewSet(viewsets.ModelViewSet):
    queryset = HorarioEstilista.objects.all().order_by('stylist', 'dia_semana')
    serializer_class = HorarioEstilistaSerializer
    permission_classes = [AllowAny]  # DESARROLLO


@api_view(['GET'])
@permission_classes([AllowAny])  # DESARROLLO
def nested_dashboard_data(request):
    estilistas = (
        Estilista.objects.select_related('hair_salon')
        .prefetch_related('horarios')
        .order_by('id')
    )
    clientes = (
        Usuario.objects.filter(rol='cliente')
        .prefetch_related('citas__service', 'citas__stylist__hair_salon')
        .order_by('id')
    )

    payload = []

    for estilista in estilistas:
        payload.append({
            'usuario_id': estilista.id,
            'nombre_completo': estilista.nombre,
            'correo_electronico': f"{slugify(estilista.nombre)}@bellaestetica.com",
            'telefono': estilista.telefono,
            'rol': 'estilista',
            'estado_cuenta': estilista.status,
            'perfil_estilista': {
                'especialidad': estilista.especialidad,
                'peluquereria_asignada': {
                    'nombre_comercial': estilista.hair_salon.nombre,
                    'telefono_contacto': estilista.hair_salon.telefono,
                    'direccion_fisica': estilista.hair_salon.direccion,
                    'descripcion': estilista.hair_salon.descripcion,
                },
                'horarios_atencion': [
                    {
                        'dia_semana': horario.dia_semana,
                        'hora_inicio': horario.hora_inicio.isoformat(),
                        'hora_fin': horario.hora_fin.isoformat(),
                        'activo': horario.activo,
                    }
                    for horario in estilista.horarios.all()
                ],
            },
        })

    for usuario in clientes:
        payload.append({
            'usuario_id': usuario.id,
            'nombre_completo': usuario.nombre,
            'correo_electronico': usuario.email,
            'telefono': usuario.telefono,
            'rol': usuario.rol,
            'estado_cuenta': usuario.status,
            'historial_citas': [
                {
                    'fecha_reserva': cita.fecha.isoformat(),
                    'hora_inicio': cita.hora_inicio.isoformat(),
                    'hora_fin': cita.hora_fin.isoformat(),
                    'estado_cita': cita.estado,
                    'lugar_cita': {
                        'nombre_comercial': cita.stylist.hair_salon.nombre,
                        'direccion_fisica': cita.stylist.hair_salon.direccion,
                    },
                    'servicio_solicitado': {
                        'nombre_servicio': cita.service.nombre,
                        'descripcion': cita.service.descripcion,
                        'costo': float(cita.service.precio),
                        'duracion_minutos': cita.service.duracion_minutos,
                    },
                    'profesional_asignado': {
                        'nombre': cita.stylist.nombre,
                        'especialidad': cita.stylist.especialidad,
                    },
                }
                for cita in usuario.citas.all()
            ],
        })

    return Response(payload)

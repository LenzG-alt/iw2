from rest_framework import serializers

from .models import Peluqueria, Usuario, Estilista, Servicio, Cita, HorarioEstilista


class PeluqueriaSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Peluqueria
        fields = ['id', 'nombre', 'direccion', 'telefono', 'descripcion', 'status']


class UsuarioSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'rol', 'status']


class EstilistaSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Estilista
        fields = ['id', 'nombre', 'telefono', 'especialidad', 'status']


class ServicioSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio', 'duracion_minutos', 'status']


class PeluqueriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peluqueria
        fields = ['id', 'nombre', 'direccion', 'telefono', 'descripcion', 'fecha_registro', 'status']
        read_only_fields = ['id', 'fecha_registro']


class UsuarioSerializer(serializers.ModelSerializer):
    citas = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'contraseña', 'telefono', 'rol', 'fecha_registro', 'status', 'citas']
        read_only_fields = ['id', 'fecha_registro']
        extra_kwargs = {'contraseña': {'write_only': True}}

    def get_citas(self, obj):
        from .serializers import CitaSerializer
        return CitaSerializer(obj.citas.all(), many=True).data


class EstilistaSerializer(serializers.ModelSerializer):
    hair_salon = PeluqueriaSummarySerializer(read_only=True)
    horarios = serializers.SerializerMethodField()

    class Meta:
        model = Estilista
        fields = ['id', 'nombre', 'telefono', 'especialidad', 'hair_salon', 'horarios', 'status']
        read_only_fields = ['id']

    def get_horarios(self, obj):
        return HorarioEstilistaSerializer(obj.horarios.all(), many=True).data


class ServicioSerializer(serializers.ModelSerializer):
    hair_salon = PeluqueriaSummarySerializer(read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio', 'duracion_minutos', 'hair_salon', 'status']
        read_only_fields = ['id']


class CitaSerializer(serializers.ModelSerializer):
    user = UsuarioSummarySerializer(read_only=True)
    stylist = EstilistaSummarySerializer(read_only=True)
    service = ServicioSummarySerializer(read_only=True)

    class Meta:
        model = Cita
        fields = [
            'id', 'user', 'stylist', 'service',
            'fecha', 'hora_inicio', 'hora_fin',
            'estado', 'observaciones', 'fecha_creacion', 'status',
        ]
        read_only_fields = ['id', 'fecha_creacion']


class HorarioEstilistaSerializer(serializers.ModelSerializer):
    stylist = EstilistaSummarySerializer(read_only=True)

    class Meta:
        model = HorarioEstilista
        fields = ['id', 'stylist', 'dia_semana', 'hora_inicio', 'hora_fin', 'activo', 'status']
        read_only_fields = ['id']

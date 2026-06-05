import os
import sys
from datetime import datetime, time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyDjangoProyect.settings')

import django

django.setup()

from MyWebApps.SAC.models import Cita, Estilista, HorarioEstilista, Peluqueria, Servicio, Usuario

print('🔄 Creando datos de ejemplo...')

Peluqueria.objects.all().delete()
Usuario.objects.all().delete()
Estilista.objects.all().delete()
Servicio.objects.all().delete()
Cita.objects.all().delete()
HorarioEstilista.objects.all().delete()

peluqueria = Peluqueria.objects.create(
    nombre='Bella Estética',
    telefono='987654321',
    direccion='Calle Principal 123',
    descripcion='Centro de belleza profesional',
    status='A',
)
print(f'✅ Peluquería: {peluqueria}')

admin = Usuario.objects.create(
    nombre='Admin',
    email='admin@bellaestetica.com',
    contraseña='admin123',
    rol='administrador',
    status='A',
)
print(f'✅ Usuario Admin: {admin}')

cliente1 = Usuario.objects.create(
    nombre='María García',
    email='maria@email.com',
    contraseña='pass123',
    telefono='987111111',
    rol='cliente',
    status='A',
)
print(f'✅ Cliente: {cliente1}')

cliente2 = Usuario.objects.create(
    nombre='Juan Pérez',
    email='juan@email.com',
    contraseña='pass123',
    telefono='987222222',
    rol='cliente',
    status='A',
)
print(f'✅ Cliente: {cliente2}')

estilista1 = Estilista.objects.create(
    nombre='Ana López',
    telefono='987123456',
    especialidad='Cortes y Tintes',
    hair_salon=peluqueria,
    status='A',
)
print(f'✅ Estilista: {estilista1}')

estilista2 = Estilista.objects.create(
    nombre='Rosa Martínez',
    telefono='987654000',
    especialidad='Peinados y Tratamientos',
    hair_salon=peluqueria,
    status='A',
)
print(f'✅ Estilista: {estilista2}')

servicio1 = Servicio.objects.create(
    nombre='Corte de cabello',
    descripcion='Corte profesional personalizado',
    precio=50.00,
    duracion_minutos=30,
    hair_salon=peluqueria,
    status='A',
)
print(f'✅ Servicio: {servicio1}')

servicio2 = Servicio.objects.create(
    nombre='Tintura',
    descripcion='Tintura profesional de calidad',
    precio=80.00,
    duracion_minutos=60,
    hair_salon=peluqueria,
    status='A',
)
print(f'✅ Servicio: {servicio2}')

servicio3 = Servicio.objects.create(
    nombre='Peinado',
    descripcion='Peinado de ocasión',
    precio=35.00,
    duracion_minutos=20,
    hair_salon=peluqueria,
    status='A',
)
print(f'✅ Servicio: {servicio3}')

HorarioEstilista.objects.create(
    stylist=estilista1,
    dia_semana='lunes',
    hora_inicio=time(9, 0),
    hora_fin=time(18, 0),
    activo=True,
    status='A',
)
HorarioEstilista.objects.create(
    stylist=estilista1,
    dia_semana='martes',
    hora_inicio=time(9, 0),
    hora_fin=time(18, 0),
    activo=True,
    status='A',
)
HorarioEstilista.objects.create(
    stylist=estilista2,
    dia_semana='lunes',
    hora_inicio=time(10, 0),
    hora_fin=time(19, 0),
    activo=True,
    status='A',
)

cita1 = Cita.objects.create(
    user=cliente1,
    stylist=estilista1,
    service=servicio1,
    fecha=datetime.now().date(),
    hora_inicio=time(10, 0),
    hora_fin=time(10, 30),
    estado='confirmada',
    status='A',
)
print(f'✅ Cita 1: {cita1} (estado={cita1.estado}, status={cita1.status})')

cita2 = Cita.objects.create(
    user=cliente2,
    stylist=estilista2,
    service=servicio2,
    fecha=datetime.now().date(),
    hora_inicio=time(11, 0),
    hora_fin=time(12, 0),
    estado='cancelada',
    status='A',
)
print(f'✅ Cita 2: {cita2} (estado={cita2.estado}, status={cita2.status})')

print('\n✨ ¡Datos de ejemplo creados exitosamente!')
print('📊 Total: 1 peluquería, 3 usuarios, 2 estilistas, 3 servicios, 3 horarios, 2 citas')

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cuestionario.models import Trabajador

class Command(BaseCommand):
    help = 'Crea y vincula usuarios de Django para trabajadores que no tienen uno'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando vinculación de usuarios...')
        
        # El código que te funcionó:
        trabajadores_sin_user = Trabajador.objects.filter(user__isnull=True)
        
        contador = 0
        for t in trabajadores_sin_user:
            # 1. Verificamos si el usuario ya existe para no duplicar
            user, created = User.objects.get_or_create(
                username=t.email,
                defaults={'email': t.email, 'first_name': t.nombre}
            )
            
            # 2. Le asignamos la contraseña correctamente (hasheada)
            user.set_password('Mohala2026')
            user.is_staff = True  
            user.save()
            
            # 3. Vinculamos el usuario al trabajador
            t.user = user
            t.save()
            
            # Usamos self.stdout.write en lugar de print para comandos de Django
            self.stdout.write(self.style.SUCCESS(f"✅ Usuario creado para: {t.email}"))
            contador += 1

        self.stdout.write(self.style.SUCCESS(f'--- Proceso finalizado. {contador} usuarios procesados ---'))
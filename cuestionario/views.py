from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Trabajador, TextosEvaluacion, Autoevaluacion

def index(request):
    trabajador_id = request.GET.get('id', 1)
    
    # Buscamos al trabajador
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    # Filtramos preguntas por su nivel
    preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico)
    
    # Obtenemos equipo si es jefe
    equipo = trabajador.subordinados.all()
    
    context = {
        'trabajador': trabajador,
        'preguntas': preguntas,
        'equipo': equipo,
        'es_jefe': trabajador.es_jefe,
    }
    
    return render(request, 'cuestionario/index.html', context)

def cuestionario_autoevaluacion(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    if request.method == 'POST':
        # Obtenemos las preguntas para saber qué IDs buscar en el POST
        preguntas_list = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico)
        
        for pregunta in preguntas_list:
            # El nombre del input en el HTML debe ser "puntaje_{{ p.id_textos_evaluacion }}"
            puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
            
            if puntaje_valor:
                # Creamos el registro en la tabla Autoevaluacion
                Autoevaluacion.objects.create(
                    puntaje=puntaje_valor,
                    fecha_evaluacion=timezone.now().date(),
                    momento_evaluacion=timezone.now(),
                    trabajador=trabajador,
                    codigo_excel=pregunta, 
                    comentario=request.POST.get('comentario', '')
                )
        
        return redirect(f'/?id={trabajador.id_trabajador}')

    preguntas = TextosEvaluacion.objects.filter(
        nivel_jerarquico=trabajador.nivel_jerarquico
    ).select_related('competencia').order_by('competencia__nombre_competencia')

    context = {
        'trabajador': trabajador,
        'preguntas': preguntas,
    }
    return render(request, 'cuestionario/autoevaluacion.html', context)
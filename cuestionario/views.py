from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Trabajador, TextosEvaluacion, Autoevaluacion, EvaluacionJefatura
from django.db import transaction

def index(request):
    trabajador_id = request.GET.get('id', 1)
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    # 1. VERIFICACIÓN DE AUTOEVALUACIÓN: Enviamos True si ya existe en la BD
    ya_hizo_autoevaluacion = Autoevaluacion.objects.filter(trabajador=trabajador).exists()
    
    preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico)
    
    # 2. VERIFICACIÓN DE EQUIPO: Marcamos a cada subordinado si ya fue evaluado
    equipo = trabajador.subordinados.all()
    for subordinado in equipo:
        subordinado.ya_evaluado = EvaluacionJefatura.objects.filter(
            evaluador=trabajador, 
            trabajador_evaluado=subordinado
        ).exists()
    
    context = {
        'trabajador': trabajador,
        'preguntas': preguntas,
        'equipo': equipo,
        'es_jefe': trabajador.subordinados.exists(),
        'ya_hizo_autoevaluacion': ya_hizo_autoevaluacion, # Esta variable activa el bloqueo en el HTML
    }
    
    return render(request, 'cuestionario/index.html', context)

def cuestionario_autoevaluacion(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    # BLOQUEO DE SEGURIDAD: Si intenta entrar por URL manual y ya existe, lo sacamos
    if Autoevaluacion.objects.filter(trabajador=trabajador).exists():
        return redirect(f'/?id={trabajador.id_trabajador}')
    
    if request.method == 'POST':
        preguntas_list = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico)
        
        # transaction.atomic asegura que se guarden todas las preguntas o ninguna (evita progreso a medias)
        with transaction.atomic():
            for pregunta in preguntas_list:
                puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
                if puntaje_valor:
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
    ).select_related('competencia').order_by('competencia__id_competencia')

    context = {
        'trabajador': trabajador,
        'preguntas': preguntas,
    }
    return render(request, 'cuestionario/autoevaluacion.html', context)

def cuestionario_jefatura(request, evaluador_id, evaluado_id):
    evaluador = get_object_or_404(Trabajador, id_trabajador=evaluador_id)
    evaluado = get_object_or_404(Trabajador, id_trabajador=evaluado_id)
    
    # BLOQUEO DE SEGURIDAD: Si el jefe ya evaluó a este trabajador, lo sacamos
    if EvaluacionJefatura.objects.filter(evaluador=evaluador, trabajador_evaluado=evaluado).exists():
        return redirect(f'/?id={evaluador.id_trabajador}')
    
    if request.method == 'POST':
        preguntas_list = TextosEvaluacion.objects.filter(nivel_jerarquico=evaluado.nivel_jerarquico)
        
        with transaction.atomic():
            for pregunta in preguntas_list:
                puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
                if puntaje_valor:
                    EvaluacionJefatura.objects.create(
                        puntaje=puntaje_valor,
                        evaluador=evaluador,
                        trabajador_evaluado=evaluado, 
                        codigo_excel=pregunta,
                        fecha_evaluacion=timezone.now().date(),
                        momento_evaluacion=timezone.now(),
                        comentario=request.POST.get('comentario', '')
                    )
        
        return redirect(f'/?id={evaluador.id_trabajador}')

    preguntas = TextosEvaluacion.objects.filter(
        nivel_jerarquico=evaluado.nivel_jerarquico
    ).select_related('competencia').order_by('competencia__id_competencia')

    context = {
        'evaluador': evaluador,
        'evaluado': evaluado,
        'preguntas': preguntas,
    }
    return render(request, 'cuestionario/evaluacion_jefe.html', context)
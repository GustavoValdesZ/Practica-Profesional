from django.shortcuts import render, get_object_or_404
from ..models import Trabajador, Autoevaluacion, EvaluacionJefatura

# =========================
# VISTA INDEX (DASHBOARD)
# =========================
def index(request):
    trabajador_id = request.GET.get('id', 1)
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    # Verifica si el usuario actual terminó su propia autoevaluación
    autoeval_completada = Autoevaluacion.objects.filter(
        trabajador=trabajador, 
        estado_finalizacion=True
    ).exists()
    
    equipo = trabajador.subordinados.all()
    
    # BUCLE DE PREPARACIÓN DE EQUIPO
    for sub in equipo:
        # Esto permite que el botón de jefatura se habilite/deshabilite en el HTML
        sub.autoevaluacion_terminada = Autoevaluacion.objects.filter(
            trabajador=sub, 
            estado_finalizacion=True
        ).exists()
        
        # Verifica si el jefe ya cerró la evaluación de este subordinado
        sub.ya_evaluado = EvaluacionJefatura.objects.filter(
            evaluador=trabajador, 
            trabajador_evaluado=sub,
            estado_finalizacion=True
        ).exists()

    context = {
        'trabajador': trabajador,
        'es_jefe': trabajador.subordinados.exists(),
        'equipo': equipo,
        'ya_hizo_autoevaluacion': autoeval_completada,
    }
    return render(request, 'cuestionario/index.html', context)

# =========================
# VISTA DE RESULTADOS
# =========================
def ver_resultados(request, trabajador_id, tipo_evaluacion):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    dimension_filtro = request.GET.get('dimension')

    if tipo_evaluacion == 'auto':
        respuestas = Autoevaluacion.objects.filter(trabajador=trabajador)
        visor_id = trabajador.id_trabajador
    else:
        evaluador_id = request.GET.get('evaluador_id')
        respuestas = EvaluacionJefatura.objects.filter(trabajador_evaluado=trabajador, evaluador_id=evaluador_id)
        visor_id = evaluador_id

    respuestas = respuestas.select_related('codigo_excel__competencia__dimension')

    if dimension_filtro:
        respuestas = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains=dimension_filtro)

    dimensiones_data = {}
    dimensiones_nombres = respuestas.values_list('codigo_excel__competencia__dimension__nombre_dimension', flat=True).distinct()
    
    for dim in dimensiones_nombres:
        dimensiones_data[dim] = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension=dim)

    context = {
        'trabajador': trabajador,
        'dimensiones': dimensiones_data,
        'comentario_final': respuestas.first().comentario if respuestas.exists() else "",
        'fecha_cierre': respuestas.first().momento_evaluacion if respuestas.exists() else None,
        'visor_id': visor_id,
        'tipo_evaluacion': tipo_evaluacion
    }
    return render(request, 'cuestionario/ver_resultados.html', context)
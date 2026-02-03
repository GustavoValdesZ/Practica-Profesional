from django.contrib import admin
from .models import (
    Dimension, NivelJerarquico, Cargo, Trabajador, 
    Competencia, TextosEvaluacion, Autoevaluacion, 
    EvaluacionJefatura, ResultadoConsolidado
)

# Registros simples
admin.site.register(Dimension)
admin.site.register(NivelJerarquico)
admin.site.register(Cargo)
admin.site.register(Trabajador)
admin.site.register(Competencia)

# Registro avanzado de Textos de Evaluación (Preguntas)
@admin.register(TextosEvaluacion)
class TextosEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('codigo_excel', 'get_dimension', 'competencia', 'nivel_jerarquico', 'get_texto_corto')
    list_filter = ('nivel_jerarquico', 'competencia__dimension', 'competencia')
    search_fields = ('codigo_excel', 'texto')
    ordering = ('id_textos_evaluacion',)

    @admin.display(description='Dimensión')
    def get_dimension(self, obj):
        return obj.competencia.dimension.nombre_dimension if obj.competencia else "-"

    @admin.display(description='Texto de la Pregunta')
    def get_texto_corto(self, obj):
        if obj.texto and len(obj.texto) > 60:
            return f"{obj.texto[:60]}..."
        return obj.texto

# Registro de Autoevaluaciones
@admin.register(Autoevaluacion)
class AutoevaluacionAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'codigo_excel', 'mostrar_competencia', 'get_nivel', 'puntaje', 'estado_finalizacion')
    ordering = ('codigo_excel__id_textos_evaluacion',)
    list_filter = ('trabajador', 'estado_finalizacion', 'codigo_excel__nivel_jerarquico')

    @admin.display(description='Competencia')
    def mostrar_competencia(self, obj):
        return obj.codigo_excel.competencia.nombre_competencia if obj.codigo_excel and obj.codigo_excel.competencia else "-"

    @admin.display(description='Nivel Jerárquico')
    def get_nivel(self, obj):
        return obj.codigo_excel.nivel_jerarquico.nombre_nivel_jerarquico if obj.codigo_excel else "-"

# Registro de Evaluación de Jefaturas
@admin.register(EvaluacionJefatura)
class EvaluacionJefaturaAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'trabajador_evaluado', 'codigo_excel', 'mostrar_competencia', 'get_nivel', 'puntaje', 'estado_finalizacion')
    ordering = ('codigo_excel__id_textos_evaluacion',)
    list_filter = ('evaluador', 'trabajador_evaluado', 'estado_finalizacion', 'codigo_excel__nivel_jerarquico')

    @admin.display(description='Competencia')
    def mostrar_competencia(self, obj):
        return obj.codigo_excel.competencia.nombre_competencia if obj.codigo_excel and obj.codigo_excel.competencia else "-"

    @admin.display(description='Nivel Jerárquico')
    def get_nivel(self, obj):
        return obj.codigo_excel.nivel_jerarquico.nombre_nivel_jerarquico if obj.codigo_excel else "-"

# Registro de Resultados Consolidados
@admin.register(ResultadoConsolidado)
class ResultadoConsolidadoAdmin(admin.ModelAdmin):
    list_display = (
        'trabajador', 
        'codigo_excel', 
        'mostrar_competencia', 
        'get_nivel', 
        'puntaje_jefe', 
        'puntaje_autoev', 
        'diferencia', 
        'periodo'
    )
    ordering = ('codigo_excel__id_textos_evaluacion',)
    list_filter = ('trabajador', 'periodo', 'codigo_excel__nivel_jerarquico')

    @admin.display(description='Competencia')
    def mostrar_competencia(self, obj):
        if hasattr(obj, 'competencia') and obj.competencia:
            return obj.competencia.nombre_competencia
        return obj.codigo_excel.competencia.nombre_competencia if obj.codigo_excel else "-"

    @admin.display(description='Nivel Jerárquico')
    def get_nivel(self, obj):
        return obj.codigo_excel.nivel_jerarquico.nombre_nivel_jerarquico if obj.codigo_excel else "-"
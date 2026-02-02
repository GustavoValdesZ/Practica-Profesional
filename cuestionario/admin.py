from django.contrib import admin
from .models import (
    Dimension,
    NivelJerarquico,
    Cargo,
    Trabajador,
    Competencia,
    TextosEvaluacion,
    Autoevaluacion,
    EvaluacionJefatura,
    ResultadoConsolidado
)

admin.site.register(Dimension)
admin.site.register(NivelJerarquico)
admin.site.register(Cargo)
admin.site.register(Trabajador)
admin.site.register(Competencia)
admin.site.register(TextosEvaluacion)
admin.site.register(Autoevaluacion)
admin.site.register(EvaluacionJefatura)
admin.site.register(ResultadoConsolidado)
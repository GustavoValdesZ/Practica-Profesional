from django.contrib import admin
from .models import (
    Dimension,
    NivelJerarquico,
    Trabajador,
    Competencia,
    TextosEvaluacion,
    Autoevaluacion,
    EvaluacionJefatura
)

admin.site.register(Dimension)
admin.site.register(NivelJerarquico)
admin.site.register(Trabajador)
admin.site.register(Competencia)
admin.site.register(TextosEvaluacion)
admin.site.register(Autoevaluacion)
admin.site.register(EvaluacionJefatura)

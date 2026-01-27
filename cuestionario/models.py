from django.db import models

class Dimension(models.Model):
    id_dimension = models.IntegerField(primary_key=True)
    nombre_dimension = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'dimension'

    def __str__(self):
        return self.nombre_dimension


class NivelJerarquico(models.Model):
    id_nivel_jerarquico = models.IntegerField(primary_key=True)
    nombre_nivel_jerarquico = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'nivel_jerarquico'

    def __str__(self):
        return self.nombre_nivel_jerarquico


class Cargo(models.Model):
    id_cargo = models.IntegerField(primary_key=True)
    nombre_cargo = models.CharField(max_length=50)
    nivel_jerarquico = models.ForeignKey(
        NivelJerarquico,
        on_delete=models.CASCADE,
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'cargo'

    def __str__(self):
        return self.nombre_cargo


class Trabajador(models.Model):
    id_trabajador = models.IntegerField(primary_key=True)
    rut = models.CharField(max_length=20)
    nombre = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=40)
    apellido_materno = models.CharField(max_length=40)
    email = models.CharField(max_length=80)
    departamento = models.CharField(max_length=40)
    cargo_texto = models.CharField(max_length=40)  # campo CARGO textual
    genero = models.CharField(max_length=10)
    nivel_jerarquico = models.ForeignKey(
        NivelJerarquico,
        on_delete=models.CASCADE,
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
        db_column='cargo_id_cargo'
    )

    class Meta:
        managed = False
        db_table = 'trabajador'

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"


class Competencia(models.Model):
    id_competencia = models.IntegerField(primary_key=True)
    nombre_competencia = models.CharField(max_length=50)
    dimension = models.ForeignKey(
        Dimension,
        on_delete=models.CASCADE,
        db_column='dimension_id_dimension'
    )

    class Meta:
        managed = False
        db_table = 'competencia'

    def __str__(self):
        return self.nombre_competencia


class TextosEvaluacion(models.Model):
    id_textos_evaluacion = models.IntegerField(primary_key=True)
    codigo_excel = models.CharField(max_length=10, unique=True)
    texto = models.TextField()
    competencia = models.ForeignKey(
        Competencia,
        on_delete=models.CASCADE,
        db_column='competencia_id_competencia'
    )
    nivel_jerarquico = models.ForeignKey(
        NivelJerarquico,
        on_delete=models.CASCADE,
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'textos_evaluacion'

    def __str__(self):
        return f"{self.codigo_excel} - {self.competencia}"


class Autoevaluacion(models.Model):
    id_autoevaluacion = models.IntegerField(primary_key=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_evaluacion = models.DateField()
    momento_evaluacion = models.DateTimeField()
    comentario = models.TextField(null=True, blank=True)
    trabajador = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        db_column='trabajador_id_trabajador'
    )
    codigo_excel = models.ForeignKey(
        TextosEvaluacion,
        on_delete=models.CASCADE,
        db_column='codigo_excel'
    )

    class Meta:
        managed = False
        db_table = 'autoevaluacion'


class EvaluacionJefatura(models.Model):
    id_evaluacion_jefatura = models.IntegerField(primary_key=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)
    evaluador = models.CharField(max_length=100)
    fecha_evaluacion = models.DateField()
    momento_evaluacion = models.DateTimeField()
    comentario = models.TextField(null=True, blank=True)
    trabajador = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        db_column='trabajador_id_trabajador'
    )
    codigo_excel = models.ForeignKey(
        TextosEvaluacion,
        on_delete=models.CASCADE,
        db_column='codigo_excel'
    )

    class Meta:
        managed = False
        db_table = 'evaluacion_jefatura'

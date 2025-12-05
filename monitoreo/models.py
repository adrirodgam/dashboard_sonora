from django.db import models

TIPO_MEDICION = (
    ('temperatura', 'Temperatura (°C)'),
    ('humedad', 'Humedad (%)'),
    ('luz', 'Iluminación (lux)'),
)


class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

    def __str__(self):
        return self.nombre


class Medicion(models.Model):
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name='mediciones'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_MEDICION)
    valor = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.municipio} - {self.tipo} - {self.valor}'


from django.db import models

# Create your models here.

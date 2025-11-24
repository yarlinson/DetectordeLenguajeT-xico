from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .automaton import ToxicityLevel, ToxicityType


class TextAnalysis(models.Model):
    """
    Modelo para almacenar análisis de texto y sus resultados de toxicidad.
    """

    SOURCE_CHOICES = (
        ('text', 'Texto ingresado'),
        ('file', 'Archivo adjunto'),
    )

    # Información del texto
    text = models.TextField(
        verbose_name="Texto analizado",
        help_text="El texto que fue analizado por el detector"
    )
    source_type = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default='text',
        verbose_name="Origen del contenido"
    )
    file_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Nombre del archivo"
    )
    file_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Tipo de archivo"
    )

    # Resultados del análisis
    is_toxic = models.BooleanField(
        default=False,
        verbose_name="Es tóxico",
        help_text="Indica si el texto contiene contenido tóxico"
    )

    toxicity_level = models.CharField(
        max_length=20,
        choices=[(level.value, level.value.title()) for level in ToxicityLevel],
        default=ToxicityLevel.SAFE.value,
        verbose_name="Nivel de toxicidad",
        help_text="Nivel de toxicidad detectado"
    )

    toxicity_types = models.JSONField(
        default=list,
        verbose_name="Tipos de toxicidad",
        help_text="Lista de tipos de toxicidad detectados"
    )

    matched_patterns = models.JSONField(
        default=list,
        verbose_name="Patrones encontrados",
        help_text="Patrones regex que coincidieron con el texto"
    )

    detected_words = models.JSONField(
        default=list,
        verbose_name="Palabras detectadas",
        help_text="Lista de palabras/frases detectadas con sus posiciones y tipos"
    )

    highlighted_text = models.TextField(
        blank=True,
        verbose_name="Texto resaltado",
        help_text="Texto con palabras tóxicas resaltadas en HTML"
    )

    afd_state = models.CharField(
        max_length=10,
        default='q0',
        verbose_name="Estado del AFD",
        help_text="Estado final del autómata (q0, q1, q2, q3)"
    )

    confidence = models.FloatField(
        default=0.0,
        verbose_name="Confianza",
        help_text="Nivel de confianza del análisis (0.0 a 1.0)"
    )

    # Metadatos
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Usuario",
        help_text="Usuario que realizó el análisis"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP",
        help_text="IP desde la cual se realizó el análisis"
    )

    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent",
        help_text="Información del navegador del usuario"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de creación",
        help_text="Fecha y hora cuando se realizó el análisis"
    )

    class Meta:
        verbose_name = "Análisis de Texto"
        verbose_name_plural = "Análisis de Textos"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_toxic']),
            models.Index(fields=['toxicity_level']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        text_preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        origin = "Archivo" if self.source_type == 'file' else "Texto"
        return f"[{origin}] {text_preview} - {self.get_toxicity_level_display()}"

    def get_toxicity_level_display(self):
        """Retorna el nivel de toxicidad formateado."""
        return dict(self._meta.get_field('toxicity_level').choices).get(
            self.toxicity_level, self.toxicity_level
        ).title()

    def get_toxicity_types_display(self):
        """Retorna los tipos de toxicidad formateados."""
        if not self.toxicity_types:
            return "Ninguno"

        type_names = []
        for toxicity_type in self.toxicity_types:
            try:
                type_obj = ToxicityType(toxicity_type)
                type_names.append(type_obj.value.title())
            except ValueError:
                type_names.append(toxicity_type.title())

        return ", ".join(type_names)

    def get_source_display(self):
        return dict(self.SOURCE_CHOICES).get(self.source_type, 'Texto ingresado')

    @property
    def confidence_percentage(self):
        return round(self.confidence * 100, 1)

    def get_words_by_type(self, toxicity_type: str):
        """Retorna las palabras detectadas para un tipo específico de toxicidad."""
        if not self.detected_words:
            return []
        return [
            word for word in self.detected_words 
            if word.get('toxicity_type') == toxicity_type and word.get('text')
        ]


class ToxicPattern(models.Model):
    """
    Modelo para almacenar patrones personalizados de toxicidad.
    Permite al administrador añadir nuevos patrones al detector.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Nombre del patrón",
        help_text="Nombre descriptivo del patrón"
    )

    pattern = models.TextField(
        verbose_name="Patrón regex",
        help_text="Expresión regular que define el patrón tóxico"
    )

    toxicity_type = models.CharField(
        max_length=20,
        choices=[(type_obj.value, type_obj.value.title()) for type_obj in ToxicityType],
        verbose_name="Tipo de toxicidad",
        help_text="Tipo de toxicidad que detecta este patrón"
    )

    toxicity_level = models.CharField(
        max_length=20,
        choices=[(level.value, level.value.title()) for level in ToxicityLevel],
        default=ToxicityLevel.LOW.value,
        verbose_name="Nivel de toxicidad",
        help_text="Nivel de toxicidad asignado a este patrón"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del patrón"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el patrón está activo en el detector"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Patrón Tóxico"
        verbose_name_plural = "Patrones Tóxicos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_toxicity_type_display()}"

    def get_toxicity_type_display(self):
        """Retorna el tipo de toxicidad formateado."""
        return dict(self._meta.get_field('toxicity_type').choices).get(
            self.toxicity_type, self.toxicity_type
        ).title()

    def get_toxicity_level_display(self):
        """Retorna el nivel de toxicidad formateado."""
        return dict(self._meta.get_field('toxicity_level').choices).get(
            self.toxicity_level, self.toxicity_level
        ).title()


class AnalysisStatistics(models.Model):
    """
    Modelo para almacenar estadísticas de análisis.
    Se actualiza automáticamente con cada nuevo análisis.
    """

    date = models.DateField(
        unique=True,
        verbose_name="Fecha",
        help_text="Fecha de las estadísticas"
    )

    total_analyses = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de análisis",
        help_text="Número total de análisis realizados en esta fecha"
    )

    toxic_analyses = models.PositiveIntegerField(
        default=0,
        verbose_name="Análisis tóxicos",
        help_text="Número de análisis que detectaron toxicidad"
    )

    safe_analyses = models.PositiveIntegerField(
        default=0,
        verbose_name="Análisis seguros",
        help_text="Número de análisis que no detectaron toxicidad"
    )

    # Estadísticas por nivel de toxicidad
    low_toxicity = models.PositiveIntegerField(
        default=0,
        verbose_name="Toxicidad baja"
    )

    medium_toxicity = models.PositiveIntegerField(
        default=0,
        verbose_name="Toxicidad media"
    )

    high_toxicity = models.PositiveIntegerField(
        default=0,
        verbose_name="Toxicidad alta"
    )

    extreme_toxicity = models.PositiveIntegerField(
        default=0,
        verbose_name="Toxicidad extrema"
    )

    # Estadísticas por tipo de toxicidad
    insults_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Insultos detectados"
    )

    threats_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Amenazas detectadas"
    )

    hate_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Odio detectado"
    )

    harassment_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Acoso detectado"
    )

    profanity_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Profanidad detectada"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Estadística de Análisis"
        verbose_name_plural = "Estadísticas de Análisis"
        ordering = ['-date']

    def __str__(self):
        return f"Estadísticas del {self.date}"

    @property
    def toxicity_rate(self):
        """Calcula el porcentaje de toxicidad."""
        if self.total_analyses == 0:
            return 0
        return (self.toxic_analyses / self.total_analyses) * 100

    @property
    def safety_rate(self):
        """Calcula el porcentaje de seguridad."""
        if self.total_analyses == 0:
            return 0
        return (self.safe_analyses / self.total_analyses) * 100

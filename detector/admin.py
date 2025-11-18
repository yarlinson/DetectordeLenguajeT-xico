from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import TextAnalysis, ToxicPattern, AnalysisStatistics


class ToxicityLevelFilter(SimpleListFilter):
    title = 'Nivel de toxicidad'
    parameter_name = 'toxicity_level'

    def lookups(self, request, model_admin):
        return [
            ('safe', 'Seguro'),
            ('low', 'Bajo'),
            ('medium', 'Medio'),
            ('high', 'Alto'),
            ('extreme', 'Extremo'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(toxicity_level=self.value())


class IsToxicFilter(SimpleListFilter):
    title = 'Es tóxico'
    parameter_name = 'is_toxic'

    def lookups(self, request, model_admin):
        return [
            ('true', 'Sí'),
            ('false', 'No'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(is_toxic=True)
        elif self.value() == 'false':
            return queryset.filter(is_toxic=False)


@admin.register(TextAnalysis)
class TextAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'text_preview', 'source_badge', 'is_toxic_badge', 'toxicity_level_badge',
        'toxicity_types_display', 'confidence_bar', 'user', 'created_at'
    ]
    list_filter = [
        'source_type', ToxicityLevelFilter, IsToxicFilter, 'created_at', 'user'
    ]
    search_fields = ['text', 'file_name', 'user__username', 'ip_address']
    readonly_fields = [
        'id', 'created_at', 'source_type', 'file_name', 'file_type',
        'toxicity_level', 'toxicity_types',
        'matched_patterns', 'detected_words', 'highlighted_text', 'confidence', 'afd_state', 'is_toxic'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Información del Análisis', {
            'fields': ('id', 'source_type', 'file_name', 'file_type', 'text', 'created_at')
        }),
        ('Resultados', {
            'fields': ('is_toxic', 'toxicity_level', 'toxicity_types', 'matched_patterns', 'detected_words', 'highlighted_text', 'confidence', 'afd_state')
        }),
        ('Metadatos', {
            'fields': ('user', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        """Muestra una vista previa del texto."""
        preview = obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
        return preview
    text_preview.short_description = 'Texto'

    def is_toxic_badge(self, obj):
        """Muestra el estado de toxicidad como badge."""
        if obj.is_toxic:
            return 'Tóxico'
        else:
            return 'Seguro'
    is_toxic_badge.short_description = 'Estado'
    is_toxic_badge.admin_order_field = 'is_toxic'

    def toxicity_level_badge(self, obj):
        """Muestra el nivel de toxicidad como badge."""
        colors = {
            'safe': 'success',
            'low': 'warning',
            'medium': 'danger',
            'high': 'danger',
            'extreme': 'dark'
        }
        color = colors.get(obj.toxicity_level, 'secondary')
        return obj.get_toxicity_level_display()
    toxicity_level_badge.short_description = 'Nivel'
    toxicity_level_badge.admin_order_field = 'toxicity_level'

    def toxicity_types_display(self, obj):
        """Muestra los tipos de toxicidad detectados."""
        if not obj.toxicity_types:
            return 'Ninguno'

        types_list = []
        for toxicity_type in obj.toxicity_types:
            types_list.append(toxicity_type.title())

        return ', '.join(types_list)
    toxicity_types_display.short_description = 'Tipos Detectados'

    def confidence_bar(self, obj):
        """Muestra la confianza como barra de progreso."""
        percentage = obj.confidence * 100
        color = 'success' if not obj.is_toxic else 'danger'

        return f'{percentage:.1f}%'
    confidence_bar.short_description = 'Confianza'
    confidence_bar.admin_order_field = 'confidence'

    def source_badge(self, obj):
        if obj.source_type == 'file':
            if obj.file_name:
                return f"Archivo ({obj.file_name})"
            return 'Archivo adjunto'
        return 'Texto ingresado'
    source_badge.short_description = 'Origen'
    source_badge.admin_order_field = 'source_type'

    def has_add_permission(self, request):
        """No permitir añadir análisis manualmente."""
        return False

    def has_change_permission(self, request, obj=None):
        """No permitir editar análisis."""
        return False


@admin.register(ToxicPattern)
class ToxicPatternAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'toxicity_type_badge', 'toxicity_level_badge',
        'pattern_preview', 'is_active_badge', 'created_at'
    ]
    list_filter = ['toxicity_type', 'toxicity_level', 'is_active', 'created_at']
    search_fields = ['name', 'pattern', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información del Patrón', {
            'fields': ('name', 'description')
        }),
        ('Configuración', {
            'fields': ('pattern', 'toxicity_type', 'toxicity_level', 'is_active')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def toxicity_type_badge(self, obj):
        """Muestra el tipo de toxicidad como badge."""
        return obj.get_toxicity_type_display()
    toxicity_type_badge.short_description = 'Tipo'
    toxicity_type_badge.admin_order_field = 'toxicity_type'

    def toxicity_level_badge(self, obj):
        """Muestra el nivel de toxicidad como badge."""
        colors = {
            'safe': 'success',
            'low': 'warning',
            'medium': 'danger',
            'high': 'danger',
            'extreme': 'dark'
        }
        color = colors.get(obj.toxicity_level, 'secondary')
        return obj.get_toxicity_level_display()
    toxicity_level_badge.short_description = 'Nivel'
    toxicity_level_badge.admin_order_field = 'toxicity_level'

    def pattern_preview(self, obj):
        """Muestra una vista previa del patrón."""
        preview = obj.pattern[:30] + "..." if len(obj.pattern) > 30 else obj.pattern
        return preview
    pattern_preview.short_description = 'Patrón'

    def is_active_badge(self, obj):
        """Muestra el estado activo como badge."""
        if obj.is_active:
            return 'Activo'
        else:
            return 'Inactivo'
    is_active_badge.short_description = 'Estado'
    is_active_badge.admin_order_field = 'is_active'


@admin.register(AnalysisStatistics)
class AnalysisStatisticsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_analyses', 'toxic_analyses', 'safe_analyses',
        'toxicity_rate_percent', 'safety_rate_percent'
    ]
    list_filter = ['date']
    search_fields = ['date']
    readonly_fields = [
        'date', 'total_analyses', 'toxic_analyses', 'safe_analyses',
        'low_toxicity', 'medium_toxicity', 'high_toxicity', 'extreme_toxicity',
        'insults_count', 'threats_count', 'hate_count', 'harassment_count', 'profanity_count',
        'created_at', 'updated_at'
    ]
    date_hierarchy = 'date'
    ordering = ['-date']

    fieldsets = (
        ('Información General', {
            'fields': ('date', 'total_analyses', 'toxic_analyses', 'safe_analyses')
        }),
        ('Distribución por Nivel', {
            'fields': ('low_toxicity', 'medium_toxicity', 'high_toxicity', 'extreme_toxicity')
        }),
        ('Distribución por Tipo', {
            'fields': ('insults_count', 'threats_count', 'hate_count', 'harassment_count', 'profanity_count')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def toxicity_rate_percent(self, obj):
        return round(obj.toxicity_rate, 1)
    toxicity_rate_percent.short_description = 'Tasa Toxicidad (%)'
    toxicity_rate_percent.admin_order_field = 'toxic_analyses'

    def safety_rate_percent(self, obj):
        return round(obj.safety_rate, 1)
    safety_rate_percent.short_description = 'Tasa Seguridad (%)'
    safety_rate_percent.admin_order_field = 'safe_analyses'

    def has_add_permission(self, request):
        """No permitir añadir estadísticas manualmente."""
        return False

    def has_change_permission(self, request, obj=None):
        """No permitir editar estadísticas."""
        return False


# Personalizar el sitio de administración
admin.site.site_header = "Detector de Lenguaje Tóxico - Administración"
admin.site.site_title = "Detector de Toxicidad"
admin.site.index_title = "Panel de Administración"

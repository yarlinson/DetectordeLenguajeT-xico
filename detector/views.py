from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
import os
from io import BytesIO

from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

from .models import TextAnalysis, ToxicPattern, AnalysisStatistics
from .automaton import toxic_detector, ToxicityLevel, ToxicityType
from .forms import TextAnalysisForm

logger = logging.getLogger(__name__)

ALLOWED_FILE_EXTENSIONS = {'.pdf', '.txt', '.html', '.htm'}


def extract_text_from_document(uploaded_file):
    """Extrae texto del archivo cargado según su tipo."""
    extension = os.path.splitext(uploaded_file.name)[1].lower()
    uploaded_file.seek(0)

    try:
        if extension == '.pdf':
            reader = PdfReader(uploaded_file)
            pages_text = []
            for page in reader.pages:
                pages_text.append(page.extract_text() or '')
            text_content = '\n'.join(pages_text)
        elif extension in {'.txt'}:
            text_content = uploaded_file.read().decode('utf-8', errors='ignore')
        elif extension in {'.html', '.htm'}:
            html_content = uploaded_file.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text(separator='\n')
        else:
            raise ValueError('Formato de archivo no soportado.')
    finally:
        uploaded_file.seek(0)

    return text_content.strip()


def home(request):
    """
    Vista principal que muestra el formulario de análisis de texto.
    """
    if request.method == 'POST':
        form = TextAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            text_input = form.cleaned_data['text']
            document = form.cleaned_data.get('document')

            source_type = 'text'
            file_name = ''
            file_type = ''
            extracted_text = text_input

            if document:
                source_type = 'file'
                file_name = document.name
                file_type = os.path.splitext(document.name)[1].lower().lstrip('.')

                try:
                    extracted_text = extract_text_from_document(document)
                except Exception as exc:
                    logger.exception("Error al extraer texto del archivo adjunto")
                    form.add_error('document', 'No se pudo leer el archivo adjunto. Asegúrate de que no esté dañado y vuelve a intentarlo.')
                    return render(request, 'detector/home.html', {'form': form, 'stats': get_general_statistics()})

                if not extracted_text:
                    form.add_error('document', 'El archivo no contiene texto legible.')
                    return render(request, 'detector/home.html', {'form': form, 'stats': get_general_statistics()})

            if not extracted_text:
                form.add_error('text', 'El texto no puede estar vacío.')
                return render(request, 'detector/home.html', {'form': form, 'stats': get_general_statistics()})

            # Realizar análisis con el autómata
            analysis_result = toxic_detector.process_text(extracted_text)

            # Preparar palabras detectadas para guardar
            detected_words_data = []
            for word in analysis_result['detected_words']:
                detected_words_data.append({
                    'text': word.text,
                    'toxicity_type': word.toxicity_type.value,
                    'pattern': word.pattern,
                    'start': word.start,
                    'end': word.end
                })

            # Guardar análisis en la base de datos
            analysis = TextAnalysis.objects.create(
                text=extracted_text,
                source_type=source_type,
                file_name=file_name,
                file_type=file_type,
                is_toxic=analysis_result['is_toxic'],
                toxicity_level=analysis_result['level'].value,
                toxicity_types=analysis_result['types'],
                matched_patterns=analysis_result['matched_patterns'],
                detected_words=detected_words_data,
                highlighted_text=analysis_result['highlighted_text'],
                afd_state=analysis_result['state'],
                confidence=analysis_result['confidence'],
                user=request.user if request.user.is_authenticated else None,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # Actualizar estadísticas
            update_statistics(analysis)

            # Mostrar resultado
            messages.success(request, 'Análisis completado exitosamente.')
            return render(request, 'detector/result.html', {
                'analysis': analysis,
                'analysis_result': analysis_result
            })
    else:
        form = TextAnalysisForm()

    # Obtener estadísticas generales para mostrar en la página principal
    stats = get_general_statistics()

    return render(request, 'detector/home.html', {
        'form': form,
        'stats': stats
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_analyze_text(request):
    """
    API endpoint para análisis de texto via AJAX.
    Retorna JSON con los resultados del análisis.
    """
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({
                'error': 'El texto no puede estar vacío'
            }, status=400)
        
        if len(text) > 10000:  # Límite de caracteres
            return JsonResponse({
                'error': 'El texto es demasiado largo (máximo 10,000 caracteres)'
            }, status=400)
        
        # Realizar análisis
        analysis_result = toxic_detector.process_text(text)
        
        # Preparar palabras detectadas para guardar
        detected_words_data = []
        for word in analysis_result['detected_words']:
            detected_words_data.append({
                'text': word.text,
                'start': word.start,
                'end': word.end,
                'pattern': word.pattern,
                'toxicity_type': word.toxicity_type.value
            })
        
        # Guardar análisis en la base de datos
        analysis = TextAnalysis.objects.create(
            text=text,
            source_type='text',
            file_name='',
            file_type='',
            is_toxic=analysis_result['is_toxic'],
            toxicity_level=analysis_result['level'].value,
            toxicity_types=analysis_result['types'],
            matched_patterns=analysis_result['matched_patterns'],
            detected_words=detected_words_data,
            highlighted_text=analysis_result['highlighted_text'],
            afd_state=analysis_result['state'],
            confidence=analysis_result['confidence'],
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Actualizar estadísticas
        update_statistics(analysis)
        
        # Preparar palabras detectadas para la respuesta
        detected_words_list = []
        for word in analysis_result['detected_words']:
            detected_words_list.append({
                'text': word.text,
                'toxicity_type': word.toxicity_type.value
            })
        
        # Preparar respuesta
        response_data = {
            'success': True,
            'analysis_id': analysis.id,
            'is_toxic': analysis_result['is_toxic'],
            'toxicity_level': analysis_result['level'].value,
            'toxicity_level_display': analysis.get_toxicity_level_display(),
            'afd_state': analysis_result['state'],
            'source_type': 'text',
            'file_name': '',
            'file_type': '',
            'toxicity_types': analysis_result['types'],
            'toxicity_types_display': analysis.get_toxicity_types_display(),
            'confidence': analysis_result['confidence'],
            'matched_patterns_count': len(analysis_result['matched_patterns']),
            'detected_words_count': len(analysis_result['detected_words']),
            'detected_words': detected_words_list,
            'highlighted_text': analysis_result['highlighted_text'],
            'created_at': analysis.created_at.isoformat()
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Datos JSON inválidos'
        }, status=400)
    except Exception as e:
        logger.error(f"Error en análisis de texto: {str(e)}")
        return JsonResponse({
            'error': 'Error interno del servidor'
        }, status=500)


@login_required
def analysis_history(request):
    """
    Vista para mostrar el historial de análisis del usuario.
    """
    analyses = TextAnalysis.objects.filter(user=request.user)
    
    # Filtros
    toxicity_filter = request.GET.get('toxicity_level')
    if toxicity_filter:
        analyses = analyses.filter(toxicity_level=toxicity_filter)
    
    is_toxic_filter = request.GET.get('is_toxic')
    if is_toxic_filter == 'true':
        analyses = analyses.filter(is_toxic=True)
    elif is_toxic_filter == 'false':
        analyses = analyses.filter(is_toxic=False)
    
    # Paginación
    paginator = Paginator(analyses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Convertir Enum a lista para el template
    toxicity_levels_list = [level for level in ToxicityLevel]
    
    return render(request, 'detector/history.html', {
        'page_obj': page_obj,
        'toxicity_levels': toxicity_levels_list,
        'current_filters': {
            'toxicity_level': toxicity_filter,
            'is_toxic': is_toxic_filter
        }
    })


@login_required
def analysis_detail(request, analysis_id):
    """
    Vista para mostrar detalles de un análisis específico.
    """
    try:
        analysis = TextAnalysis.objects.get(id=analysis_id, user=request.user)
        return render(request, 'detector/detail.html', {
            'analysis': analysis
        })
    except TextAnalysis.DoesNotExist:
        messages.error(request, 'Análisis no encontrado.')
        return redirect('detector:history')


def statistics_view(request):
    """
    Vista para mostrar estadísticas generales del sistema.
    """
    stats = get_general_statistics()
    
    # Estadísticas por fecha (últimos 30 días)
    recent_stats = AnalysisStatistics.objects.order_by('-date')[:30]
    
    # Estadísticas por tipo de toxicidad
    toxicity_type_stats = TextAnalysis.objects.filter(
        is_toxic=True
    ).values('toxicity_types').annotate(
        count=Count('id')
    )
    
    return render(request, 'detector/statistics.html', {
        'stats': stats,
        'recent_stats': recent_stats,
        'toxicity_type_stats': toxicity_type_stats
    })


def get_client_ip(request):
    """
    Obtiene la IP del cliente desde la request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_general_statistics():
    """
    Obtiene estadísticas generales del sistema.
    """
    total_analyses = TextAnalysis.objects.count()
    toxic_analyses = TextAnalysis.objects.filter(is_toxic=True).count()
    safe_analyses = total_analyses - toxic_analyses
    
    # Estadísticas por nivel de toxicidad
    toxicity_level_stats = {}
    toxicity_level_percentages = {}
    for level in ToxicityLevel:
        count = TextAnalysis.objects.filter(toxicity_level=level.value).count()
        toxicity_level_stats[level.value] = count
        if total_analyses > 0:
            toxicity_level_percentages[level.value] = (count / total_analyses) * 100
        else:
            toxicity_level_percentages[level.value] = 0
    
    # Estadísticas por tipo de toxicidad
    toxicity_type_stats = {}
    toxicity_type_percentages = {}
    for toxicity_type in ToxicityType:
        # Usar una consulta compatible con SQLite
        count = TextAnalysis.objects.filter(
            toxicity_types__icontains=toxicity_type.value
        ).count()
        toxicity_type_stats[toxicity_type.value] = count
        if toxic_analyses > 0:
            toxicity_type_percentages[toxicity_type.value] = (count / toxic_analyses) * 100
        else:
            toxicity_type_percentages[toxicity_type.value] = 0
    
    return {
        'total_analyses': total_analyses,
        'toxic_analyses': toxic_analyses,
        'safe_analyses': safe_analyses,
        'toxicity_rate': (toxic_analyses / total_analyses * 100) if total_analyses > 0 else 0,
        'safety_rate': (safe_analyses / total_analyses * 100) if total_analyses > 0 else 0,
        'toxicity_level_stats': toxicity_level_stats,
        'toxicity_level_percentages': toxicity_level_percentages,
        'toxicity_type_stats': toxicity_type_stats,
        'toxicity_type_percentages': toxicity_type_percentages
    }


def update_statistics(analysis):
    """
    Actualiza las estadísticas diarias con un nuevo análisis.
    """
    today = timezone.now().date()
    
    # Obtener o crear estadísticas del día
    stats, created = AnalysisStatistics.objects.get_or_create(
        date=today,
        defaults={
            'total_analyses': 0,
            'toxic_analyses': 0,
            'safe_analyses': 0,
            'low_toxicity': 0,
            'medium_toxicity': 0,
            'high_toxicity': 0,
            'extreme_toxicity': 0,
            'insults_count': 0,
            'threats_count': 0,
            'hate_count': 0,
            'harassment_count': 0,
            'profanity_count': 0
        }
    )
    
    # Actualizar contadores generales
    stats.total_analyses += 1
    if analysis.is_toxic:
        stats.toxic_analyses += 1
    else:
        stats.safe_analyses += 1
    
    # Actualizar contadores por nivel de toxicidad
    if analysis.toxicity_level == ToxicityLevel.LOW.value:
        stats.low_toxicity += 1
    elif analysis.toxicity_level == ToxicityLevel.MEDIUM.value:
        stats.medium_toxicity += 1
    elif analysis.toxicity_level == ToxicityLevel.EXTREME.value:
        stats.extreme_toxicity += 1
    
    # Actualizar contadores por tipo de toxicidad
    for toxicity_type in analysis.toxicity_types:
        if toxicity_type == ToxicityType.INSULT.value:
            stats.insults_count += 1
        elif toxicity_type == ToxicityType.THREAT.value:
            stats.threats_count += 1
        elif toxicity_type == ToxicityType.HATE.value:
            stats.hate_count += 1
        elif toxicity_type == ToxicityType.HARASSMENT.value:
            stats.harassment_count += 1
        elif toxicity_type == ToxicityType.PROFANITY.value:
            stats.profanity_count += 1
    
    stats.save()


def about(request):
    """
    Vista para mostrar información sobre el detector de toxicidad.
    """
    automaton_stats = toxic_detector.get_statistics()
    
    return render(request, 'detector/about.html', {
        'automaton_stats': automaton_stats
    })


def automaton_explanation(request):
    """
    Vista para explicar el funcionamiento del AFD de manera detallada.
    """
    automaton_stats = toxic_detector.get_statistics()
    
    # Información teórica del AFD
    afd_info = {
        'states': {
            'q0': {'name': 'SAFE', 'description': 'Estado inicial - Texto seguro', 'level': 'safe', 'final': True},
            'q1': {'name': 'LOW', 'description': 'Toxicidad baja - Insultos o profanidad', 'level': 'low', 'final': True},
            'q2': {'name': 'MEDIUM', 'description': 'Toxicidad media - Acoso', 'level': 'medium', 'final': True},
            'q3': {'name': 'EXTREME', 'description': 'Toxicidad extrema - Amenazas u odio', 'level': 'extreme', 'final': True}
        },
        'transitions': [
            # Desde q0
            {'from': 'q0', 'to': 'q1', 'trigger': 'Patrones de insultos', 'example': 'estúpido, idiota, imbécil'},
            {'from': 'q0', 'to': 'q1', 'trigger': 'Patrones de profanidad', 'example': 'mierda, joder, coño'},
            {'from': 'q0', 'to': 'q2', 'trigger': 'Patrones de acoso', 'example': 'acosar, molestar, fastidiar'},
            {'from': 'q0', 'to': 'q3', 'trigger': 'Patrones de amenazas', 'example': 'te voy a matar, te mato'},
            {'from': 'q0', 'to': 'q3', 'trigger': 'Patrones de odio', 'example': 'odio, asco, repugnante'},
            # Desde q1
            {'from': 'q1', 'to': 'q1', 'trigger': 'Patrones de insultos', 'example': 'Permanece en LOW'},
            {'from': 'q1', 'to': 'q1', 'trigger': 'Patrones de profanidad', 'example': 'Permanece en LOW'},
            {'from': 'q1', 'to': 'q2', 'trigger': 'Patrones de acoso', 'example': 'Sube a MEDIUM'},
            {'from': 'q1', 'to': 'q3', 'trigger': 'Patrones de amenazas', 'example': 'Sube a EXTREME'},
            {'from': 'q1', 'to': 'q3', 'trigger': 'Patrones de odio', 'example': 'Sube a EXTREME'},
            # Desde q2
            {'from': 'q2', 'to': 'q2', 'trigger': 'Patrones de insultos', 'example': 'Permanece en MEDIUM'},
            {'from': 'q2', 'to': 'q2', 'trigger': 'Patrones de profanidad', 'example': 'Permanece en MEDIUM'},
            {'from': 'q2', 'to': 'q2', 'trigger': 'Patrones de acoso', 'example': 'Permanece en MEDIUM'},
            {'from': 'q2', 'to': 'q3', 'trigger': 'Patrones de amenazas', 'example': 'Sube a EXTREME'},
            {'from': 'q2', 'to': 'q3', 'trigger': 'Patrones de odio', 'example': 'Sube a EXTREME'},
            # Desde q3 (estado absorbente)
            {'from': 'q3', 'to': 'q3', 'trigger': 'Cualquier patrón', 'example': 'Permanece en EXTREME'}
        ],
        'quintuple': {
            'Q': 'Conjunto de estados: {q₀, q₁, q₂, q₃}',
            'Sigma': 'Alfabeto: Conjunto de patrones regex de toxicidad',
            'delta': 'Función de transición: δ(estado, patrón) = nuevo_estado',
            'q0': 'Estado inicial: q₀ (SAFE)',
            'F': 'Estados finales: {q₀, q₁, q₂, q₃} (todos son finales)'
        },
        'examples': [
            {
                'text': 'Hola, ¿cómo estás?',
                'path': ['q0'],
                'result': 'Seguro',
                'description': 'Texto sin patrones tóxicos - Permanece en q₀ (SAFE)'
            },
            {
                'text': 'Eres un estúpido',
                'path': ['q0', 'q1'],
                'result': 'Tóxico - Low',
                'description': 'Insulto detectado - Transición q₀ → q₁ (LOW)'
            },
            {
                'text': 'Te voy a matar',
                'path': ['q0', 'q3'],
                'result': 'Tóxico - Extreme',
                'description': 'Amenaza detectada - Transición q₀ → q₃ (EXTREME)'
            },
            {
                'text': 'Odio a todos',
                'path': ['q0', 'q3'],
                'result': 'Tóxico - Extreme',
                'description': 'Odio detectado - Transición q₀ → q₃ (EXTREME)'
            },
            {
                'text': 'Eres un estúpido y te voy a acosar',
                'path': ['q0', 'q1', 'q2'],
                'result': 'Tóxico - Medium',
                'description': 'Insulto seguido de acoso - Transición q₀ → q₁ → q₂ (LOW → MEDIUM)'
            }
        ]
    }
    
    return render(request, 'detector/automaton_explanation.html', {
        'automaton_stats': automaton_stats,
        'afd_info': afd_info
    })

"""
Módulo que implementa un AFD (Autómata Finito Determinista) para detectar lenguaje tóxico.
El autómata analiza texto y determina si contiene contenido agresivo o tóxico.

AFD: M = (Q, Σ, δ, q₀, F)
- Q: {q₀, q₁, q₂, q₃}
- q₀: Estado inicial (SAFE)
- Σ: Conjunto de patrones regex de toxicidad
- F: {q₀, q₁, q₂, q₃} (todos son estados finales)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum


class ToxicityLevel(Enum):
    """Niveles de toxicidad detectados por el autómata."""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    EXTREME = "extreme"


class ToxicityType(Enum):
    """Tipos de toxicidad detectados."""
    INSULT = "insult"
    THREAT = "threat"
    HATE = "hate"
    HARASSMENT = "harassment"
    PROFANITY = "profanity"


class DetectedWord:
    """Representa una palabra o frase detectada por un patrón."""
    def __init__(self, text: str, start: int, end: int, pattern: str, toxicity_type: ToxicityType):
        self.text = text
        self.start = start
        self.end = end
        self.pattern = pattern
        self.toxicity_type = toxicity_type


class ToxicDetectorAutomaton:
    """
    AFD para detectar lenguaje tóxico en texto.
    
    Estados:
    - q₀: SAFE (Estado inicial)
    - q₁: LOW
    - q₂: MEDIUM
    - q₃: EXTREME
    
    Funciones de transición:
    Desde q₀:
    - δ(q₀, Patron_insultos) = q₁
    - δ(q₀, Patron_Profanidad) = q₁
    - δ(q₀, Patron_Acoso) = q₂
    - δ(q₀, Patron_Amenazas) = q₃
    - δ(q₀, Patron_Odio) = q₃
    
    Desde q₁:
    - δ(q₁, Patron_insultos) = q₁
    - δ(q₁, Patron_Profanidad) = q₁
    - δ(q₁, Patron_Acoso) = q₂
    - δ(q₁, Patron_Amenazas) = q₃
    - δ(q₁, Patron_Odio) = q₃
    
    Desde q₂:
    - δ(q₂, Patron_insultos) = q₂
    - δ(q₂, Patron_Profanidad) = q₂
    - δ(q₂, Patron_Acoso) = q₂
    - δ(q₂, Patron_Amenazas) = q₃
    - δ(q₂, Patron_Odio) = q₃
    
    Desde q₃:
    - δ(q₃, cualquier_patrón) = q₃ (estado absorbente)
    """
    
    def __init__(self):
        self.current_state = 'q0'  # Estado inicial
        self._load_toxic_patterns()
    
    def _load_toxic_patterns(self):
        """Carga patrones de palabras tóxicas organizadas por categorías."""
        data_path = Path(__file__).resolve().parent / "data" / "toxic_patterns.json"

        if not data_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de patrones tóxicos en {data_path}. "
                "Asegúrate de que el archivo exista y contenga un diccionario JSON válido."
            )

        try:
            with data_path.open("r", encoding="utf-8") as patterns_file:
                patterns_data = json.load(patterns_file)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "El archivo de patrones tóxicos contiene un JSON inválido. "
                "Revísalo e inténtalo de nuevo."
            ) from exc

        toxic_patterns: Dict[ToxicityType, List[str]] = {}
        for key, patterns in patterns_data.items():
            try:
                toxicity_type = ToxicityType(key)
            except ValueError as exc:
                raise ValueError(
                    f"Tipo de toxicidad desconocido '{key}' en el archivo de patrones."
                ) from exc

            if not isinstance(patterns, list):
                raise ValueError(
                    f"Los patrones para el tipo '{key}' deben estar en una lista."
                )

            toxic_patterns[toxicity_type] = patterns

        self.toxic_patterns = toxic_patterns
    
    def reset(self):
        """Reinicia el autómata al estado inicial."""
        self.current_state = 'q0'
    
    def _transition(self, current_state: str, toxicity_type: ToxicityType) -> str:
        """
        Aplica la función de transición δ(estado, tipo_patrón) = nuevo_estado
        
        Args:
            current_state: Estado actual (q0, q1, q2, q3)
            toxicity_type: Tipo de patrón detectado
            
        Returns:
            Nuevo estado según las reglas de transición
        """
        # Estado q₃ es absorbente (siempre permanece en q₃)
        if current_state == 'q3':
            return 'q3'
        
        # Desde q₀
        if current_state == 'q0':
            if toxicity_type in [ToxicityType.INSULT, ToxicityType.PROFANITY]:
                return 'q1'  # LOW
            elif toxicity_type == ToxicityType.HARASSMENT:
                return 'q2'  # MEDIUM
            elif toxicity_type in [ToxicityType.THREAT, ToxicityType.HATE]:
                return 'q3'  # EXTREME
        
        # Desde q₁
        elif current_state == 'q1':
            if toxicity_type in [ToxicityType.INSULT, ToxicityType.PROFANITY]:
                return 'q1'  # Permanece en LOW
            elif toxicity_type == ToxicityType.HARASSMENT:
                return 'q2'  # Sube a MEDIUM
            elif toxicity_type in [ToxicityType.THREAT, ToxicityType.HATE]:
                return 'q3'  # Sube a EXTREME
        
        # Desde q₂
        elif current_state == 'q2':
            if toxicity_type in [ToxicityType.INSULT, ToxicityType.PROFANITY, ToxicityType.HARASSMENT]:
                return 'q2'  # Permanece en MEDIUM
            elif toxicity_type in [ToxicityType.THREAT, ToxicityType.HATE]:
                return 'q3'  # Sube a EXTREME
        
        # Si no hay transición definida, mantener estado actual
        return current_state
    
    def _get_level_from_state(self, state: str) -> ToxicityLevel:
        """Convierte el estado del AFD al nivel de toxicidad."""
        state_to_level = {
            'q0': ToxicityLevel.SAFE,
            'q1': ToxicityLevel.LOW,
            'q2': ToxicityLevel.MEDIUM,
            'q3': ToxicityLevel.EXTREME
        }
        return state_to_level.get(state, ToxicityLevel.SAFE)
    
    def process_text(self, text: str) -> Dict:
        """
        Procesa el texto de entrada y determina su nivel de toxicidad usando el AFD.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Dict con información sobre la toxicidad detectada, incluyendo palabras resaltadas
        """
        self.reset()

        detected_toxicity = {
            'is_toxic': False,
            'level': ToxicityLevel.SAFE,
            'state': 'q0',
            'types': [],
            'matched_patterns': [],
            'detected_words': [],  # Lista de palabras/frases detectadas
            'confidence': 0.0,
            'original_text': text,
            'highlighted_text': text  # Texto con palabras resaltadas
        }

        seen_spans = set()
        a = 0;

        # Buscar todos los patrones en el texto (usando el texto original para mantener posiciones)
        for toxicity_type, patterns in self.toxic_patterns.items():
            for pattern in patterns:
                # Buscar todas las coincidencias del patrón en el texto original
                # pero usando re.IGNORECASE para que sea case-insensitive
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    a = a+1;
                    start_pos = match.start()
                    end_pos = match.end()
                    print(f"texto: {text} . a: {a}")
                    print(f"Found match: {match.group()} at {start_pos}-{end_pos}")
                    # Evitar duplicados exactos del mismo segmento
                    span_key = (start_pos, end_pos)
                    if span_key in seen_spans:
                        continue
                    seen_spans.add(span_key)
                    print(f"seen_spans: {seen_spans}")

                    matched_text = match.group()  # Texto original con mayúsculas/minúsculas

                    # Crear objeto DetectedWord con el texto original
                    detected_word = DetectedWord(
                        text=matched_text,
                        start=start_pos,
                        end=end_pos,
                        pattern=pattern,
                        toxicity_type=toxicity_type
                    )
                    detected_toxicity['detected_words'].append(detected_word)
                    

                    # Aplicar transición del AFD
                    new_state = self._transition(self.current_state, toxicity_type)
                    self.current_state = new_state
                    print(f"new_state: {new_state}")
                    print(f"current_state: {self.current_state}")
                    
                    # Actualizar información
                    detected_toxicity['is_toxic'] = True
                    if toxicity_type.value not in detected_toxicity['types']:
                        detected_toxicity['types'].append(toxicity_type.value)
                    # Guardar el patrón para referencia técnica, pero el conteo se hará por tipos únicos
                    if pattern not in detected_toxicity['matched_patterns']:
                        detected_toxicity['matched_patterns'].append(pattern)
                    

        
        # Actualizar nivel final basado en el estado del AFD
        detected_toxicity['level'] = self._get_level_from_state(self.current_state)
        detected_toxicity['state'] = self.current_state
        print(f"Despues de salir del fordetected_toxicity: {detected_toxicity.get('state')}")
        
        # Calcular confianza basada en el número de palabras detectadas
        if detected_toxicity['is_toxic']:
            num_words = len(detected_toxicity['detected_words'])
            detected_toxicity['confidence'] = min(1.0, num_words * 0.15)
        
        # Generar texto resaltado
        detected_toxicity['highlighted_text'] = self._highlight_detected_words(
            text, 
            detected_toxicity['detected_words']
        )
        
        return detected_toxicity
    
    def _highlight_detected_words(self, original_text: str, detected_words: List[DetectedWord]) -> str:
        """
        Genera el texto con las palabras detectadas resaltadas con colores HTML.
        
        Args:
            original_text: Texto original
            detected_words: Lista de palabras detectadas
            
        Returns:
            Texto HTML con palabras resaltadas
        """
        if not detected_words:
            return original_text
        
        import html
        
        # Ordenar palabras por posición
        sorted_words = sorted(detected_words, key=lambda w: w.start)
        
        # Colores por tipo de toxicidad
        color_map = {
            ToxicityType.INSULT: '#ffc107',      # Amarillo (LOW)
            ToxicityType.PROFANITY: '#ffc107',   # Amarillo (LOW)
            ToxicityType.HARASSMENT: '#fd7e14',  # Naranja (MEDIUM)
            ToxicityType.THREAT: '#dc3545',      # Rojo (EXTREME)
            ToxicityType.HATE: '#6f42c1'         # Morado (EXTREME)
        }
        
        segments: List[str] = []
        last_end = 0
        text_len = len(original_text)
        
        for word in sorted_words:
            # Ignorar coincidencias inválidas
            if word.start < 0 or word.end > text_len or word.start >= word.end:
                continue
            
            # Saltar palabras que se superponen con la anterior ya resaltada
            if word.start < last_end:
                continue
            
            # Texto normal antes de la palabra detectada
            if word.start > last_end:
                segments.append(html.escape(original_text[last_end:word.start]))
            
            color = color_map.get(word.toxicity_type, '#ffc107')
            word_text = html.escape(original_text[word.start:word.end])
            toxicity_type_escaped = html.escape(word.toxicity_type.value)
            
            segments.append(
                '<span style="background-color: {color}; color: #000; font-weight: bold; '
                'padding: 2px 4px; border-radius: 3px;" title="{title}">{text}</span>'.format(
                    color=color,
                    title=toxicity_type_escaped,
                    text=word_text
                )
            )
            
            last_end = word.end
        
        # Añadir el resto del texto después de la última palabra resaltada
        if last_end < text_len:
            segments.append(html.escape(original_text[last_end:]))
        
        return ''.join(segments)
    
    def add_custom_pattern(self, pattern: str, toxicity_type: ToxicityType):
        """
        Añade un patrón personalizado al detector.
        
        Args:
            pattern: Patrón regex a añadir
            toxicity_type: Tipo de toxicidad
        """
        if toxicity_type not in self.toxic_patterns:
            self.toxic_patterns[toxicity_type] = []
        
        self.toxic_patterns[toxicity_type].append(pattern)
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas del autómata."""
        total_patterns = sum(len(patterns) for patterns in self.toxic_patterns.values())
        
        return {
            'total_states': 4,  # q0, q1, q2, q3
            'total_patterns': total_patterns,
            'patterns_by_type': {
                toxicity_type.value: len(patterns) 
                for toxicity_type, patterns in self.toxic_patterns.items()
            }
        }


# Instancia global del detector
toxic_detector = ToxicDetectorAutomaton()
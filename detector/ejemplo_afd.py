"""
Script de ejemplo que muestra el recorrido paso a paso del AFD
con un texto pequeño para entender cómo funciona.
"""

from automaton import ToxicDetectorAutomaton, ToxicityLevel, ToxicityType

def ejemplo_afd_paso_a_paso():
    """Muestra el recorrido del AFD con un ejemplo pequeño."""
    
    print("=" * 70)
    print("EJEMPLO: Recorrido del AFD paso a paso")
    print("=" * 70)
    print()
    
    # Crear instancia del autómata
    automaton = ToxicDetectorAutomaton()
    
    # Ejemplo 1: Texto simple con un insulto
    texto = "Eres un idiota"
    print(f"[TEXTO DE ENTRADA]: '{texto}'")
    print()
    
    print("[INICIALIZACION]:")
    print(f"   Estado inicial: {automaton.current_state} (SAFE)")
    print()
    
    # Procesar el texto
    resultado = automaton.process_text(texto)
    
    print("[PROCESAMIENTO]:")
    print(f"   1. Se busca el patron 'idiota' en el texto")
    print(f"   2. Se encuentra coincidencia: '{resultado['detected_words'][0].text}'")
    print(f"   3. Tipo detectado: {resultado['detected_words'][0].toxicity_type.value.upper()}")
    print()
    
    print("[TRANSICION DEL AFD]:")
    print(f"   Estado anterior: q0 (SAFE)")
    print(f"   Patron detectado: INSULT")
    print(f"   Funcion de transicion: delta(q0, INSULT) = q1")
    print(f"   Estado nuevo: {resultado['state']} ({resultado['level'].value.upper()})")
    print()
    
    print("[RESULTADO FINAL]:")
    print(f"   Es toxico?: {resultado['is_toxic']}")
    print(f"   Nivel de toxicidad: {resultado['level'].value.upper()}")
    print(f"   Estado del AFD: {resultado['state']}")
    print(f"   Tipos detectados: {', '.join(resultado['types'])}")
    print(f"   Confianza: {resultado['confidence'] * 100:.1f}%")
    print(f"   Palabras detectadas: {len(resultado['detected_words'])}")
    print()
    
    print("=" * 70)
    print()
    
    # Ejemplo 2: Texto con múltiples patrones
    texto2 = "Eres un idiota, ojala te mueras"
    print(f"[TEXTO DE ENTRADA]: '{texto2}'")
    print()
    
    automaton.reset()
    resultado2 = automaton.process_text(texto2)
    
    print("[PROCESAMIENTO PASO A PASO]:")
    print()
    
    estado_anterior = 'q0'
    for i, palabra in enumerate(resultado2['detected_words'], 1):
        print(f"   Paso {i}:")
        print(f"   - Detecta: '{palabra.text}'")
        print(f"   - Tipo: {palabra.toxicity_type.value.upper()}")
        
        # Simular la transición
        if estado_anterior == 'q0':
            if palabra.toxicity_type in [ToxicityType.INSULT, ToxicityType.PROFANITY]:
                nuevo_estado = 'q1'
            elif palabra.toxicity_type == ToxicityType.HARASSMENT:
                nuevo_estado = 'q2'
            else:
                nuevo_estado = 'q3'
        elif estado_anterior == 'q1':
            if palabra.toxicity_type in [ToxicityType.INSULT, ToxicityType.PROFANITY]:
                nuevo_estado = 'q1'
            elif palabra.toxicity_type == ToxicityType.HARASSMENT:
                nuevo_estado = 'q2'
            else:
                nuevo_estado = 'q3'
        elif estado_anterior == 'q2':
            if palabra.toxicity_type in [ToxicityType.THREAT, ToxicityType.HATE]:
                nuevo_estado = 'q3'
            else:
                nuevo_estado = 'q2'
        else:
            nuevo_estado = 'q3'  # Absorbente
        
        nivel = {
            'q0': 'SAFE',
            'q1': 'LOW',
            'q2': 'MEDIUM',
            'q3': 'EXTREME'
        }[nuevo_estado]
        
        print(f"   - Transicion: {estado_anterior} -> {nuevo_estado} ({nivel})")
        print()
        
        estado_anterior = nuevo_estado
    
    print("[RESULTADO FINAL]:")
    print(f"   Estado final del AFD: {resultado2['state']} ({resultado2['level'].value.upper()})")
    print(f"   Tipos detectados: {', '.join(resultado2['types'])}")
    print(f"   Confianza: {resultado2['confidence'] * 100:.1f}%")
    print()
    
    print("=" * 70)
    print()
    
    # Ejemplo 3: Mostrar la función de transición
    print("[TABLA DE TRANSICIONES (delta)]:")
    print()
    print("   Desde q0 (SAFE):")
    print("     - INSULT o PROFANITY -> q1 (LOW)")
    print("     - HARASSMENT -> q2 (MEDIUM)")
    print("     - THREAT o HATE -> q3 (EXTREME)")
    print()
    print("   Desde q1 (LOW):")
    print("     - INSULT o PROFANITY -> q1 (permanece)")
    print("     - HARASSMENT -> q2 (MEDIUM)")
    print("     - THREAT o HATE -> q3 (EXTREME)")
    print()
    print("   Desde q2 (MEDIUM):")
    print("     - INSULT, PROFANITY o HARASSMENT -> q2 (permanece)")
    print("     - THREAT o HATE -> q3 (EXTREME)")
    print()
    print("   Desde q3 (EXTREME):")
    print("     - Cualquier patron -> q3 (absorbente, permanece)")
    print()
    
    print("=" * 70)


if __name__ == "__main__":
    ejemplo_afd_paso_a_paso()


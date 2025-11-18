# FLUJO DE PROCESAMIENTO DETALLADO - DETECTOR DE LENGUAJE TÓXICO

## 📋 RESUMEN DEL PIPELINE

El sistema procesa texto en **6 pasos principales**:
1. **Normalización del texto**
2. **Búsqueda de patrones con regex**
3. **Registro de patrones encontrados**
4. **Clasificación con AFD (transiciones)**
5. **Determinación del nivel final**
6. **Cálculo de confianza**

---

## 🔍 PASO 1: NORMALIZACIÓN DEL TEXTO

**¿Qué hace?** Convierte el texto a minúsculas para búsqueda insensible a mayúsculas.

**Ubicación en el código:**
```python
# Archivo: detector/automaton.py
# Línea: 157

def process_text(self, text: str) -> Dict:
    self.reset()
    text_lower = text.lower()  # ← AQUÍ: Normalización
```

**Código completo:**
```python
# detector/automaton.py, línea 141-157
def process_text(self, text: str) -> Dict:
    """
    Procesa el texto de entrada usando expresiones regulares para encontrar patrones
    y un AFD para clasificar los resultados.
    """
    # Inicializar el AFD en el estado inicial q0
    self.reset()  # Línea 156
    text_lower = text.lower()  # ← PASO 1: Normalización (Línea 157)
```

**También se llama desde:**
- `detector/views.py`, línea 30: `analysis_result = toxic_detector.process_text(text)`
- `detector/views.py`, línea 88: `analysis_result = toxic_detector.process_text(text)`

---

## 🔍 PASO 2: BÚSQUEDA DE PATRONES CON EXPRESIONES REGULARES

**¿Qué hace?** Itera sobre todos los patrones regex y busca coincidencias en el texto.

**Ubicación en el código:**
```python
# Archivo: detector/automaton.py
# Líneas: 179-183

# Buscar patrones usando expresiones regulares
for toxicity_type, patterns in self.toxic_patterns.items():  # Línea 180
    for pattern in patterns:  # Línea 181
        # Buscar coincidencias usando regex
        if re.search(pattern, text_lower, re.IGNORECASE):  # ← PASO 2: Búsqueda regex (Línea 183)
```

**Código completo:**
```python
# detector/automaton.py, líneas 179-187
# PASO 1: USAR EXPRESIONES REGULARES PARA ENCONTRAR PATRONES
# Mapeo de tipos de toxicidad a estados del AFD
type_to_state = {
    ToxicityType.INSULT: 'q1',
    ToxicityType.THREAT: 'q2',
    ToxicityType.HATE: 'q3',
    ToxicityType.HARASSMENT: 'q4',
    ToxicityType.PROFANITY: 'q5'
}

# Buscar patrones usando expresiones regulares
for toxicity_type, patterns in self.toxic_patterns.items():  # Línea 180
    for pattern in patterns:  # Línea 181
        # Buscar coincidencias usando regex
        if re.search(pattern, text_lower, re.IGNORECASE):  # ← PASO 2 (Línea 183)
            # Guardar información del patrón encontrado
            detected_toxicity['is_toxic'] = True  # Línea 185
            detected_toxicity['types'].append(toxicity_type.value)  # Línea 186
            detected_toxicity['matched_patterns'].append(pattern)  # Línea 187
```

**Patrones definidos en:**
- `detector/automaton.py`, líneas 91-119: Método `_load_toxic_patterns()`

**Ejemplo de patrón:**
```python
# detector/automaton.py, líneas 94-97
ToxicityType.INSULT: [
    r'\b(estúpido|idiota|imbécil|tonto|burro|animal|cerdo|basura|mierda)\b',
    r'\b(puto|puta|hijo de puta|cabrón|gilipollas|capullo)\b',
    r'\b(inútil|fracasado|perdedor|basura humana)\b'
]
```

---

## 📝 PASO 3: REGISTRO DE PATRONES ENCONTRADOS

**¿Qué hace?** Guarda información sobre cada patrón que coincide: tipo, patrón regex, y marca el texto como tóxico.

**Ubicación en el código:**
```python
# Archivo: detector/automaton.py
# Líneas: 184-187

if re.search(pattern, text_lower, re.IGNORECASE):
    # Guardar información del patrón encontrado
    detected_toxicity['is_toxic'] = True  # ← PASO 3: Marcar como tóxico (Línea 185)
    detected_toxicity['types'].append(toxicity_type.value)  # ← PASO 3: Guardar tipo (Línea 186)
    detected_toxicity['matched_patterns'].append(pattern)  # ← PASO 3: Guardar patrón (Línea 187)
```

**Código completo:**
```python
# detector/automaton.py, líneas 183-187
if re.search(pattern, text_lower, re.IGNORECASE):
    # PASO 3: REGISTRO DE PATRONES ENCONTRADOS
    detected_toxicity['is_toxic'] = True  # Línea 185
    detected_toxicity['types'].append(toxicity_type.value)  # Línea 186
    detected_toxicity['matched_patterns'].append(pattern)  # Línea 187
```

**Estructura de `detected_toxicity`:**
```python
# detector/automaton.py, líneas 159-167
detected_toxicity = {
    'is_toxic': False,  # Se actualiza en PASO 3
    'level': ToxicityLevel.SAFE,
    'types': [],  # Se actualiza en PASO 3
    'matched_patterns': [],  # Se actualiza en PASO 3
    'confidence': 0.0,
    'original_text': text,
    'state_path': [self.current_state.name]  # Se actualiza en PASO 4
}
```

---

## 🔄 PASO 4: CLASIFICACIÓN CON AFD (TRANSICIONES)

**¿Qué hace?** Realiza transiciones en el AFD basándose en los patrones encontrados. Si encuentra un patrón, transiciona de q₀ a q₁-q₅. Si ya está en un estado tóxico y encuentra otro patrón, transiciona a q₆.

**Ubicación en el código:**
```python
# Archivo: detector/automaton.py
# Líneas: 189-194

# PASO 2: USAR EL AFD PARA CLASIFICAR
# Realizar transición en el AFD basada en el tipo de toxicidad encontrado
target_state = type_to_state.get(toxicity_type)  # Línea 191
if target_state:
    self._transition_to_state(target_state)  # ← PASO 4: Transición AFD (Línea 193)
    detected_toxicity['state_path'].append(self.current_state.name)  # Línea 194
```

**Función de transición:**
```python
# detector/automaton.py, líneas 125-139
def _transition_to_state(self, target_state_name: str):
    """
    Realiza una transición del AFD a un estado específico.
    """
    if target_state_name in self.states:
        # Si ya estamos en un estado tóxico (q1-q5) y encontramos otro patrón,
        # transicionar al estado final q6
        if self.current_state.name in ['q1', 'q2', 'q3', 'q4', 'q5']:  # Línea 135
            self.current_state = self.states['q6']  # ← Transición a q6 (Línea 136)
        else:
            # Transición desde q0 (estado inicial) al estado de detección
            self.current_state = self.states[target_state_name]  # ← Transición q0→q1/q2/q3/q4/q5 (Línea 139)
```

**Mapeo de tipos a estados:**
```python
# detector/automaton.py, líneas 171-177
type_to_state = {
    ToxicityType.INSULT: 'q1',      # Insulto → q1
    ToxicityType.THREAT: 'q2',      # Amenaza → q2
    ToxicityType.HATE: 'q3',         # Odio → q3
    ToxicityType.HARASSMENT: 'q4',   # Acoso → q4
    ToxicityType.PROFANITY: 'q5'     # Profanidad → q5
}
```

**Inicialización del AFD:**
```python
# detector/automaton.py, líneas 121-123
def reset(self):
    """Reinicia el autómata al estado inicial."""
    self.current_state = self.initial_state  # ← Vuelve a q0
```

**Estados definidos:**
```python
# detector/automaton.py, líneas 78-86
self.states = {
    'q0': State('q0', False, ToxicityLevel.SAFE),  # Estado inicial
    'q1': State('q1', False, ToxicityLevel.LOW, ToxicityType.INSULT),
    'q2': State('q2', False, ToxicityLevel.MEDIUM, ToxicityType.THREAT),
    'q3': State('q3', False, ToxicityLevel.HIGH, ToxicityType.HATE),
    'q4': State('q4', False, ToxicityLevel.MEDIUM, ToxicityType.HARASSMENT),
    'q5': State('q5', False, ToxicityLevel.LOW, ToxicityType.PROFANITY),
    'q6': State('q6', True, ToxicityLevel.EXTREME)  # Estado final tóxico
}
```

---

## 🎯 PASO 5: DETERMINACIÓN DEL NIVEL FINAL DE TOXICIDAD

**¿Qué hace?** Determina el nivel final de toxicidad basándose en el estado final del AFD.

**Ubicación en el código:**
```python
# Archivo: detector/automaton.py
# Líneas: 196-208

# Clasificación final basada en el estado del AFD
# El estado final del AFD determina el nivel de toxicidad
final_state = self.current_state  # ← PASO 5: Obtener estado final (Línea 198)

if final_state.name != 'q0':  # Si no estamos en el estado seguro
    detected_toxicity['level'] = final_state.toxicity_level  # ← PASO 5: Asignar nivel (Línea 201)
    
    # Si llegamos al estado final q6, el nivel es extremo
    if final_state.name == 'q6':  # Línea 204
        detected_toxicity['level'] = ToxicityLevel.EXTREME  # ← PASO 5: Nivel extremo (Línea 205)
else:
    # Si no se encontraron patrones, permanecemos en q0 (seguro)
    detected_toxicity['level'] = ToxicityLevel.SAFE  # ← PASO 5: Nivel seguro (Línea 208)
```

**Código completo:**
```python
# detector/automaton.py, líneas 196-208
# Clasificación final basada en el estado del AFD
# El estado final del AFD determina el nivel de toxicidad
final_state = self.current_state  # Línea 198

if final_state.name != 'q0':  # Si no estamos en el estado seguro
    detected_toxicity['level'] = final_state.toxicity_level  # Línea 201
    
    # Si llegamos al estado final q6, el nivel es extremo
    if final_state.name == 'q6':  # Línea 204
        detected_toxicity['level'] = ToxicityLevel.EXTREME  # Línea 205
else:
    # Si no se encontraron patrones, permanecemos en q0 (seguro)
    detected_toxicity['level'] = ToxicityLevel.SAFE  # Línea 208
```

**Mapeo de estados a niveles:**
- **q₀** → `ToxicityLevel.SAFE` (Seguro)
- **q₁** → `ToxicityLevel.LOW` (Bajo - Insultos)
- **q₂** → `ToxicityLevel.MEDIUM` (Medio - Amenazas)
- **q₃** → `ToxicityLevel.HIGH` (Alto - Odio)
- **q₄** → `ToxicityLevel.MEDIUM` (Medio - Acoso)
- **q₅** → `ToxicityLevel.LOW` (Bajo - Profanidad)
- **q₆** → `ToxicityLevel.EXTREME` (Extremo - Múltiples tipos)

---

## 📊 PASO 6: CÁLCULO DE CONFIANZA

**¿Qué hace?** Calcula el nivel de confianza del análisis basándose en el número de patrones encontrados.

**Ubicación en el código:**
```python
# Archivo: detector/automaton.py
# Líneas: 210-215

# Eliminar tipos duplicados
detected_toxicity['types'] = list(set(detected_toxicity['types']))  # Línea 211

# Calcular confianza basada en el número de patrones encontrados
if detected_toxicity['is_toxic']:  # Línea 214
    detected_toxicity['confidence'] = min(1.0, len(detected_toxicity['matched_patterns']) * 0.2)  # ← PASO 6 (Línea 215)
```

**Fórmula de confianza:**
```
confianza = min(1.0, número_de_patrones × 0.2)
```

**Ejemplos:**
- 1 patrón → confianza = 0.2 (20%)
- 2 patrones → confianza = 0.4 (40%)
- 3 patrones → confianza = 0.6 (60%)
- 4 patrones → confianza = 0.8 (80%)
- 5+ patrones → confianza = 1.0 (100%)

---

## 🔄 FLUJO COMPLETO EN EL SISTEMA

### **1. Entrada del usuario (Vista)**
```python
# detector/views.py, líneas 24-30
if request.method == 'POST':
    form = TextAnalysisForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']  # Texto del usuario
        
        # Realizar análisis con el autómata
        analysis_result = toxic_detector.process_text(text)  # ← Llama al pipeline
```

### **2. Procesamiento (Autómata)**
```python
# detector/automaton.py, línea 141
def process_text(self, text: str) -> Dict:
    # PASO 1: Normalización (línea 157)
    # PASO 2: Búsqueda regex (líneas 180-183)
    # PASO 3: Registro (líneas 185-187)
    # PASO 4: Transiciones AFD (líneas 191-194)
    # PASO 5: Nivel final (líneas 196-208)
    # PASO 6: Confianza (líneas 210-215)
    return detected_toxicity
```

### **3. Guardado en base de datos (Vista)**
```python
# detector/views.py, líneas 33-43
analysis = TextAnalysis.objects.create(
    text=text,
    is_toxic=analysis_result['is_toxic'],
    toxicity_level=analysis_result['level'].value,
    toxicity_types=analysis_result['types'],
    matched_patterns=analysis_result['matched_patterns'],
    confidence=analysis_result['confidence'],
    user=request.user if request.user.is_authenticated else None,
    ip_address=get_client_ip(request),
    user_agent=request.META.get('HTTP_USER_AGENT', '')
)
```

### **4. Actualización de estadísticas (Vista)**
```python
# detector/views.py, línea 46
update_statistics(analysis)  # Actualiza estadísticas diarias
```

### **5. Visualización (Template)**
```python
# detector/views.py, líneas 50-53
return render(request, 'detector/result.html', {
    'analysis': analysis,
    'analysis_result': analysis_result
})
```

---

## 📍 RESUMEN DE UBICACIONES EN EL CÓDIGO

| Paso | Descripción | Archivo | Líneas |
|------|-------------|---------|-------|
| **1** | Normalización del texto | `detector/automaton.py` | 157 |
| **2** | Búsqueda con regex | `detector/automaton.py` | 180-183 |
| **3** | Registro de patrones | `detector/automaton.py` | 185-187 |
| **4** | Transiciones AFD | `detector/automaton.py` | 125-139, 191-194 |
| **5** | Nivel final | `detector/automaton.py` | 196-208 |
| **6** | Cálculo de confianza | `detector/automaton.py` | 210-215 |
| **Inicialización** | Reset del AFD | `detector/automaton.py` | 121-123, 156 |
| **Llamada desde vista** | Invocación del pipeline | `detector/views.py` | 30, 88 |
| **Guardado en BD** | Persistencia de resultados | `detector/views.py` | 33-43 |
| **Estadísticas** | Actualización de métricas | `detector/views.py` | 46, 262-317 |

---

## 🎯 EJEMPLO COMPLETO DE EJECUCIÓN

**Texto de entrada:** `"Eres un estúpido y te voy a matar"`

### **Paso 1: Normalización**
```python
text_lower = "eres un estúpido y te voy a matar"
# Línea 157: text.lower()
```

### **Paso 2: Búsqueda regex**
```python
# Línea 183: re.search(pattern, text_lower, re.IGNORECASE)
# Encuentra: "estúpido" → ToxicityType.INSULT
# Encuentra: "te voy a matar" → ToxicityType.THREAT
```

### **Paso 3: Registro**
```python
# Líneas 185-187
detected_toxicity['is_toxic'] = True
detected_toxicity['types'] = ['insult', 'threat']
detected_toxicity['matched_patterns'] = [
    r'\b(estúpido|idiota|...)\b',
    r'\b(te voy a matar|te mato|...)\b'
]
```

### **Paso 4: Transiciones AFD**
```python
# Primera transición (línea 193)
# q₀ → q₁ (por insulto)
# state_path = ['q0', 'q1']

# Segunda transición (línea 193)
# q₁ → q₆ (por amenaza adicional)
# state_path = ['q0', 'q1', 'q6']
```

### **Paso 5: Nivel final**
```python
# Líneas 198-205
final_state = q₆
detected_toxicity['level'] = ToxicityLevel.EXTREME
```

### **Paso 6: Confianza**
```python
# Línea 215
detected_toxicity['confidence'] = min(1.0, 2 * 0.2) = 0.4 (40%)
```

### **Resultado final:**
```python
{
    'is_toxic': True,
    'level': ToxicityLevel.EXTREME,
    'types': ['insult', 'threat'],
    'matched_patterns': [...],
    'confidence': 0.4,
    'state_path': ['q0', 'q1', 'q6']
}
```

---

**Fin del documento**


# Recorrido del AFD en el Código - Explicación Detallada

## 🎯 Ejemplo Pequeño: "Eres un idiota"

### Paso 1: Inicialización (línea 190 en `automaton.py`)

```python
def process_text(self, text: str) -> Dict:
    self.reset()  # current_state = 'q0'
```

**Estado del AFD**: `q0` (SAFE)

---

### Paso 2: Búsqueda de Patrones (líneas 207-211)

```python
for toxicity_type, patterns in self.toxic_patterns.items():
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
```

**Acción**: Busca el patrón `"idiota"` en el texto `"Eres un idiota"`

**Resultado**: ✅ Encuentra coincidencia en la posición 9-15

---

### Paso 3: Crear Objeto DetectedWord (líneas 224-231)

```python
detected_word = DetectedWord(
    text="idiota",
    start=9,
    end=15,
    pattern=r"\bidiota\b",
    toxicity_type=ToxicityType.INSULT
)
detected_toxicity['detected_words'].append(detected_word)
```

**Información guardada**:
- Texto detectado: `"idiota"`
- Posición: caracteres 9-15
- Tipo: `INSULT`

---

### Paso 4: Aplicar Transición del AFD (líneas 234-235)

```python
new_state = self._transition(self.current_state, toxicity_type)
self.current_state = new_state
```

**Llamada a `_transition`** (líneas 127-168):

```python
def _transition(self, current_state: str, toxicity_type: ToxicityType) -> str:
    if current_state == 'q0':  # ← Estamos aquí
        if toxicity_type in [ToxicityType.INSULT, ToxicityType.PROFANITY]:
            return 'q1'  # ← Retorna q1
```

**Transición aplicada**: 
- Estado anterior: `q0` (SAFE)
- Patrón detectado: `INSULT`
- Función: `δ(q0, INSULT) = q1`
- Estado nuevo: `q1` (LOW)

---

### Paso 5: Actualizar Información (líneas 238-242)

```python
detected_toxicity['is_toxic'] = True
if toxicity_type.value not in detected_toxicity['types']:
    detected_toxicity['types'].append(toxicity_type.value)  # Añade 'insult'
if pattern not in detected_toxicity['matched_patterns']:
    detected_toxicity['matched_patterns'].append(pattern)
```

**Estado actualizado**:
- `is_toxic`: `True`
- `types`: `['insult']`
- `matched_patterns`: `[r'\bidiota\b']`

---

### Paso 6: Calcular Nivel Final (líneas 244-246)

```python
detected_toxicity['level'] = self._get_level_from_state(self.current_state)
detected_toxicity['state'] = self.current_state
```

**Función `_get_level_from_state`** (líneas 170-178):

```python
def _get_level_from_state(self, state: str) -> ToxicityLevel:
    state_to_level = {
        'q0': ToxicityLevel.SAFE,
        'q1': ToxicityLevel.LOW,  # ← Retorna LOW
        'q2': ToxicityLevel.MEDIUM,
        'q3': ToxicityLevel.EXTREME
    }
    return state_to_level.get(state, ToxicityLevel.SAFE)
```

**Resultado**: `ToxicityLevel.LOW`

---

### Paso 7: Calcular Confianza (líneas 249-251)

```python
if detected_toxicity['is_toxic']:
    num_words = len(detected_toxicity['detected_words'])  # = 1
    detected_toxicity['confidence'] = min(1.0, num_words * 0.15)  # = 0.15
```

**Cálculo**: `min(1.0, 1 * 0.15) = 0.15` → **15%**

---

### Paso 8: Generar Texto Resaltado (líneas 254-257)

```python
detected_toxicity['highlighted_text'] = self._highlight_detected_words(
    text, 
    detected_toxicity['detected_words']
)
```

**Función `_highlight_detected_words`** (líneas 261-325):
- Recibe: texto original y lista de palabras detectadas
- Genera HTML con `<span>` para resaltar palabras
- Retorna: `"Eres un <span style='background-color: #ffc107;...'>idiota</span>"`

---

## 📊 Resultado Final

```python
{
    'is_toxic': True,
    'level': ToxicityLevel.LOW,
    'state': 'q1',
    'types': ['insult'],
    'matched_patterns': [r'\bidiota\b'],
    'detected_words': [DetectedWord(text='idiota', start=9, end=15, ...)],
    'confidence': 0.15,
    'original_text': 'Eres un idiota',
    'highlighted_text': 'Eres un <span style="...">idiota</span>'
}
```

---

## 🔄 Flujo Visual del Código

```
┌─────────────────────────────────────────────────────────────┐
│ process_text("Eres un idiota")                              │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. reset() → current_state = 'q0'                          │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Bucle: Buscar patrones en texto                         │
│    re.finditer(pattern, text)                               │
│    → Encuentra "idiota" (INSULT)                           │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Crear DetectedWord                                       │
│    - text: "idiota"                                         │
│    - start: 9, end: 15                                      │
│    - type: INSULT                                           │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. _transition('q0', INSULT)                                │
│    → Retorna 'q1'                                           │
│    → current_state = 'q1'                                   │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Actualizar información                                   │
│    - is_toxic = True                                        │
│    - types.append('insult')                                 │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. _get_level_from_state('q1')                              │
│    → Retorna ToxicityLevel.LOW                              │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Calcular confianza                                       │
│    confidence = min(1.0, 1 * 0.15) = 0.15                  │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. _highlight_detected_words()                              │
│    → Genera HTML con palabras resaltadas                    │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Retornar diccionario con resultados                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Funciones Clave del Código

### 1. `_transition(current_state, toxicity_type)` (líneas 127-168)
**Propósito**: Aplica la función de transición δ del AFD

**Lógica**:
- Si estado es `q3` → siempre retorna `q3` (absorbente)
- Si estado es `q0`:
  - `INSULT` o `PROFANITY` → `q1`
  - `HARASSMENT` → `q2`
  - `THREAT` o `HATE` → `q3`
- Si estado es `q1`:
  - `INSULT` o `PROFANITY` → `q1` (permanece)
  - `HARASSMENT` → `q2`
  - `THREAT` o `HATE` → `q3`
- Si estado es `q2`:
  - `THREAT` o `HATE` → `q3`
  - Otros → `q2` (permanece)

### 2. `_get_level_from_state(state)` (líneas 170-178)
**Propósito**: Convierte estado del AFD (q0-q3) a nivel de toxicidad

**Mapeo**:
- `q0` → `SAFE`
- `q1` → `LOW`
- `q2` → `MEDIUM`
- `q3` → `EXTREME`

### 3. `_highlight_detected_words(text, detected_words)` (líneas 261-325)
**Propósito**: Genera HTML con palabras detectadas resaltadas

**Proceso**:
1. Ordena palabras por posición
2. Itera sobre el texto original
3. Inserta `<span>` con colores según tipo de toxicidad
4. Escapa HTML para prevenir XSS

---

## 💡 Puntos Importantes

1. **El AFD procesa de izquierda a derecha**: Cada patrón encontrado aplica una transición inmediata.

2. **El estado se actualiza en cada detección**: `current_state` cambia cada vez que se encuentra un patrón.

3. **q3 es absorbente**: Una vez que el AFD llega a `q3`, nunca puede volver a estados anteriores.

4. **Múltiples patrones**: Si se detectan varios patrones, cada uno aplica su transición en orden.

5. **La confianza es acumulativa**: Se calcula al final basándose en el número total de palabras detectadas.

---

## 🎓 Ejemplo con Múltiples Patrones

**Texto**: `"Eres un idiota, ojalá te mueras"`

**Recorrido**:
1. Detecta `"idiota"` (INSULT) → `q0` → `q1` (LOW)
2. Detecta `"ojalá te mueras"` (THREAT) → `q1` → `q3` (EXTREME)
3. **Estado final**: `q3` (EXTREME)
4. **Confianza**: `min(1.0, 2 * 0.15) = 0.30` (30%)

**Código relevante**:
```python
# Primera detección
new_state = self._transition('q0', ToxicityType.INSULT)  # → 'q1'
self.current_state = 'q1'

# Segunda detección
new_state = self._transition('q1', ToxicityType.THREAT)  # → 'q3'
self.current_state = 'q3'  # Estado final
```

---

## 🎓 Ejemplo: Secuencia LOW → MEDIUM → EXTREME

**Texto**: "Eres un idiota, deja de acosarme, te voy a matar"

Este ejemplo ilustra cómo el autómata escala progresivamente cuando detecta tres patrones con severidad creciente.

### Paso 1: Patrón LOW (`INSULT`)

```python
new_state = self._transition('q0', ToxicityType.INSULT)  # → 'q1'
self.current_state = 'q1'
```

- Estado anterior: `q0` (SAFE)
- Patrón detectado: "idiota" → `INSULT`
- Nuevo estado: `q1` (LOW)

### Paso 2: Patrón MEDIUM (`HARASSMENT`)

```python
new_state = self._transition('q1', ToxicityType.HARASSMENT)  # → 'q2'
self.current_state = 'q2'
```

- Estado anterior: `q1` (LOW)
- Patrón detectado: "deja de acosarme" → `HARASSMENT`
- Nuevo estado: `q2` (MEDIUM)

### Paso 3: Patrón EXTREME (`THREAT`)

```python
new_state = self._transition('q2', ToxicityType.THREAT)  # → 'q3'
self.current_state = 'q3'
```

- Estado anterior: `q2` (MEDIUM)
- Patrón detectado: "te voy a matar" → `THREAT`
- Nuevo estado: `q3` (EXTREME)

### Resultado Final

- Estado final del AFD: `q3` (EXTREME)
- Tipos detectados: `['insult', 'harassment', 'threat']`
- Confianza: `min(1.0, 3 * 0.15) = 0.45` (45%)


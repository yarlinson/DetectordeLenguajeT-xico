# Explicación del Recorrido del AFD (Autómata Finito Determinista)

## 📋 Componentes del AFD

**Quíntupla del AFD: M = (Q, Σ, δ, q₀, F)**

- **Q (Estados)**: `{q₀, q₁, q₂, q₃}`
  - `q₀`: Estado inicial → **SAFE** (Seguro)
  - `q₁`: Estado → **LOW** (Bajo)
  - `q₂`: Estado → **MEDIUM** (Medio)
  - `q₃`: Estado → **EXTREME** (Extremo) - **Estado absorbente**

- **Σ (Alfabeto)**: Patrones regex de toxicidad organizados por tipo:
  - `INSULT` (Insultos)
  - `PROFANITY` (Profanidad)
  - `HARASSMENT` (Acoso)
  - `THREAT` (Amenazas)
  - `HATE` (Odio)

- **δ (Función de Transición)**: Reglas que definen cómo cambiar de estado según el patrón detectado

- **q₀**: Estado inicial (`q0`)

- **F (Estados Finales)**: Todos los estados son finales `{q₀, q₁, q₂, q₃}`

---

## 🔄 Tabla de Transiciones

| Estado Actual | Patrón Detectado | Nuevo Estado | Nivel de Toxicidad |
|---------------|------------------|--------------|-------------------|
| q₀ | INSULT, PROFANITY | q₁ | LOW |
| q₀ | HARASSMENT | q₂ | MEDIUM |
| q₀ | THREAT, HATE | q₃ | EXTREME |
| q₁ | INSULT, PROFANITY | q₁ | LOW (permanece) |
| q₁ | HARASSMENT | q₂ | MEDIUM |
| q₁ | THREAT, HATE | q₃ | EXTREME |
| q₂ | INSULT, PROFANITY, HARASSMENT | q₂ | MEDIUM (permanece) |
| q₂ | THREAT, HATE | q₃ | EXTREME |
| q₃ | **Cualquier patrón** | q₃ | EXTREME (absorbente) |

---

## 📝 Ejemplo Paso a Paso

### Ejemplo 1: Texto Simple
**Texto de entrada**: `"Eres un idiota"`

#### Paso 1: Inicialización
```python
# En automaton.py, línea 190
self.reset()  # current_state = 'q0'
detected_toxicity = {
    'is_toxic': False,
    'level': ToxicityLevel.SAFE,
    'state': 'q0',
    'types': [],
    'matched_patterns': [],
    'detected_words': [],
    'confidence': 0.0
}
```

**Estado del AFD**: `q₀` (SAFE)

#### Paso 2: Búsqueda de Patrones
```python
# Líneas 207-211: Se itera sobre todos los patrones
for toxicity_type, patterns in self.toxic_patterns.items():
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Busca "idiota" en el texto
```

**Patrón encontrado**: `"idiota"` → Tipo: `INSULT`

#### Paso 3: Aplicar Transición
```python
# Línea 234: Aplicar función de transición
new_state = self._transition(self.current_state, toxicity_type)
# _transition('q0', INSULT) → retorna 'q1'
```

**Función de transición** (líneas 143-145):
```python
if current_state == 'q0':
    if toxicity_type in [ToxicityType.INSULT, ToxicityType.PROFANITY]:
        return 'q1'  # LOW
```

**Estado del AFD**: `q₀` → `q₁` (LOW)

#### Paso 4: Actualizar Información
```python
# Líneas 238-242
detected_toxicity['is_toxic'] = True
detected_toxicity['types'].append('insult')
detected_toxicity['matched_patterns'].append(pattern)
detected_toxicity['detected_words'].append(DetectedWord(...))
```

#### Paso 5: Calcular Nivel Final
```python
# Líneas 244-246
detected_toxicity['level'] = self._get_level_from_state('q1')
# Retorna: ToxicityLevel.LOW
```

#### Paso 6: Calcular Confianza
```python
# Líneas 249-251
num_words = 1  # Se detectó 1 palabra
confidence = min(1.0, 1 * 0.15) = 0.15  # 15%
```

**Resultado Final**:
```python
{
    'is_toxic': True,
    'level': ToxicityLevel.LOW,
    'state': 'q1',
    'types': ['insult'],
    'confidence': 0.15,
    'detected_words': [DetectedWord(text='idiota', start=9, end=15, ...)]
}
```

---

### Ejemplo 2: Texto con Múltiples Patrones
**Texto de entrada**: `"Eres un idiota, ojalá te mueras"`

#### Recorrido del AFD:

1. **Estado inicial**: `q₀` (SAFE)

2. **Detecta "idiota"** (INSULT):
   - `δ(q₀, INSULT) = q₁`
   - **Estado actual**: `q₁` (LOW)

3. **Detecta "ojalá te mueras"** (THREAT):
   - `δ(q₁, THREAT) = q₃`
   - **Estado actual**: `q₃` (EXTREME)

4. **Resultado**: 
   - Nivel: **EXTREME** (q₃)
   - Tipos: `['insult', 'threat']`
   - Confianza: `min(1.0, 2 * 0.15) = 0.30` (30%)

---

### Ejemplo 3: Estado Absorbente
**Texto de entrada**: `"Te voy a matar, eres basura, muérete"`

#### Recorrido:

1. **q₀** → Detecta "matar" (THREAT) → **q₃** (EXTREME)

2. **q₃** → Detecta "basura" (INSULT) → **q₃** (permanece en EXTREME)
   ```python
   # Línea 139: Estado absorbente
   if current_state == 'q3':
       return 'q3'  # Siempre permanece en q3
   ```

3. **q₃** → Detecta "muérete" (THREAT) → **q₃** (permanece)

**Resultado**: Nivel **EXTREME** (una vez que llega a q₃, nunca baja)

---

## 🔍 Flujo Completo en el Código

```
1. process_text(text) [línea 180]
   │
   ├─> reset() [línea 190]
   │   └─> current_state = 'q0'
   │
   ├─> Bucle: Buscar patrones [líneas 207-242]
   │   │
   │   ├─> re.finditer(pattern, text) [línea 211]
   │   │   └─> Encuentra coincidencia
   │   │
   │   ├─> _transition(current_state, toxicity_type) [línea 234]
   │   │   └─> Calcula nuevo estado según tabla de transiciones
   │   │
   │   ├─> Actualiza current_state [línea 235]
   │   │
   │   └─> Guarda palabra detectada [líneas 224-231]
   │
   ├─> _get_level_from_state(current_state) [línea 245]
   │   └─> Convierte estado (q0-q3) a nivel (SAFE-EXTREME)
   │
   ├─> Calcula confianza [líneas 249-251]
   │
   └─> _highlight_detected_words() [línea 254]
       └─> Genera HTML con palabras resaltadas
```

---

## 💡 Puntos Clave

1. **El AFD procesa el texto de izquierda a derecha**, aplicando transiciones cada vez que encuentra un patrón.

2. **El estado final es el más alto alcanzado**: Si el texto pasa por q₀ → q₁ → q₃, el resultado es q₃ (EXTREME).

3. **q₃ es absorbente**: Una vez que el AFD llega a q₃, permanece ahí sin importar qué más detecte.

4. **Múltiples patrones del mismo tipo**: Si detecta varios insultos, permanece en q₁ (LOW) hasta que detecte algo más grave.

5. **La confianza se calcula al final**: Basada en el número total de palabras detectadas (máximo 1.0 = 100%).

---

## 🎯 Resumen Visual

```
Texto: "Eres un idiota, ojalá te mueras"
       ↓
[Inicio: q₀ (SAFE)]
       ↓
Detecta "idiota" (INSULT)
       ↓
[q₁ (LOW)]
       ↓
Detecta "ojalá te mueras" (THREAT)
       ↓
[q₃ (EXTREME)] ← Estado final
       ↓
Resultado: EXTREME, tipos: [insult, threat], confianza: 30%
```


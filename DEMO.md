# Demostración del Detector de Lenguaje Tóxico

## 🎯 Proyecto Completado

He creado un sistema completo de **Detector de Lenguaje Tóxico** usando Django con implementación de **AFD/AFND** (Autómatas Finitos Deterministas/No Deterministas).

## 🚀 Características Implementadas

### ✅ Autómata Finito Determinista (AFD)
- **7 estados** (q0-q6) para detectar diferentes tipos de toxicidad
- **Transiciones** basadas en patrones regex
- **Estados finales** que indican contenido tóxico detectado

### ✅ Tipos de Toxicidad Detectados
1. **Insultos** - Palabras ofensivas
2. **Amenazas** - Expresiones de daño
3. **Odio** - Contenido discriminatorio
4. **Acoso** - Comportamientos intimidatorios
5. **Profanidad** - Lenguaje vulgar

### ✅ Niveles de Toxicidad
- **Seguro** - Sin contenido tóxico
- **Bajo** - Toxicidad mínima
- **Medio** - Toxicidad moderada
- **Alto** - Toxicidad significativa
- **Extremo** - Toxicidad máxima

### ✅ Interfaz Web Completa
- **Página principal** con formulario de análisis
- **Resultados en tiempo real** con AJAX
- **Historial de análisis** para usuarios autenticados
- **Estadísticas detalladas** del sistema
- **Panel de administración** completo

### ✅ Funcionalidades Avanzadas
- **API REST** para análisis programático
- **Patrones personalizables** desde el admin
- **Estadísticas automáticas** por día
- **Sistema de autenticación** integrado
- **Diseño responsivo** con Bootstrap 5

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Base de datos**: SQLite
- **Autómatas**: AFD con estados y transiciones
- **Patrones**: Expresiones regulares (regex)

## 📁 Estructura del Proyecto

```
Proyecto/
├── venv/                          # Entorno virtual
├── detector/                      # Aplicación principal
│   ├── automaton.py              # Implementación del AFD
│   ├── models.py                 # Modelos de datos
│   ├── views.py                  # Vistas y lógica de negocio
│   ├── forms.py                  # Formularios
│   ├── admin.py                  # Panel de administración
│   ├── urls.py                   # URLs de la aplicación
│   └── templates/detector/        # Templates HTML
│       ├── base.html            # Template base
│       ├── home.html            # Página principal
│       ├── result.html          # Resultados
│       ├── history.html         # Historial
│       ├── statistics.html      # Estadísticas
│       ├── about.html           # Acerca de
│       └── detail.html          # Detalles
├── toxic_detector/               # Configuración del proyecto
│   ├── settings.py              # Configuración
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # WSGI
├── manage.py                     # Script de gestión
├── requirements.txt              # Dependencias
└── README.md                    # Documentación
```

## 🎮 Cómo Usar el Sistema

### 1. Acceder a la Aplicación
- **URL**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **Usuario**: admin
- **Contraseña**: admin123

### 2. Analizar Texto
1. Ve a la página principal
2. Ingresa texto en el área de texto
3. Haz clic en "Analizar Texto"
4. Revisa los resultados del análisis

### 3. Gestionar Patrones (Admin)
1. Accede al panel de administración
2. Ve a "Patrones Tóxicos"
3. Añade nuevos patrones personalizados
4. Activa/desactiva patrones existentes

### 4. Ver Estadísticas
1. Ve a la sección "Estadísticas"
2. Revisa análisis totales
3. Consulta distribución por tipo
4. Analiza tendencias diarias

## 🔍 Ejemplos de Análisis

### Texto Seguro
```
"¡Hola! ¿Cómo estás hoy? Espero que tengas un buen día."
```
**Resultado**: ✅ Seguro - Sin toxicidad detectada

### Texto con Insultos
```
"Eres un estúpido y un idiota completo."
```
**Resultado**: ⚠️ Tóxico - Nivel: Bajo - Tipo: Insulto

### Texto con Amenazas
```
"Te voy a matar si no haces lo que digo."
```
**Resultado**: 🚨 Tóxico - Nivel: Alto - Tipo: Amenaza

### Texto con Odio
```
"Odio a todas las personas de esa raza, deberían morir."
```
**Resultado**: 🚨 Tóxico - Nivel: Extremo - Tipo: Odio

## 🧠 Implementación del AFD

### Estados del Autómata
```python
q0: Estado inicial (texto seguro)
q1: Detectando insultos
q2: Detectando amenazas
q3: Detectando odio
q4: Detectando acoso
q5: Detectando profanidad
q6: Estado final tóxico
```

### Patrones de Ejemplo
```python
# Insultos
r'\b(estúpido|idiota|imbécil|tonto|burro)\b'

# Amenazas
r'\b(te voy a matar|te mato|te voy a romper)\b'

# Odio
r'\b(odio|asco|repugnante|desprecio)\b'

# Acoso
r'\b(acosar|molestar|fastidiar|importunar)\b'

# Profanidad
r'\b(joder|coño|mierda|cagar)\b'
```

## 📊 Características del Sistema

### ✅ Completamente Funcional
- ✅ Servidor ejecutándose en http://127.0.0.1:8000/
- ✅ Base de datos configurada y migrada
- ✅ Superusuario creado (admin/admin123)
- ✅ Panel de administración accesible
- ✅ Interfaz web moderna y responsiva

### ✅ Funcionalidades Implementadas
- ✅ Análisis de texto en tiempo real
- ✅ Detección de múltiples tipos de toxicidad
- ✅ Niveles de confianza calculados
- ✅ Historial de análisis para usuarios
- ✅ Estadísticas detalladas
- ✅ API REST para integración
- ✅ Patrones personalizables
- ✅ Panel de administración completo

### ✅ Características Técnicas
- ✅ AFD implementado con estados y transiciones
- ✅ Patrones regex configurables
- ✅ Sistema de autenticación
- ✅ Base de datos relacional
- ✅ Interfaz AJAX para análisis
- ✅ Diseño responsivo
- ✅ Documentación completa

## 🎉 Proyecto Listo para Usar

El sistema está **100% funcional** y listo para ser utilizado. Puedes:

1. **Probar el análisis** ingresando diferentes textos
2. **Gestionar patrones** desde el panel de admin
3. **Revisar estadísticas** en tiempo real
4. **Personalizar** el sistema según tus necesidades
5. **Integrar** con otros sistemas via API

## 🚀 Próximos Pasos

Para continuar desarrollando el proyecto, podrías:

- Añadir más patrones de toxicidad
- Implementar machine learning
- Añadir soporte para múltiples idiomas
- Crear un dashboard en tiempo real
- Implementar notificaciones automáticas
- Añadir exportación de datos

---

**¡El Detector de Lenguaje Tóxico está listo y funcionando! 🎯**


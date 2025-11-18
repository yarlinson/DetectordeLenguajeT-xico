# Detector de Lenguaje Tóxico con AFD/AFND

Un sistema inteligente de análisis de texto desarrollado en Django que utiliza autómatas finitos deterministas (AFD) para detectar contenido agresivo o tóxico en tiempo real.

## 🚀 Características

- **Detección en tiempo real** de lenguaje tóxico usando AFD
- **Múltiples tipos de toxicidad**: insultos, amenazas, odio, acoso, profanidad
- **Niveles de toxicidad**: seguro, bajo, medio, alto, extremo
- **Interfaz web moderna** con Bootstrap 5
- **Panel de administración** completo para gestionar patrones
- **Estadísticas detalladas** y análisis histórico
- **API REST** para integración con otros sistemas
- **Patrones personalizables** desde el panel de admin

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Base de datos**: SQLite (desarrollo)
- **Autómatas**: AFD (Autómata Finito Determinista)
- **Patrones**: Expresiones regulares (regex)

## 📋 Requisitos

- Python 3.8+
- pip
- Entorno virtual (recomendado)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
# Si tienes git
git clone <url-del-repositorio>
cd toxic-detector

# O simplemente descargar y extraer el archivo ZIP
```

### 2. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

### 7. Acceder a la aplicación

- **Aplicación principal**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/

## 🎯 Uso del Sistema

### Análisis de Texto

1. Ve a la página principal
2. Ingresa el texto que deseas analizar
3. Haz clic en "Analizar Texto"
4. Revisa los resultados del análisis

### Panel de Administración

1. Accede a `/admin/`
2. Inicia sesión con tu superusuario
3. Gestiona patrones tóxicos en "Patrones Tóxicos"
4. Revisa análisis en "Análisis de Textos"
5. Consulta estadísticas en "Estadísticas de Análisis"

### API REST

```bash
# Analizar texto via API
curl -X POST http://127.0.0.1:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Tu texto aquí"}'
```

## 🏗️ Arquitectura del Sistema

### Autómata Finito Determinista (AFD)

El sistema utiliza un AFD con los siguientes estados:

- **q0**: Estado inicial (texto seguro)
- **q1**: Detectando insultos
- **q2**: Detectando amenazas  
- **q3**: Detectando odio
- **q4**: Detectando acoso
- **q5**: Detectando profanidad
- **q6**: Estado final tóxico

### Modelos de Datos

- **TextAnalysis**: Almacena análisis de texto y resultados
- **ToxicPattern**: Patrones personalizables de toxicidad
- **AnalysisStatistics**: Estadísticas diarias del sistema

### Tipos de Toxicidad Detectados

1. **Insultos**: Palabras ofensivas dirigidas a personas
2. **Amenazas**: Expresiones que implican daño físico o psicológico
3. **Odio**: Contenido que promueve discriminación o violencia
4. **Acoso**: Comportamientos intimidatorios o persistentes
5. **Profanidad**: Lenguaje vulgar o inapropiado

## 📊 Estadísticas

El sistema proporciona estadísticas detalladas:

- Análisis totales realizados
- Distribución por nivel de toxicidad
- Distribución por tipo de toxicidad
- Estadísticas diarias
- Tasas de toxicidad y seguridad

## 🔒 Seguridad y Privacidad

- Los textos analizados se almacenan de forma segura
- No se comparten datos personales
- Los patrones específicos se mantienen confidenciales
- Sistema de autenticación integrado

## 🎨 Interfaz de Usuario

- **Diseño responsivo** que funciona en móviles y escritorio
- **Interfaz intuitiva** con iconos y colores informativos
- **Análisis en tiempo real** con AJAX
- **Resultados visuales** con barras de progreso y badges
- **Navegación fácil** entre secciones

## 🔧 Personalización

### Añadir Nuevos Patrones

1. Accede al panel de administración
2. Ve a "Patrones Tóxicos"
3. Haz clic en "Añadir Patrón Tóxico"
4. Completa los campos:
   - **Nombre**: Descripción del patrón
   - **Patrón**: Expresión regular
   - **Tipo de toxicidad**: Categoría
   - **Nivel de toxicidad**: Severidad
   - **Descripción**: Detalles adicionales

### Ejemplos de Patrones

```regex
# Insultos básicos
\b(estúpido|idiota|imbécil)\b

# Amenazas
\b(te voy a matar|te mato)\b

# Profanidad
\b(joder|coño|mierda)\b
```

## 🐛 Solución de Problemas

### Error de migraciones

```bash
# Si hay problemas con migraciones
python manage.py migrate --fake-initial
```

### Error de permisos

```bash
# En Linux/Mac, asegúrate de tener permisos de escritura
chmod +x manage.py
```

### Puerto ocupado

```bash
# Usar un puerto diferente
python manage.py runserver 8080
```

## 📈 Mejoras Futuras

- [ ] Integración con APIs de detección de toxicidad externas
- [ ] Machine Learning para mejorar la precisión
- [ ] Soporte para múltiples idiomas
- [ ] API más robusta con autenticación
- [ ] Dashboard en tiempo real
- [ ] Notificaciones automáticas
- [ ] Exportación de datos
- [ ] Integración con sistemas de moderación

## 📝 Licencia

Este proyecto es una demostración educativa de cómo implementar un detector de toxicidad usando autómatas finitos deterministas.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas:

- Revisa la documentación
- Consulta los logs del sistema
- Verifica la configuración de la base de datos
- Asegúrate de que todas las dependencias estén instaladas

---

**Desarrollado con ❤️ usando Django y AFD/AFND**




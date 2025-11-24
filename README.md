# Detector de Lenguaje Tóxico con AFD/AFND

Un sistema inteligente de análisis de texto desarrollado en Django que utiliza autómatas finitos deterministas (AFD) para detectar contenido agresivo o tóxico en tiempo real.

## 🚀 Características

- **Detección en tiempo real** de lenguaje tóxico usando AFD (Autómata Finito Determinista)
- **5 tipos de toxicidad**: insultos, profanidad, acoso, amenazas, odio
- **4 niveles de toxicidad**: SAFE (seguro), LOW (bajo), MEDIUM (medio), EXTREME (extremo)
- **Interfaz web moderna** con Bootstrap 5 y diseño responsivo
- **Panel de administración** completo para gestionar patrones
- **Estadísticas detalladas** y análisis histórico
- **API REST** para integración con otros sistemas
- **Patrones personalizables** desde el panel de admin
- **Dockerización completa** para fácil despliegue
- **Explicación detallada del AFD** con diagramas y ejemplos

## ⚡ Inicio Rápido con Docker

```bash
# 1. Clonar el proyecto
git clone <url-del-repositorio>
cd toxic-detector

# 2. Levantar el contenedor
docker-compose up --build

# 3. Crear superusuario (en otra terminal)
docker-compose exec web python manage.py createsuperuser

# 4. Acceder a la aplicación
# http://localhost:8000/
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript (AJAX)
- **Base de datos**: SQLite (desarrollo)
- **Autómatas**: AFD (Autómata Finito Determinista) con 4 estados
- **Patrones**: Expresiones regulares (regex)
- **Contenedores**: Docker y Docker Compose
- **Procesamiento de archivos**: PyPDF2, BeautifulSoup (PDF, TXT, HTML)

## 📋 Requisitos

### Opción 1: Docker (Recomendado)
- Docker
- Docker Compose

### Opción 2: Instalación Local
- Python 3.8+
- pip
- Entorno virtual (recomendado)

## 🔧 Instalación

### Opción 1: Docker (Recomendado) 🐳

#### 1. Clonar o descargar el proyecto

```bash
# Si tienes git
git clone <url-del-repositorio>
cd toxic-detector

# O simplemente descargar y extraer el archivo ZIP
```

#### 2. Construir y ejecutar con Docker Compose

```bash
# Construir y levantar el contenedor
docker-compose up --build

# O en modo detached (en segundo plano)
docker-compose up -d --build
```

#### 3. Crear superusuario (primera vez)

```bash
# Ejecutar comando dentro del contenedor
docker-compose exec web python manage.py createsuperuser
```

#### 4. Acceder a la aplicación

- **Aplicación principal**: http://localhost:8000/
- **Panel de administración**: http://localhost:8000/admin/

#### Comandos útiles de Docker Compose

```bash
# Ver logs del contenedor
docker-compose logs -f

# Detener el contenedor
docker-compose down

# Detener y eliminar volúmenes (elimina la base de datos)
docker-compose down -v

# Ejecutar comandos Django dentro del contenedor
docker-compose exec web python manage.py <comando>

# Ejecutar shell de Django
docker-compose exec web python manage.py shell

# Reconstruir la imagen
docker-compose build --no-cache

# Ver contenedores en ejecución
docker-compose ps

# Reiniciar el contenedor
docker-compose restart
```

#### Usar Docker sin Docker Compose

Si prefieres usar solo Docker (sin docker-compose):

```bash
# Construir la imagen
docker build -t toxic-detector .

# Ejecutar el contenedor
docker run -d \
  --name toxic_detector \
  -p 8000:8000 \
  -v $(pwd):/app \
  toxic-detector

# Crear superusuario
docker exec -it toxic_detector python manage.py createsuperuser

# Ver logs
docker logs -f toxic_detector

# Detener el contenedor
docker stop toxic_detector

# Eliminar el contenedor
docker rm toxic_detector
```

#### Solución de problemas con Docker

```bash
# Si el contenedor no inicia, verifica los logs
docker-compose logs web

# Si hay problemas con permisos en Windows
# Asegúrate de compartir la unidad en Docker Desktop

# Si necesitas limpiar todo y empezar de nuevo
docker-compose down -v
docker system prune -a
docker-compose up --build

# Si el puerto 8000 está ocupado, cambia el puerto en docker-compose.yml
# Cambia "8000:8000" por "8080:8000" y accede en http://localhost:8080
```

### Opción 2: Instalación Local

#### 1. Clonar o descargar el proyecto

```bash
# Si tienes git
git clone <url-del-repositorio>
cd toxic-detector

# O simplemente descargar y extraer el archivo ZIP
```

#### 2. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar la base de datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

#### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

#### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

#### 7. Acceder a la aplicación

- **Aplicación principal**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/

## 🎯 Uso del Sistema

### Análisis de Texto

1. Ve a la página principal
2. Ingresa el texto que deseas analizar
3. Haz clic en "Analizar Texto"
4. Revisa los resultados del análisis

### 📋 Ejemplos para Probar

Para probar el sistema con diferentes casos, tienes dos opciones:

1. **[EJEMPLOS_PRUEBA.md](EJEMPLOS_PRUEBA.md)** - Documento completo con:
   - Textos seguros (sin toxicidad)
   - Ejemplos de cada tipo de toxicidad (insultos, amenazas, odio, acoso, profanidad)
   - Textos con diferentes niveles de toxicidad
   - Casos especiales y edge cases
   - Textos mixtos con múltiples tipos de toxicidad
   - Variantes regionales (colombiano)
   - Guía de uso para pruebas

2. **[ejemplos_rapidos.txt](ejemplos_rapidos.txt)** - Archivo simple con ejemplos listos para copiar y pegar rápidamente

### Páginas Disponibles

- **Página Principal** (`/`): Interfaz para analizar texto en tiempo real
- **Acerca de** (`/about/`): Información general sobre el sistema y su funcionamiento
- **Explicación del AFD** (`/automaton/`): Explicación detallada del autómata finito determinista con diagramas y ejemplos
- **Estadísticas** (`/statistics/`): Estadísticas generales del sistema
- **Historial** (`/history/`): Historial de análisis realizados (requiere autenticación)

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

El sistema utiliza un AFD con 4 estados para clasificar el nivel de toxicidad:

- **q₀ (SAFE)**: Estado inicial - Texto seguro sin toxicidad detectada
- **q₁ (LOW)**: Toxicidad baja - Detecta insultos o profanidad
- **q₂ (MEDIUM)**: Toxicidad media - Detecta acoso
- **q₃ (EXTREME)**: Toxicidad extrema - Detecta amenazas u odio (estado absorbente)

#### Reglas de Transición

**Desde q₀ (SAFE):**
- INSULT o PROFANITY → q₁ (LOW)
- HARASSMENT → q₂ (MEDIUM)
- THREAT o HATE → q₃ (EXTREME)

**Desde q₁ (LOW):**
- INSULT o PROFANITY → q₁ (permanece en LOW)
- HARASSMENT → q₂ (sube a MEDIUM)
- THREAT o HATE → q₃ (sube a EXTREME)

**Desde q₂ (MEDIUM):**
- INSULT, PROFANITY o HARASSMENT → q₂ (permanece en MEDIUM)
- THREAT o HATE → q₃ (sube a EXTREME)

**Desde q₃ (EXTREME):**
- Cualquier patrón → q₃ (estado absorbente, permanece en EXTREME)

> **Nota:** El estado q₃ es absorbente, lo que significa que una vez alcanzado, el autómata permanece ahí sin importar qué más detecte. Todos los estados son estados finales.

### Modelos de Datos

- **TextAnalysis**: Almacena análisis de texto y resultados
- **ToxicPattern**: Patrones personalizables de toxicidad
- **AnalysisStatistics**: Estadísticas diarias del sistema

### Niveles de Toxicidad

El sistema clasifica el texto en 4 niveles de toxicidad:

- **SAFE (Seguro)** 🟢 - Verde (#28a745)
  - No se detectó ningún patrón tóxico
  - Estado inicial del AFD (q₀)

- **LOW (Bajo)** 🟡 - Amarillo/Naranja claro (#ffc107)
  - Detecta insultos o profanidad
  - Estado q₁ del AFD

- **MEDIUM (Medio)** 🟠 - Naranja (#fd7e14)
  - Detecta acoso
  - Estado q₂ del AFD

- **EXTREME (Extremo)** 🔴 - Rojo (#dc3545)
  - Detecta amenazas u odio
  - Estado q₃ del AFD (estado absorbente)

### Tipos de Toxicidad Detectados

1. **Insultos (INSULT)** - Nivel: LOW 🟡
   - Palabras ofensivas dirigidas a personas
   - Descalificaciones, epítetos ofensivos, expresiones de desprecio
   - Color: Amarillo (#ffc107)

2. **Profanidad (PROFANITY)** - Nivel: LOW 🟡
   - Lenguaje vulgar o inapropiado
   - Palabrotas, maldiciones, blasfemias
   - Color: Amarillo (#ffc107)

3. **Acoso (HARASSMENT)** - Nivel: MEDIUM 🟠
   - Comportamientos intimidatorios o persistentes
   - Expresiones de persecución, amenazas de acoso continuo
   - Color: Naranja (#fd7e14)

4. **Amenazas (THREAT)** - Nivel: EXTREME 🔴
   - Expresiones que implican daño físico o psicológico
   - Amenazas de muerte, violencia física, venganza
   - Color: Rojo (#dc3545)

5. **Odio (HATE)** - Nivel: EXTREME 🔴
   - Contenido que promueve discriminación o violencia
   - Expresiones de odio general, términos discriminatorios, deshumanización
   - Color: Rojo (#dc3545)

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

### Docker

#### Error de migraciones en Docker

```bash
# Ejecutar migraciones manualmente
docker-compose exec web python manage.py migrate

# O forzar migraciones
docker-compose exec web python manage.py migrate --fake-initial
```

#### Puerto ocupado en Docker

```bash
# Cambiar el puerto en docker-compose.yml
# Cambia "8000:8000" por "8080:8000"
# Luego accede en http://localhost:8080
```

#### Problemas con volúmenes en Docker

```bash
# Si los cambios no se reflejan, reconstruye la imagen
docker-compose down
docker-compose build --no-cache
docker-compose up
```

#### Error "Permission denied" en Docker (Linux/Mac)

```bash
# Asegúrate de que el script entrypoint.sh tenga permisos de ejecución
chmod +x entrypoint.sh
```

### Instalación Local

#### Error de migraciones

```bash
# Si hay problemas con migraciones
python manage.py migrate --fake-initial
```

#### Error de permisos

```bash
# En Linux/Mac, asegúrate de tener permisos de escritura
chmod +x manage.py
```

#### Puerto ocupado

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




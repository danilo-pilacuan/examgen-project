### Ítems de Acción

- [ ]  Danilo: Configurar el endpoint del modelo de forma dinámica (apuntar al servidor BLLM y cambiar solo el nombre del modelo, sin hardcodear)
- [ ]  Danilo: Desplegar la versión actualizada al servidor y notificar a Felipe para que pueda acceder y hacer pruebas
- [ ]  Danilo: Guardar en la base de datos el **Raw Answer** (respuesta completa del modelo) y el **Raw Thinking** (cadena de pensamiento) como columnas separadas
- [ ]  Danilo: Agregar tool para **eliminar archivos** del sistema
- [ ]  Danilo: Agregar tool para **eliminar preguntas** por ID
- [ ]  Danilo: Agregar tool para **descargar el JSON** generado antes de pasar a la plantilla LaTeX
- [ ]  Danilo: Añadir instrucción en el **prompt del sistema** para forzar que todo sea en inglés
- [ ]  Danilo: Investigar si la clase `exam` de LaTeX soporta aleatorización y generación de múltiples versiones; confirmar o implementar lógica de **random seeds**
- [ ]  Danilo: Explorar e implementar un **dashboard** que liste materias y preguntas, posiblemente con el Open Web UI embebido
- [ ]  Objetivo: cerrar el proyecto en **octubre**

---

### Contexto General del Sistema

- La interfaz usa **Open Web UI** customizado, conectado directamente a un agente propio
- El agente expone herramientas (tools) específicas y restringe los inputs disponibles (sin generación de imágenes, sin conectores externos)
- La base de datos usa **PostgreSQL** para datos estructurados y la extensión **pgVector** para embeddings
- Los archivos subidos se convierten a embeddings vía RAG y se almacenan en un volumen Docker

### Problema Técnico: Cambio de Endpoint

- El equipo de infraestructura reemplazó el modelo **DeepSeek** por **GLM**, lo que dejó el despliegue apuntando al modelo anterior
- Felipe solicitó que el modelo sea configurable sin necesidad de redesplegar toda la aplicación
- Solución acordada: apuntar siempre al servidor BLLM y parametrizar solo el nombre del modelo

### Demo del Sistema

- Se pueden **registrar materias** por chat; se guardan con ID en PostgreSQL
- Se pueden **subir archivos** (PDF, diapositivas); se indexan como embeddings
- Se pueden **generar preguntas** con metadatos: tema, nivel de dificultad, etiqueta de Bloom, respuesta esperada y opciones en JSON
- Se pueden **listar materias** y **listar preguntas** mediante lenguaje natural; el agente llama a la tool correspondiente
- La generación de exámenes usa plantillas **Jinja → LaTeX** a partir de un JSON estructurado

### Funcionalidades Pendientes y Mejoras Discutidas

- **Eliminación de archivos y preguntas**: actualmente no hay tools para borrar; se acordó implementarlas
- **Almacenamiento de respuesta cruda y pensamiento**: se quiere preservar el razonamiento completo del modelo para análisis futuros o verificación con un LLM más avanzado
- **Aleatorización y versiones de examen**: se requiere soporte para versiones A/B/C/D con hojas de respuestas; confirmar si la clase `exam` lo soporta o implementarlo manualmente con random seeds
- **Filtrado por topic en el banco de preguntas**: cada pregunta tiene etiquetas de tema (ej. "regresión lineal") que permiten seleccionar preguntas por categoría antes de enviar a LaTeX
- **Idioma**: todo el sistema debe operar en inglés; si se necesita español, se traduce en otro paso
- **Visibilidad de ejecución de tools**: Felipe quiere ver qué tool se ejecuta en cada momento para evitar alucinaciones
- **Dashboard**: se discutió crear un dashboard separado que liste materias y preguntas, con posibilidad de embeber el Open Web UI como un chat widget
- **Descarga del JSON intermedio**: agregar opción de descargar el JSON antes del renderizado LaTeX, para tener acceso a la data cruda
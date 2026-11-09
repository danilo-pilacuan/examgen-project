### Acciones y próximos pasos

- [ ]  Danilo: agregar en el Question Bank los campos de fecha y hora de creación y de verificación de cada pregunta
- [ ]  Danilo: añadir al flujo "Generate" de exámenes una selección por checkboxes de los tipos de pregunta a incluir (por ejemplo, solo multiple choice)
- [ ]  Danilo: compartir el repositorio con Felipe y dejar el levante automático (una sola instrucción tipo "Claude, levanta esto"), con Docker como único requisito
- [ ]  Danilo: hacer el mini QA / capacitación de uso con la asistente de cátedra de Felipe y resolver detalles con ella
- [ ]  Danilo: enviar por WhatsApp la figura del flujo / arquitectura del agente
- [ ]  Danilo: enviar esa figura el lunes; si el feriado complica, el miércoles o hasta una semana después
- [ ]  Danilo: escribir el documento centrado en la arquitectura del agente, con figuras, detalles técnicos de RAG y las métricas de los cuatro experimentos
- [ ]  Felipe: pedir a Joshua que contacte a Danilo para la transferencia del repo a la organización de la USFQ y darle también acceso propio
- [ ]  Emilia: contactar a Danilo (aún no lo ha hecho)
- [ ]  Definir la defensa en noviembre y mantener el escrito hasta el 18 de diciembre

### Demo del estado actual de la aplicación

- Interfaz basada en el chat, personalizada para un flujo clásico de interacción; se apoya en el servicio ya levantado en `localhost:3000`
- El "activo" es la materia sobre la que trabaja el chat; se puede iniciar una nueva conversación y cargar data de prueba (copias para rondas de circunscripción)
- Las preguntas generadas son exclusivas del activo seleccionado y se muestra su estado
- Material: permite subir y borrar archivos, se actualiza la inyección y se pueden ver los chunks extraídos en Markdown
- Sección de exámenes: resultados de exámenes de la materia; al generar se definen número de preguntas, versiones, taxonomía de Bloom, balanced / basic / advanced, título, y la selección de preguntas es aleatoria; se puede descargar un examen de ejemplo
- Backend de exámenes: LaTeX con la clase de examen acordada; entrega el examen sin responder y el respondido
- Desde el chat se piden preguntas con dificultad, se guardan y verifican ("Save and Verify", respuesta correcta) y quedan añadidas al question bank
- Se dispone del JSON completo y nativo del banco de preguntas, además de las plantillas de pregunta y del file creator; el prompt no se guarda

### Configuración de LLM y API keys

- Actualmente usa la API de la infraestructura de la USFQ; Joshua explicó la conexión (URL y conexión típica)
- La configuración vive en el archivo de entorno interno; para usar una API key propia de ChatGPT solo cambia el endpoint/URL y la key
- La key adicional del sistema de secretos/autenticación no es necesaria si se usa de forma standalone
- Felipe pidió dejar un comentario indicando dónde cambiar el endpoint y la key

### Repositorio, Docker y transferencia institucional

- El proyecto se reestructuró de un repo a un monorepo ("repo padre con su módulo")
- Danilo tiene todos los scripts de levantamiento; puede añadir una "receta" para un agente más un script fijo como respaldo si algo falla
- Felipe quiere solo decirle a Claude que levante todo, sin copiar archivos manualmente, con Docker instalado
- Felipe añadirá el repo a la organización de la USFQ; Joshua es administrador del grupo institucional y gestiona accesos y permisos

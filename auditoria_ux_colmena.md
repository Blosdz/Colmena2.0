# Auditoría UI/UX — Colmena (Encuestas inteligentes)

Fecha: 18 de agosto de 2026
Alcance: flujo metodológico completo (Proyecto → Variables y dimensiones → Datos exógenos → Formulario → Link → Respuestas → Resultados), probado creando un proyecto piloto "Satisfacción del usuario con una plataforma digital".

## Resumen

El flujo de 6 pasos está bien pensado metodológicamente: obliga a definir variables, dimensiones y preguntas antes de publicar, separa datos exógenos (perfil, sin scoring) de las variables puntuables, y ya tiene módulos avanzados en Resultados (Baremos, Normalidad, Spearman, Segmentación, Diccionario). Eso es una base sólida para una tesis. Los huecos encontrados son sobre todo de consistencia, feedback y curva de aprendizaje — no de arquitectura.

## Hallazgos

### 1. Mezcla de idioma español/inglés en etiquetas de estado (Alta prioridad)
La interfaz está en español, pero varias etiquetas de sistema aparecen en inglés sin traducir: `INDEPENDENT`, `ACADEMIC`, `DRAFT`, `OPEN`, `INSTRUMENT`. Aparecen en la lista de variables, en la tabla de estudios (Link) y en el encabezado del formulario publicado. Para una tesista que no maneja jerga técnica en inglés, esto genera fricción y se ve inconsistente con el resto de la app, que sí está cuidadosamente traducida. Se recomienda traducir estos enums a etiquetas visibles ("Independiente", "Académico", "Borrador", "Abierto", "Instrumento") sin tocar el valor interno.

### 2. El rol analítico seleccionado no se reflejó correctamente (posible bug)
Al crear la variable "Satisfacción del usuario" se seleccionó explícitamente "Dependiente" en el desplegable Rol analítico, pero la tarjeta de la variable quedó mostrando `INDEPENDENT`. Puede ser un problema de guardado del valor o solo de visualización, pero en cualquiera de los dos casos rompe la confianza del usuario en que la app registró lo que pidió. Vale la pena verificar el binding del select al guardar.

### 3. El resaltado del menú lateral no siempre coincide con la página activa
Al entrar a "Link" (clic en el enlace dentro de Formulario), el sidebar dejó marcado "Telemetría" en vez de resaltar la sección real. El usuario pierde la referencia de "dónde estoy" dentro de un flujo que ya tiene 6 pasos + submenús — justo donde más se necesita orientación.

### 4. El placeholder del campo "Nombre" del estudio se confunde con un valor ya cargado
Al crear un nuevo estudio, el campo Nombre muestra "Aplicación 2026-I" en gris como placeholder, visualmente casi idéntico a un valor real precargado. Un usuario que no se fija bien intenta guardar, y recién ahí aparece el error "Ingresa un nombre". Sugerencia: usar el placeholder solo como ejemplo claramente diferenciado (ej. "Ej.: Aplicación 2026-I") o precargar un valor real editable en vez de un placeholder.

### 5. Abrir/Cerrar un estudio no pide confirmación
El botón "Abrir" pasa el estudio de `DRAFT` a `OPEN` (queda con link público activo) de forma instantánea, sin confirmación ni mensaje de éxito (toast). Es una acción con consecuencia real — se abre la recolección pública — y merece al menos un pequeño feedback visual de que la acción se aplicó, y opcionalmente una confirmación antes de publicar.

### 6. Ejemplo desalineado en "Datos exógenos"
Al agregar un campo nuevo, el placeholder de Código/Nombre sugiere "edad" / "Edad", pero las opciones de respuesta que aparecen precargadas son "Femenino / Masculino / Prefiero no responder" (propias de un campo Sexo, no Edad). El ejemplo confunde en vez de guiar.

### 7. Jerga metodológica expuesta al encuestado final
En el formulario público, la sección se titula "Instrumento" con la bajada "Ítems del instrumento de medición" — lenguaje de investigador, no de encuestado. La persona que responde la encuesta no necesita (ni debería) ver esa terminología; conviene reemplazar por el nombre de la dimensión/variable en lenguaje natural o simplemente omitir el rótulo técnico.

### 8. Estados vacíos poco diferenciados y sin guía de siguiente paso
"Sin variables", "Sin campos de perfil", "Todavía no hay estudios" y "Faltan variables calculadas" (en Resultados) comparten el mismo ícono genérico de bandeja y un texto breve, pero no explican qué acción concreta lleva a desbloquear la sección (p. ej. en Resultados no se aclara que primero hay que recolectar N respuestas mínimas o "ejecutar el cálculo"). Un CTA más específico ("Necesitas al menos 5 respuestas válidas para ver esta comparación") ayudaría a una tesista sin experiencia previa.

### 9. Curva de aprendizaje del vocabulario metodológico sin apoyo in-app
Conceptos como "Rol analítico: Independiente/Dependiente/Control/Resultado", "Datos exógenos" o "Baremos" son estándar en investigación, pero muchos usuarios de pregrado los usan por primera vez. No hay tooltips ni un "¿Qué es esto?" junto a estos campos, a pesar de que la app ya invierte en microcopy explicativo en otras partes (como los textos de ayuda en "Agregar pregunta Likert").

### 10. Contraste de texto placeholder/gris posiblemente bajo
El texto gris claro usado en placeholders y subtítulos (p. ej. en la tabla de escalas Likert y en los inputs vacíos) se ve con contraste ajustado sobre el fondo crema. Recomendable pasar los tonos de placeholder por un checker de contraste WCAG AA antes de la entrega final de la tesis, ya que la accesibilidad suele ser parte de la evaluación de un capítulo de UX.

## Priorización sugerida

1. Corregir el bug de rol analítico (#2) — afecta integridad de datos metodológicos.
2. Unificar idioma en badges de estado (#1) y el rótulo "Instrumento" cara al público (#7).
3. Arreglar resaltado de sidebar (#3) y confirmación al abrir/cerrar estudio (#5).
4. Placeholder vs. valor precargado (#4) y ejemplo de Datos exógenos (#6).
5. Mejoras de guía/tooltips y estados vacíos (#8, #9) y revisión de contraste (#10) — mejoras de pulido, no bloqueantes.

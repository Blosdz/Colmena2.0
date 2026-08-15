# COLMENA — División funcional de secciones según los PDFs CENSOPAS-COPSOQ

## 1. Objetivo de este documento

Este documento traduce los tres PDFs de diseño CENSOPAS-COPSOQ para Colmena a una **arquitectura funcional de producto**, tomando como punto de partida las secciones que Colmena ya tiene o está planteando:

- creación del proyecto;
- constructor;
- formulario público para responder el survey;
- telemetría;
- resultados;
- selección de herramientas estadísticas;
- reportes;
- exportaciones.

La conclusión principal es que la estructura actual de Colmena va en la dirección correcta, pero conviene separar con claridad **telemetría, resultados oficiales, analítica avanzada y seguimiento preventivo**. No deberían ser una sola pantalla.

---

# 2. Fuentes revisadas

1. **Manual técnico para la digitalización del método CENSOPAS-COPSOQ en Colmena** — 58 páginas.
2. **Guía y modelos de reporte CENSOPAS-COPSOQ para Colmena** — 25 páginas.
3. **Colmena Analytics — Modelo premium de reporte CENSOPAS-COPSOQ** — 28 páginas.

Los tres documentos distinguen entre:

- instrumento y captura;
- calidad/participación;
- resultado CENSOPAS-COPSOQ;
- analítica complementaria;
- intervención y seguimiento;
- reporte/exportación reproducible.

---

# 3. Conclusión rápida sobre las secciones actuales

| Sección actual/planteada en Colmena | ¿Está respaldada por los PDFs? | Ajuste recomendado |
|---|---:|---|
| Creación del proyecto | ✅ Sí | Convertirla en configuración del estudio: versión, población, período, unidades de análisis, evaluador y reglas de privacidad. |
| Constructor | ✅ Sí | Para CENSOPAS debe funcionar como **constructor protegido**. El núcleo oficial no puede modificarse libremente. |
| Formulario para exponer el survey | ✅ Sí | Debe ser autoaplicado, anónimo/confidencial, guardar códigos crudos y separar identidad de respuestas. |
| Telemetría | ✅ Sí | Debe mostrar participación y calidad de captura. **No es el lugar principal para la analítica premium.** |
| Resultados | ✅ Sí | Debe mostrar primero el resultado oficial/descriptivo CENSOPAS: dimensiones, subdimensiones cuando corresponda, unidades y priorización. |
| Elección de herramientas | ✅ Sí, como analítica complementaria | Debe estar en una sección **Analítica**, separada de Resultados. Las herramientas no deben alterar la clasificación oficial. |
| Gráficos premium | ✅ Sí | Principalmente en **Analítica Premium** y en el resumen ejecutivo; algunos KPI de calidad pueden estar en Telemetría. |
| Reportes | ✅ Sí | Debe construir el informe automático con estructura, narrativa, privacidad, plan preventivo y anexo técnico. |
| Exportaciones | ✅ Sí | Aplicar anonimato, supresión, versión, denominadores, método y hash. El modelo premium explicita PDF, XLSX y JSON reproducibles. |
| Plan preventivo / seguimiento | ✅ Sí y es importante | Si hoy no existe como sección, falta. El reporte premium incluye responsables, metas, KPIs, alertas y Balanced Scorecard. |

---

# 4. Arquitectura recomendada de navegación

```text
COLMENA
│
├── 1. Proyecto
│
├── 2. Constructor / Instrumento
│
├── 3. Aplicación / Survey
│
├── 4. Telemetría
│
├── 5. Resultados
│
├── 6. Analítica
│   ├── Analítica descriptiva complementaria
│   ├── Inferencial
│   ├── Segmentación
│   ├── Multivariada
│   └── Analítica premium
│
├── 7. Plan preventivo y seguimiento
│   ├── Priorización
│   ├── Acciones
│   ├── KPIs
│   ├── Balanced Scorecard
│   └── Alertas / seguimiento
│
├── 8. Reportes
│
└── 9. Exportaciones
```

La separación es importante porque el modelo premium define cuatro capas distintas:

```text
1. Descriptiva oficial
2. Inferencial
3. Multivariada
4. Estratégica
```

La categoría oficial CENSOPAS-COPSOQ debe conservarse como resultado principal y las capas avanzadas sólo la complementan.

**Fuente:** Modelo premium, p. 3.

---

# 5. Sección 1 — Proyecto

## 5.1 Para qué sirve

Representa el contexto general de trabajo en Colmena. Para CENSOPAS debe contener la configuración que los PDFs llaman principalmente **study / estudio**.

El Manual técnico propone como entidad mínima `study` con información de centro laboral, versión, período, unidades de análisis, evaluador y acuerdos.

**Fuente:** Manual técnico, p. 9.

## 5.2 Datos recomendados

```text
Nombre del proyecto
Tipo de proyecto
Centro laboral
Periodo de evaluación
Población convocada
Versión del instrumento
Fecha de inicio
Fecha de cierre
Evaluador responsable
Unidades de análisis
Regla mínima de publicación
Estado del estudio
```

## 5.3 Elección de versión

### Versión corta

- 42 preguntas.
- 31 ítems psicosociales.
- Salida en 6 dimensiones.
- Orientada a centros laborales con menos de 25 trabajadores o participación efectiva menor de 25.

### Versión media

- 112 preguntas.
- 69 ítems psicosociales.
- 6 dimensiones y 20 subdimensiones.
- Incluye además salud, bienestar y satisfacción como información descriptiva.
- Orientada a centros con 25 o más trabajadores y participación suficiente.

**Fuente:** Manual técnico, p. 5.

## 5.4 Regla de producto

Cuando el estudio empiece a recibir respuestas, Colmena debe **congelar la versión del instrumento y el baremo** para evitar que la definición cambie a mitad de la evaluación.

**Fuente:** Manual técnico, flujo de cálculo, p. 9.

---

# 6. Sección 2 — Constructor / Instrumento

## 6.1 Sí corresponde con los PDFs

El Manual técnico define explícitamente:

- `instrument_version`;
- `item`;
- `response_option`;
- `construct`;
- `construct_item`;
- `barem`.

Por lo tanto, la lógica que ya tenía Colmena de trabajar con:

```text
variables
 dimensiones
 subdimensiones
 ítems
 opciones
 puntuación
```

encaja con el modelo funcional.

**Fuente:** Manual técnico, p. 9.

## 6.2 Pero CENSOPAS no debe ser un builder libre

Para proyectos académicos o surveys propios, el constructor puede ser editable.

Para CENSOPAS debe existir un modo:

```text
INSTRUMENTO PROTEGIDO
```

El Manual indica que dentro del núcleo CENSOPAS-COPSOQ no se deben cambiar, eliminar ni añadir preguntas. Los módulos como teletrabajo, violencia, hostigamiento o ergonomía deben ser complementarios y no alterar la puntuación CENSOPAS.

**Fuente:** Manual técnico, p. 7.

## 6.3 Qué sí puede configurarse

El Manual permite adaptación limitada en determinados campos, bajo condiciones:

- nivel de instrucción;
- tiempo en el puesto;
- relación laboral;
- horario;
- área/departamento;
- puesto.

Área y puesto pueden utilizar catálogos locales, siempre cuidando anonimato y agrupando unidades pequeñas.

**Fuente:** Manual técnico, p. 6.

## 6.4 Diseño recomendado del constructor

```text
Constructor
│
├── Versión
├── Variables descriptivas
├── Dimensiones
├── Subdimensiones
├── Ítems
├── Opciones
├── Matriz ítem → constructo
├── Polaridad / scoring
├── Baremo
└── Módulos complementarios
```

Para el núcleo oficial:

```text
[solo lectura / protegido]
```

Para módulos propios:

```text
[editable]
```

---

# 7. Sección 3 — Aplicación / Formulario para exponer el survey

Esta sección corresponde directamente con el método.

## 7.1 Requisitos funcionales

La aplicación CENSOPAS debe ser:

- autoaplicada;
- anónima;
- confidencial;
- voluntaria.

**Fuente:** Manual técnico, p. 5.

## 7.2 Privacidad

Colmena no debe almacenar junto a las respuestas:

```text
nombre
DNI
correo corporativo
identificadores directos
```

La autenticación o validación de participación debe estar separada del contenido mediante tokens no reversibles.

**Fuente:** Manual técnico, pp. 9–10.

## 7.3 Captura correcta

El formulario debe guardar el código marcado por el usuario como dato primario:

```text
raw_code
```

No se debe reemplazar directamente por el puntaje transformado.

Después, el motor deriva:

```text
raw_code
   ↓
risk_value
   ↓
score_0_100
   ↓
construct_score
   ↓
clasificación
```

**Fuente:** Manual técnico, p. 8.

## 7.4 Estructura de formulario

### Versión corta

```text
Sociodemográficas
Condiciones laborales
Factores psicosociales
```

### Versión media

```text
Sociodemográficas
Condiciones laborales
Factores psicosociales
Salud, bienestar y satisfacción
```

---

# 8. Sección 4 — Telemetría

## 8.1 Qué debería significar Telemetría en Colmena

Telemetría debe responder:

> ¿Cómo está avanzando la aplicación y qué tan confiable es el dataset que se está recolectando?

No debería ser la pantalla principal de resultados estadísticos.

## 8.2 Indicadores que sí pertenecen aquí

De los modelos de reporte y el modelo premium:

```text
Convocados
Cuestionarios recibidos
Registros válidos
Registros excluidos
No respondieron
Tasa recibida
Tasa válida
Ítems omitidos
Tiempo mediano de respuesta
Patrones lineales o respuestas sospechosas
Completitud
Duplicidad
Coherencia
Celdas suprimidas por privacidad
```

**Fuentes:** Guía, pp. 9 y 14; Modelo premium, pp. 6–7.

## 8.3 Dashboard de Telemetría recomendado

```text
┌────────────────────────────────────────────────────────────┐
│ TELEMETRÍA DEL ESTUDIO                                    │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│ Convocados  │ Recibidos   │ Válidos     │ Tasa válida       │
│ 200         │ 186         │ 180         │ 90%               │
├─────────────┴─────────────┴─────────────┴──────────────────┤
│ Flujo de participación                                   │
│ Convocados → Respondieron → Válidos → Excluidos          │
├────────────────────────────────────────────────────────────┤
│ Calidad de captura                                        │
│ omitidos | duración | patrones | incompletos | alertas    │
└────────────────────────────────────────────────────────────┘
```

## 8.4 ¿Los gráficos premium deberían ir aquí?

**No todos.**

Telemetría puede tener gráficos premium de **calidad del dato y participación**, pero no debería contener:

- ranking de subdimensiones;
- regresión;
- correlaciones;
- clústeres;
- IC 95% de exposición;
- mapa de calor de riesgos;
- Balanced Scorecard.

Esos pertenecen a Resultados, Analítica o Seguimiento.

---

# 9. Sección 5 — Resultados

## 9.1 Esta sección debe contener primero el resultado CENSOPAS

El modelo premium establece como regla de oro que la categoría oficial no debe ser reemplazada por un índice inventado por Colmena.

**Fuente:** Modelo premium, p. 3.

Por ello Resultados debe ser una sección estable y separada del selector de herramientas.

## 9.2 Sub-secciones recomendadas

```text
Resultados
│
├── Resumen ejecutivo
├── Perfil sociolaboral
├── Resultados por dimensión
├── Resultados por subdimensión
├── Unidades de análisis
├── Salud, bienestar y satisfacción
├── Interpretación
└── Priorización
```

## 9.3 Resumen ejecutivo

Debe mostrar:

- participación;
- principales riesgos;
- factores protectores;
- prioridades;
- mensajes de acción.

**Fuente:** Guía, p. 5.

## 9.4 Resultados por dimensión

Para corta y media:

```text
D1 Exigencias psicológicas
D2 Conflicto trabajo-familia
D3 Control sobre el trabajo
D4 Apoyo social y calidad de liderazgo
D5 Compensaciones
D6 Capital social
```

Cada resultado debe mostrar:

```text
n válido
% favorable
% intermedio
% desfavorable
nivel final
nota interpretativa
```

El visual recomendado es **barra horizontal apilada al 100%**.

**Fuente:** Guía, p. 6.

## 9.5 Resultados por subdimensión

Sólo versión media.

Debe mostrar las 20 subdimensiones.

La versión corta **no debe producir 20 subdimensiones como resultados separados**.

**Fuentes:** Manual técnico, pp. 6–7 y 11; Guía, p. 5.

## 9.6 Unidades de análisis

Se puede analizar por:

```text
área
puesto
contrato
turno
otra unidad aprobada
```

Siempre con `n >= 5` y evitando combinaciones que permitan reidentificación.

**Fuente:** Manual técnico, p. 10.

## 9.7 Privacidad obligatoria

Si una unidad tiene entre 1 y 4 personas:

```text
NO PUBLICAR
```

Colmena debe:

```text
ocultar
agrupar
bloquear la visualización
```

según corresponda.

**Fuente:** Guía, p. 6.

## 9.8 Estado provisional / oficial

Los PDFs entregados indican que no contienen los puntos de corte numéricos peruanos completos ni una tabla oficial completa de inversión por ítem.

Por ello Colmena debe bloquear una salida equivalente a oficial mientras falten:

```text
polaridad verificada
algoritmo autorizado
puntos de corte vigentes
versión del baremo
prueba de concordancia
```

**Fuente:** Manual técnico, pp. 2, 8–9.

---

# 10. Sección 6 — Analítica / Elección de herramientas

## 10.1 Sí debe existir, pero separada de Resultados

La pregunta planteada era si en **Resultados** debería estar la elección de herramientas.

La arquitectura recomendada según los PDFs es:

```text
Resultados = qué obtuvo CENSOPAS
Analítica  = qué análisis complementarios quiere ejecutar Colmena
```

Esto evita mezclar el resultado metodológico del instrumento con análisis propios de Colmena.

## 10.2 Capas que define el modelo premium

### Capa 1 — Descriptiva oficial

```text
Baremos
Prevalencias
Distribución favorable/intermedia/desfavorable
Tablas
```

Esta debe vivir principalmente en **Resultados**.

### Capa 2 — Inferencial

```text
IC 95%
Pruebas estadísticas
Corrección Benjamini-Hochberg
Tamaño de efecto
```

### Capa 3 — Multivariada

```text
Correlaciones
Clústeres
Modelo ajustado / regresión
```

### Capa 4 — Estratégica

```text
Balanced Scorecard
Portafolio
Metas
Alertas
Seguimiento
```

Esta última conviene moverla a una sección propia de **Plan preventivo y seguimiento**.

**Fuente:** Modelo premium, p. 3.

## 10.3 Herramientas estadísticas mostradas en el PDF premium

El modelo premium utiliza o propone:

```text
Intervalos de confianza al 95%
Chi-cuadrado
Kruskal-Wallis
Mann-Whitney
Spearman
Benjamini-Hochberg
Tamaño de efecto
Alfa
Omega
K-means
Regresión logística
AUC / calibración del modelo
```

**Fuentes:** Modelo premium, pp. 6, 12, 14, 16–17.

## 10.4 La UI no debería dejar ejecutar cualquier prueba a ciegas

El propio modelo premium define para el motor:

```text
Comparación
    ↓
validar supuestos y tamaño
    ↓
elegir prueba y efecto
```

**Fuente:** Modelo premium, p. 26.

Por ello una UX mejor sería:

```text
¿Qué deseas analizar?

[ Comparar grupos ]
[ Buscar asociación ]
[ Ver correlación ]
[ Evaluar confiabilidad ]
[ Segmentar perfiles ]
[ Modelo multivariable ]
```

Y el backend decide/recomienda el método estadísticamente compatible.

## 10.5 Analítica premium recomendada

```text
Analítica
│
├── Panorama ejecutivo
├── Precisión / IC 95%
├── Segmentación
│   ├── sede
│   ├── área
│   ├── turno
│   ├── contrato
│   ├── sexo agrupado
│   └── edad agrupada
│
├── Comparaciones
├── Correlaciones
├── Confiabilidad
├── Patrones / Clústeres
└── Modelo multivariable
```

## 10.6 Versión corta

El modelo premium explícitamente presenta la versión corta con 20 registros como **analítica restringida**.

Por lo tanto, Colmena no debe asumir que todos los estudios pueden ejecutar regresión o clústeres. La disponibilidad debe depender de:

- tamaño de muestra;
- cantidad de eventos;
- estabilidad;
- privacidad;
- supuestos del método.

**Fuente:** portada del Modelo premium y reglas del motor, p. 26.

---

# 11. Sección 7 — Plan preventivo y seguimiento

Esta sección es necesaria para cumplir la parte preventiva del método y para aprovechar el modelo premium.

## 11.1 El reporte no termina en una gráfica

La Guía exige que cada hallazgo pueda conducir a:

```text
causa / hipótesis de origen
medida
responsable
plazo
indicador
seguimiento
```

**Fuente:** Manual técnico, p. 10; Guía, pp. 5 y 12.

## 11.2 Sub-secciones

```text
Plan preventivo
│
├── Priorización
├── Hipótesis de origen
├── Medidas
├── Responsables
├── Plazos
├── Indicadores
├── Metas
├── Evidencias
└── Estado
```

## 11.3 Balanced Scorecard

El modelo premium plantea una capa estratégica con:

```text
objetivos
KPI
línea base
meta
dueño
frecuencia
semáforo
acciones
seguimiento
```

El BSC traduce riesgos en objetivos, indicadores, metas, responsables y seguimiento.

**Fuente:** Modelo premium, pp. 3, 26 y 28.

## 11.4 Alertas

Las alertas pueden activarse por:

```text
exposición
incumplimiento
calidad del dato
cambio temporal
```

Nunca por el resultado de una persona.

**Fuente:** Modelo premium, p. 26.

---

# 12. Sección 8 — Reportes

## 12.1 Qué debe generar

La Guía propone una estructura de informe final de 12 bloques:

1. Portada y control documental.
2. Resumen ejecutivo.
3. Ficha técnica.
4. Calidad de datos.
5. Perfil sociolaboral.
6. Resultados por dimensión.
7. Resultados por subdimensión — sólo media.
8. Unidades de análisis.
9. Salud, bienestar y satisfacción — sólo media.
10. Análisis cualitativo.
11. Priorización y plan.
12. Conclusiones y anexos.

**Fuente:** Guía, p. 5.

## 12.2 Bloques reutilizables del motor

La Guía define bloques automáticos para:

```text
Control documental
Participación
Perfil
Dimensiones
Subdimensiones
Unidades
Salud
Priorización
Plan
Auditoría
```

**Fuente:** Guía, p. 25.

## 12.3 Control antes de generar el PDF

Debe validarse:

```text
instrumento
población
cálculo
clasificación
privacidad
visuales
narrativa
plan
trazabilidad
aprobación
```

**Fuente:** Guía, p. 7.

## 12.4 Narrativa automática

La interpretación debe responder:

```text
¿Qué muestra?
¿Qué nivel alcanza?
¿Dónde se concentra?
¿Qué origen debe investigarse?
¿Qué acción corresponde?
¿Qué no puede concluirse?
```

No debe afirmar causalidad individual ni diagnóstico.

**Fuente:** Guía, pp. 6–7.

---

# 13. Sección 9 — Exportaciones

## 13.1 Exportación reproducible

El modelo premium define que la exportación debe aplicar:

```text
notas
supresión de grupos pequeños
filtros
método
fecha
versión
hash de salida
```

Y menciona como salidas reproducibles:

```text
PDF
XLSX
JSON
```

**Fuente:** Modelo premium, p. 26.

## 13.2 Reglas de exportación

Cada exportación debe conservar:

- confidencialidad;
- denominadores;
- versión del instrumento;
- baremo;
- algoritmo;
- filtros;
- exclusiones;
- supresión por privacidad;
- hash.

La Guía indica además que la exportación debe insertar notas, denominadores, versión del algoritmo y marca de confidencialidad.

**Fuente:** Guía, p. 25.

## 13.3 Formatos adicionales de Colmena

Si Colmena mantiene CSV, SPSS, Power BI u otros formatos, son extensiones válidas del producto, pero **los tres PDFs revisados no los establecen como requisito central con el mismo nivel de detalle que PDF/XLSX/JSON**. Deben heredar las mismas reglas de privacidad y trazabilidad.

---

# 14. Qué parte del modelo premium va en cada pantalla

| Elemento premium | Sección Colmena recomendada |
|---|---|
| Cobertura válida | Telemetría |
| Recibidos / válidos / excluidos | Telemetría |
| Ítems omitidos | Telemetría |
| Tiempo mediano | Telemetría |
| Alfa / Omega | Analítica → Confiabilidad |
| Panorama general favorable/intermedio/desfavorable | Resultados |
| Resultado por dimensión | Resultados |
| Ranking de subdimensiones | Resultados / Analítica premium |
| Mapa de calor por área | Resultados → Unidades / Analítica premium |
| Explorador de segmentos | Analítica premium |
| IC 95% | Analítica premium |
| Chi-cuadrado | Analítica |
| Mann-Whitney | Analítica |
| Kruskal-Wallis | Analítica |
| Spearman | Analítica |
| Benjamini-Hochberg | Motor de Analítica |
| Tamaño de efecto | Analítica |
| K-means / perfiles | Analítica premium |
| Regresión logística | Analítica premium |
| AUC / calibración | Analítica premium |
| Matriz impacto-esfuerzo | Plan preventivo |
| Balanced Scorecard | Plan preventivo y seguimiento |
| KPIs y metas | Plan preventivo y seguimiento |
| Alertas | Plan preventivo y seguimiento |
| PDF | Reportes |
| XLSX / JSON | Exportaciones |
| Hash / auditoría | Transversal a Reportes y Exportaciones |

---

# 15. Flujo funcional completo recomendado

```text
CREAR PROYECTO
      │
      ▼
CONFIGURAR ESTUDIO
      │
      ├── población
      ├── versión corta/media
      ├── unidades de análisis
      ├── evaluador
      └── privacidad
      │
      ▼
CONSTRUCTOR / INSTRUMENTO
      │
      ├── núcleo CENSOPAS protegido
      ├── catálogos permitidos
      └── módulos complementarios separados
      │
      ▼
PUBLICAR FORMULARIO
      │
      ▼
CAPTURAR RAW RESPONSES
      │
      ▼
TELEMETRÍA
      │
      ├── participación
      ├── completitud
      ├── calidad
      └── privacidad
      │
      ▼
CERRAR / VALIDAR ESTUDIO
      │
      ▼
MOTOR CENSOPAS
      │
      ├── raw_code
      ├── risk_value
      ├── score_0_100
      ├── construct_score
      ├── baremo
      └── clasificación colectiva
      │
      ▼
RESULTADOS OFICIALES / DESCRIPTIVOS
      │
      ├── dimensiones
      ├── subdimensiones si media
      ├── unidades
      └── priorización
      │
      ▼
ANALÍTICA COMPLEMENTARIA
      │
      ├── IC 95%
      ├── comparación de grupos
      ├── efectos
      ├── correlaciones
      ├── segmentación
      ├── clústeres
      └── regresión
      │
      ▼
PLAN PREVENTIVO / BSC
      │
      ├── acción
      ├── responsable
      ├── plazo
      ├── KPI
      ├── meta
      └── seguimiento
      │
      ▼
REPORTES
      │
      ▼
EXPORTACIONES
```

---

# 16. Reglas que deben ser transversales a todas las secciones

## 16.1 Privacidad

```text
Nunca resultado individual CENSOPAS
Nunca identidad + respuestas
n < 5 → bloquear / suprimir / agrupar
```

## 16.2 Trazabilidad

Todo resultado relevante debe conocer:

```text
versión
baremo
algoritmo
fecha
filtros
n válido
exclusiones
hash
```

## 16.3 Separar dato primario y dato calculado

```text
Respuesta capturada != puntaje derivado
```

`raw_code` debe conservarse intacto.

## 16.4 No confundir analítica Colmena con resultado oficial

Debe haber etiquetas visuales distintas:

```text
RESULTADO CENSOPAS-COPSOQ
ANALÍTICA COMPLEMENTARIA COLMENA
```

## 16.5 No usar color como único código

Los gráficos deben incluir también:

```text
texto
porcentaje
etiqueta
leyenda
```

**Fuente:** Guía, p. 6.

---

# 17. Qué falta si se compara la estructura actual con los PDFs

Partiendo de:

```text
Proyecto
Constructor
Formulario
Telemetría
Resultados
Herramientas
Reportes
Exportación
```

los cambios principales serían:

### A. Cambiar el significado de Telemetría

Telemetría = **participación + calidad del dato**, no resultados estadísticos completos.

### B. Crear Analítica como sección propia

Aquí debe estar la selección/recomendación de herramientas.

### C. Mantener Resultados separado

Resultados = salida CENSOPAS y lectura organizacional.

### D. Crear Plan preventivo y seguimiento

Es una pieza importante que aparece reiteradamente en la Guía y en el modelo premium.

### E. Proteger el Constructor CENSOPAS

No puede funcionar igual que un survey libre.

### F. Implementar estados metodológicos

```text
provisional
verificado
oficial / habilitado
bloqueado
```

La clasificación equivalente a oficial debe permanecer bloqueada hasta disponer de los activos metodológicos autorizados.

---

# 18. Estructura final de tabs dentro de un proyecto CENSOPAS

La propuesta más limpia sería:

```text
[ Resumen ]
[ Constructor ]
[ Formulario ]
[ Telemetría ]
[ Resultados ]
[ Analítica ]
[ Plan y seguimiento ]
[ Reportes ]
[ Exportaciones ]
```

## Resumen

```text
estado del proyecto
instrumento
versión
periodo
población
participación
último análisis
último reporte
alertas
```

## Constructor

```text
instrumento
variables
ítems
dimensiones
subdimensiones
opciones
scoring
baremo
```

## Formulario

```text
preview
publicación
link/token
estado
fechas
```

## Telemetría

```text
convocados
recibidos
válidos
excluidos
completitud
duración
calidad
```

## Resultados

```text
resumen ejecutivo
perfil sociolaboral
dimensiones
subdimensiones
unidades
salud descriptiva
interpretación
prioridades
```

## Analítica

```text
selector de objetivo
métodos disponibles
IC 95%
comparaciones
correlaciones
confiabilidad
segmentación
clustering
regresión
```

## Plan y seguimiento

```text
hallazgos
hipótesis de origen
acciones
responsables
plazos
KPIs
metas
BSC
alertas
```

## Reportes

```text
plantilla corta
plantilla media
reporte premium
historial de generación
control de calidad
```

## Exportaciones

```text
PDF
XLSX
JSON
otros formatos Colmena
historial
hash
filtros aplicados
```

---

# 19. Prioridad de implementación sugerida por los propios PDFs

El roadmap del modelo premium propone:

```text
FASE 1 — Motor oficial
- diccionario y validación
- puntaje y baremo
- PDF corta y media
- pruebas de concordancia

FASE 2 — Dashboard
- modelo de datos
- filtros seguros
- drilldown
- XLSX / JSON

FASE 3 — Analítica
- IC y efectos
- múltiples pruebas
- clústeres
- regresión y validación

FASE 4 — BSC
- KPIs y metas
- portafolio
- alertas
- seguimiento continuo
```

El primer MVP recomendado por el documento es:

```text
versión corta y media
dashboard descriptivo
IC 95%
mapa de áreas
plan de acción
BSC
```

Y deja clústeres y regresión para después de validar el motor base.

**Fuente:** Modelo premium, p. 27.

---

# 20. Decisión de arquitectura recomendada

La navegación de Colmena debería reflejar esta separación conceptual:

```text
CAPTURA
Proyecto → Constructor → Formulario

CONTROL
Telemetría

RESULTADO DEL MÉTODO
Resultados

CIENCIA DE DATOS COMPLEMENTARIA
Analítica

GESTIÓN PREVENTIVA
Plan y seguimiento

SALIDAS
Reportes → Exportaciones
```

Esta división respeta mejor los tres PDFs que colocar todos los gráficos premium dentro de Telemetría o todas las herramientas estadísticas dentro de Resultados.

---

# 21. Referencias internas por PDF

## Manual técnico

Puntos utilizados principalmente:

- p. 5: alcance, versiones y población objetivo.
- pp. 6–7: campos adaptables, límite de adaptación y arquitectura del constructo.
- p. 8: raw_code, risk_value, score_0_100, baremos y polaridad.
- p. 9: entidades mínimas, flujo de cálculo, privacidad y clasificación organizacional.
- p. 10: reporte automático.
- pp. 11–55: bancos de ítems y matrices.
- pp. 56–58: módulos adicionales, verificación y trazabilidad.

## Guía y modelos de reporte

- p. 5: estructura recomendada del reporte.
- p. 6: privacidad, tablas y gráficos.
- p. 7: control de calidad.
- pp. 9–12: modelo versión corta.
- pp. 14–23: modelo versión media.
- p. 25: bloques reutilizables y reglas automáticas.

## Modelo premium

- p. 3: cuatro capas de analítica.
- pp. 4–11: dashboard, calidad, resultados y segmentación.
- p. 12: inferencia, BH y tamaño de efecto.
- pp. 13–17: correlaciones, clústeres y regresión.
- p. 26: reglas del motor de reportes.
- p. 27: roadmap.
- p. 28: especificación final.

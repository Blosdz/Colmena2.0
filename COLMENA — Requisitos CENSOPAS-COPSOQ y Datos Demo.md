# COLMENA — Requisitos funcionales CENSOPAS-COPSOQ

## Especificación para implementación, auditoría y población de datos demo

Este documento define qué debe tener **Colmena** para implementar el flujo CENSOPAS-COPSOQ descrito en los documentos de referencia.

La implementación debe ser comprobable visual y funcionalmente.

No basta con crear componentes vacíos.

El sistema debe quedar poblado con **proyectos demo completos**, de forma que puedan probarse:

- creación del proyecto;
- instrumento;
- formulario;
- captura;
- telemetría;
- resultados;
- privacidad;
- analítica;
- plan preventivo;
- reportes;
- exportaciones.

---

# 1. Regla principal para el harness

El harness debe trabajar sobre el proyecto existente.

Antes de implementar debe:

1. inspeccionar el backend;
2. identificar los endpoints existentes;
3. identificar los modelos/tablas existentes;
4. identificar los endpoints que ya alimentan cada pantalla;
5. identificar endpoints faltantes;
6. reutilizar los endpoints existentes siempre que sea posible.

## Está prohibido

No se permite:

```text
hardcodear resultados en componentes React
hardcodear datasets directamente en Chart.js
crear JSON estáticos como fuente principal
simular endpoints en frontend si el backend ya existe
inventar rutas API sin revisar el backend
calcular el scoring CENSOPAS en frontend
crear baremos oficiales ficticios
mostrar datos individuales
mostrar grupos con n < 5
```

Todo lo que aparezca en:

```text
Proyecto
Constructor
Formulario
Telemetría
Resultados
Analítica
Plan
Reportes
Exportaciones
```

debe provenir de datos obtenidos mediante los endpoints reales de Colmena.

---

# 2. Regla especial de datos demo

El desarrollo DEBE crear datos demo persistentes.

No basta con mocks.

Se requieren proyectos demo capaces de recorrer el sistema completo.

Crear como mínimo:

```text
DEMO 1
CENSOPAS versión corta
20 trabajadores válidos

DEMO 2
CENSOPAS versión media
200 convocados
186 cuestionarios recibidos
180 registros válidos

DEMO 3
CENSOPAS versión media premium
180 registros válidos
segmentación suficiente para analítica avanzada
```

Los proyectos deben estar claramente identificados como:

```text
DATOS SINTÉTICOS
NO CORRESPONDE A UNA EVALUACIÓN REAL
NO USAR PARA DECISIONES LABORALES
```

---

# 3. Cómo deben crearse los datos demo

Preferencia:

```text
seed backend
      ↓
servicios existentes
      ↓
base de datos
      ↓
endpoints reales
      ↓
frontend
```

También es válido que exista un comando:

```bash
python seed_censopas_demo.py
```

o equivalente.

Pero el resultado final debe quedar persistido en la misma estructura de datos que utilizaría un estudio real.

## No hacer

```text
frontend/demoData.ts
frontend/fakeResults.json
frontend/mockCensopas.js
const dimensions = [...]
```

como fuente principal de las pantallas.

---

# 4. Los datos demo deben ser reproducibles

Debe poder ejecutarse varias veces:

```text
reset demo
seed demo
```

sin crear datos inconsistentes.

Idealmente:

```text
seed_version = CENSOPAS_DEMO_V1
```

y cada proyecto demo debe tener un código estable.

Ejemplo:

```text
SYN-C20-2026
SYN-M200-2026
SYN-PREMIUM-M200-2026
```

---

# 5. Arquitectura funcional mínima de Colmena

Para CENSOPAS, Colmena debe exponer claramente estas áreas:

```text
COLMENA
│
├── Proyecto
│
├── Constructor / Instrumento
│
├── Formulario
│
├── Telemetría
│
├── Resultados
│
├── Analítica
│
├── Plan y seguimiento
│
├── Reportes
└── Exportaciones
```

No mezclar todas las responsabilidades dentro de un único dashboard.

---

# 6. PDF 1 — Manual Técnico CENSOPAS-COPSOQ

El primer documento define principalmente:

```text
instrumento
versiones
preguntas
constructos
scoring
baremos
privacidad
trazabilidad
flujo de cálculo
modelo funcional
```

---

# 7. Proyecto CENSOPAS

Al crear un proyecto CENSOPAS debe solicitarse como mínimo:

```text
Nombre del estudio
Centro laboral
Tipo de proyecto = CENSOPAS
Versión
Población convocada
Periodo
Fecha de inicio
Fecha de cierre
Evaluador
Unidades de análisis
Estado
```

## Selector de versión

Debe soportar:

```text
CENSOPAS — versión corta
CENSOPAS — versión media
```

---

# 8. Regla automática de versión

## Versión corta

Corresponde a:

```text
42 preguntas totales
31 ítems psicosociales
6 dimensiones
```

No debe publicar las veinte subdimensiones como resultados separados.

## Versión media

Corresponde a:

```text
112 preguntas totales
69 ítems psicosociales
6 dimensiones
20 subdimensiones
```

También incluye información descriptiva de:

```text
salud
bienestar
satisfacción
```

---

# 9. Constructor CENSOPAS protegido

Colmena puede tener un constructor general de instrumentos.

Sin embargo, CENSOPAS debe funcionar en modo:

```text
INSTRUMENTO PROTEGIDO
```

El núcleo CENSOPAS no debe permitir que un usuario común:

```text
edite texto de preguntas
elimine preguntas
añada preguntas al núcleo
modifique dimensión
modifique subdimensión
cambie opciones arbitrariamente
cambie pesos arbitrariamente
```

Debe mostrarse visualmente:

```text
Instrumento oficial / protegido
```

---

# 10. Campos adaptables

Debe existir configuración limitada para:

```text
nivel de instrucción
tiempo en el puesto
relación laboral
horario
área / departamento
puesto
```

Área y puesto pueden usar catálogos propios de la organización.

Ejemplo demo:

```text
Áreas
- Operaciones
- Mantenimiento
- Administración
- Logística
- Comercial
- SST y RR. HH.
```

---

# 11. Remuneración

No modificar automáticamente los rangos originales del instrumento.

Si Colmena quiere registrar remuneración actualizada deberá hacerlo como:

```text
MÓDULO DESCRIPTIVO COMPLEMENTARIO
```

separado de la puntuación CENSOPAS.

---

# 12. Módulos complementarios

Colmena puede permitir módulos como:

```text
Teletrabajo
Ergonomía
Violencia
Hostigamiento
Clima laboral
Otros
```

pero deben almacenarse como:

```text
COMPLEMENTARY_MODULE
```

y jamás deben modificar:

```text
CENSOPAS score
dimensiones CENSOPAS
subdimensiones CENSOPAS
clasificación CENSOPAS
```

---

# 13. Modelo del instrumento

El frontend debe permitir visualizar, al menos:

```text
Instrumento
└── Versión
    ├── Variables descriptivas
    ├── Dimensiones
    │   └── Subdimensiones
    │       └── Ítems
    │           └── Opciones
    └── Configuración de puntuación
```

---

# 14. Seis dimensiones obligatorias

Debe existir exactamente la estructura CENSOPAS correspondiente:

```text
D1 — Exigencias psicológicas en el trabajo

D2 — Conflicto trabajo-familia

D3 — Control sobre el trabajo

D4 — Apoyo social y calidad de liderazgo

D5 — Compensaciones del trabajo

D6 — Capital social
```

---

# 15. Veinte subdimensiones de la versión media

Debe existir soporte para:

```text
S1  Exigencias cuantitativas
S2  Ritmo de trabajo
S3  Exigencias emocionales
S4  Exigencia de esconder emociones
S5  Doble presencia
S6  Influencia
S7  Posibilidades de desarrollo
S8  Sentido del trabajo
S9  Apoyo social de los compañeros
S10 Apoyo social de superiores
S11 Calidad de liderazgo
S12 Sentimiento de grupo
S13 Previsibilidad
S14 Claridad de rol
S15 Conflicto de rol
S16 Reconocimiento
S17 Inseguridad sobre el empleo
S18 Inseguridad sobre las condiciones de trabajo
S19 Justicia
S20 Confianza vertical
```

En versión corta pueden existir internamente para trazabilidad, pero:

```text
NO PUBLICAR RESULTADOS INDIVIDUALES POR SUBDIMENSIÓN
```

---

# 16. Formulario CENSOPAS

El formulario debe ser:

```text
autoaplicado
anónimo
confidencial
voluntario
```

Cada respuesta debe guardar el código marcado originalmente.

Ejemplo:

```json
{
  "item": "25.b",
  "raw_code": 1
}
```

No sustituirlo directamente por el score.

---

# 17. Separación obligatoria del scoring

La arquitectura debe conservar:

```text
raw_code
   ↓
risk_value
   ↓
score_0_100
   ↓
construct_score
   ↓
classification
```

Estos conceptos NO deben mezclarse en una misma columna.

---

# 18. Raw response

Ejemplo:

```text
raw_code = 1
```

significa únicamente:

```text
la opción que efectivamente seleccionó el participante
```

Debe conservarse siempre para auditoría.

---

# 19. Puntaje transformado

La transformación propuesta en los documentos es provisional.

Por tanto debe existir estado metodológico.

Ejemplo:

```text
scoring_status:
PROVISIONAL
VERIFIED
OFFICIAL
BLOCKED
```

Mientras no existan:

```text
tabla de polaridad verificada
algoritmo autorizado
C1 autorizado
C2 autorizado
versión de baremo
prueba de concordancia
```

Colmena NO debe presentarse como equivalente al motor oficial.

---

# 20. Bloqueo de equivalencia oficial

Crear una propiedad equivalente a:

```text
official_equivalence_enabled = false
```

Mientras sea `false`, mostrar:

> Resultados demostrativos/provisionales. No equivalentes a una clasificación oficial CENSOPAS-COPSOQ.

---

# 21. Baremo

Debe existir entidad para almacenar:

```text
version
population
construct
cut_1
cut_2
direction
source
effective_date
status
```

Nunca utilizar automáticamente:

```text
33.33
66.67
```

como cortes oficiales.

Los terciles de una población de referencia no equivalen a dividir arbitrariamente una escala 0–100.

---

# 22. Privacidad obligatoria

No almacenar junto a las respuestas:

```text
nombre
DNI
correo corporativo
identificador laboral directo
```

Utilizar:

```text
anonymous_token
```

o mecanismo equivalente.

---

# 23. Separar participación de respuesta

Arquitectura esperada:

```text
participation
    token
    estado

responses
    anonymous_token
    item
    raw_code
```

El sistema de negocio no debe poder reconstruir directamente:

```text
trabajador → respuestas psicológicas
```

---

# 24. Supresión n < 5

Regla transversal:

```text
n = 1 → SUPPRESSED
n = 2 → SUPPRESSED
n = 3 → SUPPRESSED
n = 4 → SUPPRESSED
n >= 5 → publicable
```

Debe aplicarse en:

```text
tablas
gráficos
tooltips
filtros
drilldowns
PDF
Excel
JSON
exportaciones
API
```

No basta con ocultarlo visualmente.

---

# 25. Supresión secundaria

También debe revisarse si una celda escondida puede reconstruirse utilizando totales.

Ejemplo:

```text
Total área = 20

A = 10
B = 7
C = SUPPRESSED
```

El usuario podría deducir:

```text
C = 3
```

Por lo tanto debe existir protección contra deducción.

---

# 26. Congelamiento del estudio

Cuando comience la captura:

```text
instrument_version
barem_version
question_matrix
scoring_version
```

deben quedar congelados para ese estudio.

No permitir modificar retroactivamente la estructura de un estudio activo.

---

# 27. Telemetría

Telemetría NO es Resultados.

Debe responder:

> ¿Cómo está avanzando la recolección y cuál es la calidad del dataset?

Mostrar como mínimo:

```text
Convocados
Recibidos
Válidos
Excluidos
No respondieron
Tasa recibida
Tasa válida
Completitud
Ítems omitidos
Tiempo mediano
Patrones sospechosos
Duplicados detectados
Errores de catálogo
```

---

# 28. Dataset demo de telemetría

Para el proyecto medio:

```text
Convocados             200
Respondieron            186
Válidos                 180
Excluidos                 6
No respondieron          14

Tasa recibida           93%
Tasa válida             90%
```

Las seis exclusiones deben existir realmente en BD.

No colocar simplemente:

```text
excluded = 6
```

en el dashboard.

El sistema debe ser capaz de obtener ese valor a partir de registros persistidos.

---

# 29. Datos inválidos deliberados

Los fixtures demo deben incluir algunos casos de QA:

```text
cuestionario incompleto
raw_code inválido
sesión duplicada
grupo con n = 4
grupo con n = 5
respuesta extremadamente rápida
patrón lineal
```

El objetivo es poder demostrar las reglas de control del sistema.

---

# 30. PDF 2 — Guía y Modelos de Reporte

El segundo documento define principalmente:

```text
estructura del informe
visualizaciones
interpretación
privacidad
plan preventivo
datos sintéticos
automatización del reporte
```

---

# 31. Sección Resultados

Debe existir una pantalla independiente:

```text
Resultados
```

que presente primero la información metodológica principal.

No debe comenzar por clustering, regresión o IA.

Orden:

```text
Resumen
Participación
Perfil sociolaboral
Dimensiones
Subdimensiones
Unidades de análisis
Salud/bienestar
Priorización
```

---

# 32. Dashboard dimensional

Mostrar las seis dimensiones mediante:

```text
barras horizontales apiladas al 100%
```

Segmentos:

```text
Favorable
Intermedio
Desfavorable
```

Cada barra debe mostrar:

```text
%
n
texto
```

No depender únicamente del color.

---

# 33. No usar como visual principal

Evitar:

```text
gráficos 3D
muchos gráficos circulares
radar como comparación principal
color sin etiqueta
```

---

# 34. Tabla de dimensiones

Debe existir además del gráfico.

Campos mínimos:

| Campo | Descripción |
|---|---|
| ID | D1–D6 |
| Dimensión | nombre |
| n válido | denominador |
| Favorable | n y % |
| Intermedio | n y % |
| Desfavorable | n y % |
| Nivel | clasificación |
| Nota | interpretación |

---

# 35. Demo versión corta

Debe existir el proyecto:

```text
SYN-C20-2026
```

con:

```text
20 trabajadores válidos
42 preguntas
31 ítems psicosociales
6 dimensiones
```

Ejemplo dimensional:

```text
D1
15% favorable
25% intermedio
60% desfavorable

D2
20% favorable
45% intermedio
35% desfavorable

D3
50% favorable
30% intermedio
20% desfavorable

D4
25% favorable
50% intermedio
25% desfavorable

D5
15% favorable
30% intermedio
55% desfavorable

D6
55% favorable
30% intermedio
15% desfavorable
```

Estos valores son sintéticos.

Deben estar marcados permanentemente como demostrativos.

---

# 36. Perfil sociolaboral demo corto

Poblar, entre otros:

```text
Sexo
Mujer       11
Hombre       9

Edad
<31          9
31–45        8
>45          3

Área
Administración 8
Operaciones    7
Comercial      5
```

Estos datos deben poder verse desde:

```text
Perfil sociolaboral
```

y obtenerse por endpoint.

---

# 37. Demo versión media

Crear:

```text
SYN-M200-2026
```

con:

```text
200 convocados
186 respuestas recibidas
180 válidas
6 registros excluidos
14 no respondieron
112 preguntas
69 ítems psicosociales
6 dimensiones
20 subdimensiones
```

---

# 38. Perfil demo medio

Poblar suficientes categorías para probar filtros.

Ejemplo:

```text
Producción
Administración
Comercial
Logística
Servicios y soporte
```

También:

```text
sexo
edad
contrato
horario
turno
```

---

# 39. Subdimensiones

Sólo para versión media debe aparecer:

```text
Resultados
    └── Subdimensiones
```

Mostrar las 20.

Visual recomendado:

```text
barras horizontales largas
+
tabla
+
ranking
```

No crear veinte dashboards separados.

---

# 40. Priorización

Crear ranking ordenado por:

```text
% desfavorable DESC
```

con referencia visual del:

```text
50%
```

Ejemplo:

```text
1. Exigencias cuantitativas
2. Ritmo de trabajo
3. Inseguridad sobre el empleo
4. Exigencias emocionales
5. Esconder emociones
...
```

---

# 41. Localización por área

Debe existir drilldown por:

```text
área
puesto
contrato
turno
```

siempre respetando:

```text
n >= 5
```

Visuales recomendados:

```text
barras agrupadas
mapa de calor
tabla
```

Cada unidad debe mostrar su `n`.

---

# 42. Mapa de calor

Crear:

```text
filas    = áreas
columnas = dimensiones
valor    = % desfavorable
```

Ejemplo:

```text
                 D1  D2  D3  D4  D5  D6
Operaciones      80  26   0  14  28   4
Mantenimiento    63  14   0  23  23   0
Logística        36   0   0  16  20   0
...
```

Los valores de esta demo son sintéticos.

---

# 43. Filtros

El usuario puede filtrar por un segmento permitido.

Ejemplo:

```text
Sede
Área
Turno
Contrato
Sexo
Edad agrupada
```

Cada cambio debe volver a consultar el backend.

No filtrar exclusivamente sobre un dataset global descargado previamente si eso pudiera eludir la regla de privacidad.

---

# 44. Estado del filtro

Todo gráfico filtrado debe mostrar:

```text
n válido
cobertura
filtros activos
celdas suprimidas
```

Si:

```text
n < 5
```

debe mostrarse:

```text
Resultado protegido por privacidad
```

sin entregar el porcentaje.

---

# 45. Interpretación narrativa

Cada resultado relevante debe responder:

```text
1. ¿Qué muestra?
2. ¿Qué nivel alcanza?
3. ¿Dónde se concentra?
4. ¿Qué posible origen debe investigarse?
5. ¿Qué acción preventiva corresponde?
6. ¿Qué no puede concluirse?
```

---

# 46. Ejemplo de narrativa

Formato:

```text
Hallazgo
+
Nivel
+
Localización
+
Hipótesis de origen
+
Acción
+
Limitación
```

Evitar frases como:

```text
"Los trabajadores tienen..."
"El área causa..."
"El empleado presenta..."
```

Preferir:

```text
"Se observó una mayor proporción..."
"La distribución sugiere revisar..."
"Debe contrastarse con..."
```

---

# 47. Plan preventivo

Debe existir una sección funcional.

Campos:

```text
Hallazgo
Dimensión/subdimensión
Hipótesis de origen
Medida
Responsable
Fecha inicio
Plazo
Indicador
Línea base
Meta
Estado
Seguimiento
```

---

# 48. Datos demo del plan

Ejemplo:

```text
Hallazgo:
D1 — riesgo elevado

Medida:
Rebalancear cargas semanales.

Responsable:
Jefatura de Operaciones

Plazo:
30 días

Indicador:
% de tareas vencidas

Meta:
Reducir 20%

Estado:
En progreso
```

Debe haber varias acciones demo para poder probar:

```text
pendiente
en progreso
cumplida
vencida
```

---

# 49. Reporte automático

El generador de reporte debe contener:

```text
1 Portada
2 Resumen ejecutivo
3 Ficha técnica
4 Calidad de datos
5 Perfil sociolaboral
6 Resultados por dimensión
7 Resultados por subdimensión
8 Unidades de análisis
9 Salud, bienestar y satisfacción
10 Análisis cualitativo
11 Priorización y plan
12 Conclusiones
13 Anexo técnico
```

Condicionales:

```text
versión corta
    ocultar subdimensiones
    ocultar salud/bienestar/satisfacción

versión media
    habilitar ambas
```

---

# 50. Control antes de generar PDF

Debe existir validación automática.

Verificar:

```text
instrumento identificado
versión identificada
baremo identificado
población conciliada
conteos correctos
porcentajes correctos
privacidad aplicada
n < 5 suprimido
narrativa válida
plan completo
algoritmo identificado
hash generado
```

---

# 51. PDF 3 — Colmena Analytics Premium

El tercer documento amplía el producto con cuatro capas.

```text
1 DESCRIPTIVA OFICIAL
2 INFERENCIAL
3 MULTIVARIADA
4 ESTRATÉGICA
```

Estas capas deben estar claramente separadas.

---

# 52. Regla de oro Premium

Nunca sustituir:

```text
resultado CENSOPAS
```

por:

```text
índice Colmena
modelo predictivo
cluster
BSC
probabilidad
```

Los modelos Colmena son análisis complementarios.

---

# 53. Dashboard ejecutivo Premium

Crear KPIs como:

```text
Cobertura válida
Riesgo prioritario
Principal brecha
Confiabilidad
Índice BSC
```

Todos deben venir del backend.

Ejemplo demo:

```text
Cobertura válida     90.0%
Principal brecha     D1
Confiabilidad        0.90
BSC                   70/100
```

Los KPIs creados por Colmena deben mostrar una etiqueta como:

```text
Indicador analítico Colmena
```

cuando no formen parte del método oficial.

---

# 54. Calidad del dato

Pantalla Premium:

```text
Tasa recibida
Tasa válida
Ítems omitidos
Patrón lineal
Tiempo mediano
```

Además:

```text
Alfa
Omega
```

por dimensión cuando corresponda.

---

# 55. Consistencia interna

Tabla:

```text
Dimensión
Número de ítems
Alfa de Cronbach
Omega de McDonald
Lectura
```

No eliminar automáticamente preguntas porque un estudio empresarial muestre una consistencia menor.

---

# 56. Analítica inferencial

Crear un módulo:

```text
Analítica
    └── Inferencial
```

Debe poder ofrecer, cuando sean metodológicamente aplicables:

```text
IC 95%
Chi-cuadrado
Mann-Whitney
Kruskal-Wallis
Spearman
Benjamini-Hochberg
Tamaño de efecto
```

---

# 57. Selector de análisis

El frontend puede mostrar:

```text
Variable/constructo objetivo

Agrupar por:
- área
- turno
- contrato
- sede
- etc.

Método sugerido

Ejecutar análisis
```

El frontend no debe hacer el cálculo estadístico.

Debe solicitarlo al backend/servicio estadístico.

---

# 58. Resultados inferenciales

Mostrar:

```text
Prueba
Estadístico
p
q ajustado
Tamaño de efecto
IC
n
Interpretación
```

No presentar únicamente:

```text
p < 0.05
```

---

# 59. Intervalos de confianza

Las prevalencias principales del dashboard premium deben poder mostrar:

```text
valor
IC 95%
```

Visual recomendado:

```text
dot + error bar
```

---

# 60. Corrección por comparaciones múltiples

Cuando se ejecuten múltiples contrastes usar soporte para:

```text
Benjamini-Hochberg
```

Mostrar separadamente:

```text
p
q_BH
```

---

# 61. Matriz de correlaciones

Crear análisis de:

```text
Spearman
```

entre constructos o variables permitidas.

Debe incluir aviso:

```text
Correlación no implica causalidad.
```

---

# 62. Clustering

Crear módulo exploratorio:

```text
Patrones ocultos
```

Puede implementar:

```text
K-means
```

sobre constructos agregados.

Mostrar:

```text
k
n por cluster
perfil promedio
silhouette
interpretación
```

---

# 63. Regla de privacidad de clusters

Nunca mostrar:

```text
Persona 123 → cluster 4
```

a usuarios de negocio.

Mostrar únicamente:

```text
Cluster A — n = 50
Cluster B — n = 42
...
```

agregados.

---

# 64. Regresión

Crear análisis multivariable cuando corresponda.

Ejemplo:

```text
regresión logística
```

Salida:

```text
Predictor
OR
IC 95%
p/q
Lectura
```

Debe mostrar explícitamente:

```text
No es diagnóstico.
No debe utilizarse para decisiones laborales individuales.
```

---

# 65. Validación predictiva

Si existe modelo predictivo debe mostrar, cuando corresponda:

```text
AUC
calibración
validación
limitaciones
```

No presentar únicamente una probabilidad.

---

# 66. Restricción por tamaño muestral

La versión corta con:

```text
n = 20
```

debe mostrar analítica restringida.

No ejecutar automáticamente modelos complejos que no sean adecuados para ese tamaño.

Ejemplo:

```text
Descriptiva                ENABLED
Resultados dimensiones     ENABLED
IC descriptivo             LIMITED
Segmentación               LIMITED
Regresión                   DISABLED/RESTRICTED
Clustering                  DISABLED/EXPLORATORY
```

La habilitación final debe depender del método y tamaño disponibles.

---

# 67. Balanced Scorecard

Debe existir módulo:

```text
Plan y seguimiento
    └── Balanced Scorecard
```

Cada objetivo debe tener:

```text
Perspectiva
Objetivo
Indicador
Fórmula
Línea base
Meta
Valor actual
Responsable
Frecuencia
Semáforo
Acciones relacionadas
```

---

# 68. Estados BSC

Ejemplo:

```text
VERDE
meta cumplida

AMARILLO
desviación moderada

ROJO
acción necesaria
```

El color siempre acompañado de texto.

---

# 69. Alertas

Crear alertas de gestión sobre datos agregados.

Ejemplos:

```text
KPI fuera de meta
acción preventiva vencida
cobertura insuficiente
n pequeño
cambio desfavorable
estudio próximo a cerrar
```

Nunca:

```text
"Trabajador X tiene riesgo alto"
```

---

# 70. Seguimiento temporal

Colmena debe poder comparar estudios únicamente si:

```text
misma versión
baremo compatible
definición de unidad compatible
población comparable
```

Si no se cumple:

```text
comparison_allowed = false
```

Mostrar explicación.

---

# 71. Gráfico temporal

Cuando sea válido:

```text
medición 1
medición 2
medición 3
```

Visual:

```text
línea
o
puntos conectados
```

No mezclar versiones corta y media como si fueran equivalentes.

---

# 72. Exportaciones

Como mínimo preparar:

```text
PDF
XLSX
JSON
```

Si Colmena incorpora además:

```text
CSV
SPSS
Power BI
```

deben heredar exactamente las mismas reglas de privacidad.

---

# 73. Trazabilidad de exportaciones

Registrar:

```text
study_id
report_version
algorithm_version
barem_version
filters
generated_at
generated_by
input_hash
output_hash
```

---

# 74. La demo debe poblar TODAS las pantallas

El harness no termina cuando consigue mostrar el dashboard inicial.

Para cada proyecto demo se debe comprobar:

| Pantalla | Debe contener datos |
|---|---:|
| Proyecto | Sí |
| Constructor | Sí |
| Formulario | Sí |
| Telemetría | Sí |
| Resultados | Sí |
| Dimensiones | Sí |
| Subdimensiones media | Sí |
| Perfil | Sí |
| Unidades | Sí |
| Analítica | Sí |
| Plan | Sí |
| BSC Premium | Sí |
| Reportes | Sí |
| Exportaciones | Sí |

---

# 75. Proyecto Demo A — versión corta

Crear:

```text
Nombre:
Servicios Andinos S.A.C. — DEMO

Código:
SYN-C20-2026

Versión:
Corta

Convocados:
20

Recibidos:
20

Válidos:
20

Preguntas:
42

Psicosociales:
31

Dimensiones:
6

Subdimensiones publicables:
NO
```

---

# 76. Proyecto Demo B — versión media

Crear:

```text
Nombre:
Industrias del Sur S.A. — DEMO

Código:
SYN-M200-2026

Versión:
Media

Convocados:
200

Recibidos:
186

Válidos:
180

Excluidos:
6

No respuesta:
14

Preguntas:
112

Psicosociales:
69

Dimensiones:
6

Subdimensiones:
20
```

---

# 77. Proyecto Demo C — Premium

Debe disponer como mínimo de:

```text
3 sedes
6 áreas
2 tipos de turno
2 tipos de contrato
sexo
edad agrupada
horas extra
variables descriptivas necesarias
180 registros válidos
```

Ejemplo:

```text
SEDES

Operación Sur      70
Lima                60
Operación Centro    50
```

Áreas:

```text
Operaciones          50
Mantenimiento        35
Administración       30
Logística            25
SST y RR. HH.        20
Comercial            20
```

Turno:

```text
Diurno      114
Rotativo     66
```

Contrato:

```text
Indefinido    120
Plazo fijo     60
```

---

# 78. Fixture especial de privacidad

Además de los proyectos visuales, crear un fixture QA con:

```text
Área A = 10
Área B = 6
Área C = 4
```

Consultar Área C.

Resultado esperado:

```json
{
  "status": "SUPPRESSED",
  "reason": "MINIMUM_GROUP_SIZE"
}
```

o equivalente.

No debe devolver un porcentaje publicable.

---

# 79. Fixture de frontera n = 5

Crear:

```text
Área D = 5
```

Resultado:

```text
publicable
```

si no existe otro riesgo de reidentificación.

Esto verifica exactamente la frontera del sistema.

---

# 80. Fixture de empate

Crear una distribución sintética para comprobar la lógica:

```text
rojo
amarillo
verde
```

sin ganador evidente.

Debe quedar registrada la necesidad de:

```text
revisión documentada
prioridad preventiva
```

y no una decisión arbitraria silenciosa.

---

# 81. Frontend: regla de consumo de endpoints

Cada página debe permitir identificar su endpoint real.

Ejemplo conceptual:

```text
ProjectPage
    ↓
GET endpoint real de project

TelemetryPage
    ↓
GET endpoint real de telemetry

ResultsPage
    ↓
GET endpoint real de results

AnalysisPage
    ↓
POST endpoint real de analysis
```

NO inventar estos paths.

El harness debe descubrir sus nombres reales en el backend.

---

# 82. Network audit

Antes de considerar terminada una pantalla, comprobar en navegador:

```text
Network
```

y verificar:

```text
request real
200/201 válido
response JSON
frontend usando ese response
sin fixture hardcodeado
```

---

# 83. Contratos de respuesta

El frontend debe tolerar:

```text
loading
empty
error
suppressed
provisional
ready
```

Ejemplo:

```text
LOADING
EMPTY
SUPPRESSED
PROVISIONAL
READY
ERROR
```

No asumir que toda consulta devolverá resultados publicables.

---

# 84. Estado provisional

Si no existe baremo autorizado, Resultados debe poder funcionar en modo:

```text
DEMO / PROVISIONAL
```

pero debe mostrar claramente la advertencia.

No inventar baremos sólo para pintar:

```text
verde
amarillo
rojo
```

como si fueran oficiales.

Las distribuciones sintéticas de los PDFs pueden utilizarse directamente para demostrar el diseño, siempre identificadas como sintéticas.

---

# 85. Motor estadístico

La lógica debe residir preferentemente:

```text
backend / servicio Python
```

y no en componentes visuales.

Separar:

```text
data acquisition
data validation
scoring
aggregation
privacy
statistics
report generation
```

---

# 86. Responsabilidad del frontend

Frontend:

```text
selecciona
consulta
filtra
visualiza
explica
exporta
```

Backend:

```text
valida
calcula
suprime
clasifica
analiza
audita
```

---

# 87. Definition of Done — Proyecto

PASS si:

- se crea proyecto CENSOPAS;
- permite elegir corta/media;
- guarda población;
- guarda unidades de análisis;
- guarda evaluador;
- guarda periodo;
- puede congelar configuración;
- el demo existe vía API.

---

# 88. Definition of Done — Constructor

PASS si:

- se visualizan las seis dimensiones;
- media muestra 20 subdimensiones;
- corta no las publica como salida;
- se visualizan ítems;
- se visualizan opciones;
- el núcleo está protegido;
- módulos complementarios están separados.

---

# 89. Definition of Done — Formulario

PASS si:

- puede contestarse;
- respuestas llegan al backend;
- se almacena raw_code;
- no se almacena identidad directa junto a respuesta;
- se respetan catálogos;
- existen datos demo reales en DB.

---

# 90. Definition of Done — Telemetría

PASS si muestra desde endpoint:

```text
convocados
recibidos
válidos
excluidos
no respuesta
tasa
faltantes
calidad
```

y los números coinciden con los registros persistidos.

---

# 91. Definition of Done — Resultados

PASS si:

- muestra seis dimensiones;
- presenta n y %;
- muestra barras apiladas;
- corta no muestra subdimensiones;
- media muestra veinte;
- existe ranking;
- existe localización;
- privacidad n < 5 funciona.

---

# 92. Definition of Done — Analítica

PASS si:

- está separada del resultado oficial;
- soporta IC cuando corresponda;
- soporta tamaños de efecto;
- ofrece pruebas permitidas;
- registra metodología;
- no hace causalidad automática;
- restringe análisis no apropiados.

---

# 93. Definition of Done — Premium

PASS si permite demostrar:

```text
dashboard ejecutivo
drilldown
explorador de segmentos
IC 95%
contrastes
correlaciones
clustering exploratorio
regresión
BSC
seguimiento
```

utilizando datos demo desde backend.

---

# 94. Definition of Done — Plan

PASS si permite:

```text
crear acción
asignar responsable
asignar plazo
definir indicador
definir meta
cambiar estado
registrar seguimiento
```

y relacionarla con:

```text
dimensión
subdimensión
hallazgo
```

---

# 95. Definition of Done — Reportes

PASS si:

- genera reporte corto;
- genera reporte medio;
- aplica secciones condicionales;
- muestra denominadores;
- aplica supresión;
- incluye limitaciones;
- registra algoritmo;
- registra hash;
- identifica datos demo.

---

# 96. Definition of Done — Exportaciones

PASS si:

- no filtra datos individuales;
- respeta n < 5;
- incluye versión;
- incluye filtros;
- incluye algoritmo;
- incluye fecha;
- registra hash.

---

# 97. Auditoría de consistencia

El harness debe comprobar:

```text
valor mostrado en frontend
        =
valor devuelto por endpoint
        =
valor calculado/persistido en backend
```

No aceptar pantallas donde los números visuales sean independientes del backend.

---

# 98. Pruebas mínimas

Crear tests para:

```text
versión corta
versión media
n = 1
n = 4
n = 5
raw_code mínimo
raw_code máximo
raw_code inválido
respuesta faltante
constructo incompleto
clasificación 49.9%
clasificación 50%
empate
filtro inseguro
exportación insegura
regresión del resultado
```

---

# 99. Prueba de reproducibilidad

Mismo:

```text
dataset
instrument_version
algorithm_version
barem_version
```

debe producir exactamente:

```text
mismos denominadores
mismos scores
mismas clasificaciones
mismas supresiones
mismos resultados
```

Guardar:

```text
input_hash
result_hash
```

---

# 100. Orden de implementación

Implementar en este orden:

```text
FASE 1
Instrumento y modelos

FASE 2
Proyecto y estudio

FASE 3
Formulario y respuestas

FASE 4
Privacidad y telemetría

FASE 5
Scoring y resultados

FASE 6
Reporte estándar

FASE 7
Segmentación y analítica

FASE 8
Premium

FASE 9
Plan + BSC

FASE 10
Exportaciones y auditoría
```

---

# 101. Prioridad absoluta

Antes de clustering, regresión o dashboards sofisticados deben funcionar correctamente:

```text
instrumento
raw responses
anonimato
n < 5
versión
scoring
baremo
resultados
trazabilidad
```

---

# 102. Entregables que debe producir el harness

Además del código, generar:

```text
docs/censopas/
├── current-state.md
├── endpoint-map.md
├── data-model.md
├── demo-seeding.md
├── scoring-status.md
├── privacy-rules.md
├── frontend-sections.md
├── analytics.md
├── report-engine.md
└── acceptance-test.md
```

---

# 103. endpoint-map.md

Debe contener algo equivalente a:

| Sección | Endpoint encontrado | Método | Estado |
|---|---|---|---|
| Proyecto | endpoint real | GET/POST | OK |
| Constructor | endpoint real | GET | OK |
| Formulario | endpoint real | GET/POST | OK |
| Telemetría | endpoint real | GET | OK |
| Resultados | endpoint real | GET | OK |
| Analítica | endpoint real | GET/POST | OK |
| Plan | endpoint real | GET/POST | OK |
| Reportes | endpoint real | POST/GET | OK |
| Exportaciones | endpoint real | GET | OK |

No escribir endpoints imaginarios.

---

# 104. demo-seeding.md

Debe registrar:

```text
seed ejecutado
proyectos creados
IDs
studies
participantes
respuestas
resultados
planes
KPIs
reportes
```

Ejemplo:

```text
SYN-C20-2026
project_id = ...
study_id = ...
20 responses completas

SYN-M200-2026
project_id = ...
study_id = ...
200 convocados
186 recibidos
180 válidos
```

---

# 105. Evidencia obligatoria

El harness debe entregar una tabla:

| Pantalla | Proyecto demo | Endpoint | Datos visibles | PASS |
|---|---|---|---|---|
| Proyecto | C20 | real | Sí | |
| Constructor | C20 | real | Sí | |
| Formulario | C20 | real | Sí | |
| Telemetría | M200 | real | Sí | |
| Resultados | M200 | real | Sí | |
| Analítica | Premium | real | Sí | |
| Plan | Premium | real | Sí | |
| Reporte | M200 | real | Sí | |

---

# 106. Condición final de aceptación

La tarea NO se considera terminada si existen:

```text
pantallas vacías
gráficos con arrays hardcodeados
KPIs ficticios en frontend
resultados sin endpoint
seed que no usa el modelo real
subdimensiones en versión corta
grupos n < 5 visibles
datos personales junto a respuestas
baremos inventados
scoring calculado exclusivamente en frontend
```

---

# 107. Resultado esperado

Al finalizar debe ser posible ejecutar:

```text
1. Resetear datos demo
2. Poblar CENSOPAS demo
3. Abrir Colmena
4. Entrar a SYN-C20-2026
5. Navegar todas sus secciones
6. Entrar a SYN-M200-2026
7. Ver telemetría 200 → 186 → 180
8. Ver seis dimensiones
9. Ver veinte subdimensiones
10. Aplicar filtros seguros
11. Intentar filtro n < 5 y comprobar bloqueo
12. Abrir analítica
13. Ejecutar análisis disponible
14. Ver plan preventivo
15. Ver Balanced Scorecard
16. Generar reporte
17. Exportar
18. Ver trazabilidad
```

sin que ninguna pantalla dependa de datos hardcodeados.

---

# 108. Regla final para Codex / harness

No asumir que una funcionalidad existe porque existe una pantalla.

Para cada requisito:

```text
INSPECCIONAR
→ ENCONTRAR ENDPOINT
→ EJECUTAR ENDPOINT
→ VALIDAR RESPONSE
→ POBLAR DATOS DEMO
→ ABRIR FRONTEND
→ VALIDAR NETWORK
→ VALIDAR UI
→ VALIDAR PRIVACIDAD
→ DOCUMENTAR EVIDENCIA
```

Si falta una funcionalidad:

```text
NO ocultarla con mock data.
```

Debe reportarse como:

```text
NOT_IMPLEMENTED
```

y posteriormente implementarse usando la arquitectura real del proyecto.

---

# 109. Fuentes de requisitos

## Documento 1

**Manual técnico para la digitalización del método CENSOPAS-COPSOQ en Colmena**

Define principalmente:

- versiones corta y media;
- núcleo protegido;
- dimensiones y subdimensiones;
- códigos crudos;
- scoring;
- baremos;
- privacidad;
- modelo funcional;
- reporte;
- trazabilidad;
- pruebas del motor.

## Documento 2

**Guía y modelos de reporte CENSOPAS-COPSOQ para Colmena**

Define principalmente:

- estructura del informe;
- privacidad;
- visualizaciones;
- interpretación narrativa;
- modelos sintéticos corto y medio;
- priorización;
- plan preventivo;
- reglas automáticas.

## Documento 3

**Colmena Analytics — Modelo Premium de Reporte CENSOPAS-COPSOQ**

Define principalmente:

- dashboard ejecutivo;
- calidad;
- segmentación;
- intervalos de confianza;
- pruebas inferenciales;
- tamaño de efecto;
- corrección múltiple;
- correlaciones;
- clustering;
- regresión;
- validación;
- Balanced Scorecard;
- KPIs;
- alertas;
- seguimiento temporal.

---

# 110. Principio rector

Colmena debe demostrar tres cosas distintas:

```text
1. QUÉ RESPONDIÓ LA POBLACIÓN
   captura y datos crudos

2. QUÉ INDICA CENSOPAS
   resultado metodológico colectivo

3. QUÉ ANÁLISIS ADICIONAL HACE COLMENA
   estadística, segmentación, gestión y seguimiento
```

Nunca mezclar estas tres capas.

El resultado final debe ser una aplicación navegable, auditable, poblada y reproducible; no una colección de pantallas con datos ficticios escritos directamente en el frontend.
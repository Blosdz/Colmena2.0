# COLMENA — Test de auditoría integral CENSOPAS-COPSOQ

## 1. Objetivo

Este documento define un **test de auditoría del sistema Colmena** para comprobar que la implementación funcional, backend, frontend, motor estadístico, privacidad, reportes y exportaciones respetan la especificación derivada de:

1. `Manual_tecnico_CENSOPAS_COPSOQ_Colmena.pdf`
2. `Guia_y_modelos_de_reporte_CENSOPAS_COPSOQ_Colmena.pdf`
3. `Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena.pdf`
4. `COLMENA_SECCIONES_CENSOPAS_SEGUN_PDFS.md`

El test debe servir tanto para una auditoría manual como para un agente de desarrollo/QA que inspeccione el repositorio y ejecute pruebas.

---

# 2. Instrucción para el agente auditor

## Rol

Actúa como **auditor técnico de Colmena**.

Tu trabajo no consiste en asumir que la implementación es correcta.

Debes:

1. inspeccionar frontend, backend, migraciones, modelos, seeds y configuración;
2. identificar qué funciones existen realmente;
3. ejecutar las pruebas disponibles;
4. crear pruebas faltantes cuando sea razonable;
5. comprobar comportamiento mediante API, base de datos y UI;
6. registrar evidencia concreta;
7. marcar cada requisito como:
   - `PASS`
   - `FAIL`
   - `PARTIAL`
   - `BLOCKED`
   - `NOT_IMPLEMENTED`
8. diferenciar claramente:
   - requisito CENSOPAS;
   - funcionalidad Colmena;
   - analítica premium;
9. no declarar equivalencia oficial CENSOPAS si faltan activos metodológicos autorizados;
10. no modificar el sistema para hacer que la auditoría "pase" antes de registrar los defectos encontrados.

---

# 3. Archivos de salida obligatorios

El auditor debe generar:

```text
docs/audit/
├── censopas-audit-report.md
├── censopas-audit-results.json
├── censopas-audit-blockers.md
├── censopas-audit-test-matrix.md
└── evidence/
```

Opcionalmente:

```text
test-results/
coverage/
playwright-report/
```

---

# 4. Formato de resultado de cada prueba

Cada prueba debe registrar:

```text
ID:
Sección:
Severidad:
Requisito:
Procedimiento:
Resultado esperado:
Resultado obtenido:
Estado:
Evidencia:
Archivo / endpoint afectado:
Recomendación:
```

Ejemplo:

```text
ID: PRIV-001
Sección: Privacidad
Severidad: BLOCKER

Requisito:
Una unidad con n < 5 no debe publicarse.

Procedimiento:
Consultar resultados para una unidad con n = 4.

Resultado esperado:
El backend devuelve estado SUPPRESSED y no entrega porcentajes publicables.

Resultado obtenido:
...

Estado:
PASS / FAIL

Evidencia:
GET /api/...
response JSON...
```

---

# 5. Severidades

| Nivel | Significado |
|---|---|
| `BLOCKER` | Impide considerar segura o metodológicamente válida la funcionalidad CENSOPAS. |
| `CRITICAL` | Riesgo alto de privacidad, cálculo o resultado incorrecto. |
| `HIGH` | Función principal incompleta o inconsistente. |
| `MEDIUM` | Incumplimiento funcional importante, pero no bloquea todo el flujo. |
| `LOW` | Mejora de presentación, trazabilidad o UX. |

---

# 6. Regla de aprobación general

El sistema **NO APRUEBA** la auditoría CENSOPAS si existe al menos uno de estos casos:

```text
BLOCKER = FAIL
```

También debe quedar como:

```text
CENSOPAS OFFICIAL = BLOCKED
```

si falta cualquiera de estos activos:

```text
polaridad verificada
algoritmo autorizado
baremos C1 y C2 vigentes
versión de baremo
pruebas de concordancia con patrón autorizado
```

La ausencia de estos activos no significa que Colmena no pueda funcionar en modo de desarrollo o prueba.

Significa que no debe presentar los resultados como equivalentes oficiales.

---

# 7. Auditoría 1 — Arquitectura general del producto

La navegación esperada para un estudio CENSOPAS es:

```text
Proyecto
Constructor / Instrumento
Formulario
Telemetría
Resultados
Analítica
Plan y seguimiento
Reportes
Exportaciones
```

## ARCH-001 — Separación de módulos

**Severidad:** HIGH

Comprobar que no se mezcle todo en una sola pantalla.

Debe poder distinguirse funcionalmente:

```text
captura
control de calidad
resultado metodológico
analítica complementaria
gestión preventiva
salidas
```

### PASS

Existe separación clara de responsabilidades.

### FAIL

Ejemplos:

```text
telemetría calcula clasificación oficial
frontend calcula scoring
analítica premium reemplaza el resultado CENSOPAS
BSC modifica puntuaciones del instrumento
```

---

## ARCH-002 — Resultado oficial vs analítica Colmena

**Severidad:** BLOCKER

Comprobar que:

```text
Resultado CENSOPAS != índice premium Colmena
```

La analítica avanzada puede complementar el resultado, pero no reemplazarlo.

---

# 8. Auditoría 2 — Proyecto / Study

## STUDY-001 — Datos mínimos

Comprobar que el estudio pueda conservar al menos:

```text
centro laboral
versión
período
población
unidades de análisis
evaluador/responsable
regla de privacidad
estado
```

---

## STUDY-002 — Selección de versión

### Versión corta

Esperado:

```text
42 preguntas totales
31 ítems psicosociales
6 dimensiones
0 subdimensiones publicables como resultado separado
```

### Versión media

Esperado:

```text
112 preguntas totales
69 ítems psicosociales
6 dimensiones
20 subdimensiones
salud, bienestar y satisfacción descriptivos
```

---

## STUDY-003 — Congelamiento del estudio

**Severidad:** BLOCKER

Procedimiento:

1. crear estudio;
2. abrirlo para recibir respuestas;
3. intentar modificar:
   - preguntas;
   - códigos;
   - opciones;
   - matriz de constructos;
   - scoring;
   - baremo.

Esperado:

```text
cambio estructural bloqueado
```

o:

```text
nueva versión requerida
```

Nunca debe mutarse silenciosamente una versión usada por un estudio abierto o cerrado.

---

# 9. Auditoría 3 — Constructor / Instrumento

## INST-001 — Conteo versión corta

Consultar banco de preguntas.

Esperado:

```text
TOTAL = 42
PSICOSOCIALES = 31
DIMENSIONES = 6
```

No debe haber:

```text
duplicados
omisiones
códigos fuente repetidos indebidamente
```

---

## INST-002 — Conteo versión media

Esperado:

```text
TOTAL = 112
PSICOSOCIALES = 69
DIMENSIONES = 6
SUBDIMENSIONES = 20
```

---

## INST-003 — Protección del núcleo

**Severidad:** BLOCKER

Intentar editar una versión protegida CENSOPAS en producción:

```text
texto de pregunta
source_code
opciones
polaridad
peso
asignación a dimensión
```

Esperado:

```text
403 / error de dominio / operación bloqueada
```

No basta con ocultar el botón en frontend.

La restricción debe existir en backend.

---

## INST-004 — Módulos complementarios

Crear una pregunta de:

```text
teletrabajo
violencia
ergonomía
hostigamiento
pregunta abierta
```

Esperado:

```text
se registra como módulo complementario
NO entra al scoring CENSOPAS
NO modifica D1-D6
NO modifica S1-S20
```

---

# 10. Auditoría 4 — Catálogos

El Manual exige probar cada catálogo con:

```text
mínimo
máximo
vacío
código inválido
```

## CAT-001 — Código mínimo válido

Enviar el menor `raw_code` válido del catálogo.

Esperado:

```text
aceptado
raw_code conservado
```

---

## CAT-002 — Código máximo válido

Esperado:

```text
aceptado
```

---

## CAT-003 — Código inválido

Ejemplo:

```json
{
  "raw_code": "9999"
}
```

Esperado:

```text
rechazado
```

No debe convertirse silenciosamente a otra opción.

---

## CAT-004 — Vacío

Comprobar comportamiento conforme a obligatoriedad y reglas de faltantes.

Esperado:

```text
missing explícito
```

No se permite imputación silenciosa.

---

# 11. Auditoría 5 — Formulario y respuestas

## RESP-001 — Persistencia de raw_code

**Severidad:** BLOCKER

Responder un ítem.

Comprobar en base de datos:

```text
responses.raw_code
```

Debe conservar exactamente el código recibido.

---

## RESP-002 — Valores derivados separados

Comprobar que:

```text
raw_code
risk_value
score_0_100
```

no sean la misma columna ni sobrescriban el dato original.

Esperado:

```text
raw_code = fuente inmutable
response_scores = valores derivados
```

o estructura equivalente.

---

## RESP-003 — Una respuesta por sesión + pregunta

Intentar duplicar respuesta para el mismo ítem.

Esperado:

```text
update controlado
```

o restricción equivalente.

No deben existir dos respuestas activas contradictorias para:

```text
response_session + question
```

---

## RESP-004 — Completitud

Crear cuestionario incompleto.

Esperado:

```text
faltantes identificados
estado de validación
regla de inclusión/exclusión trazable
```

---

# 12. Auditoría 6 — Anonimato y privacidad

## PRIV-001 — Separación de identidad

**Severidad:** BLOCKER

Comprobar que las respuestas CENSOPAS no incluyan directamente:

```text
nombre
DNI
correo
teléfono
identificador laboral
```

El motor analítico debe trabajar con identificadores técnicos anónimos.

---

## PRIV-002 — Grupo con n = 1

Esperado:

```text
SUPPRESSED
```

No publicar:

```text
conteos identificables
porcentaje
color
clasificación
```

---

## PRIV-003 — Grupo con n = 4

Esperado:

```text
SUPPRESSED
```

---

## PRIV-004 — Grupo con n = 5

Esperado:

```text
publicable
```

si no existe riesgo adicional de reidentificación.

---

## PRIV-005 — Supresión por cruce

Crear:

```text
Área = Operaciones
Turno = Noche
Contrato = Temporal
n = 3
```

Esperado:

```text
bloqueo/supresión
```

aunque cada variable individual tenga n suficiente.

---

## PRIV-006 — Ataque por totales

Comprobar que una celda oculta no pueda deducirse restando:

```text
TOTAL - otras categorías visibles
```

Esperado:

```text
supresión secundaria / agrupación
```

cuando corresponda.

---

## PRIV-007 — Privacidad transversal

Ejecutar la misma consulta mediante:

```text
API
dashboard
analítica
PDF
XLSX
JSON
Power BI / dataset externo si existe
```

Esperado:

```text
misma regla de privacidad
```

**FAIL crítico:** backend entrega datos y sólo frontend los oculta.

---

# 13. Auditoría 7 — Scoring CENSOPAS

## SCORE-001 — Prueba por ítem

Para cada ítem puntuable probar los cinco niveles transformados esperados:

```text
0
25
50
75
100
```

según la regla de polaridad configurada.

Debe comprobarse tanto:

```text
polaridad directa
polaridad inversa
```

---

## SCORE-002 — No sobrescribir raw_code

Antes y después de ejecutar scoring:

```text
hash/raw_code inicial
==
hash/raw_code posterior
```

---

## SCORE-003 — Constructo exacto

Para cada dimensión/subdimensión:

1. obtener matriz esperada;
2. obtener ítems realmente usados por el motor;
3. comparar conjuntos.

Esperado:

```text
exact match
```

No se aceptan ítems extra o faltantes.

---

## SCORE-004 — Faltantes por constructo

Crear respuestas faltantes.

Esperado:

```text
n válido explícito
denominador correcto
```

No imputar respuestas sin regla documentada.

---

## SCORE-005 — Transformación provisional

Mientras el algoritmo no esté autorizado:

Esperado:

```text
classification_status = PROVISIONAL o BLOCKED
```

Nunca:

```text
OFFICIAL
```

---

# 14. Auditoría 8 — Baremos

## BAREM-001 — Ausencia de baremo

**Severidad:** BLOCKER

Retirar/deshabilitar baremo autorizado.

Ejecutar resultados.

Esperado:

```text
colores oficiales bloqueados
estado de prueba/provisional visible
```

---

## BAREM-002 — Versionado

Comprobar que el baremo tenga al menos:

```text
versión
población
constructo
C1
C2
dirección
fuente
fecha
checksum/hash o trazabilidad equivalente
```

---

## BAREM-003 — Límite inferior C1

Probar:

```text
C1 - epsilon
C1
C1 + epsilon
```

Verificar la clasificación exacta definida por el baremo.

---

## BAREM-004 — Límite C2

Probar:

```text
C2 - epsilon
C2
C2 + epsilon
```

---

## BAREM-005 — No usar 33.33 / 66.67 inventados

Buscar hardcodes como:

```text
33.33
66.67
33.3
66.6
```

cuando pretendan actuar como cortes oficiales.

Si se usan sin baremo autorizado:

```text
FAIL BLOCKER
```

---

# 15. Auditoría 9 — Clasificación colectiva

Sólo ejecutar como clasificación metodológica habilitada cuando los prerrequisitos estén disponibles.

## CLASS-001 — Rojo 49.9%

Entrada:

```text
rojo = 49.9%
```

Esperado:

```text
NO riesgo alto únicamente por regla del 50%
```

---

## CLASS-002 — Rojo 50.0%

Entrada:

```text
rojo = 50.0%
```

Esperado:

```text
riesgo alto
```

---

## CLASS-003 — Verde 50.0%

Entrada:

```text
verde = 50.0%
rojo < 50%
```

Esperado:

```text
factor protector
```

---

## CLASS-004 — Amarillo predominante

Esperado:

```text
riesgo medio
```

si no se cumple condición de rojo o verde.

---

## CLASS-005 — Empate

Crear distribución semejante/empate.

Esperado:

```text
REVIEW_REQUIRED
```

o estado equivalente.

Debe quedar registro de decisión documentada.

No inventar una clasificación silenciosa.

---

# 16. Auditoría 10 — Telemetría

Telemetría debe describir principalmente participación y calidad.

## TEL-001 — Convocados

Verificar conteo contra base.

---

## TEL-002 — Recibidos

Verificar conteo.

---

## TEL-003 — Válidos

Verificar conteo.

---

## TEL-004 — Excluidos

Verificar conteo y razones.

---

## TEL-005 — Tasa válida

Comprobar fórmula:

```text
válidos / convocados * 100
```

---

## TEL-006 — Calidad de captura

Cuando la funcionalidad exista comprobar:

```text
completitud
ítems omitidos
duración
patrones
duplicidad
coherencia
```

Las banderas de calidad no deben convertirse automáticamente en diagnóstico.

---

# 17. Auditoría 11 — Resultados

## RES-001 — Seis dimensiones

Corta y media deben mostrar:

```text
D1
D2
D3
D4
D5
D6
```

---

## RES-002 — Versión corta sin subdimensiones publicadas

**Severidad:** BLOCKER

Abrir resultados de versión corta.

Esperado:

```text
NO mostrar S1-S20 como resultados separados
```

---

## RES-003 — Versión media con 20 subdimensiones

Esperado:

```text
S1 ... S20
```

---

## RES-004 — Resultado completo

Cada dimensión publicable debe incluir:

```text
n válido
favorable n / %
intermedio n / %
desfavorable n / %
nivel
versión
```

---

## RES-005 — Visual principal

El visual recomendado para composición es:

```text
barra horizontal apilada al 100%
```

El color nunca debe ser el único medio de interpretación.

Debe existir:

```text
etiqueta
porcentaje
leyenda o texto
```

---

## RES-006 — Perfil sociolaboral

Debe presentar variables descriptivas mediante:

```text
n
%
```

aplicando privacidad.

No debe incorporarlas al scoring psicosocial.

---

## RES-007 — Salud versión media

Debe ser:

```text
descriptiva
no diagnóstica
```

No debe mezclarse con clasificación psicosocial oficial.

---

# 18. Auditoría 12 — Analítica

## ANA-001 — Separación metodológica

Analítica avanzada debe identificarse como:

```text
Analítica Colmena
```

o equivalente.

No debe aparecer como una nueva dimensión oficial CENSOPAS.

---

## ANA-002 — Disponibilidad de métodos

Cuando estén implementados verificar al menos:

```text
descriptiva
frecuencias
chi-cuadrado
Mann-Whitney
Kruskal-Wallis
Spearman
alfa
omega
Benjamini-Hochberg
```

y posteriormente:

```text
K-means
regresión logística
```

---

## ANA-003 — Validación de método

Intentar ejecutar una prueba incompatible con los datos.

Esperado:

```text
rechazo
warning estructurado
método alternativo
```

No ejecutar cualquier prueba sobre cualquier variable.

---

## ANA-004 — Múltiples pruebas

Si se realizan múltiples contrastes:

Esperado:

```text
p
q ajustado / adjusted_p_value
```

cuando corresponda.

---

## ANA-005 — Tamaño de efecto

Toda comparación inferencial relevante debe incluir:

```text
effect_size
effect_label
```

cuando corresponda.

No presentar únicamente `p < 0.05`.

---

## ANA-006 — Intervalos

Las prevalencias principales premium deben incluir:

```text
IC 95%
```

cuando esta capa esté habilitada.

---

## ANA-007 — Clustering

Si K-means está habilitado comprobar:

```text
n suficiente
semilla
parámetros
métrica de estabilidad/silhouette
salida agregada
```

Nunca exponer asignación individual a usuarios de negocio.

---

## ANA-008 — Regresión

Si está habilitada comprobar:

```text
OR
IC 95%
validación
desempeño
versión del modelo
limitaciones
```

No debe utilizarse para decisiones laborales individuales.

---

# 19. Auditoría 13 — Plan preventivo y seguimiento

## PLAN-001 — Hallazgo → acción

Toda prioridad debe poder vincularse a:

```text
hallazgo
hipótesis de origen
medida
responsable
plazo
indicador
meta
estado
```

---

## PLAN-002 — Riesgo alto sin acción

Crear resultado prioritario sin acción.

Esperado:

```text
warning de plan incompleto
```

antes de aprobar reporte final, si el flujo exige plan.

---

## PLAN-003 — BSC

Cuando esté habilitado:

cada KPI debe tener:

```text
nombre
fórmula
línea base
meta
dueño
frecuencia
estado
```

---

## PLAN-004 — No compensación

Un KPI favorable no debe borrar automáticamente un riesgo metodológico.

BSC y resultado CENSOPAS son capas distintas.

---

# 20. Auditoría 14 — Reportes

## REP-001 — Estructura mínima

El reporte final debe comprobar al menos:

```text
portada/control documental
resumen ejecutivo
ficha técnica
calidad de datos
perfil sociolaboral
resultados por dimensión
subdimensiones sólo si media
unidades de análisis si publicables
salud descriptiva sólo si media
análisis cualitativo cuando exista
priorización
plan preventivo
conclusiones
anexo técnico/auditoría
```

---

## REP-002 — Denominadores

Cada tabla relevante debe indicar:

```text
N total
n válido
```

cuando corresponda.

---

## REP-003 — Faltantes

El reporte debe informar:

```text
faltantes
exclusiones
```

No ocultarlos.

---

## REP-004 — Estado provisional

Si no hay equivalencia oficial:

Esperado:

```text
advertencia visible
```

No debe esconderse en metadatos.

---

## REP-005 — Narrativa

Buscar textos prohibidos o problemáticos como:

```text
"este trabajador tiene..."
"diagnóstico..."
"la persona..."
"el turno causa..."
```

cuando impliquen diagnóstico o causalidad individual no soportada.

La narrativa debe ser colectiva y prudente.

---

## REP-006 — Hash y reproducibilidad

Generar dos veces el mismo reporte con:

```text
mismos datos
misma versión
mismo baremo
mismo algoritmo
mismos filtros
```

Esperado:

```text
mismo hash lógico de entrada
mismos resultados numéricos
```

La representación binaria del PDF puede variar por metadatos de generación; la auditoría debe distinguir hash de datos/entrada de hash de archivo cuando aplique.

---

# 21. Auditoría 15 — Exportaciones

## EXP-001 — PDF

Debe heredar:

```text
privacidad
denominadores
versión
algoritmo
confidencialidad
```

---

## EXP-002 — XLSX

Intentar exportar un grupo n < 5.

Esperado:

```text
dato suprimido/agregado
```

No debe reaparecer una celda ocultada en dashboard.

---

## EXP-003 — JSON

Misma regla.

---

## EXP-004 — Exportación reproducible

Registrar:

```text
study
filtros
fecha
versión algoritmo
baremo
hash
usuario
```

---

## EXP-005 — Datos individuales CENSOPAS

Comprobar permisos y formato.

Una exportación de negocio no debe entregar una tabla que permita reconstruir respuestas individuales identificables.

---

# 22. Auditoría 16 — Trazabilidad

## AUD-001 — Eventos mínimos

Comprobar bitácora para:

```text
creación de instrumento
nueva versión
edición de ítem
edición de dimensión
edición de scoring
edición de baremo
apertura de estudio
cierre de estudio
ejecución analítica
generación de reporte
exportación
```

---

## AUD-002 — Analysis run

Cada análisis importante debe registrar:

```text
study
método
parámetros
versión del motor
versión algoritmo
input hash
inicio
fin
estado
error
```

o equivalentes.

---

## AUD-003 — Report run

Debe poder identificarse:

```text
datos usados
análisis usados
plantilla
versión
fecha
hash
```

---

# 23. Auditoría 17 — Comparación temporal

## TIME-001 — Versiones diferentes

Comparar dos mediciones con distinta versión.

Esperado:

```text
bloqueo
```

o advertencia explícita de no comparabilidad.

---

## TIME-002 — Baremos diferentes

Esperado:

```text
bloqueo / advertencia
```

---

## TIME-003 — Unidad redefinida

Si "Operaciones" cambia de definición entre mediciones:

Esperado:

```text
no presentar la serie como directamente comparable sin advertencia
```

---

# 24. Auditoría 18 — Seguridad metodológica

## SAFE-001 — Sin baremo oficial

Intentar cambiar manualmente:

```text
classification_status = OFFICIAL
```

Esperado:

```text
rechazado por backend / regla de dominio
```

---

## SAFE-002 — Modificar instrumento usado

Esperado:

```text
bloqueo
```

---

## SAFE-003 — Calcular scoring en frontend

Buscar código de:

```text
C1
C2
risk_value
score_0_100
clasificación 50%
```

en componentes frontend.

Si la UI está calculando el resultado metodológico:

```text
FAIL HIGH/BLOCKER
```

El frontend debe presentar; el backend debe validar, calcular y proteger.

---

# 25. Auditoría 19 — Pruebas automáticas

Estas herramientas son una recomendación de implementación Colmena, no un requisito del método CENSOPAS.

## Backend

Preferir:

```text
pytest
```

Cobertura mínima esperada:

```text
catálogos
instrument locking
raw_code
scoring
constructos
baremos
clasificación
privacidad
análisis
reportes
exportaciones
```

---

## Frontend

Si el proyecto ya usa Vitest/React Testing Library, cubrir:

```text
dashboard
instrumento bloqueado
survey
telemetría
privacy suppression
banner provisional
dimensiones
subdimensiones condicionadas por versión
analysis polling
reporte/exportación
```

---

## E2E

Si Playwright ya está disponible:

```text
crear proyecto CENSOPAS
seleccionar versión corta
publicar
responder
cerrar estudio
ver telemetría
ver resultados
comprobar ausencia de subdimensiones
generar reporte
exportar
```

y:

```text
crear proyecto CENSOPAS
seleccionar versión media
publicar
responder
cerrar
ver 6 dimensiones
ver 20 subdimensiones
aplicar filtro n < 5
comprobar supresión
ejecutar analítica
crear plan
generar reporte
```

---

# 26. Dataset sintético obligatorio de QA

Crear fixtures que NO pretendan ser baremos oficiales.

## Dataset A — versión corta

```text
20 sesiones válidas
42 respuestas esperadas por sesión
6 dimensiones
sin subdimensiones publicables
```

Debe incluir deliberadamente:

```text
grupo de 4 personas
grupo de 5 personas
respuestas incompletas
código inválido
caso de empate
```

---

## Dataset B — versión media

```text
200 convocados
186 recibidos
180 válidos
112 preguntas
69 puntuables
6 dimensiones
20 subdimensiones
```

Debe incluir:

```text
varias áreas
turnos
contratos
grupo n < 5
faltantes
un caso de filtro inseguro
```

Los valores de riesgo usados en fixtures son para QA.

No deben presentarse como baremos oficiales.

---

# 27. Prueba de regresión obligatoria

El Manual exige verificar que el mismo conjunto de datos y versión produzca el mismo resultado reproducible.

## REG-001

Ejecutar análisis A.

Guardar:

```text
input_hash
algorithm_version
result JSON
```

Ejecutar nuevamente sin cambios.

Esperado:

```text
mismos valores
mismas clasificaciones
mismos denominadores
mismas supresiones
```

---

## REG-002

Modificar una sola respuesta.

Esperado:

```text
input_hash diferente
```

y nueva ejecución trazable.

---

# 28. Prueba de concordancia

**Severidad:** BLOCKER para equivalencia oficial.

Cuando exista un patrón autorizado:

```text
fixture oficial
     ↓
Colmena
     ↓
resultado Colmena
     ↓
comparación con resultado esperado
```

Comparar:

```text
puntajes
constructos
categorías
clasificación
supresión
```

Resultado requerido:

```text
100% concordante en casos patrón autorizados
```

La tolerancia numérica, si corresponde, debe documentarse.

Hasta tener estos casos:

```text
official_equivalence_enabled = false
```

o estado equivalente.

---

# 29. Prueba visual

Revisar manualmente:

```text
desktop
tablet
móvil
PDF
```

Comprobar:

```text
texto legible
n visible
porcentajes visibles
color acompañado de etiqueta
gráficos sin recortes
tablas sin columnas perdidas
advertencia provisional visible
supresión visible sin revelar el dato
```

---

# 30. Criterios de aceptación por módulo

| Módulo | Para aprobar |
|---|---|
| Proyecto | versión y configuración congelables |
| Constructor | estructura correcta y núcleo protegido |
| Formulario | captura anónima y raw_code conservado |
| Telemetría | participación y calidad conciliadas |
| Resultados | estructura corta/media correcta |
| Privacidad | n < 5 protegido en todas las salidas |
| Scoring | separación raw/derivado y pruebas unitarias |
| Baremo | versionado y bloqueos correctos |
| Analítica | separada del resultado oficial |
| Plan | acción, responsable, plazo, KPI y seguimiento |
| Reportes | estructura, limitaciones y trazabilidad |
| Exportaciones | privacidad y reproducibilidad |
| Auditoría | eventos y hashes registrados |

---

# 31. Resultado final de auditoría

El reporte final debe comenzar con:

```text
COLMENA CENSOPAS AUDIT
======================

Fecha:
Commit:
Ambiente:
Base de datos:
Backend:
Frontend:

Tests ejecutados:
PASS:
FAIL:
PARTIAL:
BLOCKED:
NOT_IMPLEMENTED:

Blockers:
1.
2.
3.

Estado funcional:
[ ] Proyecto
[ ] Constructor
[ ] Formulario
[ ] Telemetría
[ ] Resultados
[ ] Analítica
[ ] Plan
[ ] Reportes
[ ] Exportaciones

Estado metodológico:
[ ] PROVISIONAL
[ ] VERIFIED
[ ] OFFICIAL
[ ] BLOCKED

Conclusión:
APROBADO / APROBADO CON OBSERVACIONES / NO APROBADO
```

---

# 32. Score de auditoría

Puede calcularse un score interno de QA para seguimiento del desarrollo:

```text
PASS = 1
PARTIAL = 0.5
FAIL = 0
NOT_IMPLEMENTED = 0
BLOCKED = no puntúa si depende de un activo externo documentado
```

Ejemplo:

```text
score_qa = puntos_obtenidos / puntos_evaluables * 100
```

Este `score_qa` es únicamente un indicador de desarrollo de Colmena.

**No es una puntuación CENSOPAS-COPSOQ.**

---

# 33. Regla final para el auditor

No finalizar con:

```text
"todo está bien"
```

sin evidencia.

La conclusión debe indicar exactamente:

```text
qué existe
qué funciona
qué falla
qué falta
qué está bloqueado por metodología
qué debe corregirse primero
qué pruebas se ejecutaron
qué pruebas no pudieron ejecutarse
```

Prioridad recomendada:

```text
1. privacidad
2. integridad del instrumento
3. raw_code y scoring
4. baremo/concordancia
5. resultados
6. reportes/exportaciones
7. analítica premium
8. BSC y seguimiento
```

---

# 34. Fuentes internas utilizadas

## Manual técnico CENSOPAS-COPSOQ para Colmena

Especialmente:

```text
p. 5      alcance y versiones
pp. 6-7   adaptación y arquitectura
p. 8      raw_code, scoring y baremos
pp. 9-10  flujo, privacidad y reporte
pp. 56-57 verificación y pruebas mínimas del motor
p. 58     doble control y trazabilidad
```

Las pruebas mínimas expresamente indicadas en el Manual incluyen:

```text
catálogos: mínimo, máximo, vacío, inválido
ítems: polaridad y 0/25/50/75/100
constructos: inclusión, faltantes y denominador
baremos: alrededor de C1/C2
agrupación: 49.9%, 50.0% y empates
privacidad: n 1-4, cruces y exportaciones
regresión: mismo dataset y versión → mismo resultado reproducible
```

## Guía y modelos de reporte

Especialmente:

```text
pp. 5-7   estructura, privacidad, gráficos y control de calidad
p. 25     reglas automáticas y bloques reutilizables
```

## Modelo premium

Especialmente:

```text
p. 3      separación de capas
pp. 4-17  dashboard y analítica
p. 26     reglas auditables del motor
p. 27     roadmap y concordancia
p. 28     especificación final
```

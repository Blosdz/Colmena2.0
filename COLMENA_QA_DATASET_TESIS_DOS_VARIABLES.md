# COLMENA — Dataset QA: tesis académica de 2 variables (Calidad del servicio → Satisfacción del cliente)

## 0. Qué es este documento

Dataset **ejecutable** para probar el flujo académico completo de Colmena (no CENSOPAS):
proyecto → variables → dimensiones → ítems → escala Likert → respuestas → scores → baremos →
descriptiva → confiabilidad → Spearman → scatter → comparación de dimensiones.

Todos los datos numéricos de este documento son **SINTÉTICOS**. Ningún valor aquí debe
presentarse como resultado real de una tesis. El mapeo de endpoints está tomado de
`backend/app/tests/integration/test_censopas_flow.py` (única prueba de integración que ejercita
el flujo variable→construct→item→scoring-rule→barem→study→response-session de extremo a extremo
en este repo), adaptado a un proyecto académico. Dos cosas **no están confirmadas** y deben
verificarse antes de correr esto contra la API real:

```text
1. El valor de study_type para un proyecto académico (test_censopas_flow.py usa "CENSO";
   revisar app/models/study.py o el enum real antes de asumir "ACADEMIC"/"GENERAL").
2. Los valores válidos de `direction` en BaremCutoff más allá de "LOWER_BETTER"
   (revisar app/schemas/censopas.py::Direction) — este dataset usa "HIGHER_BETTER" para
   Calidad/Satisfacción (más puntaje = mejor), asumiendo que existe como opuesto simétrico.
```

Si alguno de los dos no existe tal cual, es un **GAP** a registrar en
`docs/frontend/ANALYTICS_GAPS.md`, no algo que deba adivinarse en producción.

---

## 1. Resumen del proyecto de prueba

```yaml
titulo: "Relación entre la calidad del servicio y la satisfacción del cliente en una empresa comercial de Arequipa, 2026"
tipo: aplicada
enfoque: cuantitativo
nivel: correlacional
diseño: no_experimental
corte: transversal
hipotesis:
  H1: "Existe relación estadísticamente significativa entre calidad del servicio y satisfacción del cliente."
  H0: "No existe relación estadísticamente significativa entre ambas variables."
alfa: 0.05
```

## 2. Estructura variable → dimensión → ítem

```text
X Calidad del servicio (INDEPENDENT, ORDINAL, LIKERT_5)
├── X_D1 Fiabilidad          → X01 X02 X03 X04
├── X_D2 Capacidad de respuesta → X05 X06 X07 X08
└── X_D3 Atención y empatía  → X09 X10 X11 X12

Y Satisfacción del cliente (DEPENDENT, ORDINAL, LIKERT_5)
├── Y_D1 Satisfacción con el servicio      → Y01 Y02 Y03 Y04
├── Y_D2 Cumplimiento de expectativas      → Y05 Y06 Y07 Y08
└── Y_D3 Fidelización e intención futura   → Y09 Y10 Y11 Y12
```

24 ítems analíticos + 4 ítems descriptivos no puntuables (edad, sexo, frecuencia de uso,
tipo de cliente). Escala para X01–X12 e Y01–Y12:

| raw_code | Etiqueta | Peso (map score_0_100 si se reusa scoring-rules) |
|---:|---|---:|
| 1 | Totalmente en desacuerdo | 0 |
| 2 | En desacuerdo | 25 |
| 3 | Ni de acuerdo ni en desacuerdo | 50 |
| 4 | De acuerdo | 75 |
| 5 | Totalmente de acuerdo | 100 |

Todos los ítems están redactados en dirección positiva → `scoring_direction: DIRECT` en los 24.
No hay ítems invertidos en esta versión de prueba (a diferencia de CENSOPAS, que sí usa `REVERSE`).

Colmena debe conservar, por dimensión y por variable, **ambos** conceptos si el `Construct`/
`ConstructScore` lo permite (confirmado en la auditoría: `ConstructScore.raw_score` y
`ConstructScore.score_0_100` existen como campos separados):

```text
raw_sum   → X_D1: 4–20   | X_TOTAL: 12–60
score_0_100 → normalizado 0–100 vía la misma fórmula ((raw-min)/(max-min))*100
```

## 3. Baremo QA (NO oficial, NO validado — solo para probar el motor)

```text
Bajo   12–27  (raw_score variable)   |  4–9   (raw_score dimensión)
Medio  28–43                          |  10–14
Alto   44–60                          |  15–20
```

Al crear el barem vía API, usar `barem_type: "EXPLORATORY"` (nunca `"OFFICIAL"`) y
`source_reference: "Dataset QA tesis dos variables — sin validez científica"` — igual que la
regla CENSOPAS de no inventar C1/C2 oficiales (§11/§98 del harness de analítica), aplicada aquí
a un baremo académico.

## 4. Secuencia real de llamadas a la API (adaptada de test_censopas_flow.py)

```text
POST /api/v1/instruments                         {"name": "Calidad-Satisfacción (QA)", "is_system": false}
POST /api/v1/instruments/{id}/versions            {"version_code": "V1", "status": "DRAFT"}

# Variables raíz (construct_type: VARIABLE)
POST /api/v1/instrument-versions/{v}/structure-variables
  {"code": "X", "name": "Calidad del servicio", "role": "INDEPENDENT"}
POST /api/v1/instrument-versions/{v}/structure-variables
  {"code": "Y", "name": "Satisfacción del cliente", "role": "DEPENDENT"}

# 24 ítems (repetir por cada X01..X12, Y01..Y12)
POST /api/v1/instrument-versions/{v}/items
  {"code": "X01", "question_text": "La empresa cumple con el servicio que ofrece.", "question_type": "LIKERT"}

# 6 dimensiones (construct_type: DIMENSION, parent_id = id de X o Y)
POST /api/v1/instrument-versions/{v}/constructs
  {"parent_id": "<X.id>", "code": "X_D1", "name": "Fiabilidad", "construct_type": "DIMENSION"}
# ... repetir para X_D2, X_D3, Y_D1, Y_D2, Y_D3

# Vincular cada ítem a su dimensión (construct_item)
POST /api/v1/constructs/{X_D1.id}/items
  {"question_id": "<X01.id>", "weight": 1, "scoring_direction": "DIRECT"}
# ... repetir para los 24 ítems contra su dimensión

# Reglas de puntuación por ítem (mapa Likert 1-5 -> 0/25/50/75/100)
POST /api/v1/instrument-versions/{v}/scoring-rules
  {"question_id": "<X01.id>", "parameters": {"map": {"1":0,"2":25,"3":50,"4":75,"5":100}}}
# ... repetir para los 24 ítems

# Barem QA por dimensión y por variable (6 + 2 = 8 cutoffs si el motor soporta 3 bandas
# con un solo cut_1/cut_2 por construct_id — ver §3)
POST /api/v1/instrument-versions/{v}/barems     {"name": "Barem QA tesis dos variables"}
POST /api/v1/barems/{barem.id}/cutoffs
  {"construct_id": "<X.id>", "cut_1": 45, "cut_2": 73.3, "direction": "HIGHER_BETTER"}
  # cut_1/cut_2 en escala 0-100 equivalen a raw 27/43 sobre rango 12-60:
  # ((27-12)/(60-12))*100 = 31.25   ((43-12)/(60-12))*100 = 64.6
  # AJUSTAR el ejemplo anterior (45/73.3) si el motor puntúa en escala 0-100 y no raw —
  # verificar contra ConstructScore.score_0_100 antes de fijar el cutoff real.

# Proyecto, encuesta y estudio
POST /api/v1/projects/{project_id}/surveys/from-instrument
  {"created_by_user_id": "<user>", "instrument_version_id": "<v>", "name": "Encuesta Calidad-Satisfacción"}
POST /api/v1/projects/{project_id}/studies
  {"survey_id": "<survey.id>", "name": "Estudio tesis QA", "study_type": "???", "min_publishable_n": 1}
  # study_type sin confirmar — ver advertencia en §0.
PATCH /api/v1/studies/{study.id}   {"barem_id": "<barem.id>"}
POST /api/v1/studies/{study.id}/open

# Por cada participante sintético (ver §5): crear sesión, responder 24 ítems, completar
POST /api/v1/studies/{study.id}/response-sessions
PUT  /api/v1/response-sessions/{rs.id}/responses/{item.id}   {"raw_code": "4"}
POST /api/v1/response-sessions/{rs.id}/complete

# Cálculo de scores (equivalente académico de /censopas/scoring — confirmar si existe un
# endpoint genérico /studies/{id}/scoring además del CENSOPAS-específico; la auditoría de
# endpoints encontró POST /studies/{id}/scoring -> ScoreRunSummary en studies.py, que es el
# que corresponde usar aquí, NO /censopas/scoring)
POST /api/v1/studies/{study.id}/scoring

# Analítica (todas confirmadas en app/api/v1/analytics.py)
POST /api/v1/studies/{study.id}/analytics/describe          {"construct_ids": ["X","Y","X_D1", "..."]}
POST /api/v1/studies/{study.id}/analytics/reliability        {"construct_ids": ["X","Y","X_D1","X_D2","X_D3","Y_D1","Y_D2","Y_D3"]}
POST /api/v1/studies/{study.id}/analytics/correlation         {"x_construct_id": "<X.id>", "y_construct_id": "<Y.id>", "method": "SPEARMAN"}
POST /api/v1/studies/{study.id}/analytics/spearman-matrix      {"construct_ids": ["X_D1","X_D2","X_D3","Y_D1","Y_D2","Y_D3"], "include_points": true}
```

## 5. Participantes sintéticos

### 5.1 Muestra mínima explícita (10 casos — igual a la ilustrada por el usuario, ya
etiquetada como sintética)

| ID | X01 | X02 | X03 | X04 | X05 | X06 | X07 | X08 | X09 | X10 | X11 | X12 | Y01 | Y02 | Y03 | Y04 | Y05 | Y06 | Y07 | Y08 | Y09 | Y10 | Y11 | Y12 |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 5|5|4|5|4|5|4|5|5|4|4|5|5|5|4|5|4|5|5|4|5|5|4|5 |
| 2 | 4|4|4|5|4|4|4|4|4|5|4|4|4|4|5|4|4|4|4|5|4|4|5|4 |
| 3 | 3|4|3|4|3|4|3|4|4|3|3|4|3|4|3|4|3|4|3|4|4|3|3|4 |
| 4 | 2|3|2|3|2|3|2|3|3|2|2|3|2|3|2|3|2|3|2|3|3|2|2|3 |
| 5 | 1|2|2|1|2|2|1|2|2|1|2|2|1|2|1|2|2|1|2|2|2|1|2|1 |
| 6 | 5|4|5|5|5|4|5|5|4|5|5|5|5|4|5|5|5|4|5|5|4|5|5|5 |
| 7 | 4|4|3|4|4|3|4|4|4|4|3|4|4|4|4|3|4|4|3|4|4|4|3|4 |
| 8 | 3|3|4|3|3|3|4|3|3|4|3|3|3|3|4|3|3|4|3|3|3|4|3|3 |
| 9 | 2|2|3|2|2|3|2|2|3|2|3|2|2|2|3|2|2|3|2|2|3|2|3|2 |
| 10| 5|4|4|5|5|4|4|5|5|4|5|4|5|4|5|5|4|5|4|5|5|4|5|5 |

Con n=10 el motor de correlación/confiabilidad debe correr sin error, pero varias pruebas
(Spearman con IC, Kruskal-Wallis por grupos) no serán estadísticamente informativas. Usarlo
solo para validar que el **pipeline** funciona de punta a punta (Caso "n insuficiente" del
harness de analítica, §70 Caso B).

### 5.2 Generador reproducible (100–400 casos, recomendado para probar analítica real)

En vez de fabricar a mano cientos de filas (lo que sería inventar datos sin trazabilidad),
usar este generador con semilla fija — produce una correlación latente controlada entre X e Y
(~0.70 esperado) y expande a Likert 1-5 con ruido:

```python
# scripts/qa/gen_tesis_dos_variables.py
import csv
import random

import numpy as np

SEED = 42
N = 200
TARGET_RHO = 0.70

rng = np.random.default_rng(SEED)

# Puntaje latente correlacionado (distribución normal truncada, luego mapeado a 1-5)
mean = [0, 0]
cov = [[1, TARGET_RHO], [TARGET_RHO, 1]]
latent = rng.multivariate_normal(mean, cov, size=N)


def to_likert(z: float, item_noise_sd: float = 0.35) -> int:
    z_noisy = z + rng.normal(0, item_noise_sd)
    # Mapea z ~ N(0,1) a 1..5 vía cuantiles aproximados
    cuts = [-1.28, -0.52, 0.52, 1.28]
    for i, c in enumerate(cuts, start=1):
        if z_noisy < c:
            return i
    return 5


rows = []
x_items = [f"X{n:02d}" for n in range(1, 13)]
y_items = [f"Y{n:02d}" for n in range(1, 13)]

for pid in range(1, N + 1):
    zx, zy = latent[pid - 1]
    row = {"id": pid}
    for code in x_items:
        row[code] = to_likert(zx)
    for code in y_items:
        row[code] = to_likert(zy)
    rows.append(row)

with open("qa_tesis_dos_variables.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", *x_items, *y_items])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generado qa_tesis_dos_variables.csv con {N} participantes, rho objetivo={TARGET_RHO}")
```

Requiere `numpy`. Correr con `python scripts/qa/gen_tesis_dos_variables.py`, luego un script de
seeding (no incluido aquí — depende de credenciales/entorno reales) que recorra el CSV y haga
`PUT /response-sessions/{id}/responses/{item_id}` por cada celda, siguiendo la secuencia de §4.

El rho resultante en la muestra real será cercano a 0.70 pero no exacto — eso es correcto y
esperado de datos simulados con ruido; no forzar el valor final a coincidir con el ejemplo
ilustrativo de la tesis (§6).

## 6. Salidas ilustrativas esperadas (SINTÉTICAS — no verdades, solo forma del contrato)

Estas cifras son las que el propio ejemplo de tesis proyecta como plausibles para n=200; sirven
para verificar que la **forma** de la respuesta de la API sea razonable, no para validar
exactitud numérica (eso lo decide el generador de §5.2 y el motor real).

```json
// POST .../analytics/correlation  (forma esperada, valores ilustrativos)
{
  "method": "SPEARMAN",
  "x": {"id": "X", "label": "Calidad del servicio"},
  "y": {"id": "Y", "label": "Satisfacción del cliente"},
  "coefficient": 0.71,
  "p_value": 0.0001,
  "n": 200
}
```

```json
// POST .../analytics/reliability (forma esperada, valores ilustrativos)
[
  {"construct_id": "X",    "n_items": 12, "alpha": 0.89, "omega": 0.90, "n_respondents": 200},
  {"construct_id": "Y",    "n_items": 12, "alpha": 0.91, "omega": 0.92, "n_respondents": 200},
  {"construct_id": "X_D1", "n_items": 4,  "alpha": 0.83, "omega": 0.84, "n_respondents": 200}
]
```

Si el endpoint real devuelve un shape distinto a estos, **registrar el gap** en
`docs/frontend/ANALYTICS_GAPS.md` (ya existe GAP-013 para confiabilidad sin UI) en vez de
adaptar el frontend a ciegas.

## 7. Casos de prueba obligatorios (equivalentes académicos de las reglas §70/§82-90 del
harness de analítica, ya auditadas contra el backend real)

| Caso | Cómo generarlo | Resultado esperado |
|---|---|---|
| Sin respuestas | Estudio abierto, 0 sesiones completas | UI: "Aún no existen respuestas." — no 0s |
| n insuficiente | Usar solo la muestra de §5.1 (n=10) | Descriptiva corre; pruebas con requisito de n mínimo deben advertir, no fallar en silencio |
| Baremo ausente | No hacer `PATCH .../studies/{id} {"barem_id": ...}` | Score visible, nivel = "Baremo no configurado" (nunca "Alto"/"Bajo" inventado) |
| Correlación sin scatter | Llamar `/analytics/correlation` sin `include_points` en el matrix endpoint | Resumen visible, scatter "no disponible" — nunca puntos inventados. Nota: la auditoría confirmó que `/spearman-matrix` con `include_points=true` devuelve **bins agregados, nunca pares (x,y) crudos** — el ScatterPlot académico también debe asumir datos binned, igual que CENSOPAS |
| Escalas incompatibles | Comparar `X_TOTAL` (12–60) contra un ítem sociodemográfico no escalado | UI debe bloquear o advertir "Las escalas utilizan rangos diferentes", no graficar directamente |

## 8. Definition of Done de este dataset

```text
[ ] proyecto académico creado con study_type confirmado (ver GAP en §0)
[ ] 2 variables, 6 dimensiones, 24 ítems + 4 descriptivos creados vía API real
[ ] scoring-rules Likert 1-5 -> 0/25/50/75/100 aplicadas a los 24 ítems escalados
[ ] barem QA (EXPLORATORY, no OFFICIAL) cargado para X, Y y las 6 dimensiones
[ ] dataset de 200 participantes generado con scripts/qa/gen_tesis_dos_variables.py
[ ] POST /studies/{id}/scoring ejecutado sin error
[ ] /analytics/describe, /reliability, /correlation, /spearman-matrix devuelven 200
[ ] los 5 casos de la tabla §7 verificados manualmente en el frontend
[ ] cualquier discrepancia de contrato registrada en docs/frontend/ANALYTICS_GAPS.md
```

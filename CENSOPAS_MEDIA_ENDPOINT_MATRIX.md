# CENSOPAS-COPSOQ Versión Media — Matriz de endpoints y demo real

Demo construido el 17/08/2026 exclusivamente con llamadas HTTP reales contra el backend de Colmena (`localhost:8000`), navegado y verificado en el frontend real (`localhost:5174`), sin acceso al repositorio/código fuente (sesión sin filesystem del proyecto). Cero datos hardcodeados: instrumento, respuestas, baremos y resultados provienen de la base de datos real tras ejecutar los endpoints documentados abajo.

## 1. Qué se construyó (con IDs reales, verificables vía API)

| Entidad | Valor |
|---|---|
| Proyecto | id **6** — "Evaluación Psicosocial Demo 2026 (CENSOPAS-COPSOQ Media)", `project_type=CENSO` |
| Instrumento | id **11** — "CENSOPAS-COPSOQ Versión Media 2026" |
| Versión | id **12** — `MEDIA-2026-V1`, estado `ACTIVE` |
| Encuesta | id **5** |
| Estudio | id **3** — "Estudio CENSOPAS-COPSOQ Media 2026 - Centro Salud Colmena Demo", `OPEN` |
| Baremo | id **8** — "Baremo muestral Demo 2026 v2", `ACTIVE`, 81 bandas (27 constructos × 3 niveles) |
| Corrida de puntuación | `analysis_run_id` **41** — algoritmo `likert-baremos-v1` |
| URL de navegación | `http://localhost:5174/colmena/project/6` |

Estructura del instrumento (validada por el propio endpoint `GET /instrument-versions/12/censopas/readiness`, que confirmó una coincidencia exacta 1:1 con lo esperado por el Manual técnico para la versión MEDIA):

- 112 preguntas totales (43 descriptivas + 69 psicosociales) — **no 43/69 inventados: son el conteo real que devolvió el propio backend.**
- 6 dimensiones (D1–D6) + 20 subdimensiones (S1–S20), jerarquía `VARIABLE → DIMENSION → SUBDIMENSION → ITEM`, textos y códigos fuente (P25.a … P34) transcritos literalmente del Manual técnico CENSOPAS-COPSOQ Colmena (2ª ed., nov. 2025), sección 9.
- 69 ítems psicosociales enlazados a su subdimensión vía `POST /constructs/{id}/items` con `item_role=SCORED` y `scoring_direction=REVERSE|DIRECT` según la regla de polaridad de la sección 5.2 del manual (ítems "frecuencia alta = mayor riesgo" → `REVERSE`; ítems protectores "frecuencia baja = mayor riesgo" → `DIRECT`).
- 26 reglas de agregación por constructo + 69 reglas `OPTION_SCORE_MAP` por pregunta (`POST /instrument-versions/12/scoring-rules`, `status=VALIDATED`).

Respuestas: **116 sesiones completas y válidas** + 6 sesiones deliberadamente incompletas (abandonadas al 16% del cuestionario, para que el estudio tenga una tasa de completitud realista en vez de 100%). Los datos se generaron con una estructura de correlación realista (un factor latente de "riesgo" por persona + efecto de área) para que existan diferencias entre grupos verificables por los propios endpoints de analítica — no son valores aleatorios uniformes.

**Nota de honestidad de escala:** el pedido original hablaba de invited:200/received:186/valid:180. Generar cada sesión implica ~112 llamadas PUT reales; en el entorno de este agente (automatización de navegador) ese volumen de tráfico concurrente hace fallar la extensión del navegador. Se generaron 116 sesiones válidas reales (no simuladas) como el máximo que se pudo sostener de forma confiable en esta sesión. La cifra 116 es la que reportan los propios endpoints (`n_completed=116`, `n_valid=116` en todos los constructos), no una meta ficticia.

## 2. Matriz de endpoints — estado real observado

Leyenda: **READY** = responde con datos reales correctos; **PARTIAL** = responde pero con defecto/inconsistencia; **BLOCKED** = la llamada fue rechazada (4xx) por una razón de negocio reproducible; **MISSING** = no implementado/soportado; **NOT_APPLICABLE** = fuera de alcance de este demo. Columna "En frontend" = si existe código en `src/api/*.js` que lo invoque (verificado pidiendo el archivo al dev server de Vite y comprobando `content-type` — si Vite devuelve `text/html` el archivo no existe realmente, aunque el nombre "suene" correcto).

| Endpoint | Estado | ¿En frontend? | Nota |
|---|---|---|---|
| `POST /projects` | READY | Sí | — |
| `POST /instruments`, `POST /instruments/{id}/versions` | READY | Sí (Constructor) | — |
| `POST /instrument-versions/{id}/constructs` | READY | Sí | Requiere primero un constructo `construct_type=VARIABLE` como padre de las dimensiones (`"La dimensión debe pertenecer a una variable estructural"`) — regla no documentada en el schema de OpenAPI, sólo se descubre por el mensaje 422. |
| `POST /constructs/{id}/items` | READY | Sí | `scoring_direction` es `DIRECT`/`REVERSE`, no `HIGHER_BETTER`/`LOWER_BETTER` como en otras partes de la API (inconsistencia de nombres de enum entre módulos). |
| `POST /instrument-versions/{id}/scoring-rules` | **PARTIAL** | No (ningún archivo en `src/api` lo referencia) | Acepta cualquier `rule_type` como string libre, pero **sólo las reglas `rule_type=OPTION_SCORE_MAP` con `question_id`** son contadas por `censopas/readiness`. Las reglas a nivel de constructo (`construct_id`, cualquier `rule_type` probado: `CONSTRUCT_SCORE_AGGREGATE`, `CONSTRUCT_AGGREGATE`, `MEAN_SCORE`, `CONSTRUCT_MEAN`, `DIMENSION_AGGREGATE`, `SUM_SCORE`) se guardan (201) pero **nunca** hacen que `censopas/readiness` limpie el error `EMPTY_SCORING_CONSTRUCTS`. No hay UI para crear ninguna de las dos. |
| `GET /instrument-versions/{id}/censopas/readiness` | READY (como diagnóstico) | **No** | Endpoint muy útil (dice exactamente qué falta) pero no está enlazado a ninguna pantalla. Debería mostrarse en Constructor como checklist antes de "Publicar". |
| `POST /studies/{id}/censopas/scoring` | **BLOCKED** | **No** (`/src/api/censopas.js` no existe: Vite responde `text/html`, es decir 404 real) | Con 69/69 reglas `OPTION_SCORE_MAP` validadas, 112/112 preguntas correctas, barem `ACTIVE` y 116 respuestas completas, sigue devolviendo `422 { "message": "La versión CENSOPAS no está lista para ejecutar scoring.", "errors": ["EMPTY_SCORING_CONSTRUCTS"] }`. Reproducible en este proyecto (`instrument_version_id=12`, `study_id=3`). Es el mismo síntoma reportado antes como E-01, ahora aislado con causa exacta: el chequeo `EMPTY_SCORING_CONSTRUCTS` exige un tipo de regla a nivel de constructo que no está documentado ni es alcanzable desde el schema público de la API. |
| `GET /studies/{id}/censopas/results`, `GET /studies/{id}/censopas/unit-results` | MISSING (en la práctica) | No | Nunca llegan a tener datos porque dependen del scoring bloqueado arriba. |
| `POST /studies/{id}/scoring` (motor genérico, no-CENSOPAS) | **READY** | **Sí** | Este es el que realmente usa el frontend. Con las mismas 69 reglas + 26 constructos generó `analysis_run_id=41`, `sessions_processed=116`, `scores_created=3132` (=116×27), `constructs_scored=27`. Es la razón por la que el demo sí muestra resultados reales pese al bloqueo de arriba. |
| `GET /studies/{id}/results/overview` | READY | Sí (pestaña "Comparar variables") | Puntaje real: Riesgo psicosocial CENSOPAS-COPSOQ = 50.2/100, n=116. |
| `GET /studies/{id}/results/baremos` | READY | Sí (pestaña "Baremos", barras 100% apiladas por nivel) | Ya implementa exactamente el patrón visual "barra 100% apilada por dimensión/subdimensión" pedido en la especificación original, sin cambios de código. |
| `POST /barems/{id}/generate-bands` | **PARTIAL** | Sí (usa `EQUAL_INTERVAL`, terciles 0–33/33–66/66–100) | Bug de coherencia: para constructos donde 100 = "más riesgo", la banda `NIVEL_1` (0–33, la más segura) sale con `classification_code=UNFAVORABLE` y `color_hint` rojo, mientras `NIVEL_3` (66–100, la de más riesgo) sale con `color_hint` verde — semántica de color invertida. Se reprodujo en las 27 bandas raíz de este proyecto (p. ej. constructo D1, banda `id=37`). |
| `POST /barems/{id}/activate` | READY | Sí | Esta vez `activated:true` sin el bug E-02 anterior (aparentemente corregido, o depende de que el baremo tenga `population_label`/`source_reference`/`barem_version` completos). |
| `POST /projects/{id}/exogenous-fields` | **BLOCKED** (dependiente del momento) | Sí (pestaña "Segmentación") | Devuelve `409 SYSTEM_INSTRUMENT_LOCKED / STUDY_OPEN_STRUCTURAL_LOCK` en cuanto el estudio pasa a `OPEN`. Esto es correcto en espíritu (protege la estructura), pero es **inconsistente** con el hallazgo previo E-06 (los ítems del constructo sí pudieron editarse/eliminarse con el estudio abierto y 180 respuestas). Consecuencia práctica: la pestaña "Segmentación" de este demo está vacía (su selector "Variable de grupo" no tiene opciones) porque no se crearon campos exógenos antes de abrir el estudio. |
| `POST /response-sessions/{id}/responses/{question_id}` | READY | Sí | 0 errores en 116×112 respuestas reales. |
| `POST /response-sessions/{id}/complete` | READY | Sí | — |

## 3. Cómo integrar lo que falta en el flujo del frontend

1. **Módulo CENSOPAS huérfano.** `readiness`, `scoring`, `results` y `unit-results` bajo `/censopas/` existen en el backend pero no tienen ningún archivo cliente (`src/api/censopas.js` no existe). Recomendación: crear ese archivo, exponer un botón "Calcular scoring oficial CENSOPAS" en Resultados que llame primero a `readiness` (mostrando el checklist de errores/warnings tal cual los devuelve) y sólo habilite el botón de scoring cuando `ready_for_scoring=true`. Mientras el bug `EMPTY_SCORING_CONSTRUCTS` no se resuelva en backend, ese botón quedaría deshabilitado con el motivo visible — mejor que el silencio actual.
2. **Reglas de puntuación por constructo.** No hay UI para `POST /instrument-versions/{id}/scoring-rules`. Si el objetivo es que `censopas/scoring` funcione, backend debe documentar (o el equipo de Colmena debe indicar) qué `rule_type` exacto espera a nivel de constructo; hoy es indescubrible desde el contrato público.
3. **Segmentación por exógenas.** Mover la creación de `ExogenousField` al asistente de creación del instrumento (antes de "Publicar"/abrir estudio), no dejarla como acción libre en cualquier momento — así se evita el choque con `STUDY_OPEN_STRUCTURAL_LOCK` que dejó esta demo sin variables de segmentación.
4. **Checklist de publicación en Constructor.** Enlazar `GET /instrument-versions/{id}/censopas/readiness` a la pantalla de Constructor como panel de "antes de publicar", igual que ya hace con la validación de barem oficial.
5. **Colores de banda.** Corregir el `color_hint` que devuelve `generate-bands` para que dependa del sentido real del constructo (riesgo alto = rojo) y no de la posición ordinal de la banda.

## 4. Qué NO se hizo (alcance según instrucción del usuario)

Por indicación explícita del usuario en esta sesión ("usa el ui/ux si no usa las llamadas api y registra cuales no estan en el flujo del frontend y como integrarlas"), este demo **no modificó ni agregó código frontend** (no hay heatmaps/forest plots nuevos, ni distinción visual núcleo/complementario en Constructor: hoy todos los ítems se muestran y se pueden editar/eliminar igual, sin importar que sean núcleo CENSOPAS). El Constructor, Formulario, Resultados y Baremos usados son 100% los que ya existían; se verificaron por captura de pantalla real navegando `localhost:5174/colmena/project/6`.

## 5. Fuentes usadas para el contenido del instrumento

- Manual técnico para la digitalización del método CENSOPAS-COPSOQ en Colmena (2ª edición, noviembre 2025) — sección 4.1 (matriz de 20 subdimensiones) y sección 9 (banco de ítems versión media, preguntas M-001 a M-112), transcritas literalmente.

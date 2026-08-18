<!-- Convertido desde: Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena.pdf -->
<!-- Las marcas de página se conservan como comentarios para trazabilidad. -->

<!-- Página 1 -->

#### COLMENA ANALYTICS

# MODELO PREMIUM DE REPORTE

# CENSOPAS-COPSOQ

Dashboard ejecutivo, estadística avanzada, segmentación y Balanced Scorecard

Modelo 1: versión media, 200 convocados y 180 registros válidos

Modelo 2: versión corta, 20 registros válidos y analítica restringida

Datos completamente sintéticos | Diseño funcional para Colmena | Agosto de 2026

<!-- Página 2 -->

## Por qué los informes actuales se perciben básicos

Auditoría funcional de los dos documentos de referencia

Informe MINSUR, 2015

Programa de Salud Mental, 2024

Aporta estructura, base legal, resultados generales y lectura por áreas. Sin embargo, trabaja con 40 evaluados de una población de 1 215, repite gráficos circulares, no presenta intervalos, tamaños de efecto ni control de grupos pequeños, y contiene denominadores 39/40 que requieren depuración.

Aporta actividades, población objetivo, cronograma y responsables. Su principal brecha es que los indicadores no conectan exposición, intervención y resultado; la fórmula de cumplimiento aparece multiplicada por 10 y la meta muestral de 35% no define precisión ni representatividad.

| Componente | Lo que conviene conservar | Brecha detectada | Mejora premium |
| --- | --- | --- | --- |
| Resultados | Distribución favorable, intermedia y desfavorable | Lectura aislada y repetitiva | Dashboard general, drilldown y ranking |
| Áreas | Localización organizacional | n muy pequeño y alta inestabilidad | Supresión n < 5, IC 95% y efecto |
| Entrevistas | Contexto cualitativo | No se integra al patrón cuantitativo | Triangulación por hipótesis de origen |
| Programa | Actividades y calendario | No vincula medidas con riesgos | Balanced Scorecard y trazabilidad |
| Indicadores | Cumplimiento y seguimiento | No hay línea base, meta ni semáforo | Ficha KPI con fórmula, dueño y frecuencia |
| Decisión | Conclusiones y recomendaciones | Priorización subjetiva | Matriz impacto-esfuerzo y reglas de alerta |

Conclusión de la auditoría

El problema no se resuelve añadiendo más gráficos. Se requiere una arquitectura analítica que muestre calidad del dato, incertidumbre, magnitud, segmentación, causas plausibles, responsables, metas y seguimiento temporal.

<!-- Página 3 -->

## Arquitectura de analítica avanzada

Cada capa responde una pregunta distinta y evita conclusiones engañosas

### 1

### 2

### 3

### 4

**DESCRIPTIVA OFICIAL** — 

**INFERENCIAL** — 

**MULTIVARIADA** — 

**ESTRATÉGICA** — 

> **¿Qué proporción está en favorable,**  
> intermedio o desfavorable?

> **¿Qué tan precisa y relevante es la diferencia**  
> observada?

> **¿Qué combinaciones y perfiles permanecen**  
> ocultos?

> **¿Qué debe hacerse, quién responde y cómo**  
> se controla?

Baremos, prevalencias, tablas y distribución

IC 95%, pruebas, q de Benjamini-Hochberg y efecto

Correlaciones, clústeres y modelo ajustado

Balanced Scorecard, portafolio, metas y alertas

Regla de oro

Límite de uso

La categoría oficial nunca se reemplaza por un índice creado por Colmena. Los modelos avanzados complementan la interpretación colectiva y deben llevar su propia etiqueta metodológica.

Los resultados son colectivos. Los perfiles, probabilidades o alertas no se utilizarán para selección, sanción, despido, diagnóstico clínico ni decisiones automatizadas sobre personas.

Resultado esperado

Un informe de dirección con capacidad de bajar desde la organización hasta sedes, áreas y grupos seguros; explicar la precisión; reconocer patrones; convertir hallazgos en acciones; y medir si la organización mejora con el tiempo.

<!-- Página 4 -->

## Panel ejecutivo

Versión media | 200 convocados | 186 recibidos | 180 válidos

COBERTURA VÁLIDA

## 90,0%

RIESGO PRIORITARIO

## 27,2%

PRINCIPAL BRECHA

## D1

CONFIABILIDAD

## 0,90

ÍNDICE BSC

## 70/100

180 de 200 convocados

2 o más dimensiones rojas

44,4% desfavorable

Omega promedio sintético

Estado general: en riesgo

![Visual de la página 4](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_004_img_01.png)

#### Hallazgos que requieren decisión

> **1**  
> Carga y ritmo

D1 concentra exposición y se intensifica en Operaciones y Mantenimiento.

> **2**  
> Turno rotativo

Eleva D2 incluso después de considerar horas extra y área.

> **3**  
> Contrato y previsibilidad

El contrato a plazo mantiene una asociación ajustada con el riesgo prioritario.

> **4**  
> Cuatro perfiles

> **Los promedios ocultan combinaciones diferentes de demanda, liderazgo e**  
> inseguridad.

Decisión ejecutiva sugerida

Activar dos frentes en los próximos 90 días: balance de carga y control de jornadas en áreas operativas; mejora de planificación, claridad de roles y comunicación de cambios. Preservar autonomía, sentido del trabajo y confianza donde se mantienen favorables.

<!-- Página 5 -->

## Ficha técnica, gobernanza y límites

La sofisticación analítica exige más trazabilidad, no menos

| Campo | Especificación del modelo |
| --- | --- |
| Instrumento | CENSOPAS-COPSOQ, versión media |
| Población invitada | 200 trabajadores |
| Recibidos | 186 cuestionarios |
| Válidos | 180 registros, 90% de cobertura |
| Exclusiones | 6 registros por incompletitud o patrón inválido |
| Segmentos | Sede, área, turno, contrato, sexo y edad agrupada |
| Regla de privacidad | No mostrar celdas con n < 5; evitar cruces que permitan reidentificación |
| Unidad de análisis | Colectiva; nunca individual |
| Analítica avanzada | IC 95%, efecto, corrección BH, clústeres y regresión logística ilustrativa |
| Trazabilidad | Versión, baremo, algoritmo, fecha, filtros, exclusiones y hash de exportación |

| Rol | Responsabilidad |
| --- | --- |
| Grupo de Trabajo | Interpreta, contrasta hipótesis y acuerda prioridades |
| SST | Custodia metodología, seguimiento e integración con el SGSST |
| RR. HH. | Implementa cambios organizacionales sin acceder a respuestas<br>individuales |
| Analista | Controla calidad, reproducibilidad, supresión y bitácora |
| Gerencia | Aprueba recursos, responsables, metas y rendición de cuentas |

Advertencia metodológica

> **Los datos sintéticos permiten demostrar el reporte, pero los valores,**  
> pruebas y modelos deben recalcularse con el CSV real y el baremo autorizado antes de cualquier uso empresarial.

Separación obligatoria

La distribución oficial de CENSOPAS-COPSOQ es el resultado principal. El índice de riesgo prioritario, la probabilidad, los clústeres y el BSC son capas analíticas o de gestión creadas para Colmena. Deben mostrarse con nombres distintos y notas permanentes para evitar que se interpreten como puntuaciones oficiales.

<!-- Página 6 -->

## Calidad del dato y consistencia interna

Antes de interpretar riesgos se debe demostrar que el proceso fue controlado

TASA RECIBIDA

## 93,0%

TASA VÁLIDA

## 90,0%

ÍTEMS OMITIDOS

## 1,8%

PATRÓN LINEAL

## 1,1%

TIEMPO MEDIANO

## 11,8 min

186 de 200

180 de 200

Antes de depuración

Revisión, no exclusión automática

Rango intercuartílico 9,4-15,1

Consistencia interna por dimensión

Matriz de control automático

| Dim. | Ítems | Alfa | Omega | Lectura |
| --- | --- | --- | --- | --- |
| D1 | 16 | 0,97 | 0,97 | Adecuada |
| D2 | 4 | 0,84 | 0,84 | Adecuada |
| D3 | 12 | 0,87 | 0,87 | Adecuada |
| D4 | 22 | 0,96 | 0,96 | Adecuada |
| D5 | 9 | 0,90 | 0,90 | Adecuada |
| D6 | 6 | 0,84 | 0,84 | Adecuada |

| Control | Regla de Colmena | Salida |
| --- | --- | --- |
| Completitud | Umbral configurable por versión | Válido, revisar o excluir |
| Tiempo | Detectar valores extremadamente cortos | Bandera, nunca exclusión<br>automática |
| Patrón | Respuesta idéntica prolongada | Revisión contextual |
| Duplicidad | Hash y metadatos no identificatorios | Conservar una respuesta |
| Coherencia | Reglas de saltos y rango | Bloqueo o corrección auditada |
| Privacidad | n < 5 | Celda suprimida |

Interpretación

Alfa y omega evalúan consistencia de los ítems, no validez del diagnóstico ni ausencia de sesgo. Deben calcularse con los ítems reales, respetando su codificación y polaridad, y nunca utilizarse para eliminar preguntas únicamente porque una muestra empresarial produzca un valor menor.

<!-- Página 7 -->

## Participación y perfil de la muestra

Los denominadores visibles permiten evaluar representatividad y riesgo de sesgo

Sede

Área

Turno

Contrato

| Sede | n | % |
| --- | --- | --- |
| Operación Sur | 70 | 38,9 |
| Lima | 60 | 33,3 |
| Operación Centro | 50 | 27,8 |

| Área | n | % |
| --- | --- | --- |
| Operaciones | 50 | 27,8 |
| Mantenimiento | 35 | 19,4 |
| Administración | 30 | 16,7 |
| Logística | 25 | 13,9 |
| SST y RR. HH. | 20 | 11,1 |
| Comercial | 20 | 11,1 |

| Turno | n | % |
| --- | --- | --- |
| Diurno | 114 | 63,3 |
| Rotativo | 66 | 36,7 |

| Contrato | n | % |
| --- | --- | --- |
| Indefinido | 120 | 66,7 |
| Plazo fijo | 60 | 33,3 |

| Etapa | n | % de convocados | Regla |
| --- | --- | --- | --- |
| Convocados | 200 | 100,0% | Población objetivo |
| Recibidos | 186 | 93,0% | Cuestionario enviado |
| Válidos | 180 | 90,0% | Ingresan al análisis |
| Incompletos | 4 | 2,0% | Excluidos según regla |
| Patrón inválido confirmado | 2 | 1,0% | Exclusión auditada |
| No respuesta | 14 | 7,0% | Analizar sesgo si hay marco |

Lectura ejecutiva

> **La cobertura total es alta. Aun así,**  
> Colmena debe comparar respuesta por sede y área para detectar grupos subrepresentados antes de interpretar diferencias.

Regla para filtros

Todo gráfico filtrado debe mostrar n válido, porcentaje de cobertura del segmento y número de celdas suprimidas. Si el filtro deja menos de cinco personas, la visualización se bloquea.

<!-- Página 8 -->

## Resultados por dimensión

Distribución oficial primero; índice analítico después

Tabla ejecutiva

![Visual de la página 8](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_008_img_01.png)

| Dim. | Desfav. | IC 95% | Lectura | Prior | idad |
| --- | --- | --- | --- | --- | --- |
| D1 | 44,4% | 37,4% a 51,7% | Exigencias psicológicas | Media |  |
| D2 | 13,9% | 9,6% a 19,7% | Conflicto trabajo-familia | Segui | miento |
| D3 | 0,6% | 0,1% a 3,1% | Control sobre el trabajo | Segui | miento |
| D4 | 15,0% | 10,5% a 20,9% | Apoyo social y liderazgo | Segui | miento |
| D5 | 18,9% | 13,8% a 25,2% | Compensaciones | Segui | miento |
| D6 | 1,7% | 0,6% a 4,8% | Capital social | Segui | miento |

Lectura central

Precisión

D1 presenta la mayor exposición desfavorable. D5 y D4 requieren vigilancia porque la proporción intermedia puede desplazarse hacia riesgo si no se actúa sobre cambios, reconocimiento, planificación y liderazgo.

El intervalo de confianza comunica cuánto podría variar la prevalencia en mediciones equivalentes. Dos porcentajes cercanos no deben declararse diferentes sólo porque uno sea mayor.

<!-- Página 9 -->

## Ranking de veinte subdimensiones

Priorizar sin perder la estructura completa del instrumento

Top de intervención

| # | Subdimensión | Dim. | % rojo | Pregunta preven | tiva |
| --- | --- | --- | --- | --- | --- |
| 1 | S1 Exigencias<br>cuantitativas | D1 | 60,6% | ¿Carga y dotación so<br>compatibles? | n |
| 2 | S2 Ritmo de trabajo | D1 | 55,6% | ¿El ritmo puede soste | nerse? |
| 3 | S17 Inseguridad sobre el<br>empleo | D5 | 48,9% | ¿Los cambios se com<br>tiempo? | unican a |
| 4 | S3 Exigencias emocionales | D1 | 43,9% | ¿Qué tareas generan<br>emocional? | demand |
| 5 | S4 Esconder emociones | D1 | 41,7% | Contrastar origen con | el Grup |
| 6 | S18 Inseguridad de<br>condiciones | D5 | 34,4% | ¿Cambian turnos o fu<br>previsión? | nciones |
| 7 | S11 Calidad de liderazgo | D4 | 33,3% | ¿La jefatura planifica | y resuel |
| 8 | S15 Conflicto de rol | D4 | 31,7% | ¿Hay órdenes contrad | ictorias |

![Visual de la página 9](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_009_img_01.png)

Uso correcto

> **El ranking ordena la conversación preventiva; no convierte una**  
> diferencia mínima en prioridad automática.

<!-- Página 10 -->

## Drilldown por área

Localización de prioridades con denominador y regla de anonimato

Resumen por área

![Visual de la página 10](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_010_img_01.png)

| Área | n | Mayor<br>brecha | % | Riesgo | 2+ |
| --- | --- | --- | --- | --- | --- |
| Operaciones | 50 | D1 | 80,0% | 50,0% |  |
| Mantenimiento | 35 | D1 | 62,9% | 34,3% |  |
| Logística | 25 | D1 | 36,0% | 24,0% |  |
| Comercial | 20 | D1 | 25,0% | 15,0% |  |
| Administración | 30 | D2 | 13,3% | 6,7% |  |
| SST y RR. HH. | 20 | D1 | 10,0% | 5,0% |  |

Filtro seguro

Todas las áreas del ejemplo tienen n >= 20.

Patrón oculto

Mantenimiento y Operaciones no comparten exactamente el mismo problema. Ambas concentran D1, pero Mantenimiento añade una señal más fuerte en D4. Por ello no conviene aplicar una intervención idéntica a toda la organización.

<!-- Página 11 -->

## Explorador de segmentos

Sede, turno, contrato, sexo y edad agrupada en una sola vista

Hallazgo 1

![Visual de la página 11](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_011_img_01.png)

> **El turno rotativo concentra D1 y D2. La**  
> comparación debe ajustarse por área y horas extra antes de atribuir el resultado al turno.

Hallazgo 2

> **El contrato a plazo incrementa D5 en el modelo**  
> sintético. La magnitud se verifica con efecto e intervalo, no sólo con porcentajes.

Hallazgo 3

> **Sexo y edad se usan para detectar desigualdad,**  
> nunca para individualizar. Cruces pequeños se suprimen automáticamente.

Interacción

> **El dashboard permite combinar un filtro por vez y**  
> muestra n en cada vista.

<!-- Página 12 -->

## Precisión, significancia y tamaño de efecto

La estadística avanzada debe cuantificar magnitud y no perseguir p < 0,05

Contrastes seleccionados

| Contraste | Prueba | p | q BH | Efecto | Lectura |
| --- | --- | --- | --- | --- | --- |
| Área x riesgo prioritario | Chi cuadrado | < 0,001 | < 0,001 | 0,39 | Moderado |
| D1 según área | Kruskal-Wallis | < 0,001 | < 0,001 | 0,39 | Moderado |
| D2 según turno | Mann-Whitney | < 0,001 | < 0,001 | 0,32 | Moderado |
| Horas extra x D1 | Spearman | < 0,001 | < 0,001 | 0,45 | Moderado |
| D5 según contrato | Mann-Whitney | < 0,001 | < 0,001 | 0,31 | Moderado |

![Visual de la página 12](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_012_img_01.png)

Corrección por múltiples pruebas

Tamaño de efecto

Cuando se exploran muchas áreas y dimensiones, Colmena ajusta los valores p mediante Benjamini-Hochberg para reducir hallazgos falsos positivos.

Una diferencia puede ser estadísticamente detectable y aun ser pequeña. El reporte siempre muestra una medida de magnitud y evita presentar p como sinónimo de importancia.

Regla narrativa

Redactar: se observó una asociación de magnitud pequeña o moderada, con su intervalo o medida de efecto. Evitar: el turno causa riesgo o el área explica por sí sola el resultado.

<!-- Página 13 -->

## Relaciones entre exposiciones

Matriz de Spearman para formular hipótesis de origen, no para afirmar causalidad

![Visual de la página 13](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_013_img_01.png)

Núcleo de demanda

> **D1 se relaciona con D2 y con horas extra. La combinación sugiere**  
> revisar simultáneamente carga, jornada y disponibilidad fuera del trabajo.

Núcleo relacional

> **D4 y D6 forman un bloque de apoyo, justicia y confianza. Las medidas**  
> de liderazgo deben proteger también la participación y el trato justo.

Resultados asociados

> **Estrés aumenta y satisfacción disminuye cuando crece la exposición**  
> global. Esta relación es descriptiva y no equivale a diagnóstico o causalidad.

Próximo paso

> **Contrastar el patrón con entrevistas, turnos, dotación, horas extra y**  
> cambios organizacionales.

<!-- Página 14 -->

## Segmentación por perfiles latentes

K-means sobre seis dimensiones estandarizadas | k = 4

Ficha de perfiles

| Perfil | n | % | Rasgo<br>dominante | Uso preventivo |
| --- | --- | --- | --- | --- |
| Demanda y doble presencia | 50 | 27,8% | D1/D5 | Explorar hipótesis |
| Inseguridad y compensación | 42 | 23,3% | D1/D5 | Explorar hipótesis |
| Liderazgo y capital social | 55 | 30,6% | D1/D4 | Explorar hipótesis |
| Recursos protectores | 33 | 18,3% | D1/D2 | Explorar hipótesis |

![Visual de la página 14](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_014_img_01.png)

Calidad del agrupamiento

Silhouette = 0,20. La separación es débil y su uso debe ser exclusivamente exploratorio. No autoriza etiquetar personas ni crear expedientes individuales.

Ventaja

Dos personas con el mismo promedio global pueden requerir medidas distintas si sus perfiles dimensionales son diferentes.

<!-- Página 15 -->

## Localización de los perfiles

La composición por área revela necesidades que el promedio general oculta

![Visual de la página 15](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_015_img_01.png)

Perfil dominante

| Área | Perfil más frecuente | % | Implicaci | ón |
| --- | --- | --- | --- | --- |
| Administración | Recursos protectores | 33,3 | Priorizar ori<br>dominante | gen |
| Comercial | Liderazgo y capital social | 40,0 | Priorizar ori<br>dominante | gen |
| Logística | Inseguridad y<br>compensación | 36,0 | Priorizar ori<br>dominante | gen |
| Mantenimiento | Liderazgo y capital social | 37,1 | Priorizar ori<br>dominante | gen |
| Operaciones | Demanda y doble<br>presencia | 44,0 | Priorizar ori<br>dominante | gen |
| SST y RR. HH. | Recursos protectores | 40,0 | Priorizar ori<br>dominante | gen |

Lectura de área

Confidencialidad

Si una unidad combina alta demanda y liderazgo crítico, la medida debe integrar capacidad operativa, planificación y resolución de conflictos. Un taller aislado tendría baja probabilidad de modificar la exposición.

Los perfiles se presentan agregados. La base exportable no debe incluir la asignación individual de clúster para usuarios de negocio; sólo el motor analítico conserva un identificador técnico temporal.

<!-- Página 16 -->

## Modelo multivariable

Probabilidad de presentar dos o más dimensiones desfavorables

Efectos ajustados

| Predictor | OR | IC 95% | Lectura |
| --- | --- | --- | --- |
| Horas extra por 5 h | 1,11 | 0,55 a 1,99 | No concluyente |
| Turno rotativo | 1,19 | 0,47 a 2,99 | No concluyente |
| Contrato a plazo | 2,34 | 1,01 a 5,70 | Mayor probabilidad |
| Área operativa | 4,89 | 2,06 a 16,21 | Mayor probabilidad |
| Liderazgo por 10 puntos | 0,99 | 0,66 a 1,37 | No concluyente |

![Visual de la página 16](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_016_img_01.png)

Qué aporta

Qué no permite

El modelo estima cada asociación manteniendo constantes las demás variables. Así evita concluir que el turno explica una diferencia que en realidad proviene del área o de las horas extra.

La probabilidad no es un diagnóstico ni una decisión laboral. Sólo sirve para orientar medidas colectivas, validar hipótesis y seleccionar variables que merecen seguimiento.

<!-- Página 17 -->

## Desempeño, calibración y uso ético

Todo modelo predictivo debe demostrar utilidad y límites

AUC VALIDADA

## 0,68

BRIER

## 0,189

![Visual de la página 17](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_017_img_01.png)

Validación cruzada 5 folds

Menor es mejor

SENSIBILIDAD

## 77,6%

ESPECIFICIDAD

## 62,6%

Umbral de Youden

Umbral de Youden

Semáforo de uso

AUC moderada: el modelo puede apoyar la priorización colectiva, pero no justificar decisiones individuales. Debe recalibrarse por empresa y revisarse por sede, sexo, edad y contrato para detectar desempeño desigual.

| Control | Regla |
| --- | --- |
| Propósito | Prevención colectiva |
| Acceso | Sólo perfiles autorizados |
| Explicación | Variables y dirección visibles |
| Equidad | Auditar desempeño por segmento |
| Caducidad | Reentrenar al cambiar versión o proceso |
| Prohibición | No selección, sanción ni despido |

Control humano obligatorio

El Grupo de Trabajo revisa los resultados, contrasta causas y decide medidas. Ninguna recomendación del motor se ejecuta automáticamente ni sustituye la participación de trabajadores y responsables del SGSST.

<!-- Página 18 -->

## Monitoreo continuo

Gráfico p para distinguir variación común, señal y tendencia

![Visual de la página 18](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_018_img_01.png)

Frecuencia

Panel operativo mensual con indicadores de acciones. Reaplicación del instrumento según plan, sin convertir un cuestionario anual en vigilancia individual continua.

Comparabilidad

> **Usar la misma versión, baremo, población objetivo y definición**  
> de segmentos. Registrar reorganizaciones, campañas o cambios de jornada.

Alerta

> **Una señal fuera de control activa revisión del proceso y no una**  
> conclusión automática de mejora o deterioro.

| Nivel | Indicador | Frecuencia | Responsable |
| --- | --- | --- | --- |
| Exposición | % desfavorable por dimensión | Reaplicación | SST |
| Intervención | % acciones en plazo | Mensual | Dueño de acción |
| Proceso | Horas extra y cambios no previstos | Mensual | Operaciones |
| Resultado | Estrés y satisfacción agregados | Trimestral | Salud ocupacional |
| Gobernanza | Celdas suprimidas y accesos | Mensual | Administrador |

Nota

> **La serie es sintética y sólo ilustra**  
> la lógica de control.

<!-- Página 19 -->

## Mapa estratégico de salud psicosocial

Balanced Scorecard adaptado al ciclo preventivo

#### Reducir exposición prioritaria y estrés asociado

**SALUD Y PREVENCIÓN** — 

#### Cerrar acciones en plazo y cubrir áreas críticas

**PROCESOS INTERNOS** — 

#### Mejorar liderazgo, reconocimiento, justicia y confianza

**PERSONAS Y CULTURA** — 

#### Formar jefaturas, codiseñar y consolidar datos

**APRENDIZAJE** — 

Lógica causal de gestión

Capacidades y datos mejoran procesos; procesos más sólidos modifican condiciones organizacionales; y esas condiciones deben reducir exposición. La asociación debe verificarse con seguimiento, no asumirse.

<!-- Página 20 -->

## Balanced Scorecard

Línea base sintética, meta, cumplimiento, responsable y semáforo

SALUD Y PREVENCIÓN

## 82

PROCESOS

## 60

PERSONAS Y CULTURA

## 73

APRENDIZAJE

## 57

Peso estratégico 35%

Peso estratégico 30%

Peso estratégico 20%

Peso estratégico 15%

| Perspectiva | Indicador | Actual | Meta | Cumpl. | Estado | Responsable |
| --- | --- | --- | --- | --- | --- | --- |
| Salud y prevención | Riesgo prioritario | 27,2% | 25,0% | 92% | En riesgo | SST/Salud |
| Salud y prevención | Cobertura válida | 90,0% | 95,0% | 95% | En riesgo | SST/Salud |
| Salud y prevención | Estrés alto | 32,2% | 20,0% | 62% | Crítico | SST/Salud |
| Procesos | Acciones cerradas a tiempo | 58,0% | 85,0% | 68% | Crítico | Dueño proceso |
| Procesos | Cobertura de áreas críticas | 42,0% | 90,0% | 47% | Crítico | Dueño proceso |
| Procesos | Días hasta primera medida | 47,0 d | 30,0 d | 64% | Crítico | Dueño proceso |
| Personas y cultura | Liderazgo favorable | 44,4% | 60,0% | 74% | En riesgo | RR. HH. |
| Personas y cultura | Reconocimiento favorable | 29,4% | 55,0% | 54% | Crítico | RR. HH. |
| Personas y cultura | Confianza favorable | 58,3% | 65,0% | 90% | En riesgo | RR. HH. |
| Aprendizaje | Jefaturas formadas | 52,0% | 90,0% | 58% | Crítico | Gerencia/SST |
| Aprendizaje | Participación en codiseño | 35,0% | 70,0% | 50% | Crítico | Gerencia/SST |
| Aprendizaje | Integración mensual de datos | 67,0% | 100,0% | 67% | Crítico | Gerencia/SST |

Regla de no compensación

Un buen cumplimiento de capacitación no puede ocultar una exposición crítica. Si un KPI de salud supera el umbral rojo, el estado global permanece en riesgo aunque el promedio ponderado sea mayor.

<!-- Página 21 -->

## Portafolio de intervención

Matriz impacto-esfuerzo conectada con dimensiones y objetivos BSC

Backlog priorizado

![Visual de la página 21](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_021_img_01.png)

| Iniciativa | Foco | Dueño | Plazo | Indicador | Decisió<br>n |
| --- | --- | --- | --- | --- | --- |
| Balance de<br>carga | D1 | Operacione<br>s | 60 d | Horas extra y tareas<br>vencidas | Iniciar |
| Comunicación<br>de cambios | D5 | RR. HH. | 30 d | % cambios<br>anticipados | Ganancia<br>rápida |
| Claridad de<br>roles | D4 | Procesos | 45 d | % roles actualizados | Ganancia<br>rápida |
| Escuela de<br>liderazgo | D4/D6 | RR.<br>HH./SST | 90 d | % acuerdos cerrados | Proyecto |
| Protocolo de<br>turnos | D2 | Operacione<br>s | 60 d | % cambios no<br>previstos | Iniciar |
| Mesa<br>participativa | D6 | Grupo de<br>Trabajo | 45 d | % medidas<br>codiseñadas | Mantener |

Principio preventivo

Las medidas actúan sobre organización, diseño del trabajo y gestión. La atención psicológica individual puede ser un apoyo complementario, pero no sustituye el control de la exposición en su origen.

<!-- Página 22 -->

## Tablero de acciones y rendición de cuentas

Cada hallazgo debe terminar en una medida verificable

| ID | Riesgo | Causa a contrastar | Medida | R | A | Plazo | Avance | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | D1/S1 | Dotación insuficiente | Rebalancear carga semanal | Oper. | Ger. | 30/09 | 35% | En riesgo |
| A-02 | D1/S2 | Picos e interrupciones | Límite de trabajo en curso | Oper. | Ger. | 15/09 | 70% | En curso |
| A-03 | D4/S11 | Planificación débil | Rutina de planificación | RR. HH. | Ger. | 30/10 | 20% | En riesgo |
| A-04 | D4/S15 | Órdenes contradictorias | Actualizar matriz RACI | Procesos | Ger. | 15/10 | 55% | En curso |
| A-05 | D5/S17 | Cambio tardío | Protocolo de comunicación | RR. HH. | Ger. | 31/08 | 90% | En curso |
| A-06 | D2 | Cambio de turno | Regla de anticipación | Oper. | Ger. | 30/09 | 40% | En riesgo |

ACCIONES ABIERTAS

## 6

AVANCE PONDERADO

## 51,7%

COBERTURA CRÍTICA

## 66,7%

PRÓXIMA REVISIÓN

## 15/09

3 fuera de trayectoria

Meta mensual 65%

4 de 6 causas con medida

Comité SST y Grupo de Trabajo

Alerta automática

Evidencia de cierre

Si una acción está vencida, no tiene responsable o no posee indicador, Colmena la marca como no controlada y no permite cerrar el ciclo preventivo.

El responsable adjunta acta, cambio de proceso, indicador y fecha. El Grupo de Trabajo valida implementación; la siguiente medición evalúa resultado colectivo.

<!-- Página 23 -->

## Versión corta con 20 trabajadores

Dashboard profesional con analítica restringida por precisión y privacidad

Prevalencia e incertidumbre

![Visual de la página 23](Modelo_premium_analitica_CENSOPAS_COPSOQ_Colmena_assets/page_023_img_01.png)

| Dim. | Rojo | % | IC 95% | Lectura |
| --- | --- | --- | --- | --- |
| D1 | 12/20 | 60,0% | 38,7% a 78,1% | Exigencias psicológicas |
| D2 | 7/20 | 35,0% | 18,1% a 56,7% | Conflicto trabajo-familia |
| D3 | 4/20 | 20,0% | 8,1% a 41,6% | Control sobre el trabajo |
| D4 | 5/20 | 25,0% | 11,2% a 46,9% | Apoyo social y liderazgo |
| D5 | 11/20 | 55,0% | 34,2% a 74,2% | Compensaciones |
| D6 | 3/20 | 15,0% | 5,2% a 36,0% | Capital social |

| Sí se permite | No se recomienda |
| --- | --- |
| Distribución de seis dimensiones | Clústeres o regresión |
| Conteos, porcentajes e IC exactos | Cruces simultáneos |
| Lectura global y plan preventivo | Comparar áreas con n < 5 |
| Narrativa y trazabilidad | Rankings individuales |

Conclusión

La versión corta puede lucir ejecutiva, pero no debe simular una precisión que la muestra no posee. Con n = 20, el valor profesional está en mostrar incertidumbre, limitar filtros y traducir hallazgos en medidas colectivas.

<!-- Página 24 -->

## Qué análisis habilitar según el tamaño muestral

Reglas prudenciales para que Colmena no ofrezca estadísticas inestables

| Capacidad | n 5-29 | n 30-79 | n 80-149 | n 150+ | Condición adicional |
| --- | --- | --- | --- | --- | --- |
| Dimensiones y prevalencias | Sí | Sí | Sí | Sí | Baremo y denominador |
| Intervalos de confianza | Exactos | Sí | Sí | Sí | Mostrar amplitud |
| Comparación de dos grupos | No | Exploratoria | Sí | Sí | Cada celda n >= 5 |
| Pruebas múltiples | No | Limitadas | Sí | Sí | Ajuste BH |
| Subdimensiones | No en corta | Según versión | Sí | Sí | Versión media |
| Clústeres | No | No | Exploratorio | Sí | Estabilidad y silhouette |
| Regresión multivariable | No | No | Muy limitada | Sí | Eventos por parámetro |
| Validación cruzada | No | No | Limitada | Sí | Sin fuga de datos |
| Balanced Scorecard | Sí | Sí | Sí | Sí | Integra KPIs externos |
| Monitoreo temporal | Sí | Sí | Sí | Sí | Misma definición y baremo |

Regla dinámica

No usar umbrales rígidos sin contexto

El motor debe ocultar automáticamente módulos que no cumplen tamaño, número de eventos, privacidad o calidad del dato. El usuario verá la razón y la acción requerida para habilitarlos.

El tamaño por sí solo no garantiza validez. También importan cobertura, distribución de categorías, número de predictores, independencia y calidad del marco poblacional.

Criterio profesional

Más estadística no siempre significa mejor análisis. La plataforma debe seleccionar la técnica mínima que responda la pregunta con supuestos verificables.

<!-- Página 25 -->

## Modelo de datos para Colmena

Arquitectura estrella para dashboards, filtros y trazabilidad

**DIM_PERSONA** — 

**DIM_TIEMPO** — 

- respondent_key

- date_id

- segmentos agrupados

**FACT_RESPUESTA** — 

- periodo

- sin nombre ni DNI

- ciclo

- study_id

- versión

- respondent_key

- item_id

- value

- score

- valid_flag

**DIM_ORGANIZACIÓN** — 

**FACT_ACCIÓN** — 

- org_id

- action_id

- sede

- risk_id

- área

- owner

- unidad

- due_date

**DIM_INSTRUMENTO** — 

- jerarquía

- status

- evidence

- version_id

- item_id

- dimensión

- subdimensión

- polaridad

- baremo

Principio de privacidad por diseño

La tabla de respuestas usa una clave seudónima. Los datos identificatorios, si existieran para invitación, permanecen en otro dominio y no se exportan al motor analítico.

<!-- Página 26 -->

## Reglas del motor de reportes

Decisiones automáticas transparentes y auditables

| Evento | Validación | Respuesta de Colmena | Registro de auditoría |
| --- | --- | --- | --- |
| Carga de CSV | Diccionario, tipos, rangos y códigos | Previsualizar errores; no calcular | Hash, usuario y fecha |
| Selección de versión | Corta o media | Habilitar módulos compatibles | version_id |
| Aplicación de baremo | Baremo autorizado y vigente | Calcular categorías oficiales | baremo_id y checksum |
| Filtro | n válido y riesgo de reidentificación | Mostrar, agrupar o suprimir | filtro y celdas ocultas |
| Comparación | Supuestos y tamaño | Elegir prueba y efecto | prueba, q, efecto |
| Clúster | n, estabilidad y silhouette | Mostrar sólo agregados | semilla y parámetros |
| Regresión | Eventos por parámetro y validación | Mostrar OR, IC y desempeño | modelo y versión |
| BSC | KPI, fórmula, línea base y meta | Semáforo con regla de no compensación | dueño y frecuencia |
| Exportación | Notas y supresión aplicadas | PDF, XLSX y JSON reproducibles | hash de salida |

Capa de explicación

Capa de alerta

Capa de acción

> **Cada gráfico incluye definición, denominador, filtros, método,**  
> fecha, nota de privacidad y enlace al detalle técnico.

> **Las alertas se activan por exposición, incumplimiento, calidad o**  
> cambio temporal. Nunca por el resultado de una persona.

> **Toda prioridad se enlaza a responsable, plazo, indicador, meta,**  
> evidencia y estado de cierre.

<!-- Página 27 -->

## Hoja de ruta de implementación

De un PDF estático a un sistema reproducible y gobernado

**FASE 1** — 

**FASE 2** — 

**FASE 3** — 

**FASE 4** — 

### Motor oficial

### Dashboard

### Analítica

### BSC

4-6 semanas

4 semanas

6-8 semanas

4-6 semanas

Diccionario y validación

Modelo estrella

IC y efectos

KPIs y metas

Puntaje y baremo

Filtros seguros

Pruebas múltiples

Portafolio

PDF corta y media

Drilldown

Clústeres

Alertas

Pruebas de concordancia

Exportación XLSX/JSON

Regresión y validación

Seguimiento continuo

Criterio de aceptación

Primer MVP recomendado

La primera obligación técnica es demostrar concordancia con casos de prueba conocidos: puntajes, categorías, supresión, filtros y exportaciones deben ser reproducibles.

Iniciar con versión corta y media, dashboard descriptivo, IC 95%, mapa de áreas, plan de acción y BSC. Activar clústeres y regresión sólo después de validar el motor base.

Entregable por fase

Código versionado, pruebas automáticas, diccionario, manual metodológico, matriz de permisos y reporte de QA visual y numérico.

<!-- Página 28 -->

## Conclusiones y especificación final

Qué debe distinguir al reporte premium de Colmena

| Principio | Aplicación final |
| --- | --- |
| Primero lo oficial | La distribución CENSOPAS-COPSOQ conserva versión, baremo, denominador y regla de lectura. |
| Mostrar incertidumbre | Toda prevalencia principal incluye IC 95%; toda comparación incluye efecto y ajuste múltiple. |
| Descubrir perfiles | La segmentación identifica combinaciones de exposición sin etiquetar ni decidir sobre personas. |
| Ajustar asociaciones | La regresión separa efectos simultáneos y se presenta con validación, calibración y límites. |
| Conectar con gestión | El BSC traduce riesgos en objetivos, indicadores, metas, dueños, acciones y seguimiento. |
| Privacidad por diseño | Los filtros pequeños se bloquean y las exportaciones mantienen agregación y trazabilidad. |
| Acción sobre el origen | La intervención modifica trabajo y procesos; la atención individual es sólo complementaria. |

Resultado

El informe deja de ser una colección de gráficos y se convierte en un sistema de decisión: explica qué ocurre, cuánta certeza existe, dónde se concentra, qué patrones se combinan, qué debe cambiar y cómo se verificará el avance.

Referencias metodológicas consideradas

Fuentes de diseño revisadas: Informe de Riesgos Psicosociales Laborales de MINSUR, sede Lima (2015); Programa de Salud Mental SSYMA-PR04.06, versión 01 (2024); Manual del Método CENSOPAS-COPSOQ, versión 2; cuestionarios CENSOPAS-COPSOQ, versiones corta y media; y estudio psicométrico peruano de validación publicado en BMC Public Health (2022).

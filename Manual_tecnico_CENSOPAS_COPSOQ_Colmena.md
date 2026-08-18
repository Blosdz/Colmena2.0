<!-- Convertido desde: Manual_tecnico_CENSOPAS_COPSOQ_Colmena.pdf -->
<!-- Las marcas de página se conservan como comentarios para trazabilidad. -->

<!-- Página 1 -->

# MANUAL TÉCNICO PARA LA

# DIGITALIZACIÓN DEL

# MÉTODO CENSOPAS-COPSOQ

# EN COLMENA

Versiones corta y media: matriz de contenido, banco de ítems, opciones de respuesta, calificación, baremos y reglas de implementación

> **Documento técnico de trabajo**  
> Segunda edición del manual fuente: noviembre de 2025 Preparado para diseño funcional y validación del motor de reportes Arequipa, Perú | Agosto de 2026

<!-- Página 2 -->

> **Advertencia de uso**  
> Este documento organiza los materiales suministrados para fines de análisis y desarrollo. No es una publicación oficial del INS ni sustituye el Manual del Método. El núcleo CENSOPAS-COPSOQ no debe modificarse. Los módulos adicionales deben mantenerse fuera de la puntuación del instrumento y someterse a validación propia.

## Resumen ejecutivo

El presente manual consolida la estructura de las versiones corta y media del CENSOPAS-COPSOQ y la convierte en una especificación funcional para Colmena. Incluye las 42 preguntas de la versión corta y las 112 preguntas de la versión media, sus códigos de origen, opciones de respuesta, categorías, dimensiones, subdimensiones y reglas provisionales de transformación. También define cómo separar los códigos crudos de los puntajes analíticos, cómo aplicar los baremos y cómo producir reportes organizacionales sin exponer resultados individuales.

La principal limitación identificada es que los materiales entregados no contienen los puntos de corte numéricos de los percentiles peruanos ni una tabla oficial completa de inversión por ítem. Por esa razón, el documento presenta la lógica de calificación y una transformación provisional auditable, pero mantiene bloqueada la clasificación oficial verde, amarilla y roja hasta que se incorporen los baremos autorizados o se concluya una calibración formal contra resultados emitidos por la plataforma oficial.

<!-- Página 3 -->

## Contenido

> **2**  
> Resumen ejecutivo

> **3**  
> Contenido

5

## 1. Objeto, alcance y jerarquía de fuentes

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5 1.1 Objeto

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5 1.2 Alcance

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5 1.3 Jerarquía documental usada

5

## 2. Ficha técnica y validación

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6 2.1 Evidencia de validación peruana

6

## 3. Marco normativo, uso y adaptación

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6 3.1 Obligación empresarial

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6 3.2 Gratuidad y acceso

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6 3.3 Campos adaptables

7

## 4. Arquitectura del constructo

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7 4.1 Matriz de las veinte subdimensiones

8

## 5. Calificación, estandarización y baremos

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8 5.1 Separación obligatoria de variables

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8 5.2 Reglas provisionales de polaridad

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8 5.3 Procedimiento de baremación

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9 5.4 Clasificación organizacional

9

## 6. Modelo funcional para Colmena

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9 6.1 Entidades mínimas

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9 6.2 Flujo de cálculo

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9 6.3 Reglas de datos y privacidad

10

## 7. Especificación del reporte automático

11

## 8. Banco de ítems de la versión corta

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11 Sociodemográfica

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11 Condiciones laborales

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13 Factores psicosociales

22

## 9. Banco de ítems de la versión media

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22 Sociodemográfica

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22 Condiciones laborales

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28 Factores psicosociales

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46 Salud, bienestar y satisfacción

50

## 10. Matrices de importación y trazabilidad

<!-- Página 4 -->

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50 10.1 Matriz compacta de la versión corta

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52 10.2 Matriz compacta de la versión media

56

## 11. Módulos adicionales y adaptación futura

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 56 11.1 Ciclo mínimo de validación de un módulo

56

## 12. Plan de verificación antes de producción

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 56 12.1 Pruebas mínimas del motor

> **58**  
> Referencias

> **58**  
> Nota final de trazabilidad

<!-- Página 5 -->

## 1. Objeto, alcance y jerarquía de fuentes

### 1.1 Objeto

Proporcionar una base documental, psicométrica y funcional para parametrizar en Colmena las versiones corta y media del CENSOPAS-COPSOQ, conservar su trazabilidad y preparar un motor de resultados reproducible. El manual sirve como especificación de producto, no como autorización de uso ni como reemplazo de la capacitación exigida por CENSOPAS/INS.

### 1.2 Alcance

- Versión corta: 42 preguntas, de las cuales 31 corresponden a factores psicosociales y se agregan en seis dimensiones.

- Versión media: 112 preguntas, de las cuales 69 corresponden a factores psicosociales y se agregan en veinte subdimensiones y seis dimensiones.

- Variables descriptivas: sociodemográficas, condiciones laborales y, sólo en la versión media, salud, bienestar y satisfacción.

- Reportes organizacionales por centro laboral y unidades de análisis con un mínimo operativo de cinco personas para preservar el anonimato.

- Módulos futuros independientes del núcleo y de su puntuación.

### 1.3 Jerarquía documental usada

| Nivel | Fuente | Uso en este manual |
| --- | --- | --- |
| 1 | Manual del Método CENSOPAS-COPSOQ, 2a edición, noviembre<br>de 2025 | Reglas de uso, estructura, adaptación, aplicación, colores y<br>clasificación final. |
| 2 | Cuestionario modelo, versión media | Texto, numeración y opciones de las 112 preguntas. |
| 2 | Cuestionario modelo, versión corta | Texto, numeración y opciones de las 42 preguntas. |
| 2 | Diccionario de datos de CSV | Códigos de columnas y correspondencia entre versiones. |
| 3 | Lucero-Perez et al. (2022) | Evidencia de validez, confiabilidad, muestra, escala 0 a 100 y uso<br>de terciles. |
| 4 | Normas peruanas y fuentes institucionales | Marco de seguridad y salud, protección de datos y acceso al<br>método. |
| Regla de precedencia<br>Si una transcripción, un diccionario o una propuesta de software contradice el Manual del Método vigente o el<br>cuestionario oficial entregado por CENSOPAS/INS, prevalece la fuente oficial más reciente. |  |  |

## 2. Ficha técnica y validación

| Campo | Versión corta | Versión media |
| --- | --- | --- |
| Población objetivo | Centros laborales con menos de 25 trabajadores, o<br>cuando la participación efectiva queda por debajo de<br>25. | Centros laborales con 25 o más trabajadores y<br>participación efectiva suficiente. |
| Total de preguntas | 42 | 112 |
| Ítems psicosociales | 31 | 69 |
| Salida estructural | 6 dimensiones | 6 dimensiones y 20 subdimensiones |
| Categorías descriptivas | Sociodemográficas y condiciones laborales | Sociodemográficas, condiciones laborales, salud,<br>bienestar y satisfacción |
| Tipo de aplicación | Autoaplicada, anónima, confidencial y voluntaria | Autoaplicada, anónima, confidencial y voluntaria |
| Unidad de interpretación | Colectivo laboral | Colectivo laboral |

<!-- Página 6 -->

### 2.1 Evidencia de validación peruana

La validación publicada evaluó a 1 707 trabajadores de empresas formales de seis actividades económicas y de la Costa, Sierra y Selva. El proceso incluyó adaptación lingüística y cultural, revisión de claridad, coherencia y pertinencia por un grupo de 60 representantes y expertos, análisis factorial confirmatorio con matrices policóricas y estimación WLSMV, y confiabilidad mediante alfa y omega. La versión corta se construyó reduciendo progresivamente los 69 ítems hasta 31, manteniendo representación de los veinte contenidos originales dentro de seis modelos dimensionales.

| Aspecto | Resultado publicado | Implicación para Colmena |
| --- | --- | --- |
| Muestra | 1 707 trabajadores, seis sectores y tres regiones<br>naturales. | Registrar versión, fecha, sector y composición de la<br>muestra en cada estudio. |
| Versión media | 17 de 20 modelos unidimensionales mostraron índices<br>evaluables; 16 presentaron consistencia interna óptima. | Mostrar advertencias metodológicas, no ocultarlas en<br>el reporte. |
| Segundo orden | Cinco de seis dimensiones tuvieron evidencia adecuada;<br>exigencias psicológicas requiere cautela. | Evitar mensajes deterministas y conservar intervalos y<br>distribución de respuestas. |
| Versión corta | Seis dimensiones con confiabilidad óptima; correlaciones<br>mayores de 0,90 con la versión media. | No reportar subdimensiones por separado en la<br>versión corta. |
| Ítems con carga menor de<br>0,40 | 25j, 26m, 27c y 30a se conservaron por relevancia<br>teórica. | No eliminar ni reponderar esos ítems sin una nueva<br>validación. |
| Interpretación correcta<br>El instrumento identifica exposición percibida a condiciones de trabajo. No diagnostica a una persona, no<br>reemplaza una evaluación clínica y no debe generar un perfil individual entregable al empleador. |  |  |

## 3. Marco normativo, uso y adaptación

### 3.1 Obligación empresarial

La Ley 29783 y su Reglamento establecen el deber del empleador de identificar, evaluar, prevenir y controlar los riesgos del trabajo. La obligación alcanza los riesgos psicosociales, pero las normas revisadas no ordenan usar exclusivamente el CENSOPAS-COPSOQ por su nombre. Este método constituye una alternativa peruana validada y con reglas propias de aplicación.

| Norma o fuente | Materia relevante |
| --- | --- |
| Ley 29783 | Sistema de gestión de seguridad y salud en el trabajo y deber general de prevención. |
| D.S. 005-2012-TR | Reglamento de la Ley 29783 y evaluación de los riesgos asociados al puesto y función. |
| R.M. 375-2008-TR | Norma básica de ergonomía y consideración de factores de riesgo, incluidos los psicosociales. |
| R.M. 050-2013-TR | Formatos referenciales y contenido mínimo de registros obligatorios del sistema de gestión. |
| Ley 29733 | Protección de datos personales, finalidad, seguridad y tratamiento responsable. |
| Manual CENSOPAS-COPSOQ, 2025 | Condiciones de uso, capacitación, adaptación limitada, anonimato y uso preventivo. |

### 3.2 Gratuidad y acceso

El Manual del Método declara el uso gratuito. También exige que el evaluador sea un profesional afín con experiencia en salud ocupacional y que apruebe la capacitación de CENSOPAS/INS para acceder a la plataforma oficial. La gratuidad del cuestionario no elimina las obligaciones de licencia, capacitación, confidencialidad, integridad del método ni protección de datos.

### 3.3 Campos adaptables

| Campo | Acción permitida | Condición |
| --- | --- | --- |
| Nivel de instrucción | Eliminar opciones no aplicables | Acuerdo del Grupo de Trabajo y preservación del anonimato. |
| Tiempo en el puesto | Eliminar opciones no aplicables | No cambiar el significado ni los límites restantes. |
| Relación laboral | Eliminar opciones no aplicables | No crear categorías identificables. |
| Horario | Eliminar opciones no aplicables | Conservar la lógica del catálogo. |
| Área o departamento | Incluir catálogo local | Derivado del organigrama y agrupado si n es menor de 5. |
| Puesto | Incluir catálogo local | Derivado de la nómina y agrupado si n es menor de 5. |

<!-- Página 7 -->

> **Rangos de remuneración**  
> El cuestionario fuente conserva tramos construidos desde 930 soles. La remuneración no figura entre los seis campos adaptables del Manual 2025. Colmena debe conservar esos tramos en el núcleo, solicitar autorización para una actualización o recopilar una remuneración actualizada en un módulo descriptivo separado.

> **Límite de adaptación**  
> No se deben cambiar, eliminar ni añadir preguntas dentro del núcleo. Si Colmena incorpora teletrabajo, violencia, hostigamiento, ergonomía u otros temas, cada conjunto debe ser un módulo complementario separado y no puede alterar el puntaje CENSOPAS-COPSOQ.

## 4. Arquitectura del constructo

Las seis dimensiones son el nivel común de las versiones corta y media. Las veinte subdimensiones son estables como salidas separadas únicamente en la versión media. La matriz siguiente usa los códigos originales del cuestionario para evitar ambigüedad durante la importación.

| ID | Dimensión | Subdimensiones | Ítems<br>media | Ítems<br>corta |
| --- | --- | --- | --- | --- |
| D1 | Exigencias psicológicas en el<br>trabajo | Exigencias cuantitativas; Ritmo de trabajo; Exigencias emocionales;<br>Exigencia de esconder emociones | 15 | 7 |
| D2 | Conflicto trabajo-familia | Doble presencia | 4 | 3 |
| D3 | Control sobre el trabajo | Influencia; Posibilidades de desarrollo; Sentido del trabajo | 11 | 5 |
| D4 | Apoyo social y calidad de<br>liderazgo | Apoyo social de los compañeros; Apoyo social de superiores; Calidad<br>de liderazgo; Sentimiento de grupo; Previsibilidad; Claridad de rol;<br>Conflicto de rol | 23 | 7 |
| D5 | Compensaciones del trabajo | Reconocimiento; Inseguridad sobre el empleo; Inseguridad sobre las<br>condiciones de trabajo | 9 | 5 |
| D6 | Capital social | Justicia; Confianza vertical | 7 | 4 |

### 4.1 Matriz de las veinte subdimensiones

| ID | Dimensi<br>ón | Subdimensión | Ítems versión media | Ítems presentes en corta |
| --- | --- | --- | --- | --- |
| S1 | D1 | Exigencias cuantitativas | 25.c, 25.e, 25.g, 25.p | 25.c, 25.e |
| S2 | D1 | Ritmo de trabajo | 25.a, 26.f, 26.m | 26.m |
| S3 | D1 | Exigencias emocionales | 25.b, 25.q, 26.d, 26.i | 25.b, 26.d |
| S4 | D1 | Exigencia de esconder emociones | 25.d, 25.f, 26.j, 26.k | 25.d, 26.j |
| S5 | D2 | Doble presencia | 25.l, 25.m, 25.n, 25.o | 25.m, 25.n, 25.o |
| S6 | D3 | Influencia | 25.h, 25.i, 25.j, 25.k | 25.j |
| S7 | D3 | Posibilidades de desarrollo | 26.a, 26.e, 26.h, 26.l | 26.a, 26.h |
| S8 | D3 | Sentido del trabajo | 26.b, 26.c, 26.g | 26.c, 26.g |
| S9 | D4 | Apoyo social de los compañeros | 28.a, 28.b, 28.c | 28.a |
| S10 | D4 | Apoyo social de superiores | 28.g, 28.h, 28.i | 28.h |
| S11 | D4 | Calidad de liderazgo | 30.k, 30.l, 30.m, 30.n | 30.m |
| S12 | D4 | Sentimiento de grupo | 28.d, 28.e, 28.f | 28.e |
| S13 | D4 | Previsibilidad | 27.a, 27.e | 27.e |
| S14 | D4 | Claridad de rol | 27.b, 27.d, 27.g, 27.h | 27.b |
| S15 | D4 | Conflicto de rol | 27.c, 27.f, 27.i, 27.j | 27.c |
| S16 | D5 | Reconocimiento | 30.a, 30.b, 30.c | 30.a |
| S17 | D5 | Inseguridad sobre el empleo | 29.d, 29.f | 29.d, 29.f |
| S18 | D5 | Inseguridad sobre las condiciones de trabajo | 29.a, 29.b, 29.c, 29.e | 29.c, 29.e |
| S19 | D6 | Justicia | 30.f, 30.g, 30.h, 30.j | 30.h, 30.j |
| S20 | D6 | Confianza vertical | 30.d, 30.e, 30.i | 30.e, 30.i |

<!-- Página 8 -->

## 5. Calificación, estandarización y baremos

> **Estado de la especificación**  
> La codificación de respuesta y la estructura de ítems están confirmadas por los cuestionarios. La transformación 0 a 100 y la dirección semántica se documentan como propuesta provisional de ingeniería. Los puntos de corte numéricos peruanos no aparecen en los materiales suministrados y deben cargarse desde una fuente autorizada antes de habilitar un resultado equivalente al oficial.

### 5.1 Separación obligatoria de variables

| Campo | Definición | Ejemplo |
| --- | --- | --- |
| raw_code | Código marcado exactamente como aparece en el cuestionario. | 1 = Siempre; 5 = Nunca |
| risk_value | Valor orientado para que un número alto represente mayor exposición<br>desfavorable. | R = 6 - raw o R = raw, según polaridad |
| score_0_100 | Transformación lineal provisional de R. | T = 25 x (R - 1) |
| construct_score | Promedio de los T válidos de la dimensión o subdimensión. | Promedio de ítems definidos en la matriz |
| cut_1 / cut_2 | Puntos de corte del baremo de referencia. | Valor autorizado por versión y constructo |
| traffic_light | Clasificación individual para agregación anónima. | Verde, amarillo o rojo |
| group_level | Clasificación colectiva final. | Factor protector, riesgo medio o riesgo<br>alto |

### 5.2 Reglas provisionales de polaridad

El cuestionario impreso codifica 1 para Siempre o Muy preocupado y 5 para Nunca o No preocupado. Para que todos los puntajes de exposición se interpreten en la misma dirección, se propone almacenar el código crudo sin cambios y crear R por separado. En los ítems desfavorables por alta frecuencia o preocupación, R = 6 - raw. En los ítems protectores, donde la ausencia del recurso implica riesgo, R = raw. La columna de cada ficha identifica la regla propuesta.

La publicación de validación describe las respuestas desde Siempre = 5 hasta Nunca = 1, mientras que los cuestionarios actuales suministrados imprimen Siempre = 1 y Nunca = 5. Esta discrepancia confirma que raw_code no debe usarse directamente como puntaje y que la tabla de polaridad debe ser verificada con la especificación oficial o con casos patrón antes de emitir resultados.

```text
Ejemplo desfavorable: P25.b, situaciones emocionalmente desgastadoras. Si raw = 1 (Siempre), R = 5 y T = 100.
Ejemplo protector: P28.a, apoyo de compañeros. Si raw = 5 (Nunca), R = 5 y T = 100.
```

### 5.3 Procedimiento de baremación

El artículo de validación informa puntajes estandarizados entre 0 y 100 y agrupación en terciles. El Manual del Método vigente indica percentiles de referencia y delega su aplicación a la plataforma oficial. Para un motor independiente deben cargarse, versionarse y auditarse dos cortes por cada dimensión y subdimensión. Si un puntaje alto significa mayor riesgo, una regla genérica es: verde cuando S es menor o igual a C1, amarillo cuando S está entre C1 y C2, y rojo cuando S es mayor que C2. Los valores C1 y C2 no deben fijarse como 33,33 y 66,67 sobre la escala: son cuantiles de una población de referencia, no porcentajes de la puntuación máxima.

| Versión | Nivel | Constructos | Corte C1 | Corte C2 | Estado |
| --- | --- | --- | --- | --- | --- |
| Corta | Dimensión | D1 a D6 | Por cargar | Por cargar | Bloqueante para<br>equivalencia oficial |
| Media | Dimensión | D1 a D6 | Por cargar | Por cargar | Bloqueante para<br>equivalencia oficial |
| Media | Subdimensión | S1 a S20 | Por cargar | Por cargar | Bloqueante para<br>equivalencia oficial |

<!-- Página 9 -->

### 5.4 Clasificación organizacional

| Nivel | Regla del Manual del Método | Color de base |
| --- | --- | --- |
| Riesgo alto | Al menos 50% de trabajadores en situación desfavorable. | Rojo |
| Riesgo medio | Menos de 50% en rojo y predominio de la situación intermedia. | Amarillo |
| Factor protector | Al menos 50% de trabajadores en situación favorable. | Verde |
| Empate o distribución<br>semejante | El Grupo de Trabajo prioriza la clasificación de riesgo y documenta el criterio. | Prioridad preventiva |

```text
p_rojo = n_rojo / n_válido
p_amarillo = n_amarillo / n_válido
p_verde = n_verde / n_válido
```

```text
si p_rojo >= 0,50: nivel = riesgo alto
si no, si p_verde >= 0,50: nivel = factor protector
si no, si p_amarillo predomina: nivel = riesgo medio
en otro caso: revisión documentada por el Grupo de Trabajo, con prioridad preventiva
```

> **Control de publicación**  
> Colmena debe impedir que un reporte use la etiqueta oficial CENSOPAS-COPSOQ si falta alguno de estos activos: tabla de polaridad verificada, algoritmo de puntuación autorizado, puntos de corte vigentes, versión del baremo y prueba de concordancia contra resultados oficiales.

## 6. Modelo funcional para Colmena

### 6.1 Entidades mínimas

| Entidad | Campos esenciales |
| --- | --- |
| instrument_version | id, nombre, edición, fecha de vigencia, estado, fuente |
| item | id interno, código fuente, texto, categoría, catálogo, polaridad, obligatorio |
| response_option | catálogo, raw_code, etiqueta, orden, vigencia |
| construct | id, tipo dimensión/subdimensión, nombre, versión |
| construct_item | construct_id, item_id, peso, orden, inclusión |
| barem | versión, población, constructo, C1, C2, dirección, fuente, fecha |
| study | centro laboral, versión, período, unidades de análisis, evaluador, acuerdos |
| response | study_id, token anónimo, item_id, raw_code, fecha, integridad _ |
| result | constructo, unidad, n válido, verde, amarillo, rojo, nivel, algoritmo |
| report | plantilla, versión, fecha, hash de datos, firma y bitácora |

### 6.2 Flujo de cálculo

| Paso | Operación | Validación automática |
| --- | --- | --- |
| 1 | Congelar versión del instrumento y baremo. | No permitir cambios después de abrir respuestas. |
| 2 | Capturar raw_code y catálogo de origen. | Rechazar códigos fuera del catálogo. |
| 3 | Evaluar completitud e integridad. | Registrar faltantes sin imputación silenciosa. |
| 4 | Crear risk_value y score_0_100. _ | Aplicar polaridad versionada y prueba unitaria por ítem. |
| 5 | Agregar por constructo. | Usar exclusivamente los ítems de la matriz vigente. |
| 6 | Aplicar baremo individual para agregación. | Exigir C1 y C2 autorizados. |
| 7 | Suprimir celdas con n menor de 5. | Combinar o marcar como no publicable. |
| 8 | Clasificar el colectivo. | Aplicar reglas de 50% y registrar empates. |
| 9 | Generar reporte y bitácora. | Incluir versión, fecha, n, exclusiones y hash. |

### 6.3 Reglas de datos y privacidad

- No almacenar nombre, DNI, correo corporativo ni identificadores directos junto con las respuestas.

- Separar autenticación de participación y contenido de respuestas mediante tokens no reversibles.

<!-- Página 10 -->

- No mostrar resultados por celdas con menos de cinco personas y revisar combinaciones que permitan reidentificación.

- Aplicar finalidad, minimización, control de acceso, cifrado, retención definida y registro de auditoría.

- No producir reportes individuales ni inferencias clínicas.

## 7. Especificación del reporte automático

| Sección | Contenido mínimo | Control de calidad |
| --- | --- | --- |
| Portada | Centro laboral, período, versión, evaluador y fecha. | No incluir datos personales de participantes. |
| Metodología | Población, participación, aplicación, baremo y unidades. | Declarar desviaciones y limitaciones. |
| Perfil sociolaboral | Frecuencias y porcentajes de variables descriptivas. | Suprimir celdas pequeñas. |
| Dimensiones | Distribución verde, amarilla y roja y nivel final. | Siempre para corta y media. |
| Subdimensiones | Distribución y nivel final por S1 a S20. | Sólo para versión media. |
| Unidades de análisis | Comparación por área, puesto, contrato, turno u otra aprobada. | n mínimo de 5 y sin rankings personales. |
| Origen cualitativo | Síntesis de entrevistas o grupos focales. | No incluir frases identificables. |
| Plan preventivo | Causa, medida, responsable, plazo, indicador y seguimiento. | Priorizar riesgo alto y medio. |
| Anexo técnico | Matriz, baremo, versión de algoritmo, faltantes y bitácora. | Reproducibilidad completa. |
| Precisión del reporte<br>La precisión no depende de agregar más preguntas al núcleo. Depende de conservar el texto y los códigos, usar<br>el baremo correcto, controlar datos faltantes, evitar unidades pequeñas, documentar el origen del riesgo y<br>validar el motor con casos conocidos. |  |  |

<!-- Página 11 -->

## 8. Banco de ítems de la versión corta

La versión corta contiene 42 preguntas: 3 sociodemográficas, 8 de condiciones laborales y 31 de factores psicosociales. Las fichas conservan el código original de la versión media para facilitar la interoperabilidad. La versión corta sólo debe informar seis dimensiones, no veinte subdimensiones separadas.

> **Lectura de la regla de calificación**  
> Las fórmulas indicadas como provisionales orientan todos los ítems hacia mayor puntaje igual a mayor riesgo. Deben verificarse antes de producción. Los códigos crudos nunca se sobrescriben.

### Sociodemográfica

#### C-001 | Pregunta 1

Eres

> **Código de implementación: C-001 Código fuente: P1 Catálogo: SEX**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Mujer
2. Hombre

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-002 | Pregunta 2

¿Qué edad tienes?

> **Código de implementación: C-002 Código fuente: P2 Catálogo: AGE**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Menos de 31 años
2. Entre 31 y 45 años
3. Más de 45 años

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-003 | Pregunta 3

¿Qué nivel de instrucción aprobaste?

> **Código de implementación: C-003 Código fuente: P3 Catálogo: EDU**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Primaria incompleta
2. Primaria completa
3. Secundaria incompleta
4. Secundaria completa
5. Técnico superior incompleta
6. Técnico superior completa
7. Superior universitario incompleta
8. Superior universitario completa

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

### Condiciones laborales

<!-- Página 12 -->

#### C-004 | Pregunta 4

Indica qué PUESTO DE TRABAJO ocupas en la actualidad.

> **Código de implementación: C-004 Código fuente: P4.a Catálogo: JOB**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Catálogo de puestos configurado según la nómina y las unidades de análisis aprobadas por el Grupo de Trabajo.

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-005 | Pregunta 5

Indica en qué ÁREA trabajas en la actualidad.

> **Código de implementación: C-005 Código fuente: P5.a Catálogo: AREA**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Catálogo de áreas, departamentos o secciones configurado según el organigrama y las unidades de análisis.

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-006 | Pregunta 6

¿Qué tipo de contrato laboral tienes?

> **Código de implementación: C-006 Código fuente: P6 Catálogo: CONTRACT**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

> **Opciones y códigos crudos**  
> 1. Soy fijo (plazo indeterminado, indefinido, nombrado) 2. Soy temporal (contrato administrativo de servicio (CAS): Por inicio de actividad / Por necesidades de mercado / Por conversión empresarial) 3. Soy contratado de naturaleza accidental (Ocasional / De suplencia (la que resulte necesaria según circunstancia) / De emergencia (lo que dure la emergencia)) 4. Soy contratado para obra o servicio (Intermitente / De temporada / terceros) 5. Tengo otro tipo de contrato (sujetos a modalidad: Régimen de exportación de productos no tradicionales / Zonas francas y otros regímenes especiales / Otros servicios sujetos a modalidad) 6. Tengo Contrato de trabajo en régimen de tiempo parcial 7. Soy funcionario/directivo 8. Soy temporal con contrato formativo (practicante, residente) 9. Trabajo sin contrato

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-007 | Pregunta 7

¿Cuánto tiempo llevas trabajando en tu actual puesto de trabajo?

> **Código de implementación: C-007 Código fuente: P10 Catálogo: TENURE**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Menos de 30 días
2. Entre 1 mes y hasta 6 meses
3. Más de 6 meses y hasta 2 años
4. Más de 2 años y hasta 5 años
5. Más de 5 años y hasta 10 años
6. Más de 10 años

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 13 -->

#### C-008 | Pregunta 8

¿Cuál es tu horario de trabajo?

> **Código de implementación: C-008 Código fuente: P14 Catálogo: SCHEDULE**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Mañana y tarde
2. Rotatorios (excepto noche)
3. Rotatorios (incluido noche)
4. Fijo mañana
5. Fijo tarde
6. Fijo noche
7. Sin horario

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-009 | Pregunta 9

Generalmente, ¿Cuántas horas a la semana trabajas para esta empresa, organización o institución?

Código de implementación: C-009 Código fuente: P19 Catálogo: WEEK_HOURS  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. 30 horas o menos
2. De 31 a 35 horas
3. De 36 a 40 horas
4. De 41 a 48 horas
5. Más de 48 horas

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-010 | Pregunta 10

Tu Sueldo es:

Código de implementación: C-010 Código fuente: P22 Catálogo: SALARY_TYPE  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Fijo
2. Todo variable (a destajo, a comisión, por producción, jornal)
3. Una parte fija y otra variable

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### C-011 | Pregunta 11

Aproximadamente, ¿Cuánto cobras al mes?

Código de implementación: C-011 Código fuente: P23 Catálogo: SALARY_RANGE  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Sin ingresos
2. Hasta 930 soles
3. De 931 a 1700 soles
4. De 1701 a 2550 soles
5. De 2551 a 3400 soles
6. De 3401 a 4250 soles
7. De 4251 a 5100 soles
8. De 5101 a 5950 soles
9. Más de 5951 soles

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

### Factores psicosociales

<!-- Página 14 -->

#### C-012 | Pregunta 12

¿Se producen en tu trabajo momentos o situaciones emocionalmente desgastadoras?

> **Código de implementación: C-012 Código fuente: P25.b Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias emocionales

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-013 | Pregunta 13

¿Te retrasas en la entrega de tu trabajo?

> **Código de implementación: C-013 Código fuente: P25.c Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias cuantitativas

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-014 | Pregunta 14

¿Tu trabajo exige que calles tu opinión?

> **Código de implementación: C-014 Código fuente: P25.d Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencia de esconder emociones

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-015 | Pregunta 15

¿La distribución de tareas es irregular y provoca que se te acumule o junte el trabajo?

> **Código de implementación: C-015 Código fuente: P25.e Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias cuantitativas

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 15 -->

#### C-016 | Pregunta 16

¿Influyes en la forma de realizar tu trabajo?

> **Código de implementación: C-016 Código fuente: P25.j Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Influencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-017 | Pregunta 17

¿Sientes que tu trabajo te genera tanto cansancio que perjudica tus actividades domésticas y familiares?

> **Código de implementación: C-017 Código fuente: P25.m Catálogo: FREQ**  
> Dimensión: Conflicto trabajo-familia Subdimensión: Doble presencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-018 | Pregunta 18

¿Sientes que tu trabajo te ocupa tanto tiempo que perjudica tus tareas domésticas y familiares?

> **Código de implementación: C-018 Código fuente: P25.n Catálogo: FREQ**  
> Dimensión: Conflicto trabajo-familia Subdimensión: Doble presencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-019 | Pregunta 19

¿Piensas en tus tareas domésticas y familiares cuando estás trabajando?

> **Código de implementación: C-019 Código fuente: P25.o Catálogo: FREQ**  
> Dimensión: Conflicto trabajo-familia Subdimensión: Doble presencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 16 -->

#### C-020 | Pregunta 20

¿Tu trabajo necesita que tengas iniciativa?

> **Código de implementación: C-020 Código fuente: P26.a Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Posibilidades de desarrollo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-021 | Pregunta 21

¿Las tareas que haces te parecen importantes?

> **Código de implementación: C-021 Código fuente: P26.c Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Sentido del trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-022 | Pregunta 22

¿Tu trabajo te afecta emocionalmente (en forma negativa)?

> **Código de implementación: C-022 Código fuente: P26.d Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias emocionales

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-023 | Pregunta 23

¿Te sientes comprometido con tu trabajo?

> **Código de implementación: C-023 Código fuente: P26.g Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Sentido del trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 17 -->

#### C-024 | Pregunta 24

¿Tu trabajo te da la oportunidad de mejorar tus conocimientos y habilidades?

> **Código de implementación: C-024 Código fuente: P26.h Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Posibilidades de desarrollo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-025 | Pregunta 25

¿Tu trabajo exige que guardes tus emociones y sentimientos?

> **Código de implementación: C-025 Código fuente: P26.j Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencia de esconder emociones

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-026 | Pregunta 26

¿El ritmo de trabajo es alto durante toda la jornada?

> **Código de implementación: C-026 Código fuente: P26.m Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Ritmo de trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-027 | Pregunta 27

¿Tu trabajo tiene objetivos claros?

> **Código de implementación: C-027 Código fuente: P27.b Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Claridad de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 18 -->

#### C-028 | Pregunta 28

¿Se te exigen cosas contradictorias en el trabajo?

> **Código de implementación: C-028 Código fuente: P27.c Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Conflicto de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-029 | Pregunta 29

¿Recibes toda la información que necesitas para realizar bien tu trabajo?

> **Código de implementación: C-029 Código fuente: P27.e Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Previsibilidad

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-030 | Pregunta 30

¿Recibes ayuda y apoyo de tus compañeros y compañeras en la realización de tu trabajo?

> **Código de implementación: C-030 Código fuente: P28.a Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de los compañeros

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-031 | Pregunta 31

¿En tu trabajo sientes que formas parte de un grupo o equipo de trabajo?

> **Código de implementación: C-031 Código fuente: P28.e Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Sentimiento de grupo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 19 -->

#### C-032 | Pregunta 32

¿Recibes ayuda y apoyo de tu jefe inmediato en la realización de tu trabajo?

> **Código de implementación: C-032 Código fuente: P28.h Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de superiores

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-033 | Pregunta 33

¿Estás preocupado/a por si te cambian de tareas contra tu voluntad?

> **Código de implementación: C-033 Código fuente: P29.c Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre las condiciones de trabajo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-034 | Pregunta 34

¿Estás preocupado/a por si te despiden o no te renuevan el contrato?

> **Código de implementación: C-034 Código fuente: P29.d Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre el empleo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-035 | Pregunta 35

¿Estás preocupado/a por si te varían el sueldo o pago (que no te lo actualicen, que te lo bajen, que introduzcan el salario variable, que te paguen en especies, etc.)?

> **Código de implementación: C-035 Código fuente: P29.e Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre las condiciones de trabajo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 20 -->

#### C-036 | Pregunta 36

¿Estás preocupado/a por lo difícil que sería encontrar otro trabajo en el caso de que te quedases sin trabajo?

> **Código de implementación: C-036 Código fuente: P29.f Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre el empleo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### C-037 | Pregunta 37

¿Tu trabajo es valorado por la gerencia, la dirección o la jefatura?

> **Código de implementación: C-037 Código fuente: P30.a Catálogo: FREQ**  
> Dimensión: Compensaciones del trabajo Subdimensión: Reconocimiento

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-038 | Pregunta 38

¿Puedes confiar de la información que viene de la gerencia, la dirección o la jefatura?

> **Código de implementación: C-038 Código fuente: P30.e Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Confianza vertical

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-039 | Pregunta 39

¿La gerencia, la dirección o la jefatura considera con la misma seriedad las propuestas procedentes de todos los trabajadores?

> **Código de implementación: C-039 Código fuente: P30.h Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Justicia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 21 -->

#### C-040 | Pregunta 40

¿Los trabajadores pueden expresar sus opiniones y emociones?

> **Código de implementación: C-040 Código fuente: P30.i Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Confianza vertical

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-041 | Pregunta 41

¿Se distribuyen las tareas de una forma justa?

> **Código de implementación: C-041 Código fuente: P30.j Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Justicia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### C-042 | Pregunta 42

¿Tu actual jefe inmediato distribuye bien el trabajo?

> **Código de implementación: C-042 Código fuente: P30.m Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Calidad de liderazgo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 22 -->

## 9. Banco de ítems de la versión media

La versión media contiene 112 preguntas: 3 sociodemográficas, 25 de condiciones laborales, 69 de factores psicosociales y 15 de salud, bienestar y satisfacción. Sólo los 69 ítems psicosociales alimentan las seis dimensiones y veinte subdimensiones. Las demás variables son descriptivas.

### Sociodemográfica

#### M-001 | Pregunta 1

Eres

> **Código de implementación: M-001 Código fuente: P1 Catálogo: SEX**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Mujer
2. Hombre

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-002 | Pregunta 2

¿Qué edad tienes?

> **Código de implementación: M-002 Código fuente: P2 Catálogo: AGE**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Menos de 31 años
2. Entre 31 y 45 años
3. Más de 45 años

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-003 | Pregunta 3

¿Qué nivel de instrucción aprobaste?

> **Código de implementación: M-003 Código fuente: P3 Catálogo: EDU**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Primaria incompleta
2. Primaria completa
3. Secundaria incompleta
4. Secundaria completa
5. Técnico superior incompleta
6. Técnico superior completa
7. Superior universitario incompleta
8. Superior universitario completa

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

### Condiciones laborales

#### M-004 | Pregunta 4

Indica qué PUESTO DE TRABAJO ocupas en la actualidad.

> **Código de implementación: M-004 Código fuente: P4.a Catálogo: JOB**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Catálogo de puestos configurado según la nómina y las unidades de análisis aprobadas por el Grupo de Trabajo.

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 23 -->

#### M-005 | Pregunta 5

En los últimos 12 meses en que puestos has trabajado (escribe los puestos; de no haber cambiado de puesto por favor colocar una línea).

> **Código de implementación: M-005 Código fuente: P4.b Catálogo: JOB**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Catálogo de puestos configurado según la nómina y las unidades de análisis aprobadas por el Grupo de Trabajo.

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-006 | Pregunta 6

Indica en qué ÁREA trabajas en la actualidad.

> **Código de implementación: M-006 Código fuente: P5.a Catálogo: AREA**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Catálogo de áreas, departamentos o secciones configurado según el organigrama y las unidades de análisis.

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-007 | Pregunta 7

En los últimos 12 meses en qué áreas has trabajado. (Escribe las áreas; de no haber cambiado de área por favor colocar una línea)

> **Código de implementación: M-007 Código fuente: P5.b Catálogo: AREA**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Catálogo de áreas, departamentos o secciones configurado según el organigrama y las unidades de análisis.

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-008 | Pregunta 8

¿Qué tipo de contrato laboral tienes?

> **Código de implementación: M-008 Código fuente: P6 Catálogo: CONTRACT**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

> **Opciones y códigos crudos**  
> 1. Soy fijo (plazo indeterminado, indefinido, nombrado) 2. Soy temporal (contrato administrativo de servicio (CAS): Por inicio de actividad / Por necesidades de mercado / Por conversión empresarial) 3. Soy contratado de naturaleza accidental (Ocasional / De suplencia (la que resulte necesaria según circunstancia) / De emergencia (lo que dure la emergencia)) 4. Soy contratado para obra o servicio (Intermitente / De temporada / terceros) 5. Tengo otro tipo de contrato (sujetos a modalidad: Régimen de exportación de productos no tradicionales / Zonas francas y otros regímenes especiales / Otros servicios sujetos a modalidad) 6. Tengo Contrato de trabajo en régimen de tiempo parcial 7. Soy funcionario/directivo 8. Soy temporal con contrato formativo (practicante, residente) 9. Trabajo sin contrato

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 24 -->

#### M-009 | Pregunta 9

¿Realizas tareas adicionales distintas a tu puesto de trabajo?

> **Código de implementación: M-009 Código fuente: P7 Catálogo: ADD_TASK**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Sí, generalmente de mayor responsabilidad
2. Sí, generalmente de menor responsabilidad
3. Sí, generalmente del mismo nivel de responsabilidad
4. Todas las anteriores
5. Generalmente no
6. No lo sé

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-010 | Pregunta 10

En el último año ¿Tus jefes te han consultado sobre cómo mejorar la forma de realizar tu trabajo?

> **Código de implementación: M-010 Código fuente: P8 Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-011 | Pregunta 11

¿El pago que recibes corresponde al puesto de trabajo que ocupas?

> **Código de implementación: M-011 Código fuente: P9 Catálogo: PAY_MATCH**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. No lo sé
2. Sí
3. No, el trabajo que hago es de mayor responsabilidad al pago que recibo
4. No, el trabajo que hago es de menor responsabilidad al pago que recibo

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-012 | Pregunta 12

¿Cuánto tiempo llevas trabajando en tu actual puesto de trabajo?

> **Código de implementación: M-012 Código fuente: P10 Catálogo: TENURE**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Menos de 30 días
2. Entre 1 mes y hasta 6 meses
3. Más de 6 meses y hasta 2 años
4. Más de 2 años y hasta 5 años
5. Más de 5 años y hasta 10 años
6. Más de 10 años

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 25 -->

#### M-013 | Pregunta 13

Considerando el tiempo que lleva en esta empresa o institución, ¿Has ascendido de puesto?

> **Código de implementación: M-013 Código fuente: P11 Catálogo: PROMOTION**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. No
2. Sí, una vez
3. Sí, dos veces
4. Sí, tres o más veces

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-014 | Pregunta 14

Al mes ¿Cuántos sábados trabajas?

> **Código de implementación: M-014 Código fuente: P12 Catálogo: SATURDAY**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Ninguno
2. Alguno excepcionalmente
3. Un sábado al mes
4. Dos sábados
5. Tres o más sábados al mes

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-015 | Pregunta 15

Al mes ¿Cuántos domingos trabajas?

> **Código de implementación: M-015 Código fuente: P13 Catálogo: SUNDAY**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Ninguno
2. Alguno excepcionalmente
3. Un domingo al mes
4. Dos domingos
5. Tres o más domingos al mes

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-016 | Pregunta 16

¿Cuál es tu horario de trabajo?

> **Código de implementación: M-016 Código fuente: P14 Catálogo: SCHEDULE**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Mañana y tarde
2. Rotatorios (excepto noche)
3. Rotatorios (incluido noche)
4. Fijo mañana
5. Fijo tarde
6. Fijo noche
7. Sin horario

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 26 -->

#### M-017 | Pregunta 17

¿Tienes tolerancia en la hora de entrada y salida?

> **Código de implementación: M-017 Código fuente: P15 Catálogo: TOLERANCE**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. No, no tengo ningún margen de tolerancia en relación a la hora de entrada y salida
2. No, porque no tengo horario
3. Sí, puedo elegir entre varios horarios fijos ya establecidos
4. Sí, tengo hasta 30 minutos de tolerancia
5. Sí, tengo más de media hora y hasta una hora de tolerancia
6. Sí, tengo más de una hora de tolerancia

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-018 | Pregunta 18

Si tienes algún asunto personal o familiar, ¿Puedes dejar tu puesto de trabajo al menos una hora?

> **Código de implementación: M-018 Código fuente: P16 Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-019 | Pregunta 19

¿Te cambian la hora de entrada y salida o los días que tienes establecido trabajar?

> **Código de implementación: M-019 Código fuente: P17 Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-020 | Pregunta 20

Durante tu jornada laboral ¿Puedes decidir en qué momento haces un descanso?

> **Código de implementación: M-020 Código fuente: P18 Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 27 -->

#### M-021 | Pregunta 21

Generalmente, ¿Cuántas horas a la semana trabajas para esta empresa, organización o institución?

Código de implementación: M-021 Código fuente: P19 Catálogo: WEEK_HOURS  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. 30 horas o menos
2. De 31 a 35 horas
3. De 36 a 40 horas
4. De 41 a 48 horas
5. Más de 48 horas

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-022 | Pregunta 22

Generalmente, ¿Cuántos días al mes trabajas más de media hora después de tu jornada laboral?

Código de implementación: M-022 Código fuente: P20 Catálogo: EXTRA_DAYS  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Ninguno
2. Algún día excepcionalmente
3. De 1 a 5 días al mes
4. De 6 a 10 días al mes
5. Más de 11 días al mes

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-023 | Pregunta 23

En tu área, ¿Falta personal?

> **Código de implementación: M-023 Código fuente: P21.a Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-024 | Pregunta 24

¿La planificación (organización del trabajo) está de acuerdo con la realidad de tu trabajo?

> **Código de implementación: M-024 Código fuente: P21.b Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 28 -->

#### M-025 | Pregunta 25

¿La tecnología (máquinas, herramientas, equipos de cómputo) con la que trabajas, es la adecuada y funciona correctamente?

> **Código de implementación: M-025 Código fuente: P21.c Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-026 | Pregunta 26

Tu Sueldo es:

Código de implementación: M-026 Código fuente: P22 Catálogo: SALARY_TYPE  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Fijo
2. Todo variable (a destajo, a comisión, por producción, jornal)
3. Una parte fija y otra variable

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-027 | Pregunta 27

Aproximadamente, ¿Cuánto cobras al mes?

Código de implementación: M-027 Código fuente: P23 Catálogo: SALARY_RANGE  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Sin ingresos
2. Hasta 930 soles
3. De 931 a 1700 soles
4. De 1701 a 2550 soles
5. De 2551 a 3400 soles
6. De 3401 a 4250 soles
7. De 4251 a 5100 soles
8. De 5101 a 5950 soles
9. Más de 5951 soles

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-028 | Pregunta 28

¿Qué parte de las tareas familiares y domésticas haces?

> **Código de implementación: M-028 Código fuente: P24 Catálogo: DOMESTIC**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Soy el principal responsable y hago la mayor parte de tareas familiares y domésticas
2. Hago aproximadamente la mitad de las tareas familiares y domésticas
3. Hago la cuarta parte de las tareas familiares y domésticas
4. Sólo hago tareas específicas
5. No hago ninguna o casi ninguna de estas tareas

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

### Factores psicosociales

<!-- Página 29 -->

#### M-029 | Pregunta 29

¿Tienes que trabajar muy rápido?

> **Código de implementación: M-029 Código fuente: P25.a Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Ritmo de trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-030 | Pregunta 30

¿Se producen en tu trabajo momentos o situaciones emocionalmente desgastadoras?

> **Código de implementación: M-030 Código fuente: P25.b Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias emocionales

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-031 | Pregunta 31

¿Te retrasas en la entrega de tu trabajo?

> **Código de implementación: M-031 Código fuente: P25.c Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias cuantitativas

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-032 | Pregunta 32

¿Tu trabajo exige que calles tu opinión?

> **Código de implementación: M-032 Código fuente: P25.d Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencia de esconder emociones

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 30 -->

#### M-033 | Pregunta 33

¿La distribución de tareas es irregular y provoca que se te acumule o junte el trabajo?

> **Código de implementación: M-033 Código fuente: P25.e Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias cuantitativas

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-034 | Pregunta 34

¿Tu trabajo exige que trates a todas las personas por igual, aunque no tengas ganas?

> **Código de implementación: M-034 Código fuente: P25.f Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencia de esconder emociones

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-035 | Pregunta 35

¿Tienes tiempo suficiente para hacer tu trabajo?

> **Código de implementación: M-035 Código fuente: P25.g Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias cuantitativas

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-036 | Pregunta 36

¿Tú decides sobre el ritmo con el que trabajas?

> **Código de implementación: M-036 Código fuente: P25.h Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Influencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 31 -->

#### M-037 | Pregunta 37

¿Influyes en las decisiones acerca de tu trabajo?

> **Código de implementación: M-037 Código fuente: P25.i Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Influencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-038 | Pregunta 38

¿Influyes en la forma de realizar tu trabajo?

> **Código de implementación: M-038 Código fuente: P25.j Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Influencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-039 | Pregunta 39

¿Influyes sobre qué haces en el trabajo?

> **Código de implementación: M-039 Código fuente: P25.k Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Influencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-040 | Pregunta 40

¿Hay momentos en los que necesitas estar en tu trabajo y en tu casa a la vez?

> **Código de implementación: M-040 Código fuente: P25.l Catálogo: FREQ**  
> Dimensión: Conflicto trabajo-familia Subdimensión: Doble presencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 32 -->

#### M-041 | Pregunta 41

¿Sientes que tu trabajo te genera tanto cansancio que perjudica tus actividades domésticas y familiares?

> **Código de implementación: M-041 Código fuente: P25.m Catálogo: FREQ**  
> Dimensión: Conflicto trabajo-familia Subdimensión: Doble presencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-042 | Pregunta 42

¿Sientes que tu trabajo te ocupa tanto tiempo que perjudica tus tareas domésticas y familiares?

> **Código de implementación: M-042 Código fuente: P25.n Catálogo: FREQ**  
> Dimensión: Conflicto trabajo-familia Subdimensión: Doble presencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-043 | Pregunta 43

¿Piensas en tus tareas domésticas y familiares cuando estás trabajando?

> **Código de implementación: M-043 Código fuente: P25.o Catálogo: FREQ**  
> Dimensión: Conflicto trabajo-familia Subdimensión: Doble presencia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-044 | Pregunta 44

¿Te resulta imposible acabar tus actividades laborales?

> **Código de implementación: M-044 Código fuente: P25.p Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias cuantitativas

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 33 -->

#### M-045 | Pregunta 45

¿En tu trabajo tienes que preocuparte o prestar atención a los problemas personales de otros?

> **Código de implementación: M-045 Código fuente: P25.q Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias emocionales

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-046 | Pregunta 46

¿Tu trabajo necesita que tengas iniciativa?

> **Código de implementación: M-046 Código fuente: P26.a Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Posibilidades de desarrollo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-047 | Pregunta 47

¿Las tareas que haces tienen sentido para ti?

> **Código de implementación: M-047 Código fuente: P26.b Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Sentido del trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-048 | Pregunta 48

¿Las tareas que haces te parecen importantes?

> **Código de implementación: M-048 Código fuente: P26.c Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Sentido del trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 34 -->

#### M-049 | Pregunta 49

¿Tu trabajo te afecta emocionalmente (en forma negativa)?

> **Código de implementación: M-049 Código fuente: P26.d Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias emocionales

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-050 | Pregunta 50

¿Tu trabajo permite que aprendas cosas nuevas?

> **Código de implementación: M-050 Código fuente: P26.e Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Posibilidades de desarrollo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-051 | Pregunta 51

¿Debes mantener un alto ritmo de trabajo durante tu jornada laboral?

> **Código de implementación: M-051 Código fuente: P26.f Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Ritmo de trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-052 | Pregunta 52

¿Te sientes comprometido con tu trabajo?

> **Código de implementación: M-052 Código fuente: P26.g Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Sentido del trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 35 -->

#### M-053 | Pregunta 53

¿Tu trabajo te da la oportunidad de mejorar tus conocimientos y habilidades?

> **Código de implementación: M-053 Código fuente: P26.h Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Posibilidades de desarrollo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-054 | Pregunta 54

¿Tu trabajo es emocionalmente desgastador?

> **Código de implementación: M-054 Código fuente: P26.i Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencias emocionales

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-055 | Pregunta 55

¿Tu trabajo exige que guardes tus emociones y sentimientos?

> **Código de implementación: M-055 Código fuente: P26.j Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencia de esconder emociones

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-056 | Pregunta 56

¿Te exigen en el trabajo ser amable con todas las personas sin importar como te traten?

> **Código de implementación: M-056 Código fuente: P26.k Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Exigencia de esconder emociones

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 36 -->

#### M-057 | Pregunta 57

¿Tu trabajo permite que apliques tus habilidades, destrezas y conocimientos?

> **Código de implementación: M-057 Código fuente: P26.l Catálogo: FREQ**  
> Dimensión: Control sobre el trabajo Subdimensión: Posibilidades de desarrollo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-058 | Pregunta 58

¿El ritmo de trabajo es alto durante toda la jornada?

> **Código de implementación: M-058 Código fuente: P26.m Catálogo: FREQ**  
> Dimensión: Exigencias psicológicas en el trabajo Subdimensión: Ritmo de trabajo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-059 | Pregunta 59

¿En tu trabajo se te informa con suficiente anticipación de los cambios, decisiones importantes y proyectos a futuro?

> **Código de implementación: M-059 Código fuente: P27.a Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Previsibilidad

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-060 | Pregunta 60

¿Tu trabajo tiene objetivos claros?

> **Código de implementación: M-060 Código fuente: P27.b Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Claridad de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 37 -->

#### M-061 | Pregunta 61

¿Se te exigen cosas contradictorias en el trabajo?

> **Código de implementación: M-061 Código fuente: P27.c Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Conflicto de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-062 | Pregunta 62

¿Sabes exactamente qué tareas son de tu responsabilidad?

> **Código de implementación: M-062 Código fuente: P27.d Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Claridad de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-063 | Pregunta 63

¿Recibes toda la información que necesitas para realizar bien tu trabajo?

> **Código de implementación: M-063 Código fuente: P27.e Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Previsibilidad

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-064 | Pregunta 64

¿Haces cosas en el trabajo que son aceptadas por algunas personas y no por otras?

> **Código de implementación: M-064 Código fuente: P27.f Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Conflicto de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 38 -->

#### M-065 | Pregunta 65

¿Sabes exactamente qué se espera de ti en el trabajo?

> **Código de implementación: M-065 Código fuente: P27.g Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Claridad de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-066 | Pregunta 66

¿Sabes exactamente que margen de autonomía tienes al realizar tu trabajo?

> **Código de implementación: M-066 Código fuente: P27.h Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Claridad de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-067 | Pregunta 67

¿Tienes que hacer tareas que crees que deberían hacerse de otra manera?

> **Código de implementación: M-067 Código fuente: P27.i Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Conflicto de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-068 | Pregunta 68

¿Tienes que realizar tareas que te parecen innecesarias?

> **Código de implementación: M-068 Código fuente: P27.j Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Conflicto de rol

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 39 -->

#### M-069 | Pregunta 69

¿Recibes ayuda y apoyo de tus compañeros y compañeras en la realización de tu trabajo?

> **Código de implementación: M-069 Código fuente: P28.a Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de los compañeros

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-070 | Pregunta 70

¿Tus compañeros y compañeras están dispuestos a escuchar tus problemas de trabajo?

> **Código de implementación: M-070 Código fuente: P28.b Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de los compañeros

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-071 | Pregunta 71

¿Tus compañeros y compañeras hablan contigo sobre cómo haces tu trabajo?

> **Código de implementación: M-071 Código fuente: P28.c Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de los compañeros

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-072 | Pregunta 72

¿Tienes un buen ambiente laboral con tus compañeros y compañeras de trabajo?

> **Código de implementación: M-072 Código fuente: P28.d Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Sentimiento de grupo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 40 -->

#### M-073 | Pregunta 73

¿En tu trabajo sientes que formas parte de un grupo o equipo de trabajo?

> **Código de implementación: M-073 Código fuente: P28.e Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Sentimiento de grupo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-074 | Pregunta 74

¿Se ayudan entre compañeros y compañeras en el trabajo?

> **Código de implementación: M-074 Código fuente: P28.f Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Sentimiento de grupo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-075 | Pregunta 75

¿Tu jefe inmediato está dispuesto a escuchar tus problemas del trabajo?

> **Código de implementación: M-075 Código fuente: P28.g Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de superiores

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-076 | Pregunta 76

¿Recibes ayuda y apoyo de tu jefe inmediato en la realización de tu trabajo?

> **Código de implementación: M-076 Código fuente: P28.h Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de superiores

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 41 -->

#### M-077 | Pregunta 77

¿Tu jefe inmediato habla contigo acerca de cómo haces tu trabajo?

> **Código de implementación: M-077 Código fuente: P28.i Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Apoyo social de superiores

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-078 | Pregunta 78

¿Estás preocupado/a por si te trasladan a otro centro de trabajo, área, departamento o sección en contra tu voluntad?

> **Código de implementación: M-078 Código fuente: P29.a Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre las condiciones de trabajo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-079 | Pregunta 79

¿Estás preocupado/a por si te cambian el horario (turno, días de la semana, horas de entrada y salida...) contra tu voluntad?

> **Código de implementación: M-079 Código fuente: P29.b Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre las condiciones de trabajo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-080 | Pregunta 80

¿Estás preocupado/a por si te cambian de tareas contra tu voluntad?

> **Código de implementación: M-080 Código fuente: P29.c Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre las condiciones de trabajo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

<!-- Página 42 -->

#### M-081 | Pregunta 81

¿Estás preocupado/a por si te despiden o no te renuevan el contrato?

> **Código de implementación: M-081 Código fuente: P29.d Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre el empleo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-082 | Pregunta 82

¿Estás preocupado/a por si te varían el sueldo o pago (que no te lo actualicen, que te lo bajen, que introduzcan el salario variable, que te paguen en especies, etc.)?

> **Código de implementación: M-082 Código fuente: P29.e Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre las condiciones de trabajo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-083 | Pregunta 83

¿Estás preocupado/a por lo difícil que sería encontrar otro trabajo en el caso de que te quedases sin trabajo?

> **Código de implementación: M-083 Código fuente: P29.f Catálogo: CONCERN**  
> Dimensión: Compensaciones del trabajo Subdimensión: Inseguridad sobre el empleo

**Opciones y códigos crudos**

1. Estoy muy preocupado
2. Estoy bastante preocupado
3. Estoy más o menos preocupado
4. Estoy un poco preocupado
5. No estoy preocupado

Regla de calificación: Provisional: R = 6 - código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia/preocupación alta = mayor riesgo

#### M-084 | Pregunta 84

¿Tu trabajo es valorado por la gerencia, la dirección o la jefatura?

> **Código de implementación: M-084 Código fuente: P30.a Catálogo: FREQ**  
> Dimensión: Compensaciones del trabajo Subdimensión: Reconocimiento

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 43 -->

#### M-085 | Pregunta 85

¿La gerencia, la dirección o la jefatura te respeta?

> **Código de implementación: M-085 Código fuente: P30.b Catálogo: FREQ**  
> Dimensión: Compensaciones del trabajo Subdimensión: Reconocimiento

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-086 | Pregunta 86

¿Recibes un trato justo de la gerencia, la dirección o la jefatura?

> **Código de implementación: M-086 Código fuente: P30.c Catálogo: FREQ**  
> Dimensión: Compensaciones del trabajo Subdimensión: Reconocimiento

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-087 | Pregunta 87

¿La gerencia, la dirección o la jefatura confía en que sus trabajadores hacen bien su trabajo?

> **Código de implementación: M-087 Código fuente: P30.d Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Confianza vertical

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-088 | Pregunta 88

¿Puedes confiar de la información que viene de la gerencia, la dirección o la jefatura?

> **Código de implementación: M-088 Código fuente: P30.e Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Confianza vertical

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 44 -->

#### M-089 | Pregunta 89

¿Se solucionan los conflictos de una manera justa?

> **Código de implementación: M-089 Código fuente: P30.f Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Justicia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-090 | Pregunta 90

¿Se te reconoce por el trabajo bien hecho?

> **Código de implementación: M-090 Código fuente: P30.g Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Justicia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-091 | Pregunta 91

¿La gerencia, la dirección o la jefatura considera con la misma seriedad las propuestas procedentes de todos los trabajadores?

> **Código de implementación: M-091 Código fuente: P30.h Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Justicia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-092 | Pregunta 92

¿Los trabajadores pueden expresar sus opiniones y emociones?

> **Código de implementación: M-092 Código fuente: P30.i Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Confianza vertical

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 45 -->

#### M-093 | Pregunta 93

¿Se distribuyen las tareas de una forma justa?

> **Código de implementación: M-093 Código fuente: P30.j Catálogo: FREQ**  
> Dimensión: Capital social Subdimensión: Justicia

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-094 | Pregunta 94

¿Tu actual jefe inmediato se asegura de que cada uno de los trabajadores tenga buenas oportunidades de desarrollo laboral?

> **Código de implementación: M-094 Código fuente: P30.k Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Calidad de liderazgo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-095 | Pregunta 95

¿Tu actual jefe inmediato planifica bien el trabajo?

> **Código de implementación: M-095 Código fuente: P30.l Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Calidad de liderazgo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

#### M-096 | Pregunta 96

¿Tu actual jefe inmediato distribuye bien el trabajo?

> **Código de implementación: M-096 Código fuente: P30.m Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Calidad de liderazgo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

<!-- Página 46 -->

#### M-097 | Pregunta 97

¿Tu actual jefe inmediato resuelve bien los conflictos laborales?

> **Código de implementación: M-097 Código fuente: P30.n Catálogo: FREQ**  
> Dimensión: Apoyo social y calidad de liderazgo Subdimensión: Calidad de liderazgo

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Provisional: R = código crudo; T = 25 x (R - 1).  
Sentido: Frecuencia baja = mayor riesgo

### Salud, bienestar y satisfacción

#### M-098 | Pregunta 98

En general ¿Dirías que tu salud es?

> **Código de implementación: M-098 Código fuente: P31 Catálogo: HEALTH**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Excelente
2. Muy buena
3. Buena
4. Regular
5. Mala

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-099 | Pregunta 99

¿Te has sentido agotado?

> **Código de implementación: M-099 Código fuente: P32.a Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-100 | Pregunta 100

¿Te has sentido emocionalmente agotado?

> **Código de implementación: M-100 Código fuente: P32.b Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 47 -->

#### M-101 | Pregunta 101

¿Te has sentido físicamente agotado?

> **Código de implementación: M-101 Código fuente: P32.c Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-102 | Pregunta 102

¿Has estado cansado?

> **Código de implementación: M-102 Código fuente: P32.d Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-103 | Pregunta 103

¿Has tenido problemas para relajarte?

> **Código de implementación: M-103 Código fuente: P32.e Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-104 | Pregunta 104

¿Has estado irritable?

> **Código de implementación: M-104 Código fuente: P32.f Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 48 -->

#### M-105 | Pregunta 105

¿Has estado tenso/a?

> **Código de implementación: M-105 Código fuente: P32.g Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-106 | Pregunta 106

¿Has estado estresado/a?

> **Código de implementación: M-106 Código fuente: P32.h Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-107 | Pregunta 107

¿Has estado muy nervioso/a?

> **Código de implementación: M-107 Código fuente: P33.a Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-108 | Pregunta 108

¿Te has sentido con la moral tan baja que nada podía animarte?

> **Código de implementación: M-108 Código fuente: P33.b Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 49 -->

#### M-109 | Pregunta 109

¿Te has sentido calmado y tranquilo?

> **Código de implementación: M-109 Código fuente: P33.c Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-110 | Pregunta 110

¿Te has sentido desanimado y triste?

> **Código de implementación: M-110 Código fuente: P33.d Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-111 | Pregunta 111

¿Te has sentido feliz?

> **Código de implementación: M-111 Código fuente: P33.e Catálogo: FREQ**  
> Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Siempre
2. Muchas veces
3. Algunas veces
4. Sólo alguna vez
5. Nunca

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

#### M-112 | Pregunta 112

¿Cuál es tu grado de satisfacción en relación con tu trabajo, tomándolo todo en consideración?

Código de implementación: M-112 Código fuente: P34 Catálogo: SATISFACTION  
Dimensión: No aplica Subdimensión: Variable descriptiva

**Opciones y códigos crudos**

1. Muy satisfecho/a
2. Satisfecho/a
3. Insatisfecho/a
4. Muy insatisfecho/a

Regla de calificación: Descriptiva. No integra el puntaje psicosocial.  
Sentido: No puntuable

<!-- Página 50 -->

## 10. Matrices de importación y trazabilidad

### 10.1 Matriz compacta de la versión corta

| ID | P<br>fuente | Categoría | Dimensión | Subdimensión de origen | Catálogo | Polaridad |
| --- | --- | --- | --- | --- | --- | --- |
| C-001 | P1 | Sociodemográfica | No aplica | Variable descriptiva | SEX | N/A |
| C-002 | P2 | Sociodemográfica | No aplica | Variable descriptiva | AGE | N/A |
| C-003 | P3 | Sociodemográfica | No aplica | Variable descriptiva | EDU | N/A |
| C-004 | P4.a | Condiciones laborales | No aplica | Variable descriptiva | JOB | N/A |
| C-005 | P5.a | Condiciones laborales | No aplica | Variable descriptiva | AREA | N/A |
| C-006 | P6 | Condiciones laborales | No aplica | Variable descriptiva | CONTRACT | N/A |
| C-007 | P10 | Condiciones laborales | No aplica | Variable descriptiva | TENURE | N/A |
| C-008 | P14 | Condiciones laborales | No aplica | Variable descriptiva | SCHEDULE | N/A |
| C-009 | P19 | Condiciones laborales | No aplica | Variable descriptiva | WEEK HOURS | N/A |
| C-010 | P22 | Condiciones laborales | No aplica | Variable descriptiva | SALARY TYPE | N/A |
| C-011 | P23 | Condiciones laborales | No aplica | Variable descriptiva | SALARY RAN GE | N/A |
| C-012 | P25.b | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias emocionales | FREQ | 6 - raw |
| C-013 | P25.c | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias cuantitativas | FREQ | 6 - raw |
| C-014 | P25.d | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencia de esconder<br>emociones | FREQ | 6 - raw |
| C-015 | P25.e | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias cuantitativas | FREQ | 6 - raw |
| C-016 | P25.j | Factores<br>psicosociales | Control sobre el trabajo | Influencia | FREQ | raw |
| C-017 | P25.m | Factores<br>psicosociales | Conflicto trabajo-familia | Doble presencia | FREQ | 6 - raw |
| C-018 | P25.n | Factores<br>psicosociales | Conflicto trabajo-familia | Doble presencia | FREQ | 6 - raw |
| C-019 | P25.o | Factores<br>psicosociales | Conflicto trabajo-familia | Doble presencia | FREQ | 6 - raw |
| C-020 | P26.a | Factores<br>psicosociales | Control sobre el trabajo | Posibilidades de desarrollo | FREQ | raw |
| C-021 | P26.c | Factores<br>psicosociales | Control sobre el trabajo | Sentido del trabajo | FREQ | raw |
| C-022 | P26.d | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias emocionales | FREQ | 6 - raw |
| C-023 | P26.g | Factores<br>psicosociales | Control sobre el trabajo | Sentido del trabajo | FREQ | raw |
| C-024 | P26.h | Factores<br>psicosociales | Control sobre el trabajo | Posibilidades de desarrollo | FREQ | raw |
| C-025 | P26.j | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencia de esconder<br>emociones | FREQ | 6 - raw |
| C-026 | P26.m | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Ritmo de trabajo | FREQ | 6 - raw |
| C-027 | P27.b | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Claridad de rol | FREQ | raw |
| C-028 | P27.c | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Conflicto de rol | FREQ | 6 - raw |
| C-029 | P27.e | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Previsibilidad | FREQ | raw |
| C-030 | P28.a | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de los<br>compañeros | FREQ | raw |

<!-- Página 51 -->

| ID | P<br>fuente | Categoría | Dimensión | Subdimensión de origen | Catálogo | Polaridad |
| --- | --- | --- | --- | --- | --- | --- |
| C-031 | P28.e | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Sentimiento de grupo | FREQ | raw |
| C-032 | P28.h | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de superiores | FREQ | raw |
| C-033 | P29.c | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre las<br>condiciones de trabajo | CONCERN | 6 - raw |
| C-034 | P29.d | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre el empleo | CONCERN | 6 - raw |
| C-035 | P29.e | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre las<br>condiciones de trabajo | CONCERN | 6 - raw |
| C-036 | P29.f | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre el empleo | CONCERN | 6 - raw |
| C-037 | P30.a | Factores<br>psicosociales | Compensaciones del trabajo | Reconocimiento | FREQ | raw |
| C-038 | P30.e | Factores<br>psicosociales | Capital social | Confianza vertical | FREQ | raw |
| C-039 | P30.h | Factores<br>psicosociales | Capital social | Justicia | FREQ | raw |
| C-040 | P30.i | Factores<br>psicosociales | Capital social | Confianza vertical | FREQ | raw |
| C-041 | P30.j | Factores<br>psicosociales | Capital social | Justicia | FREQ | raw |
| C-042 | P30.m | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Calidad de liderazgo | FREQ | raw |

<!-- Página 52 -->

### 10.2 Matriz compacta de la versión media

| ID | P<br>fuente | Categoría | Dimensión | Subdimensión | Catálogo | Polaridad |
| --- | --- | --- | --- | --- | --- | --- |
| M-001 | P1 | Sociodemográfica | No aplica | Variable descriptiva | SEX | N/A |
| M-002 | P2 | Sociodemográfica | No aplica | Variable descriptiva | AGE | N/A |
| M-003 | P3 | Sociodemográfica | No aplica | Variable descriptiva | EDU | N/A |
| M-004 | P4.a | Condiciones laborales | No aplica | Variable descriptiva | JOB | N/A |
| M-005 | P4.b | Condiciones laborales | No aplica | Variable descriptiva | JOB | N/A |
| M-006 | P5.a | Condiciones laborales | No aplica | Variable descriptiva | AREA | N/A |
| M-007 | P5.b | Condiciones laborales | No aplica | Variable descriptiva | AREA | N/A |
| M-008 | P6 | Condiciones laborales | No aplica | Variable descriptiva | CONTRACT | N/A |
| M-009 | P7 | Condiciones laborales | No aplica | Variable descriptiva | ADD TASK | N/A |
| M-010 | P8 | Condiciones laborales | No aplica | Variable descriptiva | FREQ | N/A |
| M-011 | P9 | Condiciones laborales | No aplica | Variable descriptiva | PAY MATCH | N/A |
| M-012 | P10 | Condiciones laborales | No aplica | Variable descriptiva | TENURE | N/A |
| M-013 | P11 | Condiciones laborales | No aplica | Variable descriptiva | PROMOTION | N/A |
| M-014 | P12 | Condiciones laborales | No aplica | Variable descriptiva | SATURDAY | N/A |
| M-015 | P13 | Condiciones laborales | No aplica | Variable descriptiva | SUNDAY | N/A |
| M-016 | P14 | Condiciones laborales | No aplica | Variable descriptiva | SCHEDULE | N/A |
| M-017 | P15 | Condiciones laborales | No aplica | Variable descriptiva | TOLERANCE | N/A |
| M-018 | P16 | Condiciones laborales | No aplica | Variable descriptiva | FREQ | N/A |
| M-019 | P17 | Condiciones laborales | No aplica | Variable descriptiva | FREQ | N/A |
| M-020 | P18 | Condiciones laborales | No aplica | Variable descriptiva | FREQ | N/A |
| M-021 | P19 | Condiciones laborales | No aplica | Variable descriptiva | WEEK HOURS | N/A |
| M-022 | P20 | Condiciones laborales | No aplica | Variable descriptiva | EXTRA DAYS | N/A |
| M-023 | P21.a | Condiciones laborales | No aplica | Variable descriptiva | FREQ | N/A |
| M-024 | P21.b | Condiciones laborales | No aplica | Variable descriptiva | FREQ | N/A |
| M-025 | P21.c | Condiciones laborales | No aplica | Variable descriptiva | FREQ | N/A |
| M-026 | P22 | Condiciones laborales | No aplica | Variable descriptiva | SALARY TYPE | N/A |
| M-027 | P23 | Condiciones laborales | No aplica | Variable descriptiva | SALARY RAN GE | N/A |
| M-028 | P24 | Condiciones laborales | No aplica | Variable descriptiva | DOMESTIC | N/A |
| M-029 | P25.a | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Ritmo de trabajo | FREQ | 6 - raw |
| M-030 | P25.b | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias emocionales | FREQ | 6 - raw |
| M-031 | P25.c | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias cuantitativas | FREQ | 6 - raw |
| M-032 | P25.d | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencia de esconder<br>emociones | FREQ | 6 - raw |
| M-033 | P25.e | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias cuantitativas | FREQ | 6 - raw |
| M-034 | P25.f | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencia de esconder<br>emociones | FREQ | 6 - raw |
| M-035 | P25.g | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias cuantitativas | FREQ | raw |
| M-036 | P25.h | Factores<br>psicosociales | Control sobre el trabajo | Influencia | FREQ | raw |
| M-037 | P25.i | Factores<br>psicosociales | Control sobre el trabajo | Influencia | FREQ | raw |

<!-- Página 53 -->

| ID | P<br>fuente | Categoría | Dimensión | Subdimensión | Catálogo | Polaridad |
| --- | --- | --- | --- | --- | --- | --- |
| M-038 | P25.j | Factores<br>psicosociales | Control sobre el trabajo | Influencia | FREQ | raw |
| M-039 | P25.k | Factores<br>psicosociales | Control sobre el trabajo | Influencia | FREQ | raw |
| M-040 | P25.l | Factores<br>psicosociales | Conflicto trabajo-familia | Doble presencia | FREQ | 6 - raw |
| M-041 | P25.m | Factores<br>psicosociales | Conflicto trabajo-familia | Doble presencia | FREQ | 6 - raw |
| M-042 | P25.n | Factores<br>psicosociales | Conflicto trabajo-familia | Doble presencia | FREQ | 6 - raw |
| M-043 | P25.o | Factores<br>psicosociales | Conflicto trabajo-familia | Doble presencia | FREQ | 6 - raw |
| M-044 | P25.p | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias cuantitativas | FREQ | 6 - raw |
| M-045 | P25.q | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias emocionales | FREQ | 6 - raw |
| M-046 | P26.a | Factores<br>psicosociales | Control sobre el trabajo | Posibilidades de desarrollo | FREQ | raw |
| M-047 | P26.b | Factores<br>psicosociales | Control sobre el trabajo | Sentido del trabajo | FREQ | raw |
| M-048 | P26.c | Factores<br>psicosociales | Control sobre el trabajo | Sentido del trabajo | FREQ | raw |
| M-049 | P26.d | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias emocionales | FREQ | 6 - raw |
| M-050 | P26.e | Factores<br>psicosociales | Control sobre el trabajo | Posibilidades de desarrollo | FREQ | raw |
| M-051 | P26.f | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Ritmo de trabajo | FREQ | 6 - raw |
| M-052 | P26.g | Factores<br>psicosociales | Control sobre el trabajo | Sentido del trabajo | FREQ | raw |
| M-053 | P26.h | Factores<br>psicosociales | Control sobre el trabajo | Posibilidades de desarrollo | FREQ | raw |
| M-054 | P26.i | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencias emocionales | FREQ | 6 - raw |
| M-055 | P26.j | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencia de esconder<br>emociones | FREQ | 6 - raw |
| M-056 | P26.k | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Exigencia de esconder<br>emociones | FREQ | 6 - raw |
| M-057 | P26.l | Factores<br>psicosociales | Control sobre el trabajo | Posibilidades de desarrollo | FREQ | raw |
| M-058 | P26.m | Factores<br>psicosociales | Exigencias psicológicas en el<br>trabajo | Ritmo de trabajo | FREQ | 6 - raw |
| M-059 | P27.a | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Previsibilidad | FREQ | raw |
| M-060 | P27.b | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Claridad de rol | FREQ | raw |
| M-061 | P27.c | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Conflicto de rol | FREQ | 6 - raw |
| M-062 | P27.d | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Claridad de rol | FREQ | raw |
| M-063 | P27.e | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Previsibilidad | FREQ | raw |
| M-064 | P27.f | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Conflicto de rol | FREQ | 6 - raw |
| M-065 | P27.g | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Claridad de rol | FREQ | raw |
| M-066 | P27.h | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Claridad de rol | FREQ | raw |

<!-- Página 54 -->

| ID | P<br>fuente | Categoría | Dimensión | Subdimensión | Catálogo | Polaridad |
| --- | --- | --- | --- | --- | --- | --- |
| M-067 | P27.i | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Conflicto de rol | FREQ | 6 - raw |
| M-068 | P27.j | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Conflicto de rol | FREQ | 6 - raw |
| M-069 | P28.a | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de los<br>compañeros | FREQ | raw |
| M-070 | P28.b | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de los<br>compañeros | FREQ | raw |
| M-071 | P28.c | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de los<br>compañeros | FREQ | raw |
| M-072 | P28.d | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Sentimiento de grupo | FREQ | raw |
| M-073 | P28.e | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Sentimiento de grupo | FREQ | raw |
| M-074 | P28.f | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Sentimiento de grupo | FREQ | raw |
| M-075 | P28.g | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de superiores | FREQ | raw |
| M-076 | P28.h | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de superiores | FREQ | raw |
| M-077 | P28.i | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Apoyo social de superiores | FREQ | raw |
| M-078 | P29.a | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre las<br>condiciones de trabajo | CONCERN | 6 - raw |
| M-079 | P29.b | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre las<br>condiciones de trabajo | CONCERN | 6 - raw |
| M-080 | P29.c | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre las<br>condiciones de trabajo | CONCERN | 6 - raw |
| M-081 | P29.d | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre el empleo | CONCERN | 6 - raw |
| M-082 | P29.e | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre las<br>condiciones de trabajo | CONCERN | 6 - raw |
| M-083 | P29.f | Factores<br>psicosociales | Compensaciones del trabajo | Inseguridad sobre el empleo | CONCERN | 6 - raw |
| M-084 | P30.a | Factores<br>psicosociales | Compensaciones del trabajo | Reconocimiento | FREQ | raw |
| M-085 | P30.b | Factores<br>psicosociales | Compensaciones del trabajo | Reconocimiento | FREQ | raw |
| M-086 | P30.c | Factores<br>psicosociales | Compensaciones del trabajo | Reconocimiento | FREQ | raw |
| M-087 | P30.d | Factores<br>psicosociales | Capital social | Confianza vertical | FREQ | raw |
| M-088 | P30.e | Factores<br>psicosociales | Capital social | Confianza vertical | FREQ | raw |
| M-089 | P30.f | Factores<br>psicosociales | Capital social | Justicia | FREQ | raw |
| M-090 | P30.g | Factores<br>psicosociales | Capital social | Justicia | FREQ | raw |
| M-091 | P30.h | Factores<br>psicosociales | Capital social | Justicia | FREQ | raw |
| M-092 | P30.i | Factores<br>psicosociales | Capital social | Confianza vertical | FREQ | raw |
| M-093 | P30.j | Factores<br>psicosociales | Capital social | Justicia | FREQ | raw |
| M-094 | P30.k | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Calidad de liderazgo | FREQ | raw |
| M-095 | P30.l | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Calidad de liderazgo | FREQ | raw |

<!-- Página 55 -->

| ID | P<br>fuente | Categoría | Dimensión | Subdimensión | Catálogo | Polaridad |
| --- | --- | --- | --- | --- | --- | --- |
| M-096 | P30.m | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Calidad de liderazgo | FREQ | raw |
| M-097 | P30.n | Factores<br>psicosociales | Apoyo social y calidad de<br>liderazgo | Calidad de liderazgo | FREQ | raw |
| M-098 | P31 | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | HEALTH | N/A |
| M-099 | P32.a | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-100 | P32.b | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-101 | P32.c | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-102 | P32.d | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-103 | P32.e | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-104 | P32.f | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-105 | P32.g | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-106 | P32.h | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-107 | P33.a | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-108 | P33.b | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-109 | P33.c | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-110 | P33.d | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-111 | P33.e | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | FREQ | N/A |
| M-112 | P34 | Salud, bienestar y<br>satisfacción | No aplica | Variable descriptiva | SATISFACTIO<br>N | N/A |

<!-- Página 56 -->

## 11. Módulos adicionales y adaptación futura

Colmena puede crecer mediante módulos adicionales, siempre que se mantengan fuera del núcleo CENSOPAS-COPSOQ y se distingan visual, lógica y contractualmente. Cada módulo debe tener una pregunta de investigación, marco conceptual, población objetivo, procedimiento de validación, consentimiento o base de tratamiento, baremo propio y reporte separado.

| Módulo sugerido | Propósito | Regla de integración |
| --- | --- | --- |
| Violencia y hostigamiento | Identificar exposición a hostigamiento laboral, sexual, ciberacoso<br>u otras conductas. | Reporte separado, rutas de atención y<br>controles reforzados. |
| Teletrabajo e hiperconectividad | Medir disponibilidad permanente, aislamiento, control digital y<br>desconexión. | No sumar a dimensiones CENSOPAS sin<br>validación. |
| Condiciones físicas y<br>ergonómicas | Relacionar carga física, ambiente y organización. | Módulo complementario del sistema de<br>SST. |
| Eventos críticos | Explorar reorganización, despidos, emergencias o cambios<br>tecnológicos. | Activación temporal y análisis<br>contextual. |
| Preguntas abiertas | Recoger origen percibido y propuestas preventivas. | Análisis cualitativo, anonimización y sin<br>puntuación. |

### 11.1 Ciclo mínimo de validación de un módulo

1. Definir constructo, finalidad, población y decisión que apoyará el resultado.

2. Revisar evidencia y redactar ítems con expertos y trabajadores.

3. Realizar validez de contenido y entrevistas cognitivas.

4. Ejecutar piloto, analizar distribución, faltantes y comprensión.

5. Evaluar estructura interna, confiabilidad y relación con variables externas.

6. Estudiar invariancia por sexo, sector, tamaño y región cuando la muestra lo permita.

7. Construir baremos con muestra de referencia adecuada y documentar incertidumbre.

8. Congelar versión, publicar manual, crear pruebas unitarias y monitorear desempeño.

> **Nombre del producto**  
> Si se transforma el cuestionario, se cambian sus preguntas o se usan baremos propios, el resultado debe denominarse instrumento o módulo Colmena. No debe presentarse como CENSOPAS-COPSOQ oficial ni como equivalente validado sin autorización y evidencia de concordancia.

## 12. Plan de verificación antes de producción

| Control | Criterio de aceptación | Estado inicial |
| --- | --- | --- |
| Banco de ítems | 42 ítems corta y 112 media, sin omisiones ni duplicados. | Completo en este manual |
| Catálogos | Opciones, códigos y orden coinciden con cuestionarios oficiales. | Completo, sujeto a revisión de<br>forma |
| Matriz | 31 y 69 ítems asignados a constructos correctos. | Completo |
| Polaridad | Regla por ítem confirmada por fuente autorizada. | Pendiente de confirmación |
| Transformación | Algoritmo de puntaje confirmado y probado. | Propuesta provisional |
| Baremos | C1 y C2 peruanos cargados, versionados y trazables. | Pendiente, bloqueante |
| Concordancia | Casos de prueba coinciden con la plataforma oficial o patrón autorizado. | Pendiente, bloqueante |
| Privacidad | No hay identificadores directos y se suprimen celdas pequeñas. | Requisito de diseño |
| Reporte | Incluye metodología, distribución, nivel, limitaciones y plan preventivo. | Especificado |
| Módulos | Separados del núcleo y con validación propia. | Requisito de arquitectura |

### 12.1 Pruebas mínimas del motor

- Prueba por cada catálogo: valores mínimo, máximo, vacío y código inválido.

<!-- Página 57 -->

- Prueba por cada ítem: polaridad directa o inversa y transformación 0, 25, 50, 75 y 100.

- Prueba por constructo: inclusión exacta de ítems, faltantes y denominador válido.

- Prueba de baremo: valores justo debajo, iguales y justo encima de C1 y C2.

- Prueba de agrupación: 49,9%, 50,0% y empates entre colores.

- Prueba de privacidad: n entre 1 y 4, cruces de variables y exportaciones.

- Prueba de regresión: el mismo conjunto de datos y versión produce el mismo hash y reporte.

<!-- Página 58 -->

## Referencias

Congreso de la República del Perú. (2011). Ley N.° 29733, Ley de Protección de Datos Personales. https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733 Congreso de la República del Perú. (2011). Ley N.° 29783, Ley de Seguridad y Salud en el Trabajo. https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/462576-29783 COPSOQ International Network. (2020). Licence, guidelines and questionnaire. https://www.copsoq-network.org/licence-guidelines-and-questionnaire Instituto Nacional de Salud. (2023). Curso autoformativo de evaluación de riesgos psicosociales laborales. https://www.gob.pe/institucion/ins/campañas/36019-curso-autoformativo-de-evaluacion-de-riesgos-psicosociales-laborales Instituto Nacional de Salud, Centro Nacional de Salud Ocupacional y Protección del Ambiente para la Salud. (2025). Manual del Método CENSOPAS-COPSOQ (2a ed.). Instituto Nacional de Salud, Centro Nacional de Salud Ocupacional y Protección del Ambiente para la Salud. (s. f.). Cuestionario para la evaluación de riesgos psicosociales en el trabajo CENSOPAS-COPSOQ: Versión corta. Instituto Nacional de Salud, Centro Nacional de Salud Ocupacional y Protección del Ambiente para la Salud. (s. f.). Cuestionario para la evaluación de riesgos psicosociales en el trabajo CENSOPAS-COPSOQ: Versión media. Lucero-Perez, M. R., Sabastizagal, I., Astete-Cornejo, J., Burgos, M. A., Villarreal-Zegarra, D., & Moncada, S. (2022). Validation of the medium and short version of CENSOPAS-COPSOQ: A psychometric study in the Peruvian population. BMC Public Health, 22, 910. https://doi.org/10.1186/s12889-022-13328-0 Ministerio de Trabajo y Promoción del Empleo. (2008). Resolución Ministerial N.° 375-2008-TR. https://www.gob.pe/institucion/mtpe/normas-legales/394457-375-2008-tr Ministerio de Trabajo y Promoción del Empleo. (2013). Resolución Ministerial N.° 050-2013-TR. https://www.gob.pe/institucion/mtpe/normas-legales/288031-050-2013-tr Presidencia de la República del Perú. (2012). Decreto Supremo N.° 005-2012-TR, Reglamento de la Ley N.° 29783. https://www.gob.pe/institucion/presidencia/normas-legales/462577-005-2012-tr

## Nota final de trazabilidad

El banco de ítems y los catálogos fueron transcritos y normalizados a partir de los archivos suministrados. La normalización corrigió espacios, saltos de línea y pequeñas inconsistencias tipográficas sin alterar el significado. Antes de cargar el contenido en producción debe efectuarse una comparación visual de doble control con los cuestionarios oficiales vigentes y dejar evidencia de aprobación del responsable técnico y del evaluador autorizado.

Fin del manual técnico.

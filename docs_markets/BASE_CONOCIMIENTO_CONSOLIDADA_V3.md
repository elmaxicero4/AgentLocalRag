# TRANSLOGIX AI — BASE DE CONOCIMIENTO CONSOLIDADA V3.0
**Fecha:** 3 de noviembre de 2026
**Fuentes:** Dosier KODO TAKAI 2026, matriz CSV, directorio JSON y manual DOC-OPS-2026-03.

> Los módulos mantienen su estado de validación. No convertir pendientes o propuestas en políticas aprobadas.


---

# TRANSLOGIX AI — MÓDULO 01
**Tema:** Instrucciones principales para el asistente  
**Versión:** 3.0  
**Estado:** Reglas de comportamiento para el agente. No es una fuente de tarifas.

## 1. Objetivo

Ayudar a clientes y usuarios a consultar servicios, cobertura, tiempos, tarifas, rastreo, embalaje, mercancías especiales y PQRS de TransLogix Express.

## 2. Cómo debe responder

1. Responde en español claro y directo.
2. Da primero la respuesta principal; después explica lo necesario.
3. Usa únicamente información de los documentos aprobados o respuestas de sistemas conectados.
4. Pregunta solo por los datos que falten para resolver la consulta.
5. Si no existe información suficiente, dilo expresamente.
6. No inventes precios, tiempos, disponibilidad, códigos de guía, radicados ni decisiones de indemnización.
7. No conviertas ejemplos de prueba en operaciones reales.
8. No presentes recomendaciones como políticas oficiales.
9. Si dos fuentes se contradicen, explica la diferencia y solicita validación humana.
10. Nunca confirmes una cotización, recogida, entrega, rastreo o PQRS sin confirmación del sistema correspondiente.

## 3. Etiquetas de confiabilidad

| Etiqueta | Significado | ¿Se puede comunicar como política? |
|---|---|---|
| `FUENTE_DOSIER` | Información del dosier KODO TAKAI 2026. | Sí, como información del caso. |
| `FUENTE_CSV` | Valor copiado de la matriz de tarifas. | Sí, como dato de matriz; no necesariamente como precio final. |
| `FUENTE_JSON` | Dato del directorio municipal. | Sí, como dato del directorio; respetar sus limitaciones. |
| `FUENTE_MANUAL` | Regla escrita en el manual operativo entregado. | Sí, como política descrita en ese manual. |
| `PENDIENTE_VALIDACION` | Hay contradicción, ambigüedad o falta aprobación. | No. Informar que se requiere validación. |
| `PROPUESTA_TECNICA` | Recomendación para diseñar el sistema. | No presentarla como política empresarial. |
| `EJEMPLO_SIMULADO` | Dato creado para probar el sistema. | Nunca presentarlo como real. |

## 4. Qué hacer ante una contradicción

- No escoger el dato que parezca más probable.
- No promediar tiempos ni tarifas.
- Mostrar qué documentos no coinciden, si ayuda al usuario.
- Marcar el caso como `PENDIENTE_VALIDACION`.
- Transferir a Operaciones o al área responsable.

## 5. Fuentes por tipo de consulta

| Consulta | Fuente principal |
|---|---|
| Datos corporativos y servicios | Módulos 02 y 03, dosier |
| Precio y ruta tarifada | Módulo 04, CSV |
| Datos de municipio | Módulo 05, JSON |
| Contradicciones de fuentes | Módulo 06 |
| Mercancías peligrosas | Módulo 07, manual operativo |
| Embalaje | Módulo 08, manual operativo |
| Estado de guía | API TMS; el dosier solo describe un endpoint de ejemplo |
| PQRS | Módulo 10 y procedimiento/API cuando se entregue |
| Transferencia | Módulo 11 y condiciones del dosier |

## 6. Datos que no se deben inventar

- Tarifa final y total a pagar.
- Aplicación de flete mínimo.
- Impuestos, peajes, reexpedición o descuentos.
- ETA definitivo cuando las fuentes discrepan.
- Disponibilidad en tiempo real.
- Estado de una guía si no se consultó TMS.
- Número de ticket si no lo devolvió el sistema.
- Aprobación de mercancía peligrosa.
- Resultado de una reclamación.

## 7. Protección de información

Solicita solo los datos necesarios para la gestión. No expongas datos personales de remitentes o destinatarios a terceros. Los procedimientos de autorización, conservación y eliminación de datos están pendientes de que la empresa entregue su política de tratamiento de datos.


---

# TRANSLOGIX AI — MÓDULO 02
**Tema:** Información de la empresa  
**Versión:** 3.0  
**Fuente principal:** Dosier Completo del Reto Técnico KODO TAKAI 2026, página 1.

## 1. Identificación corporativa

| Campo | Información del dosier |
|---|---|
| Razón social | TransLogix Colombia S.A.S. |
| Nombre comercial | TransLogix Express |
| NIT | 901.684.329-8 |
| Matrícula mercantil | 00385921 |
| Cámara de Comercio | Bogotá |
| CIIU principal | 4923 — Transporte de carga por carretera |
| CIIU secundario | 5210 — Almacenamiento y depósito |
| Sede principal | Calle 26 # 96J-15, Zona Franca Fontibón, Bogotá |
| Antigüedad declarada | Más de 12 años |

**Nota:** estos datos corresponden al caso de estudio KODO TAKAI 2026. No se presentan como una verificación independiente de una sociedad real.

## 2. Hubs mencionados en el dosier

- Bogotá: Zona Franca Fontibón.
- Rionegro: centro logístico asociado a Medellín.
- Yumbo: centro logístico asociado a Cali.
- Malambo: centro logístico asociado a Barranquilla.

El directorio municipal utiliza nombres adicionales de hubs operativos. Consultar el Módulo 05 para la asignación registrada por municipio. No asumir que “centro logístico” y “hub operativo asignado” son términos equivalentes.

## 3. Flota declarada

| Tipo de vehículo | Cantidad | Uso indicado |
|---|---:|---|
| Tractocamiones S3 | 120 | Carga masiva |
| Camiones C2/C3 | 180 | Transporte intermunicipal |
| Turbos y vans | 130 | Última milla |
| Furgones termo | 50 | Cadena de frío |
| **Total** | **480** | |

La suma de las categorías es 480 unidades.

## 4. Indicadores generales

| Indicador | Valor del dosier |
|---|---:|
| Despachos mensuales | 45.000 |
| OTIF (On-Time In-Full) | 92,4 % |
| Cobertura declarada | 32 departamentos |
| Municipios cubiertos declarados | Más de 650 |

El directorio suministrado contiene 31 municipios. Es una lista parcial frente a la cobertura corporativa declarada; no representa los más de 650 municipios.

## 5. Canales de atención

| Canal | Participación |
|---|---:|
| WhatsApp Business API | 60 % |
| Web Chat | 25 % |
| PBX telefónico | 15 % |
| **Total** | **100 %** |

El dosier informa más de 18.000 interacciones diarias.

## 6. Problemas operativos descritos

| Problema | Dato del dosier |
|---|---|
| Espera en hora pico | 14,5 minutos |
| Consultas repetitivas | 78 % |
| Abandono del chat | 22 % |
| Consultas de rastreo | 55 % de las interacciones diarias |
| Búsqueda manual de una condición | 4,5 minutos promedio |
| Errores en cotizaciones manuales | 12 % |
| PQRS radicadas incompletas | 40 % |

No se informa la metodología, periodo de medición ni denominador de todos los indicadores. No calcular tendencias o proyecciones con estos valores sin datos adicionales.

## 7. Uso por la IA

Si preguntan “¿quiénes son?” o “¿qué tamaño tiene la operación?”, resumir razón social, servicios, flota e indicadores. Aclarar que son cifras del dosier del caso KODO TAKAI 2026.


---

# TRANSLOGIX AI — MÓDULO 03
**Tema:** Portafolio de servicios  
**Versión:** 3.0  
**Fuente principal:** Dosier KODO TAKAI 2026, página 1.

## 1. Transporte de carga masiva y semimasiva (FTL / LTL)

Transporte intermunicipal de:
- Contenedores de 20 pies.
- Contenedores de 40 pies.
- Carga suelta.

El dosier indica que el servicio incluye:
- Precintado de seguridad.
- Póliza de cobertura por trayecto.
- Monitoreo GPS 24/7 integrado al centro de control.

FTL y LTL son modalidades distintas. La empresa debe confirmar cuál corresponde al envío y su disponibilidad.

## 2. Paquetería empresarial y mensajería exprés

El dosier describe envíos de:
- Documentos.
- Muestras comerciales.
- Paquetes de hasta 50 kg.

El dosier presenta tiempos generales de 24 a 48 horas a nivel nacional. Sin embargo, la matriz y el directorio incluyen destinos con 72 y 96 horas. Por tanto, la IA debe consultar los módulos 04, 05 y 06 antes de informar un tiempo específico.

El dosier menciona Same Day en Bogotá, Medellín y Cali. El directorio municipal y algunas observaciones de rutas contienen otros valores; consultar el Módulo 06 y no prometer Same Day si existe discrepancia.

## 3. Almacenamiento, WMS y fulfillment e-commerce

El dosier describe:
- Gestión de inventarios mediante WMS corporativo.
- Bodegas de ambiente controlado.
- Operación en zonas francas.
- Recibo de mercancía.
- Pick & Pack.
- Etiquetado.
- Integración con Shopify, WooCommerce y VTEX.

No se entregaron tarifas, límites de almacenamiento, SLA de preparación, horarios de corte ni condiciones de integración. No inventarlos.

## 4. Transporte con cadena de frío certificada

El dosier informa:
- Flota con refrigeración multitemperatura.
- Rango indicado: -20 °C a 8 °C.
- Registrómetros digitales.
- Sectores mencionados: farmacéutico, hospitalario, biológico y alimentos perecederos.

Antes de confirmar un servicio, verificar:
1. Temperatura requerida por el producto.
2. Disponibilidad de refrigeración en el municipio.
3. Ruta y tiempo.
4. Tipo de embalaje.
5. Condiciones de conservación del producto.

El rango de la flota no significa que todos los productos puedan transportarse a cualquier temperatura dentro de ese intervalo.

## 5. Logística inversa y gestión de devoluciones

El dosier describe:
1. Recolección en punto de venta o domicilio del consumidor.
2. Inspección del estado físico.
3. Reempaque.
4. Consolidación.
5. Retorno al centro de distribución.

No se entregaron políticas de causales, costos, tiempos, autorizaciones ni reembolsos. Escalar preguntas sobre esas condiciones.

## 6. Respuesta breve sugerida

“TransLogix ofrece transporte FTL/LTL, paquetería y mensajería exprés, almacenamiento y fulfillment, transporte con cadena de frío y logística inversa. La disponibilidad, tarifa y tiempo dependen del origen, destino y tipo de mercancía.”


---

# TRANSLOGIX AI — MÓDULO 04
**Tema:** Cotizaciones y matriz de tarifas  
**Versión:** 3.0  
**Fuente principal:** `matriz_tarifas_y_fletes(1).csv` y dosier KODO TAKAI 2026, página 3.

## 1. Alcance de este módulo

La matriz contiene **25 rutas y 16 columnas**. Cada ruta tiene origen, destino, departamento, tipo de cobertura, tarifas por kg, divisor, mínimos, seguro, recargos, tiempo y observación.

Los importes están expresados en COP. Las columnas de tarifa indican valor por kg. La matriz no informa si los valores incluyen impuestos.

## 2. Datos que debe solicitar la calculadora

Para cotizar, pedir:
1. Ciudad de origen.
2. Ciudad de destino.
3. Alto en centímetros.
4. Ancho en centímetros.
5. Largo en centímetros.
6. Peso real en kilogramos.
7. Valor declarado en COP.
8. Tipo de mercancía.
9. Indicar si requiere cadena de frío o si es mercancía peligrosa.

Si la persona solo pregunta por una tarifa general, explicar qué datos hacen falta sin obligarla a completar todo de inmediato.

## 3. Fórmulas expresamente incluidas en el dosier

**Peso volumétrico:**

`peso_volumetrico_kg = (alto_cm * ancho_cm * largo_cm) / 4000`

**Peso facturable:**

`peso_facturable_kg = max(peso_real_kg, peso_volumetrico_kg)`

**Seguro según la fórmula del dosier:**

`seguro = max(0.01 * valor_declarado_COP, 2500)`

**Flete total según la fórmula del dosier:**

`flete_total = flete_base + seguro`

El dosier no especifica redondeos, decimales ni reglas de peso mínimo facturable.

## 4. Reglas tarifarias que NO están definidas

La matriz contiene estos campos, pero los archivos no explican cómo combinarlos:
- Tarifa por kg real.
- Tarifa por kg volumétrico.
- Flete mínimo.
- Seguro mínimo por ruta.
- Recargo de cadena de frío.
- Recargo de mercancía peligrosa.
- Tiempo de entrega.

Por tanto, no está confirmado:
1. Si se aplica tarifa real o volumétrica según el tipo de peso facturable.
2. Si el flete base es peso facturable × tarifa seleccionada.
3. Si el flete mínimo se aplica con `max(flete_calculado, flete_minimo)`.
4. Si el seguro mínimo de la ruta reemplaza el mínimo general de $2.500.
5. Si el porcentaje de seguro se calcula sobre valor declarado en todos los servicios.
6. Sobre qué base se calcula el recargo de cadena de frío.
7. Si el recargo de mercancía peligrosa es por envío, kg, unidad o despacho.
8. Si los recargos se acumulan.
9. Cómo se calcula reexpedición, peajes, recogida, entrega especial, impuestos y descuentos.

**Regla obligatoria:** hasta que la empresa apruebe esas reglas, la IA puede calcular peso volumétrico y mostrar los valores de la ruta, pero no debe emitir un precio final vinculante.

## 5. Diferencia entre el seguro general y el seguro por ruta

- El dosier indica 1 % del valor declarado, con mínimo de $2.500 COP.
- La matriz registra 1 % y mínimos por ruta entre $3.000 y $5.000 COP.

No se especifica cuál mínimo prevalece. No seleccionar uno automáticamente.

## 6. Matriz de rutas — valores originales

El nombre del campo original `factor_divisitivas_volumetrico` tiene un error de escritura. Se conserva el nombre fuente para trazabilidad; su valor corresponde al divisor volumétrico descrito como 4000 en el dosier.

### TLX-BOG-MED-001 — Bogotá D.C. (Cundinamarca) → Medellín (Antioquia)

- Código: `TLX-BOG-MED-001`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Medellín, Antioquia
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.450 COP/kg.
- Tarifa base por kg volumétrico: $1.600 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $18.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Ruta de alto flujo por Corredor Bogotá-Medellín. Admite Same Day si se despacha antes de las 09:00 AM.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-CLO-002 — Bogotá D.C. (Cundinamarca) → Cali (Valle del Cauca)

- Código: `TLX-BOG-CLO-002`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Cali, Valle del Cauca
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.500 COP/kg.
- Tarifa base por kg volumétrico: $1.650 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $19.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Tránsito continuo vía La Linea. Sujeto a restricciones climáticas en paso de montaña.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-BAQ-003 — Bogotá D.C. (Cundinamarca) → Barranquilla (Atlántico)

- Código: `TLX-BOG-BAQ-003`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Barranquilla, Atlántico
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.850 COP/kg.
- Tarifa base por kg volumétrico: $2.050 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $22.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.000 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $50.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 48 horas.
- Observación de ruta: Corredor Ruta del Sol / Troncal del Magdalena. Monitoreo constante de temperatura por clima cálido.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-CTG-004 — Bogotá D.C. (Cundinamarca) → Cartagena (Bolívar)

- Código: `TLX-BOG-CTG-004`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Cartagena, Bolívar
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.900 COP/kg.
- Tarifa base por kg volumétrico: $2.100 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $23.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.000 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $50.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 48 horas.
- Observación de ruta: Servicio directo a Zona Franca Mamonal y bodegas urbanas.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-BGA-005 — Bogotá D.C. (Cundinamarca) → Bucaramanga (Santander)

- Código: `TLX-BOG-BGA-005`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Bucaramanga, Santander
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.400 COP/kg.
- Tarifa base por kg volumétrico: $1.550 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $17.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Ruta activa por Cañón del Chicamocha / Barbosa. Salidas diarias nocturnas.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-PEI-006 — Bogotá D.C. (Cundinamarca) → Pereira (Risaralda)

- Código: `TLX-BOG-PEI-006`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Pereira, Risaralda
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.420 COP/kg.
- Tarifa base por kg volumétrico: $1.580 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $18.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Eje Cafetero Hub principal. Distribución regional a Manizales y Armenia.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-CUC-007 — Bogotá D.C. (Cundinamarca) → Cúcuta (Norte de Santander)

- Código: `TLX-BOG-CUC-007`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Cúcuta, Norte de Santander
- Tipo de cobertura: Frontera
- Tarifa base por kg real: $2.100 COP/kg.
- Tarifa base por kg volumétrico: $2.300 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $25.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.500 COP.
- Recargo de cadena de frío: 30%.
- Recargo de mercancía peligrosa: $60.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 48 horas.
- Observación de ruta: Zona fronteriza. Requiere manifiesto de carga detallado para inspecciones DIAN/Polfa.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-PSO-008 — Bogotá D.C. (Cundinamarca) → Pasto (Nariño)

- Código: `TLX-BOG-PSO-008`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Pasto, Nariño
- Tipo de cobertura: Frontera
- Tarifa base por kg real: $2.250 COP/kg.
- Tarifa base por kg volumétrico: $2.450 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $26.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.500 COP.
- Recargo de cadena de frío: 30%.
- Recargo de mercancía peligrosa: $60.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 72 horas.
- Observación de ruta: Corredor Sur. Restricciones frecuentes por paso de montaña y novedades viales.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-IPI-009 — Bogotá D.C. (Cundinamarca) → Ipiales (Nariño)

- Código: `TLX-BOG-IPI-009`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Ipiales, Nariño
- Tipo de cobertura: Frontera
- Tarifa base por kg real: $2.400 COP/kg.
- Tarifa base por kg volumétrico: $2.600 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $28.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $5.000 COP.
- Recargo de cadena de frío: 30%.
- Recargo de mercancía peligrosa: $65.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 72 horas.
- Observación de ruta: Punto fronterizo Rumichaca (Colombia-Ecuador). Exige declaración de tránsito internacional si aplica.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-VVC-010 — Bogotá D.C. (Cundinamarca) → Villavicencio (Meta)

- Código: `TLX-BOG-VVC-010`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Villavicencio, Meta
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.350 COP/kg.
- Tarifa base por kg volumétrico: $1.500 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $16.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $40.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Puerta a los Llanos Orientales. Sujeto a cierres preventivos en la vía al Llano.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-MED-BOG-011 — Medellín (Antioquia) → Bogotá D.C. (Cundinamarca)

- Código: `TLX-MED-BOG-011`
- Origen: Medellín, Antioquia
- Destino: Bogotá D.C., Cundinamarca
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.450 COP/kg.
- Tarifa base por kg volumétrico: $1.600 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $18.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Ruta inversa principal. Frecuencia cada 4 horas.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-MED-CLO-012 — Medellín (Antioquia) → Cali (Valle del Cauca)

- Código: `TLX-MED-CLO-012`
- Origen: Medellín, Antioquia
- Destino: Cali, Valle del Cauca
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.550 COP/kg.
- Tarifa base por kg volumétrico: $1.700 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $19.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Conexión Pacífico-Occidente. Cobertura directa.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-MED-BAQ-013 — Medellín (Antioquia) → Barranquilla (Atlántico)

- Código: `TLX-MED-BAQ-013`
- Origen: Medellín, Antioquia
- Destino: Barranquilla, Atlántico
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.750 COP/kg.
- Tarifa base por kg volumétrico: $1.950 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $21.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.000 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $50.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 48 horas.
- Observación de ruta: Corredor Antioquia - Costa Atlántica vía Caucasia/Planeta Rica.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-CLO-BOG-014 — Cali (Valle del Cauca) → Bogotá D.C. (Cundinamarca)

- Código: `TLX-CLO-BOG-014`
- Origen: Cali, Valle del Cauca
- Destino: Bogotá D.C., Cundinamarca
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.500 COP/kg.
- Tarifa base por kg volumétrico: $1.650 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $19.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Salida Hub Yumbo / Palmira hacia el centro del país.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-CLO-BUN-015 — Cali (Valle del Cauca) → Buenaventura (Valle del Cauca)

- Código: `TLX-CLO-BUN-015`
- Origen: Cali, Valle del Cauca
- Destino: Buenaventura, Valle del Cauca
- Tipo de cobertura: Trayecto Especial
- Tarifa base por kg real: $1.300 COP/kg.
- Tarifa base por kg volumétrico: $1.450 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $17.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $55.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Corredor Portuario. Manejo de carga de importación/exportación y contenedores sueltos.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BAQ-SMR-016 — Barranquilla (Atlántico) → Santa Marta (Magdalena)

- Código: `TLX-BAQ-SMR-016`
- Origen: Barranquilla, Atlántico
- Destino: Santa Marta, Magdalena
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.100 COP/kg.
- Tarifa base por kg volumétrico: $1.250 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $15.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.000 COP.
- Recargo de cadena de frío: 20%.
- Recargo de mercancía peligrosa: $40.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Vía Ciénaga / Troncal del Caribe. Servicio Same Day disponible.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BAQ-CTG-017 — Barranquilla (Atlántico) → Cartagena (Bolívar)

- Código: `TLX-BAQ-CTG-017`
- Origen: Barranquilla, Atlántico
- Destino: Cartagena, Bolívar
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.150 COP/kg.
- Tarifa base por kg volumétrico: $1.300 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $15.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.000 COP.
- Recargo de cadena de frío: 20%.
- Recargo de mercancía peligrosa: $40.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Vía al Mar / Cordialidad. Conexión interportuaria diaria.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BGA-CUC-018 — Bucaramanga (Santander) → Cúcuta (Norte de Santander)

- Código: `TLX-BGA-CUC-018`
- Origen: Bucaramanga, Santander
- Destino: Cúcuta, Norte de Santander
- Tipo de cobertura: Frontera
- Tarifa base por kg real: $1.600 COP/kg.
- Tarifa base por kg volumétrico: $1.800 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $20.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.000 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $50.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Tránsito por Páramo de Berlín. Exige embalaje térmico para productos sensibles.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-PEI-MZL-019 — Pereira (Risaralda) → Manizales (Caldas)

- Código: `TLX-PEI-MZL-019`
- Origen: Pereira, Risaralda
- Destino: Manizales, Caldas
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.050 COP/kg.
- Tarifa base por kg volumétrico: $1.200 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $14.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.000 COP.
- Recargo de cadena de frío: 20%.
- Recargo de mercancía peligrosa: $35.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Conurbación Eje Cafetero. Entregas express intradía.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-NVA-020 — Bogotá D.C. (Cundinamarca) → Neiva (Huila)

- Código: `TLX-BOG-NVA-020`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Neiva, Huila
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.500 COP/kg.
- Tarifa base por kg volumétrico: $1.680 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $18.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $3.500 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $45.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 24 horas.
- Observación de ruta: Ruta Sur vía Girardot / Espinal. Cobertura completa al Huila.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-FLA-021 — Bogotá D.C. (Cundinamarca) → Florencia (Caquetá)

- Código: `TLX-BOG-FLA-021`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Florencia, Caquetá
- Tipo de cobertura: Zona ZOMAC
- Tarifa base por kg real: $2.350 COP/kg.
- Tarifa base por kg volumétrico: $2.550 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $27.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.500 COP.
- Recargo de cadena de frío: 30%.
- Recargo de mercancía peligrosa: $65.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 72 horas.
- Observación de ruta: Puerta de la Amazonía. Trayecto ZOMAC con frecuencia de despacho 3 veces por semana.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-MTR-022 — Bogotá D.C. (Cundinamarca) → Montería (Córdoba)

- Código: `TLX-BOG-MTR-022`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Montería, Córdoba
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.800 COP/kg.
- Tarifa base por kg volumétrico: $1.980 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $21.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.000 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $50.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 48 horas.
- Observación de ruta: Conexión agroindustrial del Caribe colombiano.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-VAL-023 — Bogotá D.C. (Cundinamarca) → Valledupar (Cesar)

- Código: `TLX-BOG-VAL-023`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Valledupar, Cesar
- Tipo de cobertura: Urbana Principal
- Tarifa base por kg real: $1.850 COP/kg.
- Tarifa base por kg volumétrico: $2.020 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $22.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.000 COP.
- Recargo de cadena de frío: 25%.
- Recargo de mercancía peligrosa: $50.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 48 horas.
- Observación de ruta: Ruta Bosconia / Valledupar. Enlace con Guajira.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-RIO-024 — Bogotá D.C. (Cundinamarca) → Riohacha (La Guajira)

- Código: `TLX-BOG-RIO-024`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Riohacha, La Guajira
- Tipo de cobertura: Trayecto Especial
- Tarifa base por kg real: $2.200 COP/kg.
- Tarifa base por kg volumétrico: $2.400 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $25.500 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $4.500 COP.
- Recargo de cadena de frío: 30%.
- Recargo de mercancía peligrosa: $60.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 72 horas.
- Observación de ruta: Extremo norte de Colombia. Exige embalaje resistente al polvo y altas temperaturas.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.

### TLX-BOG-QUI-025 — Bogotá D.C. (Cundinamarca) → Quibdó (Chocó)

- Código: `TLX-BOG-QUI-025`
- Origen: Bogotá D.C., Cundinamarca
- Destino: Quibdó, Chocó
- Tipo de cobertura: Zona ZOMAC
- Tarifa base por kg real: $2.650 COP/kg.
- Tarifa base por kg volumétrico: $2.850 COP/kg.
- Divisor volumétrico: 4000.
- Flete mínimo registrado: $30.000 COP.
- Porcentaje de seguro: 1%.
- Seguro mínimo registrado: $5.000 COP.
- Recargo de cadena de frío: 35%.
- Recargo de mercancía peligrosa: $75.000 COP. La unidad o base de aplicación no está definida.
- Tiempo estimado en la matriz: 96 horas.
- Observación de ruta: Zona de difícil acceso por condición de vías. Despachos programados los días martes y viernes.

**Regla para la IA:** esta ficha entrega valores de la matriz, no una cotización final. No sumar ni aplicar mínimos o recargos hasta que la empresa confirme la fórmula comercial.


## 7. Ejemplo de cálculo que sí puede hacer la IA

Si la caja mide 40 × 30 × 50 cm:

`40 * 30 * 50 / 4000 = 15 kg`

El peso volumétrico es 15 kg. Para determinar el peso facturable aún se necesita el peso real:

- Si el peso real es 10 kg, el mayor es 15 kg.
- Si el peso real es 20 kg, el mayor es 20 kg.

Este ejemplo no determina el flete ni el seguro.

## 8. Respuesta modelo cuando falta información tarifaria

“Encontré la ruta y sus valores en la matriz. El peso volumétrico es [X] kg y el peso facturable preliminar es [Y] kg. Para confirmar el precio final debo validar la aplicación del flete mínimo, el seguro por ruta y los recargos. No quiero darte un valor incorrecto.”

## 9. Control de versión

Fuente: `matriz_tarifas_y_fletes(1).csv`, 25 registros, 16 campos. Si se actualiza el CSV, regenerar este módulo y revisar el Módulo 06.


---

# TRANSLOGIX AI — MÓDULO 05
**Tema:** Directorio de cobertura y tiempos  
**Versión:** 3.0  
**Fuente principal:** `directorio_cobertura_y_tiempos(1).json`.

## 1. Alcance

El archivo JSON contiene **31 registros municipales**. El dosier declara cobertura de 32 departamentos y más de 650 municipios. Por tanto, este JSON es un directorio parcial, no el listado nacional completo.

## 2. Cómo consultar cobertura

1. Identificar el municipio exacto y el departamento.
2. Buscarlo en este directorio.
3. Informar el tipo de cobertura y tiempo estándar del registro.
4. Revisar Same Day y servicio refrigerado.
5. Informar frecuencia y restricciones.
6. Para precio, verificar que exista una ruta en el Módulo 04.
7. Si el tiempo de la ruta y el del municipio no coinciden, consultar el Módulo 06 y escalar.

La presencia de un municipio en el directorio no significa que exista una tarifa desde cualquier ciudad de origen.

## 3. Resumen calculado del archivo

- Municipios registrados: 31.
- Registros con Same Day marcado como disponible: 11.
- Registros con servicio refrigerado marcado como disponible: 28.
- Registros sin servicio refrigerado: Ipiales, Florencia, Quibdó.

| Tiempo estándar en JSON | Número de municipios |
|---:|---:|
| 24 horas | 18 |
| 48 horas | 8 |
| 72 horas | 4 |
| 96 horas | 1 |

## 4. Advertencia sobre peso máximo

El campo `peso_maximo_paquete_kg` registra valores entre 500 y 3000 kg. El dosier de negocio dice que la paquetería maneja paquetes de hasta 50 kg.

No se debe interpretar el valor municipal como límite por paquete hasta que Operaciones aclare si corresponde a:
- Peso máximo de paquete.
- Peso máximo por despacho.
- Capacidad de vehículo.
- Capacidad de recepción del hub.

Mantener el valor fuente, pero marcarlo como `PENDIENTE_VALIDACION`.

## 5. Directorio municipal completo

### Bogotá D.C. — Cundinamarca

- Código DANE: `11001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 45.0 m³.
- Hub asignado: Hub Central Zona Franca Fontibón.
- Frecuencia de despacho: Continuo 24/7.
- Restricción operativa: Restricción de movilidad para vehículos de carga pesada en zonas urbanas según horario de Pico y Placa ambiental.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Medellín — Antioquia

- Código DANE: `05001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 40.0 m³.
- Hub asignado: Hub Regional Itagüí - Antioquia.
- Frecuencia de despacho: Continuo (4 salidas diarias).
- Restricción operativa: Restricción de ingreso al centro urbano para camiones de más de 2 ejes entre 06:00 y 20:00.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Envigado — Antioquia

- Código DANE: `05266`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Regional Itagüí - Antioquia.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Acceso restringido en zonas residenciales montañosas para vehículos superiores a 5 toneladas.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Itagüí — Antioquia

- Código DANE: `05837`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 45.0 m³.
- Hub asignado: Hub Regional Itagüí - Antioquia.
- Frecuencia de despacho: Continuo 24/7.
- Restricción operativa: Zona industrial con libre circulación de vehículos pesados.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Bello — Antioquia

- Código DANE: `05088`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Regional Itagüí - Antioquia.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Tránsito denso en autopista Norte en horas pico.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Rionegro — Antioquia

- Código DANE: `05615`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 35.0 m³.
- Hub asignado: Sub-Hub Aeropuerto José María Córdova.
- Frecuencia de despacho: Diaria (3 turnos).
- Restricción operativa: Conexión estratégica para carga aérea y zonas francas del Oriente antioqueño.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Cali — Valle del Cauca

- Código DANE: `76001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 40.0 m³.
- Hub asignado: Hub Regional Yumbo - Valle.
- Frecuencia de despacho: Continuo (4 salidas diarias).
- Restricción operativa: Control de emisión de gases estricto y pico y placa comercial.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Yumbo — Valle del Cauca

- Código DANE: `76892`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 3000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 50.0 m³.
- Hub asignado: Hub Regional Yumbo - Valle.
- Frecuencia de despacho: Continuo 24/7.
- Restricción operativa: Zona industrial principal sin restricción de tonelaje.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Palmira — Valle del Cauca

- Código DANE: `76520`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Regional Yumbo - Valle.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Atención especializada a ingenios azucareros y sector agroindustrial.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Buenaventura — Valle del Cauca

- Código DANE: `76109`
- Tipo de cobertura: Trayecto Especial
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 3000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 50.0 m³.
- Hub asignado: Nodo Portuario Buenaventura.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Requiere cita previa de ingreso a terminales portuarias (SPRBUN, Aguadulce, TCBUEN).

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Barranquilla — Atlántico

- Código DANE: `08001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 40.0 m³.
- Hub asignado: Hub Caribe Barranquilla (Zona Galapa).
- Frecuencia de despacho: Continuo (3 salidas diarias).
- Restricción operativa: Condiciones climáticas de alta humedad; requiere almacenamiento en bodegas climatizadas.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Soledad — Atlántico

- Código DANE: `08758`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Caribe Barranquilla (Zona Galapa).
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Zona urbana con congestión vial en horas pico.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Cartagena — Bolívar

- Código DANE: `13001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 45.0 m³.
- Hub asignado: Sub-Hub Mamonal Cartagena.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Restricción de paso de carga pesada por el Centro Histórico y Bocagrande.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Santa Marta — Magdalena

- Código DANE: `47001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Caribe Barranquilla (Zona Galapa).
- Frecuencia de despacho: Diaria (1 turno nocturno).
- Restricción operativa: Control ambiental estricto por proximidad a parque nacional Sierra Nevada.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Bucaramanga — Santander

- Código DANE: `68001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1800 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 35.0 m³.
- Hub asignado: Hub Nororiente Girón - Santander.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Geografía accidentada; entregas de última milla prioritarias en vehículos tipo van/turbo.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Floridablanca — Santander

- Código DANE: `68276`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1200 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 25.0 m³.
- Hub asignado: Hub Nororiente Girón - Santander.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Zona residencial y universitaria; restricciones para camiones mayores a 3.5 toneladas.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Girón — Santander

- Código DANE: `68547`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 45.0 m³.
- Hub asignado: Hub Nororiente Girón - Santander.
- Frecuencia de despacho: Continuo 24/7.
- Restricción operativa: Centro logístico e industrial del área metropolitana de Bucaramanga.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Pereira — Risaralda

- Código DANE: `66001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1800 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 35.0 m³.
- Hub asignado: Hub Eje Cafetero Dosquebradas.
- Frecuencia de despacho: Diaria (3 turnos).
- Restricción operativa: Punto neurálgico de distribución interdepartamental en el Eje Cafetero.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Dosquebradas — Risaralda

- Código DANE: `66170`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: Sí.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 45.0 m³.
- Hub asignado: Hub Eje Cafetero Dosquebradas.
- Frecuencia de despacho: Continuo 24/7.
- Restricción operativa: Ubicación de bodegas principales de almacenamiento y consolidación.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Manizales — Caldas

- Código DANE: `17001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Eje Cafetero Dosquebradas.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Topografía empinada; requiere flota especializada con tracción 4x2 reforzada y freno de ahogo.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Armenia — Quindío

- Código DANE: `63001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Eje Cafetero Dosquebradas.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Operación regular sin novedades especiales de movilidad.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Cúcuta — Norte de Santander

- Código DANE: `54001`
- Tipo de cobertura: Frontera
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 40.0 m³.
- Hub asignado: Nodo Fronterizo Cúcuta.
- Frecuencia de despacho: Diaria (1 turno).
- Restricción operativa: Inspecciones aduaneras DIAN/POLFA frecuentes en vías de acceso.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Pasto — Nariño

- Código DANE: `52001`
- Tipo de cobertura: Frontera
- Tiempo estándar del directorio: 72 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Nodo Sur Pasto.
- Frecuencia de despacho: Interdiaria (Lunes, Miércoles, Viernes).
- Restricción operativa: Sujeto a eventuales derrumbes o cierres en la vía Panamericana.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Ipiales — Nariño

- Código DANE: `52356`
- Tipo de cobertura: Frontera
- Tiempo estándar del directorio: 72 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: No.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Nodo Sur Pasto.
- Frecuencia de despacho: Interdiaria (Lunes, Miércoles, Viernes).
- Restricción operativa: Paso fronterizo Rumichaca. Validación de guías de carga internacional.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Villavicencio — Meta

- Código DANE: `50001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 2000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 35.0 m³.
- Hub asignado: Sub-Hub Llanos Villavicencio.
- Frecuencia de despacho: Diaria (2 turnos).
- Restricción operativa: Sujeto a cierres preventivos en la Vía al Llano por desprendimiento de tierra.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Neiva — Huila

- Código DANE: `41001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 24 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1800 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Sur Neiva.
- Frecuencia de despacho: Diaria (1 turno).
- Restricción operativa: Clima cálido extremo; exigencia de empaque protector para insumos sensibles al calor.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Florencia — Caquetá

- Código DANE: `18001`
- Tipo de cobertura: Zona ZOMAC / Difícil Acceso
- Tiempo estándar del directorio: 72 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: No.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 800 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 15.0 m³.
- Hub asignado: Hub Sur Neiva.
- Frecuencia de despacho: Semanal (Martes y Jueves).
- Restricción operativa: Zona ZOMAC. Vías secundarias con restricciones durante temporada invernal.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Montería — Córdoba

- Código DANE: `23001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Caribe Barranquilla (Zona Galapa).
- Frecuencia de despacho: Diaria (1 turno nocturno).
- Restricción operativa: Atención a sectores ganaderos y agroindustriales del Sinú.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Valledupar — Cesar

- Código DANE: `20001`
- Tipo de cobertura: Urbana Principal
- Tiempo estándar del directorio: 48 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 30.0 m³.
- Hub asignado: Hub Caribe Barranquilla (Zona Galapa).
- Frecuencia de despacho: Diaria (1 turno nocturno).
- Restricción operativa: Punto de distribución hacia la alta y baja Guajira.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Riohacha — La Guajira

- Código DANE: `44001`
- Tipo de cobertura: Trayecto Especial
- Tiempo estándar del directorio: 72 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: Sí.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 1000 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 20.0 m³.
- Hub asignado: Nodo La Guajira Riohacha.
- Frecuencia de despacho: Interdiaria (Lunes, Miércoles, Viernes).
- Restricción operativa: Altas temperaturas y polvo; empaque antipolvo industrial obligatorio.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.

### Quibdó — Chocó

- Código DANE: `27001`
- Tipo de cobertura: Zona ZOMAC / Difícil Acceso
- Tiempo estándar del directorio: 96 horas.
- Same Day según directorio: No.
- Servicio refrigerado según directorio: No.
- Peso máximo registrado (`peso_maximo_paquete_kg`): 500 kg. **Campo pendiente de aclaración**, porque el dosier general habla de paquetes de hasta 50 kg.
- Volumen máximo registrado: 10.0 m³.
- Hub asignado: Hub Regional Itagüí - Antioquia.
- Frecuencia de despacho: Semanal (Martes y Viernes).
- Restricción operativa: Vía terrestre de alto riesgo climático. Entregas sujetas a estado de la vía Ciudad Bolívar - Quibdó.

**Regla para la IA:** el dato de este registro describe el municipio. No confirma por sí solo que exista una ruta tarifada desde cualquier origen.


## 6. Reglas de respuesta

- Decir “el directorio registra” cuando se comunique un dato del JSON.
- No asegurar que un municipio no listado carece de servicio; puede estar cubierto en el universo nacional no entregado.
- No prometer tiempos garantizados: los archivos hablan de tiempos estimados/estándar.
- Informar restricciones de vía, clima, acceso, terminales y frecuencia cuando sean relevantes.
- No inferir servicio refrigerado de la existencia de recargo de frío en la matriz.


---

# TRANSLOGIX AI — MÓDULO 06
**Tema:** Diferencias y contradicciones entre fuentes  
**Versión:** 3.0  
**Estado:** Documento de control. No usar para cotizar ni prometer servicios.

## 1. Objetivo

Este módulo evita que la IA resuelva contradicciones por intuición. Cuando dos archivos entregan valores distintos, la IA debe informar que se requiere validación.

## 2. Diferencias de tiempo entre matriz y directorio

La matriz contiene tiempos por trayecto. El JSON contiene tiempos estándar por municipio de destino. Se encontraron 4 diferencias:

| Código de ruta | Trayecto | Matriz CSV | Directorio JSON | Acción |
|---|---|---:|---:|---|
| `TLX-CLO-BUN-015` | Cali → Buenaventura | 24 h | 48 h | No elegir automáticamente. Validar con Operaciones. |
| `TLX-BAQ-SMR-016` | Barranquilla → Santa Marta | 24 h | 48 h | No elegir automáticamente. Validar con Operaciones. |
| `TLX-BAQ-CTG-017` | Barranquilla → Cartagena | 24 h | 48 h | No elegir automáticamente. Validar con Operaciones. |
| `TLX-BGA-CUC-018` | Bucaramanga → Cúcuta | 24 h | 48 h | No elegir automáticamente. Validar con Operaciones. |

No promediar los tiempos ni escoger automáticamente el más corto o el más largo.

## 3. Diferencias sobre Same Day

- El dosier dice que Same Day está disponible en Bogotá, Medellín y Cali.
- El directorio marca Same Day en 11 municipios: Bogotá D.C., Medellín, Envigado, Itagüí, Bello, Cali, Yumbo, Barranquilla, Soledad, Pereira, Dosquebradas.
- La observación de la ruta `TLX-BOG-MED-001` dice que admite Same Day si se despacha antes de las 09:00 AM.
- La observación de `TLX-BAQ-SMR-016` dice que hay Same Day Barranquilla–Santa Marta.
- El directorio de Santa Marta marca Same Day como No.

**Acción:** no prometer Same Day fuera de la información que Operaciones confirme. Validar también hora de corte, días de servicio y cobertura por dirección.

## 4. Diferencias sobre tiempos nacionales

- El dosier describe paquetería con entrega de 24 a 48 horas a nivel nacional.
- La matriz y el directorio incluyen trayectos o destinos de 72 y 96 horas.

**Acción:** tratar 24–48 horas como descripción general del dosier, no como promesa universal. Consultar la ruta y municipio concretos.

## 5. Diferencias sobre peso

- Dosier: paquetes de hasta 50 kg.
- JSON: `peso_maximo_paquete_kg` registra valores entre 500 y 3000 kg.

**Acción:** no mostrar esos valores como peso permitido por paquete hasta que la empresa aclare la unidad operativa del campo.

## 6. Diferencias sobre seguro

- Dosier: seguro del 1 % del valor declarado, mínimo $2.500 COP.
- CSV: porcentaje 1 % y seguro mínimo por ruta entre $3.000 y $5.000 COP.

**Acción:** falta una regla de precedencia. No calcular seguro final automático.

## 7. Diferencias internas en el manual de mercancías peligrosas

### 7.1 Ácido clorhídrico

- La sección Clase 8 permite líquidos corrosivos en envases de hasta 5 litros en paquetería y exige caja de doble pared.
- El ejemplo de atención RAG habla de máximo 5 litros por caja, bolsa calibre 4 y otros detalles que no aparecen todos en la regla específica de Clase 8.

**Acción:** no reutilizar el ejemplo como política definitiva. Solicitar aclaración a Operaciones sobre si el límite es por envase o por caja y cuál es el embalaje exacto para corrosivos.

### 7.2 Equipos electrónicos y baterías

- La sección de embalaje dice retirar baterías o bloquear físicamente el botón de encendido.
- La sección Clase 9 dice que teléfonos, computadores y herramientas con batería instalada (ONU 3481) son aceptados bajo la política descrita.

**Acción:** aclarar que la instrucción de embalaje no debe interpretarse como obligación de retirar una batería integrada. Validar con Operaciones la aplicación por tipo de equipo.

### 7.3 Clase 2.1

El manual habla de vehículos certificados con “blindaje de tanque” y plan de contingencia. La terminología y el requisito deben ser revisados por el responsable técnico antes de automatizar una aprobación.

## 8. Diferencias entre centros logísticos y hubs

- El dosier nombra centros en Rionegro, Yumbo y Malambo.
- El JSON asigna hubs como Itagüí, Dosquebradas, Galapa, Girón, entre otros.

Puede tratarse de centros físicos, hubs de distribución o nodos operativos distintos. No asumir que son equivalentes ni que un dato invalida el otro.

## 9. Diferencias jurídicas del módulo PQRS

- El dosier menciona 10 días hábiles para reclamaciones por pérdida o avería y cita Ley 1480 de 2011 y artículo 1028 del Código de Comercio.
- Esa afirmación debe ser revisada por Jurídica antes de convertirse en plazo automático para clientes.
- La versión anterior de la base agregó referencias a plazos de 3 días y 15 días que no están explicadas en los archivos originales entregados en esta actualización. No deben presentarse como política aprobada a partir de estos documentos.

## 10. Regla general

Ante cualquier diferencia:
1. No elegir un valor por intuición.
2. No inventar una regla de prioridad.
3. Registrar la fuente A y la fuente B.
4. Informar que el dato requiere validación.
5. Escalar al responsable correspondiente.


---

# TRANSLOGIX AI — MÓDULO 07
**Tema:** Mercancías peligrosas y restricciones de carga  
**Versión:** 3.0  
**Fuente principal:** `manual_de_mercanc_as_peligrosas_y_embalaje(1).md`, código DOC-OPS-2026-03.

## 1. Regla general

La clasificación de una mercancía debe basarse en su Hoja de Datos de Seguridad (HDS/MSDS), composición, número ONU, clase, concentración, cantidad, envase y modalidad de transporte.

No clasificar un producto únicamente por su nombre comercial. Si falta la HDS o no se identifica con certeza, no autorizar el envío y escalar a Operaciones.

Las políticas siguientes reproducen el manual interno entregado para el caso. No sustituyen la revisión normativa ni la aprobación operativa.

## 2. Marco normativo mencionado por el manual

- Decreto 1079 de 2015, en particular la sección sobre transporte terrestre automotor de mercancías peligrosas por carretera.
- Decreto 1609 de 2002: el Ministerio de Transporte explica que sus disposiciones fueron compiladas en la Sección 8 del Capítulo 7, Título 1, Parte 2, Libro 2 del Decreto 1079 de 2015. No tratar ambos textos como dos regímenes independientes sin revisar la compilación.
- NTC 1692: clasificación, etiquetado y rotulado.
- NTC 4532: tarjetas de emergencia para transporte automotor.
- NTC 4435: hojas de datos de seguridad en 16 secciones.

La vigencia, modificación y aplicabilidad actual debe revisarse en la versión consolidada del Decreto 1079 y con el responsable jurídico/técnico. El Ministerio de Transporte mantiene un portal específico de mercancías peligrosas; consultar el Módulo 17.

## 3. Clases de mercancías peligrosas

### Clase 1 — Explosivos
**Política del manual: PROHIBIDO en su totalidad.**

No transportar fuegos artificiales, municiones, detonadores, dinamita ni pólvora negra en FTL, LTL o paquetería.

### Clase 2 — Gases comprimidos, licuados o disueltos a presión

**Subclase 2.1 — Gas inflamable**
- Ejemplos del manual: propano, butano y acetileno.
- Política: aceptado únicamente en FTL.
- Condiciones descritas: vehículos certificados con blindaje de tanque y plan de contingencia avalado por el Ministerio de Transporte.
- Prohibido en paquetería exprés.
- Requiere revisión del Comité/Operaciones antes de cualquier aceptación.

**Subclase 2.2 — Gas no inflamable y no tóxico**
- Ejemplos: nitrógeno líquido, oxígeno comprimido y argón.
- Requiere revisión previa de la HDS.
- Los cilindros deben tener prueba hidrostática vigente con antigüedad menor a 5 años.

**Subclase 2.3 — Gas tóxico por inhalación**
- Ejemplos: cloro y fosgeno.
- Estado: restringido.
- Requiere aprobación del Comité Operativo y custodia de escolta vehicular.

### Clase 3 — Líquidos inflamables
- El manual describe esta clase como líquidos con punto de inflamación inferior a 60,5 °C.
- FTL: hasta 15.000 litros en cisterna o tambores certificados de 55 galones UN 1A1, según condiciones del manual.
- Paquetería LTL: envases metálicos o de HDPE de máximo 1 litro por envase, dentro de caja máster con vermiculita u otro absorbente inerte y rotulado Clase 3.
- El manual establece un punto de inflamación mínimo admitido en paquetería de 23 °C.

No autorizar por el solo hecho de que el envase cumpla el volumen. Revisar HDS, número ONU, grupo de embalaje, modalidad y aprobación operativa.

### Clase 4 — Sólidos inflamables

**Subclase 4.1**
- Ejemplos: azufre, fósforos y virutas de magnesio.
- Política del manual: aceptados en empaques sellados al vacío.
- Requiere revisión de Operaciones.

**Subclase 4.2**
- Ejemplos: carbón activado y fósforo blanco.
- Prohibido en paquetería.
- Solo FTL especializado según el manual.

**Subclase 4.3**
- Ejemplos: sodio y potasio metálico.
- Prohibido.

### Clase 5 — Comburentes y peróxidos orgánicos

**Subclase 5.1 — Comburentes**
- Ejemplos: nitrato de amonio y peróxido de hidrógeno mayor al 20 %.
- Aceptación condicionada.
- Estibar separado de líquidos inflamables.

**Subclase 5.2 — Peróxidos orgánicos**
- Requieren control constante de temperatura.
- El manual indica transporte solo en flota certificada de cadena de frío.

### Clase 6 — Sustancias tóxicas e infecciosas

**Subclase 6.1 — Sustancias tóxicas/venenosas**
- Ejemplos: plaguicidas, cianuro y plomo.
- El manual permite bajo embalaje primario hermético.
- No consolidar en la misma unidad de transporte con alimentos, medicinas o cosméticos.

**Subclase 6.2 — Sustancias infecciosas/biológicas**
- Aceptado según el manual: únicamente muestras biológicas de diagnóstico en triple contenedor conforme a P650.
- Prohibido: residuos biológicos peligrosos y material infeccioso Categoría A ONU 2814.
- Validar clasificación, embalaje y aplicabilidad de P650 antes de aceptar.

### Clase 7 — Material radiactivo
**Política del manual: PROHIBIDO ABSOLUTAMENTE** en la red TransLogix Express.

### Clase 8 — Sustancias corrosivas
- Ejemplos: ácido sulfúrico, ácido clorhídrico/muriático, hidróxido de sodio/soda cáustica y baterías húmedas de plomo-ácido.
- Baterías automotrices húmedas: guacal plástico antifugas y bornes aislados con cinta dieléctrica.
- Líquidos corrosivos en paquetería: el manual menciona envases de máximo 5 litros y caja exterior de cartón corrugado de doble pared (7 capas).
- El manual no define con claridad si existe un límite total por caja o envío. Ver Módulo 06.

### Clase 9 — Sustancias y objetos peligrosos diversos

**Baterías de litio ONU 3480 / ONU 3481**
- Batería instalada en teléfono, computador o herramienta (ONU 3481): el manual dice que se acepta sin recargo.
- Batería suelta (ONU 3480): proteger terminales contra cortocircuitos y colocar etiqueta de batería de litio con número telefónico de emergencia.
- La aceptación debe revisarse con la clasificación y los requisitos aplicables. No asumir que “sin recargo” significa sin controles.

## 4. Documentación obligatoria indicada por el manual

Para cualquier despacho con mercancías peligrosas o sustancias químicas, el remitente debe entregar los documentos antes del cargue:

### 4.1 Hoja de Datos de Seguridad (HDS/MSDS)
- En español.
- Con 16 secciones.
- El manual exige que la revisión/actualización no supere 3 años.
- Secciones que el manual destaca para la revisión: 9 (propiedades físicas y químicas), 14 (información de transporte, número ONU y clase) y 15 (información reglamentaria).

### 4.2 Tarjeta de emergencia
- Conforme a NTC 4532, según el manual.
- Impresa a color y disponible en la cabina.
- El manual incluye estos contactos:
  - CISPROQUIM: 01 8000 916 012.
  - Bogotá: +57 601 288 6012.
- Incluye primeros auxilios y acciones ante derrame o incendio.

### 4.3 Manifiesto y remesa
- Manifiesto de carga / remesa terrestre de carga (RNDC), según el manual.
- El manual indica que lo expide TransLogix y que está interconectado con el Ministerio de Transporte.

## 5. Artículos expresamente prohibidos

El manual dice que estos productos no serán recibidos ni transportados bajo ninguna circunstancia:

1. Dinero en efectivo, monedas, billetes, títulos valores, cheques al portador y lingotes de oro o plata.
2. Armas de fuego, piezas de armamento, municiones, silenciadores, armas neumáticas, pistolas de fogueo y armas blancas de combate.
3. Estupefacientes, drogas ilícitas, sustancias psicotrópicas e insumos químicos controlados sin salvoconducto legal.
4. Restos humanos, cenizas de cremación y cadáveres animales.
5. Animales vivos: mamíferos, aves, reptiles, insectos y peces.
6. Joyas de alto valor, gemas preciosas sueltas y obras de arte de patrimonio nacional no aseguradas.
7. Explosivos, fuegos pirotécnicos, pólvora, nitroglicerina y mechas de ignición.
8. Material radiactivo de cualquier tipo.
9. Mercancías de contrabando o que incumplan requisitos legales de importación.

## 6. Respuesta de la IA ante un producto restringido

La IA debe:
1. Pedir HDS, número ONU, concentración, cantidad y modalidad cuando la clasificación no sea clara.
2. Explicar la condición del manual sin garantizar aceptación.
3. No indicar cómo ocultar, cambiar etiquetas o evadir controles.
4. No autorizar la mercancía.
5. Transferir a Operaciones cuando la política indique aceptación condicionada o restringida.

## 7. Advertencia de seguridad

Este módulo resume un manual de caso. Las mercancías peligrosas requieren revisión por personal competente y verificación de normativa vigente. La IA no sustituye la aprobación técnica ni documental.


---

# TRANSLOGIX AI — MÓDULO 08
**Tema:** Estándares de embalaje  
**Versión:** 3.0  
**Fuente principal:** Manual DOC-OPS-2026-03, sección 4.

## 1. Responsabilidad del embalaje

El manual indica que el cliente/remitente es responsable de entregar la mercancía debidamente embalada para resistir:
- Vibración durante el transporte.
- Frenado de emergencia.
- Inclinación.
- Apilamiento.
- Condiciones de las vías.

La IA debe explicar los requisitos del manual, pero no certificar que un embalaje es seguro solo a partir de una descripción breve o una fotografía.

## 2. Estructura general recomendada

El esquema del manual contiene:
1. Caja máster exterior de cartón corrugado de doble pared.
2. Material de amortiguación, como burbuja o vermiculita, según el producto.
3. Contenedor primario hermético de vidrio o plástico, cuando corresponda.

El embalaje se debe adaptar al tipo de mercancía. No usar un mismo esquema para mercancía común y mercancía peligrosa.

## 3. Productos frágiles

Ejemplos: vidrio, cerámica e instrumentos de medición.

Requisitos del manual:
1. Aplicar sistema “caja dentro de caja”.
2. Envolver cada producto individualmente con plástico burbuja de al menos 3 cm de espesor.
3. Dejar mínimo 5 cm entre el producto y las paredes internas de la caja exterior.
4. Rellenar espacios libres con maní de poliestireno (Esporflex) o espuma inyectada.
5. Usar cinta roja con la leyenda “FRÁGIL - MANEJE CON CUIDADO”.
6. Incluir flechas “ESTE LADO ARRIBA”.

## 4. Líquidos y fluidos no peligrosos

Ejemplos: cosméticos, aceites comestibles y bebidas.

Requisitos del manual:
1. Sellar la tapa rosca con termoencogible o cinta de seguridad contra manipulación.
2. Introducir envases de vidrio o plástico delgado en bolsa plástica calibre 4, sellada herméticamente.
3. Colocar absorbente en la parte inferior de la caja.
4. El absorbente debe poder retener el 100 % del volumen del líquido si ocurre una rotura.

**Importante:** esta sección se refiere a líquidos no peligrosos. No aplicar automáticamente estas instrucciones a corrosivos, inflamables u otras mercancías peligrosas.

## 5. Alimentos perecederos y medicamentos refrigerados

El manual indica:
- Rango de conservación: -20 °C a 8 °C.
- Nevera interior de poliestireno expandido (icopor industrial).
- Paredes de mínimo 30 mm.
- Ice Packs precongelados a -18 °C.
- Ubicar refrigerantes en la parte superior y laterales.
- No poner congelantes directamente sobre medicamentos sensibles a la congelación.
- Introducir la nevera en caja de cartón corrugado exterior.
- Conservación pasiva indicada: hasta 48 horas.

Antes de prometer transporte:
1. Confirmar la temperatura exigida por el fabricante.
2. Confirmar disponibilidad de servicio refrigerado en el destino.
3. Confirmar ruta y tiempo.
4. Confirmar que el embalaje corresponde al producto.
5. Validar con Operaciones la capacidad real de mantener la temperatura durante el trayecto.

El rango de la flota no significa que todos los productos soporten todas las temperaturas del rango.

## 6. Equipos electrónicos y maquinaria de precisión

Ejemplos: laptops, servidores y celulares.

Requisitos del manual:
1. Envolver el equipo en bolsa antiestática rosa o metalizada (Shielding Bag).
2. Proteger las ocho esquinas con esquineras de espuma EPE de alta densidad.
3. Retirar baterías o asegurar el botón de encendido con bloqueo físico para evitar activación accidental.

**Contradicción pendiente:** el mismo manual dice que equipos con batería de litio instalada (ONU 3481) son aceptados. No interpretar que todas las baterías integradas deban retirarse. Consultar Módulo 06 y validar con Operaciones.

## 7. Preguntas frecuentes de embalaje

**¿Cómo empaco un vaso o una pieza de vidrio?**  
Envolver individualmente, usar caja dentro de caja, mantener 5 cm de separación, rellenar espacios y marcar como frágil.

**¿Puedo enviar un líquido en una botella?**  
Primero se debe identificar si es peligroso. Para líquidos no peligrosos, seguir el procedimiento de la sección 4. Para químicos, consultar el Módulo 07.

**¿Puedo enviar medicamentos refrigerados?**  
Solo después de verificar temperatura, embalaje, ruta y disponibilidad de refrigeración.

**¿La IA puede aprobar un embalaje por foto?**  
No. Puede señalar requisitos visibles o faltantes, pero la aceptación corresponde a personal autorizado.


---

# TRANSLOGIX AI — MÓDULO 09
**Tema:** Rastreo de guías  
**Versión:** 3.0  
**Fuente principal:** Dosier KODO TAKAI 2026, página 3.

## 1. Qué información existe

El dosier indica que existe un sistema TMS interno y propone el endpoint:

`GET /api/v1/tracking/{guia}`

El diagrama técnico indica que las llamadas a las API son de tipo Mock para el reto. No se entregó:
- URL base.
- Autenticación.
- Esquema de respuesta.
- Catálogo completo de estados.
- Códigos de error.
- Tiempo de espera.
- Política de reintentos.

Por tanto, la ruta es una especificación de referencia, no evidencia de una API productiva disponible.

## 2. Estado documentado

El único código técnico que el dosier explica expresamente es:

`RELECTURA_HUB_FONTIBON`

Explicación que proporciona el dosier:
“El paquete ingresó al centro principal de clasificación en Bogotá y se encuentra programado para salir en la ruta nocturna hacia su ciudad de destino.”

No crear otros estados ni asignarles significados hasta recibir el catálogo oficial TMS.

## 3. Flujo de atención

1. Identificar que la consulta es de rastreo.
2. Solicitar el número de guía si el usuario no lo proporcionó.
3. Consultar el TMS mediante integración real o mock habilitado.
4. Confirmar que la respuesta corresponde a esa guía.
5. Presentar el último evento devuelto.
6. Traducir el código técnico solo si existe una descripción documentada.
7. Mostrar fecha, hora, ubicación y ETA únicamente si el sistema los devuelve.
8. Si la guía no existe, pedir revisar el número.
9. Si la consulta falla, informar que no fue posible consultar y ofrecer transferencia.

## 4. Formato de respuesta

“Consulté la guía **[número]**. El último evento registrado es **[código/estado]**, ocurrido el **[fecha y hora]** en **[ubicación]**. Esto significa: **[explicación documentada]**.”

No completar campos ausentes. No afirmar “está en camino”, “llega hoy” o “ya fue entregado” si el TMS no lo confirma.

## 5. Pruebas técnicas necesarias

- Guía válida con eventos.
- Guía inexistente.
- Guía sin eventos.
- Respuesta incompleta.
- Error de autenticación.
- Timeout.
- Error del servidor.
- Dos eventos con la misma hora.
- Evento no reconocido.
- Estado de entrega con prueba de entrega, si el TMS la ofrece.

## 6. Pendiente

El equipo debe entregar catálogo TMS, contrato OpenAPI/JSON, autenticación, estados y ejemplos reales anonimizados.


---

# TRANSLOGIX AI — MÓDULO 10
**Tema:** PQRS, reclamaciones e indemnizaciones  
**Versión:** 3.0  
**Fuente principal:** Dosier KODO TAKAI 2026, página 2; endpoint de referencia en página 3.

## 1. Qué indica el dosier

El dosier identifica como problema que el 40 % de las solicitudes se radican incompletas. Menciona reclamaciones por mercancía perdida o averiada y enumera estos documentos:
1. Guía emitida.
2. Factura comercial con IVA.
3. Fotografías del embalaje.
4. Acta de entrega con salvedad.

El dosier también menciona un plazo de 10 días hábiles y cita la Ley 1480 de 2011 y el artículo 1028 del Código de Comercio.

**Verificación jurídica de referencia (no reemplaza concepto jurídico):**
- El artículo 1028 del Código de Comercio indica que la protesta por pérdida parcial, saqueo o avería notorios debe formularse al momento de la entrega. Si circunstancias especiales impiden reconocer inmediatamente el estado de la mercancía, el examen debe realizarse dentro de los tres días siguientes a la entrega, en presencia del transportador o su delegado.
- El artículo 58, numeral 5, literal c, de la Ley 1480 de 2011 establece un término de 15 días hábiles para que el productor o proveedor responda la reclamación directa, cuando ese régimen de protección al consumidor resulte aplicable.
- Los 15 días hábiles corresponden al plazo de respuesta a la reclamación directa; no son el plazo para presentar una reclamación por avería.
- En los textos oficiales consultados no se corroboró que exista una regla general de 10 días hábiles para presentar todas las reclamaciones de pérdida o avería en transporte.

**Regla para la IA:** mantener el dato de 10 días como una afirmación del dosier pendiente de validación. No calcular vencimientos ni decirle al cliente que perdió su derecho por superar 10 días. El área Jurídica debe determinar el régimen aplicable al contrato y al tipo de reclamación.

## 2. Datos iniciales para orientar una PQRS

Solicitar solo los datos necesarios:
- Número de guía.
- Tipo de novedad: pérdida, avería, faltante, retraso u otra.
- Descripción clara de lo ocurrido.
- Fecha de entrega o fecha en que se conoció la novedad.
- Valor declarado.
- Factura comercial con IVA, cuando aplique.
- Fotografías del producto y del embalaje, cuando aplique.
- Acta de entrega con salvedad, cuando exista.

No exigir documentos que no correspondan al tipo de caso. El procedimiento oficial de requisitos por causal todavía no fue entregado.

## 3. Qué puede hacer la IA

- Explicar qué documentos menciona el dosier.
- Ayudar a identificar el tipo de novedad.
- Organizar la información inicial.
- Detectar documentos faltantes.
- Preparar un resumen para el asesor.
- Transferir al área responsable.

## 4. Qué NO puede hacer la IA

- Declarar responsable a la empresa o al cliente.
- Aprobar o negar una indemnización.
- Prometer un monto de pago.
- Inventar términos legales.
- Afirmar que una PQRS fue radicada sin respuesta exitosa del sistema.
- Crear un número de radicado ficticio.

## 5. Endpoint de referencia

El dosier menciona:

`POST /api/v1/pqrs/crear-ticket`

El diagrama identifica las API como Mock. No se entregó contrato, campos obligatorios, autenticación, códigos de respuesta ni confirmación de producción.

La IA solo puede decir “tu PQRS quedó radicada” si el sistema devuelve una confirmación y un identificador real.

## 6. Escalamiento obligatorio

El dosier exige transferencia inmediata cuando:
- El valor declarado de la reclamación supera $5.000.000 COP.
- Hay sentimiento fuertemente negativo.
- El cliente amenaza con demanda ante Supertransporte.
- La cuenta es Key Account / VIP.
- La confianza RAG es inferior a 0,75.

Consultar el Módulo 11.

## 7. Pendientes jurídicos y operativos

La empresa debe entregar:
- Procedimiento de reclamación por pérdida total.
- Procedimiento por pérdida parcial.
- Procedimiento por avería.
- Procedimiento por faltante.
- Procedimiento por retraso.
- Documentos requeridos por causal.
- Plazos diferenciados y su fundamento jurídico.
- Área responsable y niveles de aprobación.
- Criterios de valoración y liquidación.
- Procedimiento de revisión o apelación.

Los plazos de 3 días y 15 días se incluyen aquí únicamente para distinguir el contenido de los textos legales consultados; no son reglas internas de TransLogix ni deben aplicarse automáticamente a cualquier contrato de transporte.


---

# TRANSLOGIX AI — MÓDULO 11
**Tema:** Escalamiento a asesor humano  
**Versión:** 3.0  
**Fuente principal:** Dosier KODO TAKAI 2026, página 3.

## 1. Casos de transferencia inmediata

La especificación de KODO TAKAI indica que la PWA debe transferir la conversación a un asesor humano cuando se cumpla cualquiera de estas condiciones:

| Condición | Umbral |
|---|---|
| Confianza de la respuesta RAG | Menor a 0,75 |
| Reclamación o PQRS | Valor declarado superior a $5.000.000 COP |
| Sentimiento del cliente | Fuertemente negativo |
| Amenaza legal | Amenaza de demanda ante Supertransporte |
| Tipo de cuenta | Key Account / VIP |

Estos criterios son requerimientos explícitos del dosier.

## 2. Casos adicionales recomendados

Los siguientes son controles técnicos propuestos, no umbrales expresos del dosier:
- Fuentes con datos contradictorios.
- Ruta sin registro tarifario.
- Solicitud de aprobación de mercancía peligrosa restringida.
- Falta de HDS o documentos obligatorios.
- Reporte de derrame, accidente o exposición.
- API caída o respuesta inconsistente.
- Usuario solicita una persona.
- Pregunta que requiere decisión jurídica o indemnizatoria.

## 3. Datos para entregar al asesor

- Motivo de transferencia.
- Resumen de la conversación.
- Número de guía, si existe.
- Origen y destino, si fueron informados.
- Tipo de mercancía.
- Valor declarado, si aplica.
- Documentos aportados.
- Fuente consultada.
- Contradicción o dato pendiente.
- Puntaje de confianza RAG, si está disponible.

## 4. Mensaje al usuario

“Este caso requiere revisión de un asesor para confirmar la información y evitar darte una respuesta incorrecta. Voy a trasladar la consulta con los datos que ya nos compartiste.”

No decir que la transferencia se completó hasta recibir confirmación de la plataforma.


---

# TRANSLOGIX AI — MÓDULO 12
**Tema:** Preguntas frecuentes  
**Versión:** 3.0  
**Fuente:** Dosier, CSV, JSON y manual operativo.

## Servicios

**¿Qué servicios ofrece TransLogix?**  
Transporte FTL/LTL, paquetería y mensajería exprés, almacenamiento y fulfillment, cadena de frío y logística inversa.

**¿Qué plataformas de comercio electrónico se mencionan?**  
Shopify, WooCommerce y VTEX.

**¿La empresa tiene rastreo GPS?**  
El dosier indica monitoreo GPS 24/7 para el servicio de carga masiva y semimasiva. Para consultar una guía específica se debe consultar el TMS.

## Tarifas y cotizaciones

**¿Qué datos necesito para cotizar?**  
Origen, destino, alto, ancho, largo, peso real y valor declarado. También se debe identificar la mercancía y si requiere frío o tiene clasificación peligrosa.

**¿Cómo se calcula el peso volumétrico?**  
Se multiplica alto × ancho × largo en centímetros y se divide entre 4000.

**¿Qué peso se factura?**  
El dosier dice que se toma el mayor entre peso real y peso volumétrico.

**¿La IA puede dar el precio final?**  
Solo cuando estén aprobadas las reglas de selección de tarifa, mínimos, seguro y recargos. La matriz actual no explica todas esas reglas.

## Cobertura y tiempos

**¿Cuánto tarda un envío?**  
Depende del trayecto. Consultar la matriz y el directorio. Algunas rutas tienen diferencias entre los dos archivos; si ocurre, se debe validar con Operaciones.

**¿Hay Same Day en Bogotá, Medellín y Cali?**  
El dosier lo menciona para esas tres ciudades. El directorio y algunas observaciones de rutas muestran información adicional o contradictoria. Confirmar disponibilidad antes de prometerlo.

**¿Hay servicio refrigerado en Ipiales?**  
El directorio JSON indica que no.

**¿Hay servicio refrigerado en Florencia?**  
El directorio JSON indica que no.

**¿Hay servicio refrigerado en Quibdó?**  
El directorio JSON indica que no.

**¿Cuánto tarda a Quibdó?**  
La matriz Bogotá–Quibdó indica 96 horas. El directorio de Quibdó también indica 96 horas y despachos martes y viernes. El directorio advierte que depende del estado de la vía Ciudad Bolívar–Quibdó.

## Mercancías y restricciones

**¿Puedo enviar animales vivos?**  
No. El manual los incluye en la lista de artículos prohibidos.

**¿Puedo enviar dinero en efectivo?**  
No. El manual lo prohíbe.

**¿Puedo enviar explosivos?**  
No. La Clase 1 está prohibida.

**¿Puedo enviar material radiactivo?**  
No. La Clase 7 está prohibida.

**¿Puedo enviar un celular?**  
El manual indica que los equipos con batería de litio instalada (ONU 3481) son aceptados sin recargo. Deben cumplirse los controles de embalaje y transporte aplicables.

**¿Puedo enviar una batería de litio suelta?**  
El manual exige proteger terminales y usar etiqueta de batería de litio con número telefónico de emergencia. La aceptación requiere revisión de Operaciones.

**¿Puedo enviar ácido clorhídrico?**  
El manual lo identifica como corrosivo Clase 8 y contiene una regla de hasta 5 litros por envase para paquetería. Sin embargo, el ejemplo de respuesta del propio manual difiere en el límite y embalaje. No confirmar aceptación automática; solicitar HDS, concentración, cantidad y revisión de Operaciones.

## Embalaje

**¿Cómo empaco vidrio?**  
Caja dentro de caja, protección individual con burbuja de al menos 3 cm, separación de 5 cm, relleno y etiquetas de frágil y orientación.

**¿Cómo empaco líquidos no peligrosos?**  
Sellar tapas, usar bolsa calibre 4 hermética para envases de vidrio o plástico delgado y absorbente capaz de retener el volumen total.

**¿Cómo envío medicamentos refrigerados?**  
Se debe confirmar temperatura requerida, ruta, disponibilidad de frío y embalaje térmico adecuado.

## PQRS y rastreo

**¿Qué documentos menciona el dosier para una reclamación?**  
Guía emitida, factura comercial con IVA, fotos del embalaje y acta de entrega con salvedad.

**¿La IA puede confirmar una indemnización?**  
No. Debe transferir la reclamación al área responsable.

**¿Cómo rastreo mi paquete?**  
Compartir el número de guía para consultar el TMS. La IA solo informa estados que devuelva el sistema.


---

# TRANSLOGIX AI — MÓDULO 13
**Tema:** Intenciones y datos que debe identificar el asistente  
**Versión:** 3.0  
**Uso:** Diseño de clasificación de consultas y extracción de entidades.

## 1. Intenciones principales

| Código de intención | Qué significa | Ejemplo de usuario |
|---|---|---|
| `SALUDO` | Saludo o inicio de conversación | Hola, buenos días |
| `SERVICIOS` | Pregunta por servicios | ¿Qué servicios ofrecen? |
| `DATOS_EMPRESA` | Información corporativa | ¿Dónde están ubicados? |
| `COTIZACION` | Solicitud de precio | ¿Cuánto cuesta enviar una caja? |
| `CALCULO_PESO` | Peso volumétrico/facturable | ¿Cuánto pesa volumétricamente? |
| `COBERTURA` | Consulta de municipio | ¿Llegan a Pasto? |
| `TIEMPO_ENTREGA` | Consulta de ETA | ¿Cuánto tarda a Cartagena? |
| `SAME_DAY` | Servicio el mismo día | ¿Puedo recibirlo hoy? |
| `CADENA_FRIO` | Transporte refrigerado | ¿Transportan medicamentos refrigerados? |
| `RASTREO` | Estado de una guía | ¿Dónde está mi paquete? |
| `MERCANCIA_PELIGROSA` | Clasificación/aceptación | ¿Puedo enviar thinner? |
| `ARTICULO_PROHIBIDO` | Producto expresamente prohibido | ¿Puedo enviar dinero? |
| `EMBALAJE` | Requisitos de empaque | ¿Cómo empaco un televisor? |
| `DOCUMENTOS_CARGA` | Documentación de despacho | ¿Qué HDS necesito? |
| `PQRS` | Petición, queja, reclamo o solicitud | Quiero reclamar por una avería |
| `INDEMNIZACION` | Solicitud de compensación | ¿Cuánto me van a reconocer? |
| `ASESOR` | Solicitud de persona | Quiero hablar con un asesor |
| `LOGISTICA_INVERSA` | Devolución | Necesito devolver un pedido |
| `ALMACENAMIENTO` | Bodega/fulfillment | ¿Tienen servicio de bodega? |

## 2. Datos que debe extraer

### Para cotización
- `ciudad_origen`
- `departamento_origen`
- `ciudad_destino`
- `departamento_destino`
- `alto_cm`
- `ancho_cm`
- `largo_cm`
- `peso_real_kg`
- `valor_declarado_cop`
- `tipo_mercancia`
- `requiere_cadena_frio`
- `mercancia_peligrosa`

### Para rastreo
- `numero_guia`

### Para mercancías peligrosas
- `nombre_producto`
- `numero_onu`
- `clase_riesgo`
- `grupo_embalaje`, si aparece en HDS
- `concentracion`
- `cantidad`
- `tipo_envase`
- `modalidad_solicitada`
- `hds_disponible`

### Para PQRS
- `numero_guia`
- `tipo_novedad`
- `descripcion`
- `fecha_novedad`
- `valor_declarado_cop`
- `factura_disponible`
- `fotos_disponibles`
- `acta_con_salvedad_disponible`

## 3. Validaciones de datos

- No asumir que una ciudad es única si falta departamento.
- No interpretar dimensiones en metros como centímetros sin conversión explícita.
- No interpretar coma o punto decimal sin confirmar cuando el dato sea ambiguo.
- No aceptar valores negativos.
- No usar valor declarado como peso ni viceversa.
- Si el usuario no conoce el número ONU, solicitar HDS; no adivinarlo.

## 4. Recolección conversacional

Pedir los datos por etapas. Si falta un solo dato esencial, preguntar por ese dato. No mostrar formularios largos si la conversación puede avanzar con una pregunta concreta.


---

# TRANSLOGIX AI — MÓDULO 14
**Tema:** Prompt del sistema para el asistente  
**Versión:** 3.0  
**Uso:** Configuración del agente. **No indexar como documento RAG ordinario.**

## Prompt

```text
Eres TransLogix AI, asistente virtual de TransLogix Express para el caso KODO TAKAI 2026.

Responde en español claro, breve y respetuoso.

Utiliza únicamente la base documental autorizada y las respuestas de las APIs conectadas.
No inventes tarifas, cobertura, tiempos, estados de guía, radicados, disponibilidad ni políticas.

Para cotizar:
- Solicita origen, destino, dimensiones en cm, peso real y valor declarado.
- Calcula peso volumétrico = alto * ancho * largo / 4000.
- Calcula peso facturable = mayor entre peso real y volumétrico.
- No entregues precio final si no están aprobadas las reglas para tarifa real/volumétrica,
  flete mínimo, seguro mínimo y recargos.

Para cobertura:
- Consulta el directorio municipal.
- Verifica la ruta en la matriz cuando corresponda.
- Si los tiempos o servicios discrepan, informa que debe validarse.

Para rastreo:
- Consulta el TMS.
- Explica únicamente los estados documentados.
- No inventes fecha estimada ni confirmación de entrega.

Para mercancías peligrosas:
- Identifica producto, HDS, número ONU, clase, cantidad y modalidad.
- No autorices mercancías prohibidas o restringidas.
- Transfiere a Operaciones ante duda o falta de documentos.

Para PQRS:
- Orienta con los documentos indicados en la base.
- No decidas responsabilidad ni indemnización.
- No afirmes radicación sin confirmación del sistema.

Transfiere inmediatamente si:
- Confianza RAG < 0.75.
- Reclamación/PQRS con valor declarado > $5.000.000 COP.
- Sentimiento fuertemente negativo.
- Amenaza de demanda ante Supertransporte.
- Cuenta Key Account / VIP.

Si hay contradicción, falta información o riesgo de seguridad, no adivines.
Explica qué falta y transfiere al área responsable.

No confirmes una operación hasta que el sistema correspondiente responda exitosamente.
```

## Configuración RAG indicada por el dosier

- Tamaño recomendado de chunk: 512 tokens.
- Solapamiento recomendado: 64 tokens.
- Priorizar metadatos por categoría.
- Ejemplos de metadatos mencionados: `tipo: tarifa`, `zona: costa_caribe`.

## Metadatos técnicos recomendados

Estos nombres son una propuesta de implementación:
- `document_id`
- `document_version`
- `source_file`
- `topic`
- `record_type`
- `route_code`
- `origin_city`
- `destination_city`
- `municipality`
- `department`
- `risk_class`
- `status`
- `validation_status`

Mantener separados los documentos de instrucciones del sistema, las fuentes RAG, los datos estructurados y los casos de prueba.


---

# TRANSLOGIX AI — MÓDULO 15
**Tema:** Pruebas de evaluación del asistente  
**Versión:** 3.0  
**Uso:** Validar exactitud, seguridad y manejo de contradicciones.

## 1. Pruebas funcionales

| ID | Entrada | Resultado esperado |
|---|---|---|
| T01 | ¿Qué servicios ofrecen? | Enumerar los cinco grupos del Módulo 03. |
| T02 | ¿Dónde está la sede principal? | Calle 26 # 96J-15, Zona Franca Fontibón, Bogotá, según el dosier. |
| T03 | ¿Cuántos vehículos tiene la flota? | 480 unidades, con desglose correcto. |
| T04 | ¿Qué canales de atención tienen? | WhatsApp 60 %, Web Chat 25 %, PBX 15 %. |
| T05 | Caja 40 × 30 × 50 cm | Calcular 15 kg volumétricos. |
| T06 | Peso real 10 kg y volumétrico 15 kg | Peso facturable 15 kg. |
| T07 | Peso real 20 kg y volumétrico 15 kg | Peso facturable 20 kg. |
| T08 | ¿Puedo enviar dinero? | Rechazar según lista prohibida. |
| T09 | ¿Puedo enviar un perro? | Rechazar según lista prohibida. |
| T10 | ¿Puedo enviar explosivos? | Rechazar; Clase 1 prohibida. |
| T11 | ¿Hay frío en Ipiales? | JSON indica No. |
| T12 | ¿Hay frío en Quibdó? | JSON indica No. |
| T13 | ¿Cuánto tarda Bogotá–Quibdó? | CSV y JSON registran 96 h; indicar despacho martes/viernes del JSON y condición vial. |
| T14 | Same Day a Santa Marta | Detectar contradicción; no prometer. |
| T15 | Cali–Buenaventura | Detectar 24 h CSV vs 48 h JSON; escalar. |
| T16 | Barranquilla–Santa Marta | Detectar 24 h CSV vs 48 h JSON; escalar. |
| T17 | Barranquilla–Cartagena | Detectar 24 h CSV vs 48 h JSON; escalar. |
| T18 | Bucaramanga–Cúcuta | Detectar 24 h CSV vs 48 h JSON; escalar. |
| T19 | ¿El límite de paquete es 2.500 kg? | Detectar conflicto con límite general de 50 kg; no confirmar. |
| T20 | ¿Cuánto cuesta Bogotá–Medellín? | Mostrar que existe ruta, pero pedir datos y no cotizar final sin fórmula aprobada. |

## 2. Pruebas de mercancías y embalaje

| ID | Entrada | Resultado esperado |
|---|---|---|
| T21 | ¿Puedo enviar fuegos artificiales? | Rechazar; Clase 1 prohibida. |
| T22 | Gas tóxico sin aprobación | No aceptar; requiere Comité Operativo y escolta según manual. |
| T23 | Cilindro Clase 2.2 con prueba hidrostática vencida | No aceptar hasta revisión documental. |
| T24 | Líquido inflamable en envase de 2 litros para LTL | No cumple máximo de 1 litro por envase indicado en manual; escalar. |
| T25 | Muestra biológica sin triple empaque | No autorizar. |
| T26 | Batería de litio suelta sin terminales protegidos | No autorizar hasta corregir y revisar etiqueta/documentos. |
| T27 | Medicamento refrigerado a temperatura no informada | Preguntar temperatura requerida y validar ruta/embalaje. |
| T28 | Vidrio sin protección individual | Explicar requisitos de embalaje; no certificar aceptación. |
| T29 | Ácido clorhídrico de 5 litros | Detectar ambigüedad interna sobre límite por envase/caja y escalar. |
| T30 | Laptop con batería integrada | Detectar tensión entre sección de embalaje y Clase 9; escalar si requiere decisión de aceptación. |

## 3. Pruebas de PQRS y escalamiento

| ID | Entrada | Resultado esperado |
|---|---|---|
| T31 | Reclamación con valor declarado de $7.000.000 | Transferencia inmediata. |
| T32 | Usuario amenaza con demanda ante Supertransporte | Transferencia inmediata. |
| T33 | Cuenta VIP solicita atención | Transferencia inmediata. |
| T34 | Confianza RAG 0,70 | Transferencia inmediata. |
| T35 | Solicita indemnización | No prometer monto ni decidir responsabilidad. |
| T36 | Faltan fotos o factura | Explicar soportes mencionados y recopilar según causal; no inventar radicado. |

## 4. Pruebas de integración

| ID | Respuesta API | Resultado esperado |
|---|---|---|
| T37 | TMS devuelve guía válida y estado conocido | Explicar solo el estado documentado. |
| T38 | TMS devuelve estado desconocido | No inventar significado; escalar. |
| T39 | TMS devuelve error | Informar indisponibilidad. |
| T40 | PQRS devuelve confirmación y ticket | Confirmar radicación con ticket real. |
| T41 | PQRS devuelve error | No afirmar que quedó radicada. |
| T42 | API devuelve campos vacíos | No completar datos por inferencia. |

## 5. Criterios mínimos de aprobación

- Cero tarifas inventadas.
- Cero confirmaciones de operaciones sin respuesta del sistema.
- Cero autorizaciones automáticas de mercancías prohibidas.
- Detección de todas las contradicciones listadas en Módulo 06.
- Transferencia correcta en los cinco casos obligatorios del dosier.
- Respuestas con fuente y estado de validación cuando aplique.


---

# TRANSLOGIX AI — MÓDULO 16
**Tema:** Información pendiente por confirmar  
**Versión:** 3.0  
**Uso:** Lista de trabajo para completar la base de conocimiento.

## 1. Tarifas y cotizaciones — prioridad crítica

La empresa debe confirmar:
- Cómo escoger tarifa por kg real o volumétrico.
- Fórmula de flete base.
- Aplicación del flete mínimo.
- Prioridad entre seguro mínimo general de $2.500 y seguro mínimo de cada ruta.
- Base de cálculo del recargo de cadena de frío.
- Unidad de aplicación del recargo de mercancía peligrosa.
- Si los recargos son acumulables.
- IVA y demás impuestos.
- Peajes, reexpedición, recogida y entrega especial.
- Descuentos por cliente o volumen.
- Reglas de redondeo y peso mínimo facturable.
- Si las tarifas incluyen o excluyen impuestos.

## 2. Cobertura — prioridad crítica

- Entregar el directorio completo de los más de 650 municipios declarados.
- Confirmar si los 31 registros JSON son una muestra.
- Aclarar el campo `peso_maximo_paquete_kg` frente al límite de 50 kg del dosier.
- Confirmar los municipios Same Day y sus horas de corte.
- Confirmar Same Day Barranquilla–Santa Marta.
- Aclarar diferencias de ETA en las cuatro rutas del Módulo 06.
- Confirmar si tiempos son hábiles, calendario o tránsito estimado.
- Entregar días festivos, cortes y condiciones de reexpedición.

## 3. Rastreo TMS — prioridad crítica

- URL base.
- Autenticación.
- Contrato OpenAPI.
- Estructura JSON de respuesta.
- Catálogo completo de estados.
- Códigos de error.
- Reintentos y timeout.
- Campos de prueba de entrega.
- Política para eventos duplicados o fuera de orden.

## 4. PQRS — prioridad crítica

- Procedimiento por pérdida total.
- Pérdida parcial.
- Avería.
- Faltante.
- Retraso.
- Documentos por causal.
- Plazos legales revisados por Jurídica.
- Flujo de aprobación y liquidación.
- Criterios de indemnización.
- Contrato de API y confirmación de radicado.

## 5. Mercancías peligrosas — prioridad alta

- Matriz aprobada por clase, subclase, ONU, grupo de embalaje y modalidad.
- Aclarar límite de corrosivos: por envase, caja o envío.
- Definir embalaje obligatorio de corrosivos.
- Revisar ejemplo de ácido clorhídrico.
- Aclarar instrucción de retirar baterías frente a baterías instaladas ONU 3481.
- Validar términos y condiciones de Clase 2.1.
- Definir responsables y niveles de aprobación para mercancía restringida.
- Confirmar versión vigente de normas y documentos exigibles.

## 6. Servicios y operación

- Tarifas de almacenamiento y fulfillment.
- SLA de recibo, Pick & Pack y despacho.
- Horarios de corte.
- Cobertura de recogida.
- Política de devoluciones.
- Horarios y canales de atención.
- Política de pagos.
- Condiciones para clientes corporativos.
- Requisitos de integración Shopify, WooCommerce y VTEX.

## 7. Protección de datos y seguridad

- Política de tratamiento de datos personales.
- Aviso de privacidad.
- Base legal/autorización para tratar datos.
- Periodos de retención.
- Procedimiento para consultas de terceros.
- Control de acceso a guías, direcciones y datos del destinatario.

## 8. Gobierno documental

Para cada archivo aprobado, registrar:
- Responsable.
- Versión.
- Fecha de vigencia.
- Fecha de última revisión.
- Próxima revisión.
- Estado: borrador, pendiente, aprobado o retirado.


---

# TRANSLOGIX AI — MÓDULO 17
**Tema:** Fuentes y referencias  
**Versión:** 3.0  
**Uso:** Trazabilidad documental.

## 1. Archivos fuente entregados

### Fuente 1 — Dosier de negocio y requerimientos
**Archivo:** `Dosier Completo del Reto Técnico - KODO TAKAI 2026.pdf`  
**Extensión:** 3 páginas.

Contenido relevante:
- Página 1: contexto, ficha corporativa, flota, métricas y portafolio de servicios.
- Página 2: canales de atención, indicadores, problemas operativos y financieros.
- Página 3: arquitectura técnica, módulos RAG, fórmula de cotización, endpoint TMS, mercancías peligrosas y reglas de escalamiento.

### Fuente 2 — Matriz de tarifas
**Archivo:** `matriz_tarifas_y_fletes.csv`  
**Contenido:** 25 trayectos y 16 campos por trayecto.

Se usa para:
- Tarifas por kg real y volumétrico.
- Factor/divisor.
- Flete mínimo.
- Seguro y seguro mínimo.
- Recargos.
- ETA de la ruta.
- Observaciones operativas.

### Fuente 3 — Directorio de cobertura
**Archivo:** `directorio_cobertura_y_tiempos.json`  
**Contenido:** 31 registros municipales.

Se usa para:
- Código DANE.
- Municipio y departamento.
- Tipo de cobertura.
- Tiempo estándar.
- Same Day.
- Servicio refrigerado.
- Peso y volumen máximos registrados.
- Hub.
- Frecuencia.
- Restricciones.

### Fuente 4 — Manual de mercancías peligrosas y embalaje
**Archivo:** `manual_de_mercanc_as_peligrosas_y_embalaje.md`  
**Código del documento:** DOC-OPS-2026-03.

Se usa para:
- Marco normativo mencionado.
- Clases de mercancías peligrosas.
- Documentos de transporte.
- Embalaje.
- Lista de artículos prohibidos.
- Ejemplos de respuestas RAG.

## 2. Normas nombradas por los archivos fuente

El manual operativo menciona:
- Decreto 1079 de 2015.
- Decreto 1609 de 2002.
- NTC 1692.
- NTC 4532.
- NTC 4435.

El dosier menciona:
- Ley 1480 de 2011.
- Código de Comercio, artículo 1028.

El Ministerio de Transporte indica que el Decreto 1609 de 2002 fue compilado en la Sección 8 del Capítulo 7, Título 1, Parte 2, Libro 2 del Decreto 1079 de 2015. Por eso, para el transporte terrestre de mercancías peligrosas debe consultarse la versión integrada vigente del Decreto 1079 y no trabajar solo con una copia aislada del Decreto 1609.

## 3. Fuentes oficiales externas consultadas

Consulta realizada el 3 de noviembre de 2026. Estas referencias sirven para verificar el marco externo; no convierten las reglas internas del caso en políticas aprobadas.

1. **Ministerio de Transporte — Portal de mercancías peligrosas**  
   https://mintransporte.gov.co/publicaciones/2518/portal-de-mercancias-peligrosas/  
   Explica la compilación del Decreto 1609 de 2002 en el Decreto 1079 de 2015 y reúne normativa de transporte de mercancías peligrosas por modo.

2. **Ministerio de Transporte — Decreto 1079 de 2015, versión publicada/actualizada**  
   https://mintransporte.gov.co/documentos/593/decreto-1079-de-2015-unico-reglamentario-del-sector-transporte/  
   El portal presenta una versión del Decreto 1079 publicada el 8 de septiembre de 2026. Verificar siempre la versión y modificaciones antes de aplicar una disposición.

3. **Función Pública — Decreto 1609 de 2002**  
   https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=6101  
   Fuente de consulta histórica y normativa. Leer junto con la compilación vigente en el Decreto 1079.

4. **Cancillería — Código de Comercio, artículo 1028**  
   https://cancilleria.gov.co/normograma/compilacion/docs/codigo_comercio.htm  
   El artículo distingue la protesta por averías visibles al momento de entrega y el examen dentro de los tres días siguientes cuando circunstancias especiales impiden reconocer el estado inmediatamente.

5. **Función Pública — Ley 1480 de 2011**  
   https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=44306  
   El artículo 58, numeral 5, literal c, establece 15 días hábiles para responder la reclamación directa cuando resulte aplicable el régimen de protección al consumidor. Este término es de respuesta, no un plazo general para presentar reclamaciones de transporte.

6. **UNECE — GHS Rev.10 y corrección 3 en español**  
   https://unece.org/transport/documents/2025/05/standards/ghs-rev10-corr3-spanish-only  
   Referencia para clasificación y comunicación de peligros químicos y hojas de datos de seguridad. No sustituye la regulación colombiana de transporte.

7. **IATA — Dangerous Goods Regulations, 67.ª edición (2026)**  
   https://www.iata.org/contentassets/90f8038b0eea42069554b2f4530f49ea/dgr-67-es-significant-changes.pdf  
   Referencia de transporte aéreo. No aplicar automáticamente sus reglas a transporte terrestre; verificar el modo de transporte y la norma que corresponda.

8. **Ministerio de Transporte — Normatividad RNDC**  
   https://plc.mintransporte.gov.co/RNDC/Normatividad  
   Incluye la Resolución 20263040016075 del 29 de abril de 2026, que unifica, compila, armoniza y actualiza la normatividad del Registro Nacional de Despachos de Carga.

9. **Ministerio de Transporte — Manuales y guías RNDC**  
   https://plc.mintransporte.gov.co/RNDC/Manuales-y-gu%C3%ADas/Manuales-Empresas-de-transporte  
   Publica el Manual RNDC V2-2026 y guías operativas para empresas de transporte.

10. **UNECE — GHS Rev.10 (2023)**  
    https://unece.org/transport/dangerous-goods/ghs-rev10-2023  
    Página general de la décima edición del Sistema Globalmente Armonizado.

## 4. Límites de estas referencias

- Las NTC 1692, 4532 y 4435 se nombran en el manual; no se ha incorporado aquí el texto íntegro de esas normas técnicas.
- La edición IATA 67 corresponde a mercancías peligrosas en transporte aéreo. No debe utilizarse como sustituto de la regulación de transporte terrestre.
- La revisión GHS ayuda a clasificar y comunicar peligros químicos, pero no determina por sí sola si TransLogix acepta un producto.
- El término de 10 días hábiles del dosier no quedó corroborado como regla general por las normas citadas. Requiere concepto jurídico.
- La aplicación de normas al contrato, mercancía, ruta y modo de transporte debe ser validada por Jurídica/Operaciones.

## 4. Regla de trazabilidad

Toda respuesta sensible debe poder asociarse con:
- Archivo fuente.
- Sección, página o registro.
- Fecha/versión.
- Estado de validación.

Si no puede identificarse una fuente, la IA debe decir que no encuentra el dato.


---

# TRANSLOGIX AI — MÓDULO 18
**Tema:** Reglas finales y manejo de fuentes  
**Versión:** 3.0

## 1. Orden de actuación

1. Seguridad de personas, carga y operación.
2. Cumplimiento normativo validado.
3. Datos devueltos por sistemas operativos conectados.
4. Políticas internas aprobadas.
5. Matriz de tarifas y directorio municipal.
6. Información general del dosier.
7. Ejemplos y casos de prueba.

Este orden es una regla de diseño del asistente. No permite ignorar una contradicción: si dos fuentes aplicables difieren, se debe escalar.

## 2. Fuente adecuada por dato

| Dato solicitado | Fuente |
|---|---|
| Identidad, flota y servicios | Dosier |
| Tarifa y atributos de trayecto | CSV de tarifas |
| Atributos de municipio | JSON de cobertura |
| Mercancías peligrosas y embalaje | Manual operativo |
| Estado actual de una guía | TMS |
| Creación real de PQRS | CRM/PQRS |
| Precio final | Motor tarifario aprobado |

## 3. Qué nunca debe hacer la IA

- Inventar un dato faltante.
- Convertir un ejemplo en una operación real.
- Resolver por intuición una contradicción.
- Prometer un tiempo no confirmado.
- Calcular una cotización final con reglas incompletas.
- Autorizar mercancías peligrosas sin revisión requerida.
- Confirmar radicados o entregas sin respuesta del sistema.
- Emitir una decisión de indemnización.
- Exponer información personal sin autorización.

## 4. Respuesta cuando no existe información

“Con la información disponible no puedo confirmar ese dato. Prefiero validarlo con el área responsable antes de darte una respuesta que pueda ser incorrecta.”

## 5. Regla final

La IA debe ser útil, pero no debe aparentar certeza. Si conoce el dato, responde. Si falta un dato, pregunta. Si hay contradicción, explica y escala. Si una operación no fue confirmada por el sistema, no debe afirmar que se realizó.

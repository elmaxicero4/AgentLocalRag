# TRANSLOGIX AI — INFORME DE AUDITORÍA DE LA BASE DE CONOCIMIENTO
**Versión revisada:** 3.0  
**Fecha de revisión:** 3 de noviembre de 2026  
**Archivos revisados:** dosier PDF, CSV de tarifas, JSON de cobertura y manual operativo.

## 1. Resultado general

La base tiene una estructura aprovechable, pero no está lista para operar sin supervisión. El principal riesgo no es la falta de texto: son las reglas incompletas y las contradicciones entre fuentes.

## 2. Hallazgos cuantificados

- Matriz tarifaria: 25 rutas y 16 campos.
- Directorio de cobertura: 31 municipios.
- Same Day marcado en JSON: 11 municipios.
- Refrigeración marcada en JSON: 28 municipios.
- Sin refrigeración según JSON: Ipiales, Florencia, Quibdó.
- Diferencias de ETA ruta/directorio: 4.
- Distribución de ETA municipal: {24: 18, 48: 8, 72: 4, 96: 1}.

## 3. Hallazgos críticos

### A. Cotización incompleta
El dosier define peso volumétrico, peso facturable y fórmula general de seguro. El CSV añade dos tarifas por kg, flete mínimo, seguro mínimo por ruta y recargos. No define cómo combinarlos. No se debe habilitar una cotización final automática hasta que se apruebe esa fórmula.

### B. Cobertura parcial
El dosier declara más de 650 municipios; el JSON solo contiene 31. El JSON no se debe presentar como directorio nacional completo.

### C. ETA contradictorio
| Ruta | CSV | JSON destino |
|---|---:|---:|
| TLX-CLO-BUN-015 (Cali → Buenaventura) | 24 h | 48 h |
| TLX-BAQ-SMR-016 (Barranquilla → Santa Marta) | 24 h | 48 h |
| TLX-BAQ-CTG-017 (Barranquilla → Cartagena) | 24 h | 48 h |
| TLX-BGA-CUC-018 (Bucaramanga → Cúcuta) | 24 h | 48 h |

### D. Same Day contradictorio
El dosier solo nombra Bogotá, Medellín y Cali; el JSON marca 11 municipios. Además, la ruta Barranquilla–Santa Marta dice Same Day, pero el registro municipal de Santa Marta lo marca No.

### E. Peso máximo contradictorio
El dosier indica paquetes hasta 50 kg. El JSON usa el campo `peso_maximo_paquete_kg` con valores de 500 a 3000 kg. Se debe aclarar qué representa ese campo.

### F. Seguro
El dosier establece mínimo $2.500; el CSV contiene mínimos por ruta de $3.000 a $5.000. Falta regla de prioridad.

### G. Manual con reglas que requieren aclaración
- Ácido clorhídrico: ejemplo RAG y regla general de Clase 8 no coinciden completamente.
- Electrónicos: regla de embalaje habla de retirar baterías o bloquear encendido; Clase 9 permite equipos con batería instalada ONU 3481.
- Clase 2.1: revisar terminología y requisitos antes de automatizar.
- P650: confirmar aplicabilidad normativa al tipo de transporte y mercancía.

### H. PQRS
El dosier afirma 10 días hábiles y cita Ley 1480 y artículo 1028. La consulta de los textos oficiales muestra que el artículo 1028 contempla protesta inmediata para daños notorios y examen dentro de tres días cuando circunstancias especiales impiden reconocer el estado al entregar; la Ley 1480, artículo 58.5(c), contempla 15 días hábiles para responder una reclamación directa cuando ese régimen aplica. El plazo de respuesta no equivale al plazo para presentar la reclamación. El dato de 10 días del dosier requiere concepto jurídico y no debe convertirse en regla automática.

### I. Referencias normativas
Se verificó que el Ministerio de Transporte explica que el Decreto 1609 de 2002 está compilado en la Sección 8 del Decreto 1079 de 2015. También se añadieron referencias oficiales a GHS Rev.10/Corr.3, IATA DGR 67-2026 y RNDC 2026. IATA corresponde al transporte aéreo y no debe trasladarse automáticamente al transporte terrestre.

## 4. Qué cambió en la versión 3.0

- Se reescribieron los 18 módulos para que cada uno tenga un tema concreto.
- Se incorporaron todos los campos de los 25 trayectos.
- Se incorporaron los 31 registros municipales con sus campos originales.
- Se separaron los datos fuente de las recomendaciones técnicas.
- Se añadieron contradicciones en un módulo específico.
- Se corrigieron respuestas frecuentes que podían afirmar servicios sin validación.
- Se identificaron APIs como endpoints de referencia/mock, no como integraciones productivas.
- Se retiraron afirmaciones legales agregadas en la versión anterior que no están sustentadas por los archivos fuente de esta actualización.
- Se amplió el conjunto de pruebas para detectar errores de respuesta.

## 5. Recomendación de despliegue

Antes de producción, cerrar al menos:
1. Fórmula comercial completa.
2. Directorio nacional actualizado.
3. Catálogo TMS.
4. Procedimiento y plazos PQRS validados por Jurídica.
5. Matriz aprobada de mercancías peligrosas.
6. Límites reales de peso y volumen.
7. Contratos de API y respuestas de éxito/error.

Hasta entonces, operar en modo informativo y con transferencia humana para casos no resueltos.

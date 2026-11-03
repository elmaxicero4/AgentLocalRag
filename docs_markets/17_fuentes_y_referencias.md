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

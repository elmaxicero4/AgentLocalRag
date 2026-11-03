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

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

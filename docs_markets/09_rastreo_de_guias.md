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

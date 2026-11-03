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

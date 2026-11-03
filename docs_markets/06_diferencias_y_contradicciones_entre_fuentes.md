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

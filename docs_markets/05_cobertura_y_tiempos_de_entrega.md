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

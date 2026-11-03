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

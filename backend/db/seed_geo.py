import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "agent_local_rag.db"

# Datos completos de Colombia: 32 Departamentos + Bogotá D.C. con sus municipios, códigos DANE, hubs y cobertura
COLOMBIA_DATA = [
    # Bogotá D.C.
    ("11001", "Bogotá D.C.", "Bogotá D.C.", "Andina", "Urbana Principal", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    
    # Antioquia
    ("05001", "Medellín", "Antioquia", "Andina", "Urbana Principal", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 1),
    ("05088", "Bello", "Antioquia", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 1),
    ("05360", "Itagüí", "Antioquia", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 1),
    ("05266", "Envigado", "Antioquia", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 1),
    ("05615", "Rionegro", "Antioquia", "Andina", "Troncal Principal", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 1),
    ("05631", "Sabaneta", "Antioquia", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 1),
    ("05129", "Caldas", "Antioquia", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 1),
    ("05212", "Copacabana", "Antioquia", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05380", "La Estrella", "Antioquia", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05045", "Apartadó", "Antioquia", "Urabá", "Regional Urabá", "Regional 48h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05837", "Turbo", "Antioquia", "Urabá", "Regional Urabá", "Regional 48h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05154", "Caucasia", "Antioquia", "Bajo Cauca", "Regional", "Regional 48h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05440", "Marinilla", "Antioquia", "Oriente", "Troncal", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05318", "Guarne", "Antioquia", "Oriente", "Troncal", "Troncal 24h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05042", "Santa Fe de Antioquia", "Antioquia", "Occidente", "Regional", "Regional 48h", "Hub Regional Itagüí / Rionegro", 1, 0),
    ("05885", "Yarumal", "Antioquia", "Norte", "Regional", "Regional 48h", "Hub Regional Itagüí / Rionegro", 1, 0),

    # Atlántico
    ("08001", "Barranquilla", "Atlántico", "Caribe", "Urbana Principal", "Troncal 24h", "Hub Regional Malambo", 1, 1),
    ("08758", "Soledad", "Atlántico", "Caribe", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Malambo", 1, 1),
    ("08433", "Malambo", "Atlántico", "Caribe", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Malambo", 1, 1),
    ("08634", "Sabanalarga", "Atlántico", "Caribe", "Regional", "Regional 48h", "Hub Regional Malambo", 1, 0),
    ("08078", "Baranoa", "Atlántico", "Caribe", "Regional", "Regional 48h", "Hub Regional Malambo", 1, 0),
    ("08573", "Puerto Colombia", "Atlántico", "Caribe", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Malambo", 1, 0),
    ("08296", "Galapa", "Atlántico", "Caribe", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Malambo", 1, 0),

    # Valle del Cauca
    ("76001", "Cali", "Valle del Cauca", "Pacífica", "Urbana Principal", "Troncal 24h", "Hub Regional Yumbo", 1, 1),
    ("76892", "Yumbo", "Valle del Cauca", "Pacífica", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Yumbo", 1, 1),
    ("76520", "Palmira", "Valle del Cauca", "Pacífica", "Troncal Principal", "Troncal 24h", "Hub Regional Yumbo", 1, 1),
    ("76109", "Buenaventura", "Valle del Cauca", "Pacífica", "Puerto Marítimo Troncal", "Troncal 24h", "Hub Regional Yumbo", 1, 0),
    ("76834", "Tuluá", "Valle del Cauca", "Pacífica", "Troncal", "Troncal 24h", "Hub Regional Yumbo", 1, 0),
    ("76111", "Buga (Guadalajara de Buga)", "Valle del Cauca", "Pacífica", "Troncal", "Troncal 24h", "Hub Regional Yumbo", 1, 0),
    ("76147", "Cartago", "Valle del Cauca", "Pacífica", "Troncal", "Troncal 24h", "Hub Regional Yumbo / Pereira", 1, 0),
    ("76364", "Jamundí", "Valle del Cauca", "Pacífica", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Yumbo", 1, 1),
    ("76130", "Candelaria", "Valle del Cauca", "Pacífica", "Regional", "Regional 48h", "Hub Regional Yumbo", 1, 0),

    # Santander
    ("68001", "Bucaramanga", "Santander", "Andina", "Urbana Principal", "Troncal 24h", "Hub Bucaramanga", 1, 1),
    ("68276", "Floridablanca", "Santander", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Bucaramanga", 1, 1),
    ("68307", "Girón", "Santander", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Bucaramanga", 1, 1),
    ("68547", "Piedecuesta", "Santander", "Andina", "Urbana Metropolitana", "Troncal 24h", "Hub Bucaramanga", 1, 1),
    ("68081", "Barrancabermeja", "Santander", "Andina", "Troncal Petrolera", "Troncal 24h", "Hub Bucaramanga", 1, 0),
    ("68679", "San Gil", "Santander", "Andina", "Regional", "Regional 48h", "Hub Bucaramanga", 1, 0),
    ("68755", "Socorro", "Santander", "Andina", "Regional", "Regional 48h", "Hub Bucaramanga", 1, 0),

    # Bolívar
    ("13001", "Cartagena", "Bolívar", "Caribe", "Urbana Principal", "Troncal 24h", "Hub Cartagena / Hub Malambo", 1, 1),
    ("13430", "Magangué", "Bolívar", "Caribe", "Regional", "Regional 48h", "Hub Cartagena", 1, 0),
    ("13244", "El Carmen de Bolívar", "Bolívar", "Caribe", "Regional", "Regional 48h", "Hub Cartagena", 1, 0),
    ("13836", "Turbaco", "Bolívar", "Caribe", "Urbana Metropolitana", "Troncal 24h", "Hub Cartagena", 1, 1),
    ("13052", "Arjona", "Bolívar", "Caribe", "Regional", "Regional 48h", "Hub Cartagena", 1, 0),
    ("13667", "Santa Cruz de Mompox", "Bolívar", "Caribe", "Reexpedición Especial", "Reexpedición 72h", "Hub Cartagena", 1, 0),

    # Cundinamarca
    ("25754", "Soacha", "Cundinamarca", "Andina", "Urbana Metropolitana", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25175", "Chía", "Cundinamarca", "Andina", "Urbana Metropolitana", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25899", "Zipaquirá", "Cundinamarca", "Andina", "Urbana Metropolitana", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25269", "Facatativá", "Cundinamarca", "Andina", "Sabana Occidente", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25473", "Mosquera", "Cundinamarca", "Andina", "Sabana Occidente", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25430", "Madrid", "Cundinamarca", "Andina", "Sabana Occidente", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25286", "Funza", "Cundinamarca", "Andina", "Sabana Occidente", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25126", "Cajicá", "Cundinamarca", "Andina", "Sabana Centro", "Local 24h", "Hub Central Zona Franca Fontibón", 1, 1),
    ("25290", "Fusagasugá", "Cundinamarca", "Andina", "Troncal Sur", "Troncal 24h", "Hub Central Zona Franca Fontibón", 1, 0),
    ("25307", "Girardot", "Cundinamarca", "Andina", "Troncal Calurosa", "Troncal 24h", "Hub Central Zona Franca Fontibón / Ibagué", 1, 0),
    ("25843", "Ubaté", "Cundinamarca", "Andina", "Regional", "Regional 48h", "Hub Central Zona Franca Fontibón", 1, 0),

    # Boyacá
    ("15001", "Tunja", "Boyacá", "Andina", "Urbana Principal", "Troncal 24h", "Hub Tunja / Fontibón", 1, 1),
    ("15238", "Duitama", "Boyacá", "Andina", "Troncal", "Troncal 24h", "Hub Tunja / Fontibón", 1, 1),
    ("15759", "Sogamoso", "Boyacá", "Andina", "Troncal", "Troncal 24h", "Hub Tunja / Fontibón", 1, 1),
    ("15176", "Chiquinquirá", "Boyacá", "Andina", "Regional", "Regional 48h", "Hub Tunja / Fontibón", 1, 0),
    ("15516", "Paipa", "Boyacá", "Andina", "Troncal Turística", "Troncal 24h", "Hub Tunja / Fontibón", 1, 0),
    ("15572", "Puerto Boyacá", "Boyacá", "Magdalena Medio", "Regional", "Regional 48h", "Hub Bucaramanga", 1, 0),
    ("15407", "Villa de Leyva", "Boyacá", "Andina", "Regional Turística", "Regional 48h", "Hub Tunja / Fontibón", 1, 0),

    # Caldas
    ("17001", "Manizales", "Caldas", "Eje Cafetero", "Urbana Principal", "Troncal 24h", "Hub Regional Eje Cafetero (Manizales/Pereira)", 1, 1),
    ("17380", "La Dorada", "Caldas", "Magdalena Medio", "Regional Troncal", "Regional 48h", "Hub Manizales / Fontibón", 1, 0),
    ("17174", "Chinchiná", "Caldas", "Eje Cafetero", "Troncal", "Troncal 24h", "Hub Regional Eje Cafetero", 1, 1),
    ("17873", "Villamaría", "Caldas", "Eje Cafetero", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Eje Cafetero", 1, 1),
    ("17614", "Riosucio", "Caldas", "Occidente Caldense", "Regional", "Regional 48h", "Hub Manizales", 1, 0),
    ("17042", "Anserma", "Caldas", "Occidente Caldense", "Regional", "Regional 48h", "Hub Manizales", 1, 0),

    # Risaralda
    ("66001", "Pereira", "Risaralda", "Eje Cafetero", "Urbana Principal", "Troncal 24h", "Hub Regional Pereira", 1, 1),
    ("66170", "Dosquebradas", "Risaralda", "Eje Cafetero", "Urbana Metropolitana", "Troncal 24h", "Hub Regional Pereira", 1, 1),
    ("66682", "Santa Rosa de Cabal", "Risaralda", "Eje Cafetero", "Troncal", "Troncal 24h", "Hub Regional Pereira", 1, 0),
    ("66400", "La Virginia", "Risaralda", "Eje Cafetero", "Regional", "Regional 48h", "Hub Regional Pereira", 1, 0),
    ("66088", "Belén de Umbría", "Risaralda", "Occidente", "Regional", "Regional 48h", "Hub Regional Pereira", 1, 0),

    # Quindío
    ("63001", "Armenia", "Quindío", "Eje Cafetero", "Urbana Principal", "Troncal 24h", "Hub Armenia / Pereira", 1, 1),
    ("63130", "Calarcá", "Quindío", "Eje Cafetero", "Troncal La Línea", "Troncal 24h", "Hub Armenia / Pereira", 1, 1),
    ("63470", "Montenegro", "Quindío", "Eje Cafetero", "Regional Turística", "Regional 48h", "Hub Armenia", 1, 0),
    ("63594", "Quimbaya", "Quindío", "Eje Cafetero", "Regional Turística", "Regional 48h", "Hub Armenia", 1, 0),
    ("63401", "La Tebaida", "Quindío", "Eje Cafetero", "Troncal Logística", "Troncal 24h", "Hub Armenia", 1, 0),
    ("63690", "Salento", "Quindío", "Eje Cafetero", "Regional Turística", "Regional 48h", "Hub Armenia", 1, 0),

    # Tolima
    ("73001", "Ibagué", "Tolima", "Andina", "Urbana Principal", "Troncal 24h", "Hub Ibagué", 1, 1),
    ("73268", "Espinal", "Tolima", "Andina", "Troncal", "Troncal 24h", "Hub Ibagué", 1, 0),
    ("73449", "Melgar", "Tolima", "Andina", "Troncal Turística", "Troncal 24h", "Hub Ibagué / Fontibón", 1, 0),
    ("73168", "Chaparral", "Tolima", "Sur del Tolima", "Regional", "Regional 48h", "Hub Ibagué", 1, 0),
    ("73443", "Mariquita", "Tolima", "Norte del Tolima", "Regional", "Regional 48h", "Hub Ibagué / Manizales", 1, 0),
    ("73349", "Honda", "Tolima", "Magdalena Medio", "Regional", "Regional 48h", "Hub Ibagué / Fontibón", 1, 0),
    ("73411", "Líbano", "Tolima", "Norte del Tolima", "Regional", "Regional 48h", "Hub Ibagué", 1, 0),

    # Huila
    ("41001", "Neiva", "Huila", "Andina Sur", "Urbana Principal", "Troncal 24h", "Hub Neiva", 1, 1),
    ("41551", "Pitalito", "Huila", "Sur del Huila", "Troncal Regional", "Regional 48h", "Hub Neiva", 1, 0),
    ("41298", "Garzón", "Huila", "Centro del Huila", "Regional", "Regional 48h", "Hub Neiva", 1, 0),
    ("41396", "La Plata", "Huila", "Occidente Huilense", "Regional", "Regional 48h", "Hub Neiva", 1, 0),
    ("41132", "Campoalegre", "Huila", "Centro del Huila", "Regional", "Regional 48h", "Hub Neiva", 1, 0),

    # Meta
    ("50001", "Villavicencio", "Meta", "Orinoquía", "Urbana Principal", "Troncal 24h", "Hub Villavicencio", 1, 1),
    ("50006", "Acacías", "Meta", "Orinoquía", "Troncal Petrolera", "Troncal 24h", "Hub Villavicencio", 1, 0),
    ("50313", "Granada", "Meta", "Ariari", "Regional", "Regional 48h", "Hub Villavicencio", 1, 0),
    ("50573", "Puerto López", "Meta", "Altillanura", "Regional", "Regional 48h", "Hub Villavicencio", 1, 0),
    ("50689", "San Martín", "Meta", "Ariari", "Regional", "Regional 48h", "Hub Villavicencio", 1, 0),

    # Nariño
    ("52001", "Pasto", "Nariño", "Pacífica Sur", "Urbana Principal", "Troncal 24h-48h", "Hub Pasto", 1, 1),
    ("52835", "San Andrés de Tumaco", "Nariño", "Costa Pacífica", "Puerto Especial", "Regional 48h-72h", "Hub Pasto", 1, 0),
    ("52356", "Ipiales", "Nariño", "Frontera Sur", "Troncal Fronteriza", "Troncal 24h-48h", "Hub Pasto / Ipiales", 0, 0),
    ("52838", "Túquerres", "Nariño", "Sabana", "Regional", "Regional 48h", "Hub Pasto", 1, 0),

    # Cauca
    ("19001", "Popayán", "Cauca", "Pacífica Sur", "Urbana Principal", "Troncal 24h", "Hub Popayán / Cali", 1, 1),
    ("19698", "Santander de Quilichao", "Cauca", "Norte del Cauca", "Troncal Industrial", "Troncal 24h", "Hub Regional Yumbo / Cali", 1, 1),
    ("19573", "Puerto Tejada", "Cauca", "Norte del Cauca", "Troncal Industrial", "Troncal 24h", "Hub Regional Yumbo / Cali", 1, 0),
    ("19532", "Patía (El Bordo)", "Cauca", "Sur del Cauca", "Regional", "Regional 48h", "Hub Popayán", 1, 0),
    ("19548", "Piendamó", "Cauca", "Centro", "Regional", "Regional 48h", "Hub Popayán", 1, 0),

    # Norte de Santander
    ("54001", "Cúcuta", "Norte de Santander", "Andina Nororiental", "Urbana Principal", "Troncal 24h", "Hub Cúcuta", 1, 1),
    ("54498", "Ocaña", "Norte de Santander", "Occidente", "Regional", "Regional 48h", "Hub Cúcuta / Bucaramanga", 1, 0),
    ("54874", "Villa del Rosario", "Norte de Santander", "Frontera", "Urbana Metropolitana", "Troncal 24h", "Hub Cúcuta", 1, 0),
    ("54405", "Los Patios", "Norte de Santander", "Metropolitana", "Urbana Metropolitana", "Troncal 24h", "Hub Cúcuta", 1, 0),
    ("54518", "Pamplona", "Norte de Santander", "Andina", "Regional Estudiantil", "Regional 48h", "Hub Cúcuta", 1, 0),
    ("54810", "Tibú", "Norte de Santander", "Catatumbo", "Reexpedición Especial", "Reexpedición 72h", "Hub Cúcuta", 0, 0),

    # Cesar
    ("20001", "Valledupar", "Cesar", "Caribe", "Urbana Principal", "Troncal 24h", "Hub Valledupar / Malambo", 1, 1),
    ("20011", "Aguachica", "Cesar", "Sur del Cesar", "Troncal Logística", "Troncal 24h-48h", "Hub Bucaramanga / Valledupar", 1, 0),
    ("20013", "Agustín Codazzi", "Cesar", "Centro", "Regional", "Regional 48h", "Hub Valledupar", 1, 0),
    ("20060", "Bosconia", "Cesar", "Cruce Troncal", "Troncal Estratégica", "Troncal 24h", "Hub Valledupar", 1, 0),
    ("20228", "Curumaní", "Cesar", "Centro", "Regional", "Regional 48h", "Hub Valledupar", 1, 0),

    # Córdoba
    ("23001", "Montería", "Córdoba", "Caribe", "Urbana Principal", "Troncal 24h", "Hub Montería / Malambo", 1, 1),
    ("23162", "Cereté", "Córdoba", "Caribe", "Troncal Agrícola", "Troncal 24h-48h", "Hub Montería", 1, 0),
    ("23660", "Sahagún", "Córdoba", "Sabanas", "Regional", "Regional 48h", "Hub Montería", 1, 0),
    ("23417", "Santa Cruz de Lorica", "Córdoba", "Bajo Sinú", "Regional", "Regional 48h", "Hub Montería", 1, 0),
    ("23466", "Montelíbano", "Córdoba", "San Jorge", "Regional Minera", "Regional 48h", "Hub Montería", 1, 0),
    ("23555", "Planeta Rica", "Córdoba", "Sabanas", "Regional", "Regional 48h", "Hub Montería", 1, 0),

    # Sucre
    ("70001", "Sincelejo", "Sucre", "Caribe", "Urbana Principal", "Troncal 24h", "Hub Sincelejo / Montería", 1, 1),
    ("70215", "Corozal", "Sucre", "Caribe", "Urbana Metropolitana", "Troncal 24h", "Hub Sincelejo", 1, 0),
    ("70708", "San Marcos", "Sucre", "San Jorge", "Regional", "Regional 48h", "Hub Sincelejo", 1, 0),
    ("70820", "Santiago de Tolú", "Sucre", "Golfo de Morrosquillo", "Regional Turística", "Regional 48h", "Hub Sincelejo", 1, 0),
    ("70678", "Sampués", "Sucre", "Sabanas", "Regional Artesanal", "Regional 48h", "Hub Sincelejo", 1, 0),

    # Magdalena
    ("47001", "Santa Marta", "Magdalena", "Caribe", "Urbana Principal", "Troncal 24h", "Hub Santa Marta / Malambo", 1, 1),
    ("47189", "Ciénaga", "Magdalena", "Caribe", "Troncal", "Troncal 24h", "Hub Santa Marta / Malambo", 1, 0),
    ("47288", "Fundación", "Magdalena", "Caribe", "Regional", "Regional 48h", "Hub Santa Marta", 1, 0),
    ("47245", "El Banco", "Magdalena", "Sur del Magdalena", "Reexpedición Fluvial", "Reexpedición 72h", "Hub Bucaramanga", 1, 0),
    ("47555", "Plato", "Magdalena", "Río", "Regional", "Regional 48h", "Hub Malambo", 1, 0),

    # La Guajira
    ("44001", "Riohacha", "La Guajira", "Caribe", "Urbana Principal", "Troncal 24h-48h", "Hub Riohacha / Malambo", 1, 1),
    ("44430", "Maicao", "La Guajira", "Frontera Norte", "Troncal Comercial", "Troncal 24h-48h", "Hub Riohacha", 1, 0),
    ("44847", "Uribia", "La Guajira", "Alta Guajira", "Reexpedición Especial", "Reexpedición 72h-96h", "Hub Riohacha", 0, 0),
    ("44650", "San Juan del Cesar", "La Guajira", "Sur Guajiro", "Regional", "Regional 48h", "Hub Valledupar", 1, 0),
    ("44279", "Fonseca", "La Guajira", "Sur Guajiro", "Regional", "Regional 48h", "Hub Valledupar", 1, 0),

    # Chocó
    ("27001", "Quibdó", "Chocó", "Pacífica", "Urbana Departamental", "Regional 48h-72h", "Hub Medellín / Pereira", 0, 0),
    ("27361", "Istmina", "Chocó", "San Juan", "Regional", "Regional 72h", "Hub Pereira", 0, 0),
    ("27205", "Condoto", "Chocó", "San Juan", "Regional", "Regional 72h", "Hub Pereira", 0, 0),
    ("27075", "Bahía Solano", "Chocó", "Costa Pacífica", "Reexpedición Aérea", "Especial 5-8 días", "Hub Fontibón / MDE Aéreo", 0, 0),
    ("27006", "Acandí", "Chocó", "Golfo de Urabá", "Reexpedición Marítima", "Especial 5-8 días", "Hub Urabá", 0, 0),

    # Caquetá
    ("18001", "Florencia", "Caquetá", "Amazonía", "Urbana Departamental", "Regional 48h", "Hub Neiva / Florencia", 0, 0),
    ("18753", "San Vicente del Caguán", "Caquetá", "Amazonía", "Regional Ganadera", "Regional 72h", "Hub Neiva", 0, 0),
    ("18094", "Belén de los Andaquíes", "Caquetá", "Amazonía", "Regional", "Regional 72h", "Hub Neiva", 0, 0),
    ("18592", "Puerto Rico", "Caquetá", "Amazonía", "Regional", "Regional 72h", "Hub Neiva", 0, 0),

    # Casanare
    ("85001", "Yopal", "Casanare", "Orinoquía", "Urbana Principal", "Troncal 24h-48h", "Hub Yopal / Fontibón", 1, 1),
    ("85010", "Aguazul", "Casanare", "Orinoquía", "Troncal Petrolera", "Troncal 24h-48h", "Hub Yopal", 1, 0),
    ("85440", "Villanueva", "Casanare", "Sur de Casanare", "Regional", "Regional 48h", "Hub Villavicencio", 1, 0),
    ("85410", "Tauramena", "Casanare", "Orinoquía", "Regional Petrolera", "Regional 48h", "Hub Yopal", 1, 0),
    ("85250", "Paz de Ariporo", "Casanare", "Norte de Casanare", "Regional", "Regional 48h-72h", "Hub Yopal", 1, 0),

    # Arauca
    ("81001", "Arauca", "Arauca", "Orinoquía", "Fronteriza Departamental", "Regional 48h-72h", "Hub Cúcuta / Bucaramanga", 1, 0),
    ("81736", "Saravena", "Arauca", "Piedemonte", "Regional", "Regional 48h-72h", "Hub Bucaramanga", 1, 0),
    ("81794", "Tame", "Arauca", "Piedemonte", "Regional", "Regional 48h-72h", "Hub Yopal", 1, 0),
    ("81065", "Arauquita", "Arauca", "Frontera", "Regional Petrolera", "Regional 72h", "Hub Cúcuta", 0, 0),

    # Putumayo
    ("86001", "Mocoa", "Putumayo", "Amazonía", "Urbana Departamental", "Regional 48h-72h", "Hub Pasto / Neiva", 1, 0),
    ("86568", "Puerto Asís", "Putumayo", "Frontera Fluvial", "Troncal Comercial", "Regional 48h-72h", "Hub Pasto", 1, 0),
    ("86320", "Orito", "Putumayo", "Bajo Putumayo", "Regional Petrolera", "Regional 72h", "Hub Pasto", 1, 0),
    ("86865", "Valle del Guamuez (La Hormiga)", "Putumayo", "Frontera", "Regional", "Regional 72h", "Hub Pasto", 0, 0),

    # San Andrés y Providencia
    ("88001", "San Andrés Isla", "San Andrés y Providencia", "Insular", "Insular Principal", "Aérea Especial 3-5 días", "Hub Fontibón (Carga Aérea El Dorado)", 1, 0),
    ("88564", "Providencia y Santa Catalina", "San Andrés y Providencia", "Insular", "Insular Remota", "Marítima Especial 5-8 días", "Hub San Andrés Isla", 0, 0),

    # Amazonas
    ("91001", "Leticia", "Amazonas", "Amazonía", "Urbana Fronteriza Tripartita", "Aérea Exclusiva 3-5 días", "Hub Fontibón (Vuelo de Carga BOG)", 1, 0),
    ("91540", "Puerto Nariño", "Amazonas", "Amazonía", "Fluvial Remota", "Fluvial Especial 6-10 días", "Hub Leticia", 0, 0),

    # Guainía
    ("94001", "Inírida", "Guainía", "Amazonía", "Urbana Fluvial", "Aérea / Fluvial Especial 4-7 días", "Hub Fontibón (Carga Aérea BOG)", 0, 0),

    # Guaviare
    ("95001", "San José del Guaviare", "Guaviare", "Amazonía", "Urbana Departamental", "Regional Terrestre 48h", "Hub Villavicencio", 1, 0),
    ("95015", "Calamar", "Guaviare", "Amazonía", "Reexpedición Selva", "Reexpedición 72h-96h", "Hub San José del Guaviare", 0, 0),
    ("95025", "El Retorno", "Guaviare", "Amazonía", "Regional", "Regional 72h", "Hub San José del Guaviare", 0, 0),

    # Vaupés
    ("97001", "Mitú", "Vaupés", "Amazonía", "Urbana Selvática", "Aérea Exclusiva 3-6 días", "Hub Fontibón (Carga Aérea BOG)", 0, 0),

    # Vichada
    ("99001", "Puerto Carreño", "Vichada", "Orinoquía", "Fronteriza Fluvial", "Aérea / Terrestre 4-7 días", "Hub Villavicencio / Fontibón", 0, 0),
    ("99773", "Cumaribo", "Vichada", "Altillanura", "Reexpedición Extensa", "Reexpedición 5-8 días", "Hub Villavicencio", 0, 0),
    ("99524", "La Primavera", "Vichada", "Río Meta", "Regional", "Regional 72h-96h", "Hub Villavicencio", 0, 0)
]

# Destinos Internacionales oficiales (Courier Internacional TransLogix Express)
PAISES_DATA = [
    ("Estados Unidos", "US", "Norteamérica", "2 a 4 días hábiles", "Hub Fontibón / Carga Aeropuerto El Dorado (BOG)", "DIAN Régimen Envíos Urgentes (Courier)", 1),
    ("España", "ES", "Europa", "3 a 5 días hábiles", "Hub Fontibón / Aeropuerto El Dorado (BOG) / Barajas (MAD)", "Aduana UE DUA Exportación", 1),
    ("México", "MX", "Norteamérica", "3 a 5 días hábiles", "Hub Fontibón / AICM (MEX)", "Trámite Pedimento de Importación", 1),
    ("Panamá", "PA", "Centroamérica", "1 a 3 días hábiles", "Hub Fontibón / Aeropuerto Tocumen (PTY)", "Conexión Hub Pacífico Zona Libre Colón", 1),
    ("Ecuador", "ECU", "Sudamérica (CAN)", "2 a 4 días hábiles", "Hub Pasto-Ipiales (Terrestre) / BOG (Aéreo)", "CENAF Rumichaca / Aduana SENAE", 1),
    ("Perú", "PE", "Sudamérica (CAN)", "3 a 5 días hábiles", "Hub Fontibón / Aeropuerto Jorge Chávez (LIM)", "Aduana SUNAT Régimen Courier", 1),
    ("Chile", "CL", "Sudamérica", "4 a 6 días hábiles", "Hub Fontibón / Aeropuerto Arturo Merino Benítez (SCL)", "Aduana Nacional de Chile", 1),
    ("Canadá", "CA", "Norteamérica", "3 a 5 días hábiles", "Hub Fontibón / Aeropuertos YYZ / YVR", "CBSA Canada Border Services", 1),
    ("Alemania", "DE", "Europa", "3 a 6 días hábiles", "Hub Fontibón / Aeropuerto Frankfurt (FRA)", "Zollamt Alemania / UE", 1),
    ("Reino Unido", "GB", "Europa", "3 a 6 días hábiles", "Hub Fontibón / Aeropuerto Heathrow (LHR)", "HMRC Post-Brexit Clearance", 1),
    ("Brasil", "BR", "Sudamérica (Mercosur)", "4 a 7 días hábiles", "Hub Fontibón / Aeropuerto Guarulhos (GRU)", "Receita Federal do Brasil", 1),
    ("Costa Rica", "CR", "Centroamérica", "2 a 4 días hábiles", "Hub Fontibón / Aeropuerto Juan Santamaría (SJO)", "Aduana de Costa Rica", 1),
    ("República Dominicana", "DO", "Caribe", "3 a 5 días hábiles", "Hub Fontibón / Aeropuerto Las Américas (SDQ)", "Dirección General de Aduanas DGA", 1),
    ("Francia", "FR", "Europa", "4 a 6 días hábiles", "Hub Fontibón / Aeropuerto CDG París", "Douane Française", 1),
    ("Italia", "IT", "Europa", "4 a 6 días hábiles", "Hub Fontibón / Aeropuerto Malpensa (MXP) / FCO", "Agenzia delle Dogane", 1),
    ("Argentina", "AR", "Sudamérica (Mercosur)", "5 a 8 días hábiles", "Hub Fontibón / Aeropuerto Ezeiza (EZE)", "AFIP / Aduana Argentina", 1)
]

def init_geo_db():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Tabla colombia_municipios
    cur.execute("""
    CREATE TABLE IF NOT EXISTS colombia_municipios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_dane TEXT UNIQUE NOT NULL,
        municipio TEXT NOT NULL,
        departamento TEXT NOT NULL,
        region TEXT NOT NULL,
        tipo_cobertura TEXT NOT NULL,
        tiempo_entrega_std TEXT NOT NULL,
        hub_asignado TEXT NOT NULL,
        servicio_refrigerado INTEGER DEFAULT 1,
        same_day INTEGER DEFAULT 0
    )
    """)

    # Tabla destinos_internacionales
    cur.execute("""
    CREATE TABLE IF NOT EXISTS destinos_internacionales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pais TEXT UNIQUE NOT NULL,
        codigo_iso TEXT NOT NULL,
        continente TEXT NOT NULL,
        tiempo_entrega TEXT NOT NULL,
        hub_salida TEXT NOT NULL,
        regimen_aduanero TEXT NOT NULL,
        activo INTEGER DEFAULT 1
    )
    """)

    # Limpiar e insertar registros
    cur.execute("DELETE FROM colombia_municipios")
    cur.execute("DELETE FROM destinos_internacionales")

    cur.executemany("""
    INSERT INTO colombia_municipios 
    (codigo_dane, municipio, departamento, region, tipo_cobertura, tiempo_entrega_std, hub_asignado, servicio_refrigerado, same_day)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, COLOMBIA_DATA)

    cur.executemany("""
    INSERT INTO destinos_internacionales
    (pais, codigo_iso, continente, tiempo_entrega, hub_salida, regimen_aduanero, activo)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, PAISES_DATA)

    conn.commit()
    total_mun = cur.execute("SELECT count(*) FROM colombia_municipios").fetchone()[0]
    total_dep = cur.execute("SELECT count(DISTINCT departamento) FROM colombia_municipios").fetchone()[0]
    total_paises = cur.execute("SELECT count(*) FROM destinos_internacionales").fetchone()[0]
    conn.close()

    print(f"✅ Base de datos geográfica inicializada con éxito:")
    print(f"   - {total_dep} Departamentos cubiertos (32 Departamentos + Bogotá D.C.)")
    print(f"   - {total_mun} Municipios y cabeceras estratégicas")
    print(f"   - {total_paises} Países y destinos internacionales oficiales")

if __name__ == "__main__":
    init_geo_db()

# backend.py
from mailmerge import MailMerge
import os

# --- 1. BASE DE DATOS SIMULADA (adaptada a los campos del Word) ---
EXPEDIENTES = {
    "123": {
        "1": "123,540",
        "2": "3,362",
        "3": "2 de septiembre de 2025",
        "4": "Constructora Acme S.A. de C.V.",
        "6": "Juan Pérez García",
        "7": "Sofía Martínez López",
        "8": "Lic. Mario Vargas y Lic. Ana Jiménez",          # Representantes del Banco
        "9": "Departamento 501, Torre A, Condominio 'Vistas del Parque', Calle Reforma 1500, Ciudad de México", # Inmueble
        "10": "Al Norte: 20m con Depto. 502; Al Sur: 20m con área común; Al Este: 10m con fachada exterior.", # Linderos
        "11": "1.25% (uno punto veinticinco por ciento)",      # Indiviso
        "14": "045-88231-05-6 (CERO CUARENTA Y CINCO...)",     # Cuenta Predial
        "15": "9876543210123456 (NUEVE OCHO SIETE...)"         # Cuenta de Agua
    },
    "124": {
        "1": "123,541",
        "2": "3,363",
        "3": "3 de septiembre de 2025",
        "4": "María Elena Rodríguez (Persona Física)",
        "6": "N/A",
        "7": "Carlos Sánchez Ruiz",
        "8": "Lic. Carlos Beltrán y Lic. Sofía Navarro",
        "9": "Casa habitación, Lote 15, Manzana 8, Calle Las Flores 21, Colonia Jardines, Ciudad de México",
        "10": "Al Norte: 10m con Lote 14; Al Sur: 10m con Lote 16; Al Este: 25m con Calle Las Flores.",
        "11": "N/A (Copropiedad no aplicable)",
        "14": "033-54879-11-2 (CERO TREINTA Y TRES...)",
        "15": "1234567890987654 (UNO DOS TRES...)"
    },
    "125": {
        "1": "123,542",
        "2": "3,364",
        "3": "4 de septiembre de 2025",
        "4": "Innovaciones Tecnológicas del Futuro S.A. de C.V.",
        "6": "Laura Gómez",
        "7": "N/A",
        "8": "Lic. Fernando Ponce y Lic. Gabriela Ríos",
        "9": "Local Comercial B, Plaza 'El Sol', Avenida Insurgentes Sur 3000, Ciudad de México",
        "10": "Al Norte: 5m con Local A; Al Sur: 5m con Local C; Al Este: 15m con fachada de la plaza.",
        "11": "0.80% (cero punto ochenta por ciento)",
        "14": "001-99854-02-B (CERO CERO UNO...)",
        "15": "5544332211009988 (CINCO CINCO CUATRO...)"
    },
    "126": {
        "1": "123,543",
        "2": "3,365",
        "3": "5 de septiembre de 2025",
        "4": "Ricardo Morales (Persona Física)",
        "6": "N/A",
        "7": "Ana Torres",
        "8": "Lic. Roberto Garza y Lic. Lucía Méndez",
        "9": "Terreno rústico, Parcela 72, Ejido 'La Esperanza', Tlalpan, Ciudad de México",
        "10": "Medidas y colindancias según plano oficial adjunto al apéndice.",
        "11": "N/A",
        "14": "999-55522-00-1 (NOVECIENTOS NOVENTA Y NUEVE...)",
        "15": "7788990011223344 (SIETE SIETE OCHO...)"
    }
}

# --- 2. DEFINICIÓN DE PLANTILLAS Y SUS CAMPOS REQUERIDOS ---
CONTRATOS = {
    "poder_v1": {
        "path": "plantillas/poder_v1.docx",
        "fields": ["1", "2", "3", "4", "6", "7"]
    },
    "constitutiva_v1": {
        "path": "plantillas/constitutiva_v1.docx",
        "fields": ["1", "2", "3", "4", "6", "7"] # <-- CAMBIO REALIZADO AQUÍ
    },
    "compraventa_v1": {
        "path": "plantillas/compraventa_v1.docx",
        "fields": ["1", "2", "3", "8", "9", "10","11","14","15"] # <-- CAMBIO REALIZADO AQUÍ
    }
}

# --- 3. FUNCIÓN PARA GENERAR EL DOCUMENTO ---
def generar_documento(contrato_id, expediente_id):
    if contrato_id not in CONTRATOS:
        return f"Error: El contrato ID '{contrato_id}' no está definido."
    if expediente_id not in EXPEDIENTES:
        return f"Error: El expediente ID '{expediente_id}' no existe."

    info_contrato = CONTRATOS[contrato_id]
    datos_expediente = EXPEDIENTES[expediente_id]
    
    plantilla_path = info_contrato["path"]
    campos_requeridos = info_contrato["fields"]
    
    datos_para_merge = {}
    for campo in campos_requeridos:
        datos_para_merge[campo] = datos_expediente.get(campo, "CAMPO_NO_ENCONTRADO")

    if not os.path.exists('generados'):
        os.makedirs('generados')
    
    output_path = f"generados/{contrato_id}_{expediente_id}_final.docx"

    try:
        documento = MailMerge(plantilla_path)
        documento.merge(**datos_para_merge)
        documento.write(output_path)
        return f"✅ ¡Éxito! Documento generado en: '{output_path}'"
    except Exception as e:
        return f"❌ Error al generar el documento: {e}"
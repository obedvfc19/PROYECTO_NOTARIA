# main.py
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from backend import generar_documento

# --- 1. CARGAR EL MODELO FINE-TUNEADO ---
print("Cargando modelo fine-tuneado...")
base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
adapter_path = "./modelo_final_notaria"

device = "cuda" if torch.cuda.is_available() else "cpu"
base_model = AutoModelForCausalLM.from_pretrained(base_model_name, torch_dtype=torch.float16, device_map=device)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model, adapter_path)
print(f"¡Modelo cargado en {device.upper()}!")

# --- 2. FUNCIÓN PARA INTERACTUAR CON EL LLM (CON EXTRACTOR INTELIGENTE) ---
def obtener_json_del_llm(instruccion_usuario):
    system_prompt = "Eres un asistente experto en notaría. Tu única función es identificar el ID del contrato y el ID del expediente de la petición del usuario y responder únicamente con un objeto JSON."
    prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{instruccion_usuario}</s>\n<|assistant|>\n"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    outputs = model.generate(
        **inputs, 
        max_new_tokens=50, 
        do_sample=False, 
        eos_token_id=tokenizer.eos_token_id
    )
    
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    json_part_raw = response_text.split('<|assistant|>')[-1].strip()

    # --- LÓGICA DE EXTRACCIÓN MEJORADA ---
    # Esta función buscará el primer JSON completo y válido en el texto.
    try:
        start_index = json_part_raw.find('{')
        if start_index == -1:
            raise ValueError("No se encontró el inicio de un objeto JSON ('{').")

        brace_level = 0
        end_index = -1
        for i in range(start_index, len(json_part_raw)):
            char = json_part_raw[i]
            if char == '{':
                brace_level += 1
            elif char == '}':
                brace_level -= 1
            
            if brace_level == 0:
                end_index = i
                break
        
        if end_index == -1:
            raise ValueError("El objeto JSON en el texto está incompleto (llaves sin cerrar).")

        json_cleaned = json_part_raw[start_index : end_index + 1]
        return json.loads(json_cleaned)

    except (ValueError, json.JSONDecodeError) as e:
        print(f"DEBUG: Error al extraer/parsear JSON. Razón: {e}")
        print(f"DEBUG: Respuesta cruda del modelo: {json_part_raw}")
        return None

# --- 3. BUCLE PRINCIPAL DE LA APLICACIÓN (Sin cambios) ---
if __name__ == "__main__":
    print("\n--- Asistente de Notaría 110 (Piloto) ---")
    print("Escribe tu petición (ej. 'elaborame poder_v1 con expediente 123') o 'salir' para terminar.")
    
    while True:
        peticion = input("> ")
        if peticion.lower() == 'salir':
            break
            
        print("Procesando petición con el LLM...")
        datos = obtener_json_del_llm(peticion)
        
        if datos and "contrato_id" in datos and "expediente_id" in datos:
            contrato_id = datos["contrato_id"]
            expediente_id = datos["expediente_id"]
            
            print(f"🤖 LLM identificó -> Contrato: {contrato_id}, Expediente: {expediente_id}")
            print("Generando documento...")
            
            resultado = generar_documento(contrato_id, expediente_id)
            print(resultado)
        else:
            print(" Lo siento, no pude entender la petición. Por favor, sé más específico.")

    print("--- Sesión terminada ---")
##############################################################################
# fine_tune.py
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig
from trl import SFTTrainer

# 1. Configuración del modelo y tokenizador
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,   # 👈 ahora es dtype, no torch_dtype
    device_map="auto",
    use_cache=False
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 2. Cargar y formatear el dataset
dataset = load_dataset("csv", data_files="dataset.csv", split="train")

def format_prompt(row):
    chat_template = [
        {"role": "system", "content": "Eres un asistente experto en notaría. Tu única función es identificar el ID del contrato y el ID del expediente de la petición del usuario y responder únicamente con un objeto JSON."},
        {"role": "user", "content": row["instruccion"]},
        {"role": "assistant", "content": row["json_output"]}
    ]
    return {"text": tokenizer.apply_chat_template(chat_template, tokenize=False)}

dataset = dataset.map(format_prompt)

# 3. Configuración de LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 4. Configuración de entrenamiento
training_args = TrainingArguments(
    output_dir="./modelo_notaria_piloto",
    num_train_epochs=10,
    per_device_train_batch_size=2,
    logging_steps=1,
    learning_rate=2e-4,
    save_strategy="epoch",
    bf16=True,  # 👈 usa bf16 si tu GPU lo soporta
    gradient_accumulation_steps=2,
)

# 5. Entrenador con nueva API de SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    tokenizer=tokenizer,              # 👈 ahora sí es válido
    args=training_args,
    max_seq_length=512,
    formatting_func=lambda ex: ex["text"],  # 👈 cómo tomar el texto
)

# 6. Iniciar el entrenamiento y guardar el modelo
print("Iniciando fine-tuning...")
trainer.train()
trainer.save_model("./modelo_final_notaria")
print("¡Fine-tuning completado! Modelo guardado en './modelo_final_notaria'")

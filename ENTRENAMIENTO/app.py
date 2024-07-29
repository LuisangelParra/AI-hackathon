from unsloth import FastLanguageModel
import torch
import os
from transformers import TextStreamer
from datasets import load_dataset
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported
import numpy as np

# 1. Configuración
max_seq_length = 2048
dtype = None
load_in_4bit = True
alpaca_prompt = """Basado en la pregunta, generar una respuesta adecuada. Eres un bot para el departamento de Administración de la Universidad del Norte, creado con el fin de resolver dudas de empleados relacionadas a procesos internos del departamento.

### Pregunta:
{}
### Respuesta:
{}

"""

pregunta = "¿Qué sistemas de información maneja la Dirección de Tecnología Informática y Comunicaciones?"
huggingface_model_name = "LuisangelParra/Meta-Llama-3.1-8B-bnb-4bit-Uninorte-Admin"

# 2. Before Training
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
    token = "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",
)

FastLanguageModel.for_inference(model)
inputs = tokenizer(
    [
        alpaca_prompt.format(
            pregunta, # Pregunta
            "", # Respuesta

        )
    ], return_tensors="pt").to("cuda")

text_streamer = TextStreamer(tokenizer)
_ = model.generate(**inputs, streamer = text_streamer, max_new_tokens=1000)


# 3. Load data
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('data.csv')

df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

df_train.to_csv('train_set.csv', index=False)
df_test.to_csv('test_set.csv', index=False)

EOS_TOKEN = tokenizer.eos_token
def formatting_prompts_func(examples):
    preguntas = examples["pregunta"]
    respuestas = examples["respuesta"]
    texts = []
    for pregunta, respuesta in zip(preguntas, respuestas):
        text = alpaca_prompt.format(pregunta, respuesta) + EOS_TOKEN
        text.append(text)
    return {"text": texts}
pass
dataset = load_dataset("csv",  data_files={'train': "train_set.csv",'test': "test_set.csv"})
dataset = dataset.map(formatting_prompts_func, batched=True)

# 4. Training
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        # num_train_epochs = 1,
        max_steps=100,
        learning_rate=2e-4,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "respuestas",
    )
)


gpu_stats = torch.cuda.get_device_properties(0)
start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB")
print(f"{start_gpu_memory} GB of memory is already reserved.")

trainer_stats = trainer.train()

used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
used_memory_for_lora = round((used_memory - start_gpu_memory), 3)
used_percentage = round((used_memory / max_memory) * 100, 3)
lora_percentage = round((used_memory_for_lora / max_memory) * 100, 3)

print(f"{trainer_stats.metrics['train_runtime']} Seconds used for training\n")
print(f"{round(trainer_stats.metrics['train_runtime']/60,2)} Minutes used for training\n")
print(f"Peak memory usage: {used_memory} GB")
print(f"Memory used for LORA: {used_memory_for_lora} GB")
print(f"Memory used percentage: {used_percentage}%")
print(f"LORA memory percentage: {lora_percentage}%")

#5. After Training
FastLanguageModel.for_inference(model)
inputs = tokenizer(
    [
        alpaca_prompt.format(
            pregunta, # Pregunta
            "", # Respuesta

        )
    ], return_tensors="pt").to("cuda")
text_streamer = TextStreamer(tokenizer)
_= model.generate(**inputs, streamer = text_streamer, max_new_tokens=1000)

# 6. Save the model
model.save_pretrained("lora_model")
tokenizer.save_pretrained("lora_model")
model.push_to_hub(huggingface_model_name, token = "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")
tokenizer.push_to_hub(huggingface_model_name, token = "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")

#Merge to 16bit

if True: model.save_pretrained_merged("model", tokenizer, save_method = "merged_16bit")
if True: model.push_to_hub_merged(huggingface_model_name,tokenizer, save_method = "merged_16bit", token = "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")

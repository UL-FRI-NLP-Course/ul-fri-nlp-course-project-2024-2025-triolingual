from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset
import json
import torch

print("tuka")

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
DATA_PATH = "qa_dataset_wikidata.json"
OUTPUT_DIR = "./mistral-lora"
MAX_LENGTH = 512

def load_dataset_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)


    formatted = [{
        "text": f"### Instruction:\n{ex['question']}\n\n### Response:\n{ex['answer']}"
    } for ex in raw]

    return Dataset.from_list(formatted)

dataset = load_dataset_from_json(DATA_PATH)

print("dataset loaded")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token



def tokenize(example):
    return tokenizer(
        example["text"],
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
    )

tokenized_dataset = dataset.map(tokenize, batched=True)

print("tokenization")

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_4bit=True
)

print("fine-tunning")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=30,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
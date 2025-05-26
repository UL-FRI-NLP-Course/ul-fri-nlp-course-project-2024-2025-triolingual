from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "./mistral-lora"
MAX_LENGTH = 512

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_answer(question):
    prompt = f"### Instruction:\n{question}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=MAX_LENGTH).to(device)
    outputs = model.generate(
        **inputs,
        max_length=MAX_LENGTH,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = text.split("### Response:")[-1].strip()
    return answer

if __name__ == "__main__":

    questions = [
        "Who is the head of state of United Kingdom?"
    ]
    
    for q in questions:
        print("Q:", q)
        print("A:", generate_answer(q))
        print("-" * 50)

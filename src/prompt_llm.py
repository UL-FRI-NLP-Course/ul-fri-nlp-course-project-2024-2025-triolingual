from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np


def load_index(index_path):
    return faiss.read_index(index_path)

def load_metadata(metadata_path):
    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)

def embed_query(query, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(emb)
    return emb

def retrieve_facts(query, index, metadata, top_k=10):
    query_emb = embed_query(query)
    distances, indices = index.search(query_emb, top_k)  # get closest facts
    results = [metadata[i] for i in indices[0]]
    return results

class Mistral7BHandler: 

    def __init__(self, model_path = "mistralai/Mistral-7B-Instruct-v0.3", device = None):

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        # print(f"Load model on {self.device}.")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, 
            device_map = "auto" if self.device == "cuda" else None, 
            torch_dtype = torch.float16 if self.device == "cuda" else torch.float32, 
            trust_remote_code = True, 
            low_cpu_mem_usage = True,
        )
        #.to(self.device)
        # print(next(self.model.parameters()).device)


    def generate(self, prompt, max_length = 32, temperature = 0.7, top_p = 0.9): 
        
        inputs = self.tokenizer(prompt, return_tensors = "pt").to(self.device) # tokenize input prompt 
        start_time = time.time()
        outputs = self.model.generate(
            **inputs, 
             max_new_tokens=32,
            # temperature = temperature, 
            # top_p = top_p, 
            do_sample = False, 
            eos_token_id=self.tokenizer.eos_token_id, # stop generation at the end of sequence token
            pad_token_id=self.tokenizer.pad_token_id # pad tokens to align inputs if needed
        )

        elapsed = time.time() - start_time
        print(f"Generation took {elapsed:.2f} seconds")
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return decoded

def rag_generate(handler, query, index, metadata, use_rag=False):
    
    if use_rag:
        retrieved_facts = retrieve_facts(query, index, metadata)
        context = " ".join([fact['text'] for fact in retrieved_facts])
        prompt = f"Context: {context}\nQuestion: {query}"
        print(prompt)
        prompt = f"Context: {context}\nQuestion: {query}\nAnswer: "


    else:
        prompt = query

    return handler.generate(prompt)


def evaluate_rag(handler, index, metadata, qa_path, use_rag=True):
    with open(qa_path, "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)

    print(qa_pairs)
    print(qa_pairs[0])
    #qa_pairs = qa_pairs[0]
    qa_pairs = qa_pairs[:30]


    results = []

    for entry in qa_pairs:
        question = entry["question"]
        ground_truth = entry["answer"]

        print(f"\n---\nQuestion: {question}")
        response = rag_generate(handler, question, index, metadata, use_rag=use_rag)
        print(f"Ground Truth: {ground_truth}")
        print(f"Model Answer: {response}")

        results.append({
            "question": question,
            "ground_truth": ground_truth,
            "predicted": response
        })

        
    with open("rag_eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":

    handler = Mistral7BHandler()

    index = load_index("../data/leaders_index.faiss")
    metadata = load_metadata("../data/leaders_metadata.json")

    qa_path = r"../data/qa_eval_data.json"

    evaluate_rag(handler, index, metadata, qa_path)

    #prompt = "Who is the Leader of Slovenia?"
    #print("Prompt: \n", prompt)
    #output = handler.generate(prompt)
    #print("Model Output:\n", output)

    #output = rag_generate(handler, prompt, index, metadata, use_rag=True)
    #print("Model Output RAG:\n", output)




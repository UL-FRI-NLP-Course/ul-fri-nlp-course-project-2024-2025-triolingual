import json
from datasets import Dataset

DATA_PATH = r"C:\Users\Biljana\Desktop\1letnikmaster\NLP_project\ul-fri-nlp-course-project-2024-2025-triolingual\data\qa_dataset_wikidata.json"

def load_and_convert_data(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    formatted = [{
        "text": f"### Instruction:\n{item['question']}\n\n### Response:\n{item['answer']}"
    } for item in raw]

    return Dataset.from_list(formatted)

dataset = load_and_convert_data(DATA_PATH)
print(dataset)

for i in range(len(dataset)):

    text = dataset[i]['text']
    lines = text.split("\n")

    question_line = lines[1].strip()  
    answer_line = lines[4].strip()  

    print("Question:", question_line)
    print("Answer:", answer_line)


"""
example: 
Question: Where was the head of state of Kingdom of the Netherlands born?
Answer: University Medical Center Utrecht
Question: Where was the head of state of Malta born?
Answer: Rabat
Question: Where was the head of state of Czech Republic born?
Answer: Planá
Question: Where was the head of state of Latvia born?
Answer: Jūrmala
Question: What university did the head of state of Luxembourg attend?
Answer: University of Geneva
Question: What university did the head of state of Luxembourg attend?
Answer: Royal Military Academy Sandhurst
Question: What university did the head of state of Luxembourg attend?
Answer: Lycée classique de Diekirch
Question: What university did the head of state of Sweden attend?
Answer: Uppsala University
Question: What university did the head of state of Sweden attend?

"""
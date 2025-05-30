import json
from bert_score import score
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import matplotlib.pyplot as plt
import numpy as np
import sys

# Download NLTK data (first time only)
import nltk
nltk.download('punkt')

def load_json_file(filepath):
    """Load JSON file with UTF-8 encoding"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        # Try with different encodings if UTF-8 fails
        try:
            with open(filepath, 'r', encoding='utf-16') as f:
                return json.load(f)
        except:
            with open(filepath, 'r', encoding='latin-1') as f:
                return json.load(f)

def evaluate_answers(data):
    """Perform all evaluations on QA pairs"""
    # Extract texts
    questions = [item['question'] for item in data]
    ground_truths = [item['ground_truth'] for item in data]
    predictions = [item['predicted'] for item in data]

    # 1. BERTScore
    print("Running BERTScore...")
    P_bert, R_bert, F1_bert = score(
        predictions, ground_truths, 
        lang='en', 
        model_type='bert-base-uncased',
        verbose=True
    )

    # 2. ROUGE-L
    print("\nCalculating ROUGE-L...")
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rouge_results = [scorer.score(gt, pred)['rougeL'] for gt, pred in zip(ground_truths, predictions)]

    # 3. BLEU
    print("\nCalculating BLEU...")
    smooth = SmoothingFunction().method4
    bleu_scores = []
    for gt, pred in zip(ground_truths, predictions):
        try:
            bleu = sentence_bleu(
                [gt.split()], 
                pred.split(),
                smoothing_function=smooth,
                weights=(0.25, 0.25, 0.25, 0.25)
            )
            bleu_scores.append(bleu)
        except:
            bleu_scores.append(0.0)  # Default score for empty/error cases

    # Compile results
    results = []
    for i in range(len(data)):
        results.append({
            **data[i],
            'scores': {
                'bertscore': {
                    'precision': float(P_bert[i]),
                    'recall': float(R_bert[i]),
                    'f1': float(F1_bert[i])
                },
                'rougeL': {
                    'precision': rouge_results[i].precision,
                    'recall': rouge_results[i].recall,
                    'fmeasure': rouge_results[i].fmeasure
                },
                'bleu': float(bleu_scores[i])
            }
        })
    
    return results

# Load your data
try:
    data = load_json_file('input.json')
except Exception as e:
    print(f"Error loading JSON file: {e}")
    sys.exit(1)

# Run evaluation
evaluated_data = evaluate_answers(data)

# Save results
try:
    with open('evaluated_results.json', 'w', encoding='utf-8') as f:
        json.dump(evaluated_data, f, indent=2, ensure_ascii=False)
except Exception as e:
    print(f"Error saving results: {e}")

# Generate report
avg_scores = {
    'BERTScore F1': np.mean([item['scores']['bertscore']['f1'] for item in evaluated_data]),
    'ROUGE-L F1': np.mean([item['scores']['rougeL']['fmeasure'] for item in evaluated_data]),
    'BLEU': np.mean([item['scores']['bleu'] for item in evaluated_data])
}

print("\n=== Evaluation Summary ===")
for metric, value in avg_scores.items():
    print(f"{metric}: {value:.3f}")

# Visualization
# Replace the visualization section with this corrected version:

plt.figure(figsize=(15, 5))
metrics = [
    ('bertscore', 'f1', 'BERTScore F1', 'skyblue'),
    ('rougeL', 'fmeasure', 'ROUGE-L F1', 'lightgreen'),
    ('bleu', None, 'BLEU Score', 'salmon')
]

for i, (metric, subkey, title, color) in enumerate(metrics):
    plt.subplot(1, 3, i+1)
    if subkey:
        values = [item['scores'][metric][subkey] for item in evaluated_data]
    else:
        values = [item['scores'][metric] for item in evaluated_data]
    plt.hist(values, bins=20, color=color, edgecolor='black')
    plt.title(title)
    plt.xlabel('Score')
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('evaluation_metrics.png', bbox_inches='tight')
plt.show()

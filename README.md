# Natural language processing course: `Integrating Structured Knowledge into Large Language Models`
**University of Ljubljana — 2024/2025**


This repository contains the coursework for the **NLP course** at the University of Ljubljana, focusing on enhancing **Large Language Models (LLMs)** with **structured knowledge**. It includes implemented experiments, literature reviews, and final results in both notebook and report form.

---

## 🔍 Project Overview

Knowledge Graphs and Vector Databases serve distinct purposes:

- **Knowledge Graphs**: Structure data into **entities** (nodes) and **relationships** (edges), enabling reasoning, context understanding, and answering complex queries through explicit connections.
- **Vector Databases**: Store data as high-dimensional **semantic vectors** ideal for **fast similarity-based retrieval** of unstructured data (e.g., text, images), though they lack interpretability and reasoning ability.

By **integrating both approaches**, we aim to combine the **semantic power** of vectors with the **explicit reasoning** of knowledge graphs for more intelligent and interpretable systems.

![alt text](related_work/img/image-6.png)

---



## 🚀 Getting Started

### 🔧 Prerequisites

Before running the project, make sure you have:

- Python 3.8+
- Jupyter Notebook 
- JupyterLab
- Recommended Python libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `networkx`
  - `scikit-learn`
  - `openai` (if using GPT APIs)


## 📁 Repository Structure

```bash
├── improved_kg_vectorstore/         # Improved KG-vectorstore implementations
├── kg_vectorstore_free/             # Basic version of KG vector store
├── kg_vectorstore_completely_free/  # Fully open implementation
├── lib/                             # Supporting libraries and tools
├── related_work/                    # Literature and prior work
│   ├── img/                         # Reference images
│   └── initial_plan.md              # Initial planning notes
├── report/                          # Final course report
│   ├── code/                        # Code used for figures or analysis
│   ├── fig/                         # Figures used in the report
│   ├── ds_report.cls                # Report LaTeX class file
│   ├── report.tex                   # Main LaTeX source
│   ├── report.pdf                   # Final compiled report
│   ├── report.bib                   # Bibliography
│   └── logo.png                     # University logo
├── notebook_LLM.ipynb              # Main Jupyter notebook with code + analysis
├── combined_qa_dataset.json        # Merged QA dataset
├── complex_qa_dataset.json         # Dataset with complex reasoning paths
├── sample_kg_data.json             # Example Knowledge Graph data
├── world_leaders_qa_dataset.json   # Real-world QA dataset
├── reasoning_path_2.png            # Diagram: sample reasoning
├── knowledge_graph_2.html/.png     # Visualization of final knowledge graph
├── requirements.txt                # Required packages
├── .gitignore                      # Git ignore rules
├── LICENSE                         # License file
└── README.md                       # You are here 🚀
```

### 📦 Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/UL-FRI-NLP-Course/ul-fri-nlp-course-project-2024-2025-triolingual
``` 

```bash
cd ul-fri-nlp-course-project-2024-2025-triolingual
``` 
```bash
pip install -r requirements.txt
``` 
## 📚 Citation

If you use or reference this project, please consider citing the course or referencing the final report.

## 📜 License

This project is licensed under the **MIT License**.

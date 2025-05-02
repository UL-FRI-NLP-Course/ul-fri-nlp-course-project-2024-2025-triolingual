# Natural language processing course: `Integrating Structured Knowledge into Large Language Models`


**University of Ljubljana — 2024/2025**

This project aims to integrate structured knowledge into Large Language Models (LLMs) using a Retrieval-Augmented Generation (RAG) approach. We aim to construct a knowledge graph dataset containing world leaders and their related facts. Subgraphs are extracted and stored in a vector database. Based on a user question, the most semantically similar facts are retrieved and used to inform the model’s response. We also analyze the use of different LLM frameworks and how prompt formulation influences the generated answers.


##  Repository structure
- `src/` – Source code for graph processing and RAG pipeline  
- `data/` – Dataset of world leader QA pairs and knowledge graphs  
- `report/` – Report for the project  

<!-- 
## Project Description

Knowledge Graphs and Vector Databases serve distinct purposes:

- **Knowledge Graphs**: Structure data into **entities** (nodes) and **relationships** (edges), enabling reasoning, context understanding, and answering complex queries through explicit connections.
- **Vector Databases**: Store data as high-dimensional **semantic vectors** ideal for **fast similarity-based retrieval** of unstructured data (e.g., text, images), though they lack interpretability and reasoning ability.

By **integrating both approaches**, we aim to combine the **semantic power** of vectors with the **explicit reasoning** of knowledge graphs for more intelligent and interpretable systems.

<!-- ![alt text](related_work/img/image-6.png) -->

---



<!--
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
-->

##  Getting Started

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



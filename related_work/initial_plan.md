### ❓ Why integrating Knowledge Graphs in LLMs

- LLMs are proefcient at learning probabilistic language patterns and conversational tasks, but they lack the ability of recalling facts while generating knowledgegrounded content.
- To overcome these limitations, one of the proposed method is to integrate knowledge based graphs.
- KGs explicitly express relationships between
  entities and intuitively display the overall structure of knowledge
  and reasoning chains, making them proper choice for knowledge modeling.
- Good overview is provided here: [Give us the Facts: Enhancing Large Language Models With Knowledge Graphs for Fact-Aware Language Modeling](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10417790)

---

- Examples where LLMs tend to fail:
  - `Multi-hop reasoning`: which means that the answer, cannot be derrived from single fact.
    ex: Who is the grandmother of Barack Obama's daughters?
  - `Logical reasoning`:
    ex: If John is the brother of Alice, and Alice is the mother of Bob, what is John's relation to Bob?

---

### 🔗 Integration techniques of KGs

- Three types of integration techniques:
  ![alt text](img/image-2.png)
- We will likely use the first post-training enchancement.

- Different represntations of KGs:

- `Direct input augmentation`:
  - Change the input to the LLM, to include the KG
  - No retraining of the model.
  - It happens during inference / prediction.
- `Graph embedding based`: apply embedding techniques which converts the graphs to dense vectors.

  - The image represents different embeddings and their usage over time.
  - From all of the methods TransE is only knowledge graph embedding and the other are general embeddings.
    ![alt text](img/image-3.png)

- `Attention-Based fusion techniques`: Include the attention mechanism in two ways: 1. different weights for the text and KG or 2. different weights for the nodes within the KGs

---

### 📊 Datasets

- Not graph representation :

  - [Complex Web Questions Dataset (Hugging Face)](https://huggingface.co/datasets/drt/complex_web_questions/viewer/complex_web_questions/train?p=1&views%5B%5D=complex_web_questions_train&row=118)
  - [MetaQA](https://github.com/yuyuz/MetaQA) This one contatins 1,2,3-hop data, useful for testing.

- Graph-based datasets:

  - [DBpedia](https://www.dbpedia.org/resources/sparql/)
  - [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)
  - additionally we can try fusion of graphs from different sources.

- Main idea: pair questions with KGs

---

### 📚 Related work:

- In most of the papers, they start with some baseline models like BERT, T-5, and than compare their integration of KGs with other integration frameworks.

- [KG-BERT: BERT for Knowledge Graph Completion
  ](https://arxiv.org/pdf/1909.03193) Explained how BERT is fine-tuned for knlowedge graph prediction, not directly related to our topic. We can use the following KGs benchmark datasets, as used in this paper:
  ![alt text](img/image-5.png)

- [DRAGON Deep Bidirectional Language-Knowledge Graph Pretraining:](https://arxiv.org/pdf/2210.09338)

  - Eeach input is represented as pairs of text segments and relevant KG subgraphs. The model bidirectionally fuses information from both the text and the KG.
  - How the KGs are generated:
    main idea starting with a base KG, `ConceptNet` is used in the general domain, and the `UMLS KG` is used in the biomedical domain. Segments of the text input are mapped to corresponding nodes in the base KG, connecting them in this step. A relevant subgraph is extracted from the base KG, centered around these nodes. This subgraph is then further fused with the input text



# Song Similarity Finder with DBpedia and Node2Vec  

This project fetches **130,000 songs** from the **DBpedia knowledge graph** and creates embeddings in a vector space for artists, genres, and related artists. Using these embeddings, the app identifies songs similar to a given song based on cosine similarity.

---

## Features  

- **Data Fetching with SPARQL**: 
  - Retrieves songs and their metadata (artist, genre, related artists) from the DBpedia knowledge graph.  
- **Custom CSV Creation**:
  - Uses `pandas` to clean, process, and store the data in a custom CSV file with the required features and attributes.  
- **Graph Construction**:
  - Leverages `networkx` to create a graph representation where nodes represent songs, artists, or genres, and edges capture their relationships.  
- **Node Embedding**:
  - Implements **Node2Vec** to embed nodes into a 64-dimensional vector space, capturing the relationships between songs, artists, and genres.  
- **Similarity Calculation**:
  - Utilizes **scikit-learn’s cosine similarity** to find and recommend songs similar to a specific song.

---

## Workflow  

1. **Fetch Songs**:  
   Use SPARQL queries to extract song data (artist, genre, related artists) from DBpedia.  

2. **Preprocess Data**:  
   - Store the fetched data in a structured CSV using `pandas`.  
   - Ensure the data is clean and properly formatted.  

3. **Build the Graph**:  
   - Create a graph using `networkx` where nodes represent songs, artists, or genres.  
   - Define edges to establish relationships between nodes.  

4. **Generate Embeddings**:  
   - Apply **Node2Vec** to the graph to create embeddings for nodes.  
   - Each node is mapped to a 64-dimensional vector, capturing its contextual similarity in the graph.  

5. **Find Similar Songs**:  
   - Use the cosine similarity metric from `scikit-learn` to identify and recommend songs similar to a given song.  

---

## Technologies Used  

- **SPARQL**: Fetch song data from the DBpedia knowledge graph.  
- **Pandas**: Data cleaning and CSV generation.  
- **NetworkX**: Build and manage the graph structure.  
- **Node2Vec**: Generate vector embeddings for graph nodes.  
- **scikit-learn**: Calculate cosine similarity for song recommendations.  

---

## Getting Started  

### Prerequisites  
- Python 3.x  
- Libraries: `pandas`, `networkx`, `node2vec`, `scikit-learn`, `SPARQLWrapper`  

### Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/kabuli-web/Song-Recommender-backend.git
   cd Song-Recommender-backend
   ```  

2. Install dependencies:  
   ```bash
   pip install pandas networkx node2vec scikit-learn SPARQLWrapper

   ```  

### Usage  

1. Run the SPARQL script to fetch song data and create a CSV file:  
   ```bash
   python Getmusic.py
   ```  

2. Build the graph and generate embeddings:  
   ```bash
   python create_embeddings.py
   ```  

3. Find similar songs for a given song:  
   ```bash
   python find_similar.py --title "Pumpy" --artist "Cadet" genre "Afroswing"
   ```  

---

## Results  

- The model creates a 64-dimensional embedding for each node in the graph, capturing relationships between songs, artists, and genres.  
- Achieves accurate and contextually relevant song recommendations based on cosine similarity in the embedding space.  

---

## Future Improvements  

- Add more metadata (e.g., album, release year) to enhance embeddings.  
- Implement advanced similarity metrics or hybrid recommendation models.  
- Integrate with a front-end interface for better user interaction.  

---

Feel free to contribute or share your feedback! 😊  

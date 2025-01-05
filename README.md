A Python App that get 130k songs from dbpedia knowledge graph then create an embedding in the vector space
for the artist, genre and related artist and based on that finds similar songs to a specif song.

Used sparql for fetching the songs
pandas to create our own csv witht the required features and attributes
used networkx to create our own graph with nodes and edges
used node2vec to create vector space of 64 dimensions
and used sklearns cosine similarity to find similar songs


from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Set up the DBpedia SPARQL endpoint
sparql = SPARQLWrapper("https://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)


# Define the base query to fetch songs from 2010 to 2025
base_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?song ?title ?artist ?genre ?instrument ?releaseDate ?relatedArtist ?relation  WHERE {
    ?song rdf:type dbo:MusicalWork .
    ?song rdfs:label ?title FILTER(lang(?title)='en' || lang(?title)='sv'). 
    ?song dbo:artist ?artist .
    ?song dbo:genre ?genre .
    ?song dbo:releaseDate ?releaseDate .
    
    OPTIONAL {
        ?artist dbo:associatedBand ?relatedArtist .
        BIND("associatedBand" AS ?relation)
    }
    OPTIONAL {
        ?artist dbo:collaboratesWith ?relatedArtist .
        BIND("collaboratesWith" AS ?relation)
    }
    OPTIONAL {
        ?artist dbo:influencedBy ?relatedArtist .
        BIND("influencedBy" AS ?relation)
    }
    OPTIONAL {
        ?artist dbo:influences ?relatedArtist .
        BIND("influences" AS ?relation)
    }
    FILTER (?releaseDate >= "2000-01-01"^^xsd:date && ?releaseDate <= "2025-12-31"^^xsd:date)
}
"""

# Fetch data in batches using OFFSET and LIMIT
def fetch_music_data_in_batches(batch_size=10000, max_records=100000):
    results = []
    for offset in range(0, max_records, batch_size):
        print(f"Fetching batch with OFFSET {offset}...")
        sparql.setQuery(base_query + f" LIMIT {batch_size} OFFSET {offset}")
        try:
            batch_results = sparql.query().convert()["results"]["bindings"]
            results.extend(batch_results)
            # Stop if fewer results are returned (end of data)
            if len(batch_results) < batch_size:
                break
        except Exception as e:
            print(f"Error fetching batch with OFFSET {offset}: {e}")
            break
    return results

# Clean URIs to extract human-readable names
def extract_name(uri):
    if uri and "http://dbpedia.org/resource/" in uri:
        return uri.split("/")[-1].replace("_", " ")
    return uri

# Process and save the results
def process_and_save_data(results, output_file="dbpedia_music_data_2010_2025.csv"):
    if not results:
        print("No data retrieved.")
        return

    # Extract relevant fields into a list of dictionaries
    data = []
    for result in results:
        data.append({
            "title": result.get("title", {}).get("value", "Unknown"),
            "artist": extract_name(result.get("artist", {}).get("value", "Unknown")),
            "genre": extract_name(result.get("genre", {}).get("value", "Unknown")),
            "relatedArtist": extract_name(result.get("relatedArtist", {}).get("value", "Unknown")),
            "relation": result.get("relation", {}).get("value", "Unknown"),
            "instrument": result.get("instrument", {}).get("value", "Unknown"),
            "releaseDate": result.get("releaseDate", {}).get("value", "Unknown"),
        })

    # Convert to a Pandas DataFrame and save to CSV
    df = pd.DataFrame(data)
    # df = df.drop_duplicates(subset=["title", "artist", "genre"])
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

# Main execution
if __name__ == "__main__":
    print("Fetching music data from DBpedia with pagination...")
    music_data = fetch_music_data_in_batches(batch_size=10000, max_records=300000)
    print(f"Retrieved {len(music_data)} records.")
    process_and_save_data(music_data, output_file="dbpedia_music_data_2010_2025.csv")



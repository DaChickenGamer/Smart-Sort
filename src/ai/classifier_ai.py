import openai
from sklearn.cluster import KMeans
import numpy as np

# Global lists to hold document embeddings and contents
document_embeddings = []
document_contents = []

def get_document_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"  # Example model
    )
    return response['data'][0]['embedding']

# AI-based classification function
def classify_and_categorize_file(file_path):
    print(f"Classifying file: {file_path}")
    
    # Read the file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Get the embedding for the document
        embedding = get_document_embedding(content)
        if embedding:
            document_embeddings.append(embedding)
            document_contents.append(content)
        else:
            print(f"Error generating embedding for file: {file_path}")
            return "Others", f"/Users/gagankarnati/Others"

        # Perform clustering only if there are enough documents
        if len(document_embeddings) >= 3:
            category = cluster_documents()
        else:
            print(f"Number of documents processed: {len(document_embeddings)}")
            category = "Others"

        return category
    except Exception as e:
        print(f"Error classifying file: {e}")
        return "Others"

# Function to cluster documents and generate dynamic categories
def cluster_documents():
    print("Starting document clustering...")
    
    if len(document_embeddings) < 3:
        return "Others"
    
    kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
    labels = kmeans.labels_

    category_names = []
    for cluster_num in range(3):
        cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
        top_keywords = get_top_keywords(cluster_docs)
        category_names.append(" ".join(top_keywords) if top_keywords else "Miscellaneous")

    return category_names[labels[-1]]

# Extract top keywords using TF-IDF
def get_top_keywords(documents, n_keywords=3):
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)
    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
    top_keywords = feature_array[tfidf_sorting][:n_keywords]
    return top_keywords
from ai.openai_utils import get_document_embedding
from sklearn.cluster import KMeans
import numpy as np

# Global lists to hold document embeddings and contents
document_embeddings = []
document_contents = []

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


























# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     print("Starting document clustering...")
#     try:
#         num_clusters = min(3, len(document_embeddings))  # Adjust number of clusters
#         kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         category_names = []
#         for cluster_num in range(num_clusters):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords) if top_keywords else "Miscellaneous")

#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=2):
#     try:
#         vectorizer = TfidfVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(documents)
#         if X.shape[1] == 0:
#             raise ValueError("No meaningful vocabulary extracted.")
#         feature_array = np.array(vectorizer.get_feature_names_out())
#         tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#         top_keywords = feature_array[tfidf_sorting][:n_keywords]
#         return " ".join(top_keywords)
#     except Exception as e:
#         print(f"Error extracting keywords: {e}")
#         return None
















# import os
# import time
# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import PyPDF2

# # Global lists to hold document embeddings and contents
# document_embeddings = []
# document_contents = []

# # Function to extract text from PDFs
# def extract_text_from_pdf(pdf_path, limit_chars=2000):
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             # Extract only the first few characters to limit the text size
#             for page_num in range(len(reader.pages)):
#                 text += reader.pages[page_num].extract_text()
#                 if len(text) >= limit_chars:
#                     break
#             return text[:limit_chars]
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return None

# # Function to split text into chunks that fit within the model's token limit
# def split_text_into_chunks(text, chunk_size=2000):
#     """Split the text into smaller chunks for embedding."""
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield " ".join(words[i:i + chunk_size])

# # Function to wait until the file is fully downloaded or written
# def wait_for_file(file_path, timeout=30, interval=2):
#     """Wait for the file to be completely written."""
#     start_time = time.time()
#     prev_size = -1

#     while time.time() - start_time < timeout:
#         if not os.path.exists(file_path):
#             return False
#         current_size = os.path.getsize(file_path)
#         if current_size == prev_size:
#             return True  # File size stabilized, likely finished writing
#         prev_size = current_size
#         time.sleep(interval)
#     return False

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     try:
#         content = None

#         # Wait for the file to be ready
#         if not wait_for_file(file_path):
#             print(f"Source file not found or not ready: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Extract content from PDF or text file
#         if file_path.endswith(".pdf"):
#             print(f"Extracting text from PDF: {file_path}")
#             content = extract_text_from_pdf(file_path)
#         else:
#             with open(file_path, 'r') as f:
#                 content = f.read()

#         if not content:
#             print(f"Skipping non-text file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Split large documents into smaller chunks and process each chunk separately
#         total_embedding = []
#         for chunk in split_text_into_chunks(content):
#             embedding = get_document_embedding(chunk)
#             if embedding:
#                 total_embedding.extend(embedding)
#             else:
#                 print(f"Error generating embedding for chunk in file: {file_path}")
#                 return "Others", f"/Users/gagankarnati/Others"

#         # Add the overall document embedding and content to lists
#         document_embeddings.append(total_embedding)
#         document_contents.append(content)

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:
#             category = cluster_documents()
#         else:
#             # Get top keywords directly if less than 3 docs
#             category = get_top_keywords([content])
#             if not category:
#                 category = "Others"

#         print(f"Category determined: {category}")
#         return category
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others"
    


















# import os
# import time
# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import PyPDF2

# # Global lists to hold document embeddings and contents
# document_embeddings = []
# document_contents = []

# # Function to extract text from PDFs
# def extract_text_from_pdf(pdf_path, limit_chars=2000):
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             # Extract only the first few characters to limit the text size
#             for page_num in range(len(reader.pages)):
#                 text += reader.pages[page_num].extract_text()
#                 if len(text) >= limit_chars:
#                     break
#             return text[:limit_chars]
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return None

# # Function to split text into chunks that fit within the model's token limit
# def split_text_into_chunks(text, chunk_size=2000):
#     """Split the text into smaller chunks for embedding."""
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield " ".join(words[i:i + chunk_size])

# # Function to wait until the file is fully downloaded or written
# def wait_for_file(file_path, timeout=30, interval=2):
#     """Wait for the file to be completely written."""
#     start_time = time.time()
#     prev_size = -1

#     while time.time() - start_time < timeout:
#         if not os.path.exists(file_path):
#             return False
#         current_size = os.path.getsize(file_path)
#         if current_size == prev_size:
#             return True  # File size stabilized, likely finished writing
#         prev_size = current_size
#         time.sleep(interval)
#     return False

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     try:
#         content = None

#         # Wait for the file to be ready
#         if not wait_for_file(file_path):
#             print(f"Source file not found or not ready: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Extract content from PDF or text file
#         if file_path.endswith(".pdf"):
#             print(f"Extracting text from PDF: {file_path}")
#             content = extract_text_from_pdf(file_path)
#         else:
#             with open(file_path, 'r') as f:
#                 content = f.read()

#         if not content:
#             print(f"Skipping non-text file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Use only the first chunk of the content for embedding
#         initial_chunk = next(split_text_into_chunks(content), "")
#         if not initial_chunk:
#             print(f"No valid text found for classification in file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Generate embedding for the initial chunk
#         embedding = get_document_embedding(initial_chunk)
#         if embedding:
#             document_embeddings.append(embedding)
#             document_contents.append(initial_chunk)
#         else:
#             print(f"Error generating embedding for file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:
#             category = cluster_documents()
#         else:
#             print(f"Number of documents processed: {len(document_embeddings)}")
#             category = "Others"

#         dest_folder = f"/Users/gagankarnati/{category}"
#         return category, dest_folder
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others", f"/Users/gagankarnati/Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     print("Starting document clustering...")
#     try:
#         num_clusters = min(3, len(document_embeddings))  # Adjust number of clusters
#         kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         category_names = []
#         for cluster_num in range(num_clusters):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords) if top_keywords else "Miscellaneous")

#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     try:
#         vectorizer = TfidfVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(documents)
#         if X.shape[1] == 0:
#             raise ValueError("No meaningful vocabulary extracted.")
#         feature_array = np.array(vectorizer.get_feature_names_out())
#         tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#         top_keywords = feature_array[tfidf_sorting][:n_keywords]
#         return top_keywords
#     except Exception as e:
#         print(f"Error extracting keywords: {e}")
#         return ["Miscellaneous"]











# import os
# import time
# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import PyPDF2

# # Global lists to hold document embeddings and contents
# document_embeddings = []
# document_contents = []

# # Function to extract text from PDFs
# def extract_text_from_pdf(pdf_path, limit_chars=2000):
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             # Extract only the first few characters to limit the text size
#             for page_num in range(len(reader.pages)):
#                 text += reader.pages[page_num].extract_text()
#                 if len(text) >= limit_chars:
#                     break
#             return text[:limit_chars]
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return None

# # Function to split text into chunks that fit within the model's token limit
# def split_text_into_chunks(text, chunk_size=2000):
#     """Split the text into smaller chunks for embedding."""
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield " ".join(words[i:i + chunk_size])

# # Function to wait until the file is fully downloaded or written
# def wait_for_file(file_path, timeout=30, interval=2):
#     """Wait for the file to be completely written."""
#     start_time = time.time()
#     prev_size = -1

#     while time.time() - start_time < timeout:
#         if not os.path.exists(file_path):
#             return False
#         current_size = os.path.getsize(file_path)
#         if current_size == prev_size:
#             return True  # File size stabilized, likely finished writing
#         prev_size = current_size
#         time.sleep(interval)
#     return False

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     try:
#         content = None

#         # Wait for the file to be ready
#         if not wait_for_file(file_path):
#             print(f"Source file not found or not ready: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Extract content from PDF or text file
#         if file_path.endswith(".pdf"):
#             print(f"Extracting text from PDF: {file_path}")
#             content = extract_text_from_pdf(file_path)
#         else:
#             with open(file_path, 'r') as f:
#                 content = f.read()

#         if not content:
#             print(f"Skipping non-text file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Split large documents into smaller chunks and process each chunk separately
#         total_embedding = []
#         for chunk in split_text_into_chunks(content):
#             embedding = get_document_embedding(chunk)
#             if embedding:
#                 total_embedding.extend(embedding)
#             else:
#                 print(f"Error generating embedding for chunk in file: {file_path}")
#                 return "Others", f"/Users/gagankarnati/Others"

#         # Add the overall document embedding and content to lists
#         document_embeddings.append(total_embedding)
#         document_contents.append(content)

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:
#             category = cluster_documents()
#         else:
#             print(f"Number of documents processed: {len(document_embeddings)}")
#             category = "Others"

#         dest_folder = f"/Users/gagankarnati/{category}"
#         return category, dest_folder
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others", f"/Users/gagankarnati/Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     print("Starting document clustering...")
#     try:
#         num_clusters = min(3, len(document_embeddings))  # Adjust number of clusters
#         kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         category_names = []
#         for cluster_num in range(num_clusters):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords) if top_keywords else "Miscellaneous")

#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     try:
#         vectorizer = TfidfVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(documents)
#         if X.shape[1] == 0:
#             raise ValueError("No meaningful vocabulary extracted.")
#         feature_array = np.array(vectorizer.get_feature_names_out())
#         tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#         top_keywords = feature_array[tfidf_sorting][:n_keywords]
#         return top_keywords
#     except Exception as e:
#         print(f"Error extracting keywords: {e}")
#         return ["Miscellaneous"]




















# import os
# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import PyPDF2

# # Global lists to hold document embeddings and contents
# document_embeddings = []
# document_contents = []

# # Function to extract a small piece of text from PDFs (limiting to 1000 characters)
# def extract_text_from_pdf(pdf_path, max_chars=1000):
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             for page_num in range(len(reader.pages)):
#                 text += reader.pages[page_num].extract_text()
#                 if len(text) >= max_chars:  # Stop once we've extracted enough characters
#                     return text[:max_chars]  # Limit the text to max_chars
#             return text[:max_chars]  # Return only the first max_chars characters
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return None

# # Function to extract a small piece of text from a regular text file (limiting to 1000 characters)
# def extract_text_from_file(file_path, max_chars=1000):
#     try:
#         with open(file_path, 'r') as f:
#             return f.read(max_chars)  # Read only the first max_chars characters
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return None

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     try:
#         content = None

#         # Extract content from PDF or text file
#         if file_path.endswith(".pdf"):
#             print(f"Extracting text from PDF: {file_path}")
#             content = extract_text_from_pdf(file_path)
#         else:
#             content = extract_text_from_file(file_path)

#         if not content:
#             print(f"Skipping non-text file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Get the embedding for the document (for a small portion)
#         embedding = get_document_embedding(content)
#         if embedding:
#             document_embeddings.append(embedding)
#             document_contents.append(content)
#         else:
#             print(f"Error generating embedding for file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:
#             category = cluster_documents()
#         else:
#             print(f"Number of documents processed: {len(document_embeddings)}")
#             category = "Others"

#         dest_folder = f"/Users/gagankarnati/{category}"
#         return category, dest_folder
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others", f"/Users/gagankarnati/Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     # Perform KMeans clustering
#     print("Starting document clustering...")
#     try:
#         kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         # Extract keywords from each cluster to dynamically name categories
#         category_names = []
#         for cluster_num in range(3):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords))

#         # Assign the current document to a category
#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     try:
#         vectorizer = TfidfVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(documents)
#         feature_array = np.array(vectorizer.get_feature_names_out())
#         tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#         top_keywords = feature_array[tfidf_sorting][:n_keywords]
#         return top_keywords
#     except Exception as e:
#         print(f"Error extracting keywords: {e}")
#         return ["Miscellaneous"]




















# import os
# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import PyPDF2

# # Global lists to hold document embeddings and contents
# document_embeddings = []
# document_contents = []

# # Function to extract text from PDFs
# def extract_text_from_pdf(pdf_path):
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             for page_num in range(len(reader.pages)):
#                 text += reader.pages[page_num].extract_text()
#             return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return None

# # Function to split text into chunks that fit within the model's token limit
# def split_text_into_chunks(text, chunk_size=2000):
#     """Split the text into smaller chunks for embedding."""
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield " ".join(words[i:i + chunk_size])

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     try:
#         content = None

#         # Extract content from PDF or text file
#         if file_path.endswith(".pdf"):
#             print(f"Extracting text from PDF: {file_path}")
#             content = extract_text_from_pdf(file_path)
#         else:
#             with open(file_path, 'r') as f:
#                 content = f.read()

#         if not content:
#             print(f"Skipping non-text file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Split large documents into smaller chunks and process each chunk separately
#         total_embedding = []
#         for chunk in split_text_into_chunks(content):
#             embedding = get_document_embedding(chunk)
#             if embedding:
#                 total_embedding.extend(embedding)
#             else:
#                 print(f"Error generating embedding for chunk in file: {file_path}")
#                 return "Others", f"/Users/gagankarnati/Others"

#         # Add the overall document embedding and content to lists
#         document_embeddings.append(total_embedding)
#         document_contents.append(content)

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:
#             category = cluster_documents()
#         else:
#             print(f"Number of documents processed: {len(document_embeddings)}")
#             category = "Others"

#         dest_folder = f"/Users/gagankarnati/{category}"
#         return category, dest_folder
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others", f"/Users/gagankarnati/Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     # Perform KMeans clustering
#     print("Starting document clustering...")
#     try:
#         kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         # Extract keywords from each cluster to dynamically name categories
#         category_names = []
#         for cluster_num in range(3):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords))

#         # Assign the current document to a category
#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     try:
#         vectorizer = TfidfVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(documents)
#         feature_array = np.array(vectorizer.get_feature_names_out())
#         tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#         top_keywords = feature_array[tfidf_sorting][:n_keywords]
#         return top_keywords
#     except Exception as e:
#         print(f"Error extracting keywords: {e}")
#         return ["Miscellaneous"]





















# import os
# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import PyPDF2

# # Global lists to hold document embeddings and contents
# document_embeddings = []
# document_contents = []

# # Function to extract text from PDFs
# def extract_text_from_pdf(pdf_path):
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             for page_num in range(len(reader.pages)):
#                 text += reader.pages[page_num].extract_text()
#             return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return None

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     try:
#         content = None

#         # Extract content from PDF or text file
#         if file_path.endswith(".pdf"):
#             print(f"Extracting text from PDF: {file_path}")
#             content = extract_text_from_pdf(file_path)
#         else:
#             with open(file_path, 'r') as f:
#                 content = f.read()

#         if not content:
#             print(f"Skipping non-text file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Get the embedding for the document
#         embedding = get_document_embedding(content)
#         if embedding:
#             document_embeddings.append(embedding)
#             document_contents.append(content)
#         else:
#             print(f"Error generating embedding for file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:
#             category = cluster_documents()
#         else:
#             print(f"Number of documents processed: {len(document_embeddings)}")
#             category = "Others"

#         dest_folder = f"/Users/gagankarnati/{category}"
#         return category, dest_folder
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others", f"/Users/gagankarnati/Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     # Perform KMeans clustering
#     print("Starting document clustering...")
#     try:
#         kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         # Extract keywords from each cluster to dynamically name categories
#         category_names = []
#         for cluster_num in range(3):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords))

#         # Assign the current document to a category
#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     try:
#         vectorizer = TfidfVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(documents)
#         feature_array = np.array(vectorizer.get_feature_names_out())
#         tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#         top_keywords = feature_array[tfidf_sorting][:n_keywords]
#         return top_keywords
#     except Exception as e:
#         print(f"Error extracting keywords: {e}")
#         return ["Miscellaneous"]

















# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# document_embeddings = []
# document_contents = []

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     # Read the file content
#     try:
#         with open(file_path, 'r') as f:
#             content = f.read()

#         # Get the embedding for the document
#         embedding = get_document_embedding(content)
#         if embedding:
#             document_embeddings.append(embedding)
#             document_contents.append(content)
#         else:
#             print(f"Error generating embedding for file: {file_path}")
#             return "Others", f"/Users/gagankarnati/Others"  # Return both category and folder

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:
#             category = cluster_documents()
#         else:
#             print(f"Number of documents processed: {len(document_embeddings)}")
#             category = "Others"

#         # Define the destination folder based on the category
#         dest_folder = f"/Users/gagankarnati/{category}"
#         return category, dest_folder  # Always return two values
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others", f"/Users/gagankarnati/Others"  # Always return two values

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     # Perform KMeans clustering
#     print("Starting document clustering...")
#     try:
#         kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         # Extract keywords from each cluster to dynamically name categories
#         category_names = []
#         for cluster_num in range(3):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords))

#         # Assign the current document to a category
#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     try:
#         vectorizer = TfidfVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(documents)
#         feature_array = np.array(vectorizer.get_feature_names_out())
#         tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#         top_keywords = feature_array[tfidf_sorting][:n_keywords]
#         return top_keywords
#     except Exception as e:
#         print(f"Error extracting keywords: {e}")
#         return ["Miscellaneous"]




















# # Path: src/ai/classifier_ai.py

# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans

# document_embeddings = []
# document_contents = []

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     print(f"Classifying file: {file_path}")
    
#     # Read the file content
#     try:
#         with open(file_path, 'r') as f:
#             content = f.read()

#         # Get the embedding for the document
#         embedding = get_document_embedding(content)
#         if embedding:
#             document_embeddings.append(embedding)
#             document_contents.append(content)
#         else:
#             print(f"Error generating embedding for file: {file_path}")
#             return "Others"

#         # Perform clustering only if there are enough documents
#         if len(document_embeddings) >= 3:  # Only cluster if we have at least 3 documents
#             return cluster_documents()
#         else:
#             print(f"Number of documents processed: {len(document_embeddings)}")
#             return "Others"
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     if len(document_embeddings) < 3:
#         print("Not enough documents for clustering")
#         return "Others"

#     # Perform KMeans clustering
#     print("Starting document clustering...")
#     try:
#         kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#         labels = kmeans.labels_

#         # Extract keywords from each cluster to dynamically name categories
#         category_names = []
#         for cluster_num in range(3):
#             cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#             top_keywords = get_top_keywords(cluster_docs)
#             category_names.append(" ".join(top_keywords))

#         # Assign the current document to a category
#         current_label = labels[-1]
#         return category_names[current_label]
#     except Exception as e:
#         print(f"Error during clustering: {e}")
#         return "Others"

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     import numpy as np

#     vectorizer = TfidfVectorizer(stop_words='english')
#     X = vectorizer.fit_transform(documents)
#     feature_array = np.array(vectorizer.get_feature_names_out())
#     tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#     top_keywords = feature_array[tfidf_sorting][:n_keywords]
#     return top_keywords





















# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans

# document_embeddings = []
# document_contents = []

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     # Read the file content
#     try:
#         with open(file_path, 'r') as f:
#             content = f.read()

#         print(f"Classifying file: {file_path}")

#         # Get the embedding for the document
#         embedding = get_document_embedding(content)
#         document_embeddings.append(embedding)
#         document_contents.append(content)

#         # Print number of documents
#         print(f"Number of documents processed: {len(document_embeddings)}")

#         # If there are enough documents, start clustering
#         if len(document_embeddings) > 1:  # Requires at least 2 documents for clustering
#             return cluster_documents()
#         return "Others", "/Users/gagankarnati/Others"
#     except Exception as e:
#         print(f"Error classifying file: {e}")
#         return "Others", "/Users/gagankarnati/Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     print("Starting document clustering...")

#     # Perform KMeans clustering
#     kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#     labels = kmeans.labels_

#     # Extract keywords from each cluster to dynamically name categories
#     category_names = []
#     for cluster_num in range(3):
#         cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#         category_names.append(f"Category {cluster_num}")

#     print(f"Cluster labels: {labels}")
#     print(f"Categories generated: {category_names}")

#     # Assign the current document to a category
#     current_label = labels[-1]
#     category = category_names[current_label]
#     folder_path = f"/Users/gagankarnati/{category.replace(' ', '_')}"
#     return category, folder_path
















# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import os
# import numpy as np

# document_embeddings = []
# document_contents = []

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     # Read the file content
#     with open(file_path, 'r') as f:
#         content = f.read()

#     # Get the embedding for the document
#     embedding = get_document_embedding(content)
#     document_embeddings.append(embedding)
#     document_contents.append(content)

#     # If there are enough documents, start clustering
#     if len(document_embeddings) > 1:
#         category = cluster_documents()
#     else:
#         category = "Others"
    
#     # Predefined folder mappings for known categories
#     folder_mapping = {
#         "Documents": "/Users/gagankarnati/Documents",
#         "Media": "/Users/gagankarnati/Media",
#         "Images": "/Users/gagankarnati/Images",
#         "Others": "/Users/gagankarnati/Others"
#     }
    
#     # If the category is predefined, return the mapped folder
#     if category in folder_mapping:
#         return category, folder_mapping[category]
    
#     # If the category is dynamically generated, create a new folder for it
#     dynamic_folder = f"/Users/gagankarnati/Downloads/{category.replace(' ', '_')}"
#     if not os.path.exists(dynamic_folder):
#         os.makedirs(dynamic_folder)
    
#     return category, dynamic_folder

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     # Perform KMeans clustering
#     kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#     labels = kmeans.labels_

#     # Extract keywords from each cluster to dynamically name categories
#     category_names = []
#     for cluster_num in range(3):
#         cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#         top_keywords = get_top_keywords(cluster_docs)
#         category_names.append(" ".join(top_keywords))

#     # Assign the current document to a category
#     current_label = labels[-1]
#     return category_names[current_label]

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     vectorizer = TfidfVectorizer(stop_words='english')
#     X = vectorizer.fit_transform(documents)
#     feature_array = np.array(vectorizer.get_feature_names_out())
#     tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#     top_keywords = feature_array[tfidf_sorting][:n_keywords]
#     return top_keywords












## AI BUT DOES NOT DO FILE MOVEMENT. 
# from ai.openai_utils import get_document_embedding
# from sklearn.cluster import KMeans
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# document_embeddings = []
# document_contents = []

# # AI-based classification function
# def classify_and_categorize_file(file_path):
#     # Read the file content
#     with open(file_path, 'r') as f:
#         content = f.read()

#     # Get the embedding for the document
#     embedding = get_document_embedding(content)
#     document_embeddings.append(embedding)
#     document_contents.append(content)

#     # If there are enough documents, start clustering
#     if len(document_embeddings) > 1:
#         return cluster_documents()
#     return "Others"

# # Function to cluster documents and generate dynamic categories
# def cluster_documents():
#     # Perform KMeans clustering
#     kmeans = KMeans(n_clusters=3, random_state=0).fit(document_embeddings)
#     labels = kmeans.labels_

#     # Extract keywords from each cluster to dynamically name categories
#     category_names = []
#     for cluster_num in range(3):
#         cluster_docs = [document_contents[i] for i in range(len(labels)) if labels[i] == cluster_num]
#         top_keywords = get_top_keywords(cluster_docs)
#         category_names.append(" ".join(top_keywords))

#     # Assign the current document to a category
#     current_label = labels[-1]
#     return category_names[current_label]

# # Extract top keywords using TF-IDF
# def get_top_keywords(documents, n_keywords=3):
#     vectorizer = TfidfVectorizer(stop_words='english')
#     X = vectorizer.fit_transform(documents)
#     feature_array = np.array(vectorizer.get_feature_names_out())
#     tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
#     top_keywords = feature_array[tfidf_sorting][:n_keywords]
#     return top_keywords
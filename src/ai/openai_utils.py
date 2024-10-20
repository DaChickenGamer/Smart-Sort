import os
import openai

# Set up OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in the environment.")

openai.api_key = openai_api_key

def categorize_with_ai(file_name):
    """
    Use OpenAI GPT-4 to categorize files based on their title.
    """
    try:
        print(f"Feeding title '{file_name}' into GPT-4 for categorization...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a file categorization assistant. Given a file title, categorize the file and suggest a folder name."
                },
                {
                    "role": "user",
                    "content": f"Categorize the file titled: {file_name}"
                }
            ]
        )
        category = response['choices'][0]['message']['content'].strip()
        print(f"AI categorized {file_name} as: {category}")
        return category
    except Exception as e:
        print(f"Error categorizing with GPT: {e}")
        return None



# import os
# import openai
# from openai.error import RateLimitError

# # Get the OpenAI API key from environment variables
# openai_api_key = os.getenv('OPENAI_API_KEY')
# if openai_api_key is None:
#     raise ValueError("OpenAI API key is not set in the environment.")

# openai.api_key = openai_api_key

# # Get embedding for a document using OpenAI API
# def get_document_embedding(content):
#     try:
#         response = openai.Embedding.create(
#             input=content,
#             model="text-embedding-ada-002"
#         )
#         embedding = response['data'][0]['embedding']
#         print(f"Generated embedding for document: {embedding[:5]}...")
#         return embedding
#     except RateLimitError as e:
#         print(f"Rate limit error: {e}")
#         return None
#     except Exception as e:
#         print(f"Error generating embedding: {e}")
#         return None






# import openai
# from openai.error import RateLimitError

# # Initialize OpenAI API key
# openai.api_key = 
# # Get embedding for a document using OpenAI API
# def get_document_embedding(content):
#     try:
#         response = openai.embeddings.create(
#             input=content,
#             model="text-embedding-ada-002"  # Embedding model designed for generating embeddings
#         )
#         embedding = response['data'][0]['embedding']
#         print(f"Generated embedding for document: {embedding[:5]}... (truncated)")  # Display part of the embedding
#         return embedding
#     except RateLimitError as e:
#         print(f"Rate limit error: {e}")
#         return None







# 


# import openai

# # Initialize OpenAI API key
# openai.api_key = '
# # Get embedding for a document using the new OpenAI API
# def get_document_embedding(content):
#     response = openai.embeddings.create(
#         input=content,
#         model="text-embedding-ada-002"  # Embedding model in the new API
#     )
#     return response['data'][0]['embedding']  # Return the embedding vector





#Doesn't work. 

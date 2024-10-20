import openai

def categorize_with_ai(file_name):
    """
    Uses GPT-4 to categorize the file based on its title.
    """
    try:
        print(f"Feeding title '{file_name}' into GPT-4 for categorization...")
        
        # Use the correct chat completion endpoint with GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that categorizes files based on their names."},
                {"role": "user", "content": f"Categorize the file with the title '{file_name}'. Suggest a folder name based on the title."}
            ],
            max_tokens=10
        )

        ai_category = response['choices'][0]['message']['content'].strip()
        print(f"AI categorized {file_name} as: {ai_category}")
        return ai_category
    
    except Exception as e:
        print(f"Error categorizing with GPT-4: {e}")
        return "Others"
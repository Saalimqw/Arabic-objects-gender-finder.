import os
from groq import Groq

# 1. Configuration
# Ensure your API key is set in your environment variables or paste it here
GROQ_API_KEY = "your_api_key_here" 
client = Groq(api_key=GROQ_API_KEY)

def get_arabic_gender(object_name):
    """
    Uses Qwen 3 32B to determine the Arabic gender of an object.
    Qwen 3 is particularly good at 'thinking' through linguistic exceptions.
    """
    
    # We use a structured prompt to ensure the output is easy for you to read
    prompt = f"""
    Target Object: {object_name}
    Task: Identify the Arabic word for this object, its grammatical gender, and the rule/reason.
    
    Please provide the response in this format:
    Word: [Arabic word with Harakat]
    Gender: [Masculine or Feminine]
    Explanation: [A short sentence on why, e.g., 'Ends in Ta-Marbuta' or 'Irregular feminine']
    """

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Arabic linguist. You provide concise, accurate grammatical information for language learners."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="qwen/qwen3-32b",
            # Qwen 3 handles reasoning best with a slightly lower temperature
            temperature=0.6, 
            max_tokens=500
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {str(e)}"

# 2. Interactive CLI
if __name__ == "__main__":
    print("--- Arabic Object Gender Lookup (Qwen 3 32B) ---")
    print("Type 'quit' to stop.")
    
    while True:
        target = input("\nEnter object (e.g. 'moon', 'window'): ").strip()
        if target.lower() in ['quit', 'exit']:
            break
        
        if target:
            result = get_arabic_gender(target)
            print("\n" + result)

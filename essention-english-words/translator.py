
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('API_KEY')

def translate_word(word, target_language="uz"):
    prompt = f"""
Translate the following English text into {target_language} naturally and correctly.
Return only the translation, without explanations or transliterations.

{word}
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional translator. Translate accurately and naturally."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    # Natijani olish
    translated_text = response.choices[0].message.content.strip()
    return translated_text